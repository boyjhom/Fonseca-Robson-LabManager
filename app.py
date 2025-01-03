from reportlab.pdfgen import canvas
from flask import Flask, render_template, request, redirect, url_for, session, make_response
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Classe para representar um usuário
class Usuario:
    def __init__(self, username, password, nome, email, cargo):
        self.username = username
        self.password = password
        self.nome = nome
        self.email = email
        self.cargo = cargo   
    def __repr__(self):
        return f"Usuario(username={self.username}, nome={self.nome})"

# Classe para gerenciar a aplicação
class Aplicacao:
    def __init__(self):
        self.usuarios = []
        self.estoque = []
        self.cautelas = []
        self.carregar_dados()  # Carrega os dados ao iniciar o programa

        # Adiciona itens de exemplo apenas se o estoque estiver vazio
        if not self.estoque:
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

    def salvar_dados(self):
        """
        Salva os dados de usuários, estoque e cautelas em arquivos JSON.
        """
        with open("usuarios.json", "w") as usuarios_file:
            json.dump([vars(u) for u in self.usuarios], usuarios_file, indent=4)

        with open("estoque.json", "w") as estoque_file:
            json.dump(self.estoque, estoque_file, indent=4)

        with open("cautelas.json", "w") as cautelas_file:
            json.dump(self.cautelas, cautelas_file, indent=4)

    def carregar_dados(self):
        """
        Carrega os dados de usuários, estoque e cautelas dos arquivos JSON.
        """
        try:
            with open("usuarios.json", "r") as usuarios_file:
                self.usuarios = [Usuario(**data) for data in json.load(usuarios_file)]
        except FileNotFoundError:
            self.usuarios = []

        try:
            with open("estoque.json", "r") as estoque_file:
                self.estoque = json.load(estoque_file)
        # Remove duplicados por 'nome'
            self.estoque = list({item['nome']: item for item in self.estoque}.values())
        except FileNotFoundError:
            self.estoque = []

        try:
            with open("cautelas.json", "r") as cautelas_file:
                self.cautelas = json.load(cautelas_file)
        except FileNotFoundError:
            self.cautelas = []


    def adicionar_usuario(self, username, password, nome, email, cargo):
        if not any(u.username == username for u in self.usuarios):
            self.usuarios.append(Usuario(username, password, nome, email, cargo))
            return True
        return False

    def autenticar_usuario(self, username, password):
        for usuario in self.usuarios:
            if usuario.username == username and usuario.password == password:
                return usuario
        return None

    def encontrar_usuario(self, username):
        return next((u for u in self.usuarios if u.username == username), None)

    def adicionar_item_estoque(self, nome, quantidade, descricao=""):
        self.estoque.append({
            'nome': nome,
            'quantidade': quantidade,
            'descricao': descricao,
            'disponivel': quantidade
        })
        self.salvar_dados() # Salva os dados após adicionar um item ao estoque

    def retirar_item(self, nome, quantidade, usuario):
        for item in self.estoque:
            if item['nome'] == nome and item['disponivel'] >= quantidade:
                item['disponivel'] -= quantidade
                self.cautelas.append({
                    'usuario': usuario,
                    'item': nome,
                    'quantidade': quantidade,
                })
                self.salvar_dados() # Salva os dados após a retirada
                return True
        return False

    def devolver_item(self, nome, quantidade, usuario):
 
        for item in self.estoque:
            if item['nome'] == nome:
            # Atualiza o estoque
                item['disponivel'] += quantidade

            # Procura a cautela correspondente
                for cautela in self.cautelas:
                    if (
                        cautela['usuario'] == usuario and
                        cautela['item'] == nome
                    ):
                        if quantidade <= cautela['quantidade']:
                        # Reduz a quantidade na cautela
                            cautela['quantidade'] -= quantidade
                        
                        # Remove a cautela se a quantidade chegar a 0
                            if cautela['quantidade'] == 0:
                                self.cautelas.remove(cautela)
                            self.salvar_dados()  # Salva os dados após a devolução
                            return True  # Devolução bem-sucedida
                        else:
                            return False  # Tentativa de devolver mais do que foi retirado
        return False  # Não encontrou o item ou a cautela correspondente

# Instância da aplicação
aplicacao = Aplicacao()

# Rotas
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = aplicacao.autenticar_usuario(username, password)
        if usuario:
            session['username'] = usuario.username
            return redirect(url_for('index'))
        return render_template('login.html', error="Nome de usuário ou senha incorretos")
    return render_template('login.html')

