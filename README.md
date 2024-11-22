# AppliedProg
A desorganização em laboratórios tende a atrasar os trabalhos, uma vez que perde-se tempo procurando peças ou equipamentos. Por isso, este projeto tem como objetivo criar um software de organização e gerenciamento de bens, peças, componentes e equipe destinado a laboratórios. Suas funcionalidades incluem o registro do tipo de objeto, bem como a quantidade, localização no laboratório, data de aquisição, estado de funcionamento, entre outras informações. Também estão previstas funções relacionadas à administração da equipe, como o registro de membros (com login e senha), funções e trabalhos em andamento. Para manter o controle de estoque, o programa busca unir essas duas vertentes, possibilitando ao usuário da equipe, ao utilizar um material ou pegá-lo para uso exclusivo, registrar essa ação na plataforma, de forma que outros colaboradores possam saber com quem está o equipamento em questão ou a quantidade restante. O sistema também avisará caso a quantidade de um componente atinja o mínimo crítico definido pelo usuário administrador. Apesar de ser planejado para laboratórios, esse software também pode ser aplicado a controles de estoque em geral.

Tutorial biblioteca gráfica:

Biblioteca gráfica utilizada: html

Crie uma pasta para o seu projeto e dentro dela, crie os seguintes arquivos:
index.html: Este será o arquivo principal que contém o HTML.
styles.css: Este será o arquivo onde você escreverá o CSS.

No arquivo html, cria-se as seções da sua interface visual, bem como a parte mais estrutural. Exemplo:
<!--<html lang="pt">
<head> [...]
</head>
<body> [...]
</body>
</html>
-->
A seção head é onde são colocados os metadados, como estilo e links; Na seção body, é colocado o código referente a estrutura da página, como as "div", que são as unidades básicas de estrutura do html. Cada div, bem como outros elementos podem ter uma classe atribuída a eles (<div class="exemplo"). Para alterar estilos de uma div, programa-se no arquivo .css , exemplo:
exemplo{
    background-color = green}
    
Esse e outros atributos podem ser alterados no arquivo css, de maneira a editar o estilo da GUI.
Além das divs, o html possuí diversos elementos estruturais a serem adicionados na GUI. Para ver a lista toda, consultar: https://developer.mozilla.org/en-US/docs/Web/HTML/Element

Os modelos para GUI seguem um layout simples e minimalista

![Inicio](https://github.com/boyjhom/AppliedProg/blob/main/esboco_GUI/Inico_GUI.png)
![Estoque](https://github.com/boyjhom/AppliedProg/blob/main/esboco_GUI/EstoqueGUI.png)
![Equipe](https://github.com/boyjhom/AppliedProg/blob/main/esboco_GUI/Equipe_GUI.png)
![Meu Perfil](https://github.com/boyjhom/AppliedProg/blob/main/esboco_GUI/Meu_perfil_GUI.png)

### **Fluxograma e Diagrama de Classes**
![Diagrama de Classes](https://github.com/boyjhom/AppliedProg/blob/main/fluxograma_e_diagrama_de_classes/Fluxograma_LabManager.png)
![Fluxograma](https://github.com/boyjhom/AppliedProg/blob/main/fluxograma_e_diagrama_de_classes/Diagrama_de_Classes.png)


### **Funcionalidades**
- **Gerenciamento de Estoque**:
  - Registro de itens com detalhes como nome, quantidade, descrição e código.
  - Atualização de quantidades no estoque diretamente pela interface do sistema.
  - Lista predefinida de itens típicos de um laboratório de robótica, como:
    - Parafusos
    - Chave inglesa
    - Sensores de proximidade
    - Motores de passo
    - Microcontroladores
    - Fonte de alimentação
    - Cabos de conexão
    - Solda em fio
    - Multímetros
    - Chave Philips
- **Administração de Equipe**:
  - Cadastro de membros da equipe com informações como nome, cargo e e-mail.
  - Exibição dos membros em uma interface bem estruturada.
- **Perfil do Usuário**:
  - Página personalizada que exibe as informações do usuário logado.
- **Sistema de Login e Cadastro**:
  - Usuários podem se registrar e acessar o sistema utilizando suas credenciais.
- **Interface Gráfica Intuitiva**:
  - Navegação por abas para acessar as páginas de "Armazenamento", "Equipe" e "Meu Perfil".
  - Design minimalista e responsivo.

---

## **Estrutura do Projeto**

### **1. Diretórios**
O projeto está organizado em três principais pastas:
- **`templates/`**: Contém os arquivos HTML que definem as páginas do sistema (ex.: `index.html`, `estoque.html`, `equipe.html`, etc.).
- **`static/`**: Contém os recursos estáticos do projeto:
  - **Imagens**: Localizadas em `static/assets/` (ex.: logos, ícones, imagens de exemplo).
  - **CSS**: Arquivos de estilo em `static/css/` (ex.: `style.css`).
- **`app.py`**: Arquivo principal do servidor Flask que gerencia as rotas e as lógicas de backend.


### 2. Implementação do Botão "Sair"
- Foi adicionado um botão "Sair" na interface, localizado ao lado direito do menu de navegação.
- O botão permite que o usuário encerre a sessão com facilidade, redirecionando-o para a página de login.

### 3. Ajustes na Página Inicial
- Correção da duplicação da mensagem "Bem-vindo, [nome do usuário]".
- Layout reformulado para melhorar a experiência do usuário:
  - O botão "Sair" foi reposicionado ao lado do menu, sem interferir no logo ou avatar.
  - Melhor alinhamento dos elementos da página.

### 4. Sistema de Cautelas
- Implementação da funcionalidade de retirada e devolução de itens no estoque:
  - **Retirada:** Permite que os usuários registrem materiais retirados, com ajuste automático das quantidades disponíveis no estoque.
  - **Devolução:** Permite devolver itens ao estoque, com atualização das quantidades.
- As operações de retirada e devolução são registradas, vinculando o nome do usuário à transação.

### 5. Geração de Relatórios em PDF
- Foi implementada a funcionalidade de geração de relatórios de cautelas em formato PDF.
- Detalhes do relatório incluem:
  - Nome do usuário.
  - Item retirado ou devolvido.
  - Quantidade de itens.
- O relatório é gerado dinamicamente e pode ser baixado ou visualizado no navegador.

#### Requisitos para Geração de Relatórios
- A funcionalidade de PDF utiliza a biblioteca **ReportLab**. 
- Certifique-se de instalar as dependências do projeto executando:
  ```bash
  pip install reportlab
  ```

### 6. Melhorias Gerais no Código
- Reestruturação do arquivo `app.py` para garantir maior clareza e organização.
- Correção de bugs relacionados à passagem de parâmetros nas rotas.
- Ajustes no CSS para melhorar o layout e a responsividade da interface.

### 7. Sistema de Pesquisa
- Adição de um sistema de pesquisa na página `index.html`.
- Correção de bugs relacionados a duplicação de itens.

---

### Dependências Necessárias
Antes de rodar o projeto, é importante garantir que todas as dependências estão instaladas. Execute:
```bash
pip install -r requirements.txt
```

Caso não tenha o arquivo `requirements.txt`, as bibliotecas principais são:
- Flask
- ReportLab

Instale-as diretamente com:
```bash
pip install flask reportlab


