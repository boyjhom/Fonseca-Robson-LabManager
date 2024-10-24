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
