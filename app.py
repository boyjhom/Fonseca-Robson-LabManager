from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessário para usar sessões

# Classe para representar um usuário
class Usuario:
    def __init__(self, username, password, nome, email, cargo):
        self.username = username
        self.password = password
        self.nome = nome
        self.email = email
        self.cargo = cargo

# Classe para gerenciar a aplicação e seus usuários
class Aplicacao:
    def __init__(self):
        self.usuarios = []
        self.estoque = []  # Lista de itens no estoque
        # Adicionando itens de exemplo ao estoque
        self.adicionar_item_estoque("Arduino Uno", 15, "Placa microcontroladora para prototipagem eletrônica")
        self.adicionar_item_estoque("Raspberry Pi 4", 10, "Computador compacto e versátil para projetos diversos")
        self.adicionar_item_estoque("Servo Motor SG90", 25, "Pequeno motor para controle de movimento")
        self.adicionar_item_estoque("Sensor Ultrassônico HC-SR04", 20, "Sensor de distância para robótica")
        self.adicionar_item_estoque("Módulo Bluetooth HC-05", 12, "Comunicação sem fio para robôs e dispositivos")
        self.adicionar_item_estoque("Motores DC com Redutor", 18, "Motores DC com redução para torque elevado")
        self.adicionar_item_estoque("Kit de Roda e Pneus", 30, "Rodas para construção de robôs móveis")
        self.adicionar_item_estoque("Fonte de Alimentação Regulável", 8, "Fornecimento de energia ajustável para projetos")
        self.adicionar_item_estoque("Jumpers e Fios Conectores", 200, "Fios para prototipagem em placas de ensaio")
        self.adicionar_item_estoque("Kit de Sensores Diversos", 15, "Conjunto com sensores de temperatura, luz, entre outros")

    def adicionar_usuario(self, username, password, nome, email, cargo):
        # Verifica se o usuário já existe
        if not any(u.username == username for u in self.usuarios):
            self.usuarios.append(Usuario(username, password, nome, email, cargo))
            return True
        return False

    def autenticar_usuario(self, username, password):
        # Verifica se as credenciais estão corretas
        for usuario in self.usuarios:
            if usuario.username == username and usuario.password == password:
                return usuario
        return None

    def encontrar_usuario(self, username):
        # Busca o usuário pelo username
        return next((u for u in self.usuarios if u.username == username), None)

    def adicionar_item_estoque(self, nome, quantidade, descricao=""):
        # Adiciona um novo item ao estoque
        self.estoque.append({
            'nome': nome,
            'quantidade': quantidade,
            'descricao': descricao
        })

    def atualizar_quantidade(self, nome, nova_quantidade):
        # Atualiza a quantidade de um item no estoque
        for item in self.estoque:
            if item['nome'] == nome:
                item['quantidade'] = nova_quantidade
                return True
        return False

# Instância da aplicação
aplicacao = Aplicacao()

# Adicionando alguns itens de estoque para teste
aplicacao.adicionar_item_estoque("Parafusos", 56, "Código: 23")
aplicacao.adicionar_item_estoque("Chave inglesa", 3, "Código: 5")

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Autentica o usuário
        usuario = aplicacao.autenticar_usuario(username, password)
        if usuario:
            session['username'] = usuario.username  # Armazena o usuário na sessão
            return redirect(url_for('index'))
        
        return render_template('login.html', error="Nome de usuário ou senha incorretos")
    
    return render_template('login.html')

# Rota para a página principal
@app.route('/index')
def index():
    username = session.get('username')  # Obtém o usuário da sessão
    if not username:
        return redirect(url_for('login'))
    
    usuario_logado = aplicacao.encontrar_usuario(username)
    if usuario_logado:
        return render_template('index.html', usuario=usuario_logado)
    
    return redirect(url_for('login'))

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']
        email = request.form['email']
        cargo = request.form['cargo']
        
        if aplicacao.adicionar_usuario(username, password, nome, email, cargo):
            return redirect(url_for('login'))
        
        return render_template('cadastro.html', error="Usuário já foi cadastrado")
    
    return render_template('cadastro.html')

# Rota para a página "Equipe"
@app.route('/equipe')
def equipe():
    username = session.get('username')  # Obtém o nome de usuário da sessão
    if not username:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver logado

    usuario_logado = aplicacao.encontrar_usuario(username)  # Busca o usuário logado
    if usuario_logado:
        return render_template('equipe.html', usuarios=aplicacao.usuarios, usuario_logado=usuario_logado)
    return redirect(url_for('login'))  # Redireciona para o login se o usuário não for encontrado


# Rota para a página "Meu Perfil"
@app.route('/meu_perfil')
def meu_perfil():
    username = session.get('username')  # Obtém o usuário da sessão
    if not username:
        return redirect(url_for('login'))

    usuario = aplicacao.encontrar_usuario(username)
    if usuario:
        return render_template('meu_perfil.html', usuario=usuario)
    return redirect(url_for('login'))

# Rota para a página "Estoque"
@app.route('/estoque')
def estoque():
    username = session.get('username')  # Verifica se o usuário está logado
    if not username:
        return redirect(url_for('login'))
    
    usuario_logado = aplicacao.encontrar_usuario(username)  # Obter o usuário logado
    # Renderiza a página estoque.html e passa a lista de itens no estoque e o usuário logado
    return render_template('estoque.html', itens=aplicacao.estoque, usuario=usuario_logado)

# Rota para atualizar a quantidade de um item no estoque
@app.route('/atualizar_estoque', methods=['POST'])
def atualizar_estoque():
    nome = request.form['nome']
    nova_quantidade = int(request.form['quantidade'])
    aplicacao.atualizar_quantidade(nome, nova_quantidade)
    return redirect(url_for('estoque'))

if __name__ == '__main__':
    app.run(debug=True)
