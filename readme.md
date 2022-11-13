# Machine Learning for Flappy Bird usando Rede Neural e Algotmo Genético

As seguintes dependências são necessárias para a execução do jogo:

1. pygame
2. Python3.9+
3. neat-python
4. matplotlib
5. graphviz

Para instalar as dependências, faça `pip3 install -r requirements.txt`

## Arquitetura da Rede Neural

Para jogar o jogo, cada indivíduo (pássaro) possui sua própria rede neural composta pelas próximas 2 camadas:

1. uma camada de entrada com 3 neurônios representando o que um pássaro vê

```
 1) distância horizontal entre o pássaro e o cano
 2) distância vertical entre o pássaro e o cano superior
 3) distância vertical entre o pássaro e o cano inferior.
```

<center></center>
<img src="imgs/demo/inputs.png" alt="drawing"/, height = 400px>
    
2. a camada oculta, que pode aumentar ou diminuir aleátoriomente de acordo com necessidade do NEAT.

3. Uma saída

# referencias

- https://neat-python.readthedocs.io/en/latest/
- https://www.youtube.com/watch?v=MMxFDaIOHsE&ab_channel=TechWithTim
- https://www.youtube.com/watch?v=GMDb2jtzKZQ&t=1514s&ab_channel=HashtagPrograma%C3%A7%C3%A3o