@app.route('/index')
def index():
    username = session.get('username')  # Obtém o usuário da sessão
    if not username:
        return redirect(url_for('login'))  # Redireciona para login se não estiver logado
    
    usuario_logado = aplicacao.encontrar_usuario(username)  # Busca o usuário logado
    if not usuario_logado:
        return redirect(url_for('login'))  # Redireciona caso o usuário não seja encontrado
    
    # Inicialmente, não há resultados
    return render_template('index.html', usuario=usuario_logado, resultados=None)


@app.route('/pesquisar_estoque', methods=['POST'])
def pesquisar_estoque():
    termo = request.form['termo']
    resultados = [item for item in aplicacao.estoque if termo.lower() in item['nome'].lower()]
    username = session.get('username')
    if username:
        usuario_logado = aplicacao.encontrar_usuario(username)
        return render_template('index.html', usuario=usuario_logado, resultados=resultados)
    return redirect(url_for('login'))


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

@app.route('/equipe')
def equipe():
    username = session.get('username')  # Obtém o nome de usuário da sessão
    if not username:
        return redirect(url_for('login'))  # Redireciona para o login se não houver usuário logado

    usuario_logado = aplicacao.encontrar_usuario(username)  # Busca o usuário logado
    if not usuario_logado:  # Caso o usuário não seja encontrado
        return redirect(url_for('login'))

    # Garante que a lista de usuários está sendo passada corretamente
    if aplicacao.usuarios:
        return render_template('equipe.html', usuarios=aplicacao.usuarios, usuario_logado=usuario_logado)
    else:
        return render_template('equipe.html', usuarios=[], usuario_logado=usuario_logado)

@app.route('/meu_perfil')
def meu_perfil():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    usuario = aplicacao.encontrar_usuario(username)
    if usuario:
        return render_template('meu_perfil.html', usuario=usuario)
    return redirect(url_for('login'))

@app.route('/estoque')
def estoque():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    usuario_logado = aplicacao.encontrar_usuario(username)
    return render_template('estoque.html', itens=aplicacao.estoque, usuario=usuario_logado)

@app.route('/atualizar_estoque', methods=['POST'])
def atualizar_estoque():
    nome = request.form['nome']
    nova_quantidade = int(request.form['quantidade'])
    for item in aplicacao.estoque:
        if item['nome'] == nome:
            item['quantidade'] = nova_quantidade
            item['disponivel'] = nova_quantidade
    return redirect(url_for('estoque'))

@app.route('/retirar', methods=['POST'])
def retirar():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    username = session.get('username')
    if aplicacao.retirar_item(nome, quantidade, username):
        return redirect(url_for('estoque'))
    return "Erro: Não foi possível retirar o item."

@app.route('/devolver', methods=['POST'])
def devolver():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    username = session.get('username')

    print(f"Tentativa de devolução: {nome}, quantidade: {quantidade}, usuário: {username}")
    print(f"Estado atual de cautelas: {aplicacao.cautelas}")

    if aplicacao.devolver_item(nome, quantidade, username):
        print(f"Devolução bem-sucedida de {quantidade} unidades de {nome} por {username}")
        return redirect(url_for('estoque'))
    
    print("Erro: Não foi possível devolver o item.")
    return "Erro: Não foi possível devolver o item. Verifique a quantidade informada."


@app.route('/relatorio_cautela')
def gerar_relatorio():
    """
    Gera um relatório em PDF com os registros de cautela atuais.
    """
    print("Cautelas ativas antes de gerar o relatório:", aplicacao.cautelas)  # Log para verificar as cautelas ativas

    # Cria um PDF em memória
    response = make_response()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=relatorio_cautela.pdf'

    # Cria o objeto canvas para desenhar no PDF
    pdf = canvas.Canvas(response.stream)
    
    # Cabeçalho do relatório
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "Relatório de Cautela de Materiais")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 780, f"Total de registros: {len(aplicacao.cautelas)}")
    pdf.line(50, 770, 550, 770)

    # Adicionando dados das cautelas ativas
    y_position = 750
    pdf.setFont("Helvetica", 10)

    for cautela in aplicacao.cautelas:
        pdf.drawString(50, y_position, f"Usuário: {cautela['usuario']}")
        pdf.drawString(200, y_position, f"Item: {cautela['item']}")
        pdf.drawString(350, y_position, f"Quantidade: {cautela['quantidade']}")
        y_position -= 20

        # Se a página estiver cheia, criar uma nova
        if y_position < 50:
            pdf.showPage()
            y_position = 800
            pdf.setFont("Helvetica", 10)

    # Finaliza o PDF
    pdf.save()
    return response


@app.route('/logout')
def logout():
    # Limpa a sessão do usuário
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


