# termo-
🎯 Termo

«Jogo de palavras desenvolvido em Python com interface gráfica utilizando Tkinter.»

O Termo é um jogo de adivinhação de palavras em que o jogador precisa descobrir uma palavra de 5 letras em até 6 tentativas.

A cada tentativa, o jogo fornece indicações visuais para ajudar o jogador a descobrir a palavra correta. A aplicação também conta com teclado virtual, animações e uma interface com estilo moderno e minimalista.

---

📸 Sobre o projeto

O projeto foi desenvolvido com o objetivo de praticar conceitos fundamentais de Python, programação orientada a objetos e desenvolvimento de interfaces gráficas.

A aplicação possui uma grade de 6 linhas por 5 colunas, representando as tentativas disponíveis e as letras de cada palavra.

---

✨ Funcionalidades

- 🎯 Palavras com 5 letras
- 🔢 Até 6 tentativas por partida
- ⌨️ Suporte ao teclado físico
- 🖱️ Teclado visual na interface
- 🟢 Identificação de letras na posição correta
- 🟡 Identificação de letras presentes em outra posição
- ⚫ Identificação de letras que não pertencem à palavra
- 🔄 Sistema de reinício da partida
- 📊 Contador de tentativas
- ✨ Animações durante as jogadas
- 🎉 Animação ao vencer
- 📝 Mensagens de status durante a partida
- 📚 Carregamento de palavras através do arquivo "listas.txt"
- 🛡️ Lista alternativa de palavras caso "listas.txt" não esteja disponível

O sistema de palavras carrega automaticamente palavras de exatamente cinco letras a partir de "listas.txt"; caso o arquivo não seja encontrado ou esteja vazio, utiliza uma lista alternativa integrada ao programa.

---

🛠️ Tecnologias

- Python 3
- Tkinter
- Programação Orientada a Objetos
- Manipulação de arquivos
- Estruturas de dados
- Eventos de teclado
- Animações em interface gráfica

Bibliotecas utilizadas no projeto:

import tkinter as tk
from tkinter import font as tkfont
import random
import os
import math

---

📂 Estrutura do projeto

Termo/
│
├── termo.py
├── listas.txt
└── README.md

"termo.py"

Arquivo principal responsável pela aplicação, interface gráfica, lógica do jogo, entrada de dados, avaliação das palavras e animações.

"listas.txt"

Arquivo utilizado para armazenar as palavras disponíveis para as partidas.

As palavras utilizadas pelo programa precisam possuir 5 letras.

---

🎮 Como jogar

1. Inicie o jogo

Execute o arquivo principal:

python termo.py

2. Digite uma palavra

Utilize o teclado do computador para inserir uma palavra de 5 letras.

3. Confirme

Pressione:

Enter

4. Analise as indicações

O jogo irá revelar o resultado de cada letra.

Indicação| Significado
🟢 Verde| Letra correta e na posição correta
🟡 Amarelo| Letra existe, mas está em outra posição
⚫ Escuro| Letra não está na palavra

A avaliação das palavras verifica primeiro as letras que estão na posição correta e depois identifica as letras presentes em outras posições.

---

⌨️ Controles

Tecla| Ação
"A-Z"| Digitar uma letra
"Enter"| Confirmar palavra
"Backspace"| Apagar letra
"Delete"| Apagar letra

O projeto também possui um teclado visual integrado à interface.

---

🧠 Conceitos praticados

Durante o desenvolvimento foram trabalhados conceitos como:

- Classes e objetos
- Funções e métodos
- Listas
- Dicionários
- Estruturas condicionais
- Laços de repetição
- Manipulação de arquivos
- Eventos de teclado
- Geração de valores aleatórios
- Atualização de elementos gráficos
- Animações
- Organização de interface gráfica

A aplicação é estruturada principalmente através da classe "Termo", que herda de "tk.Tk".

---

🎨 Interface

A interface utiliza uma identidade visual escura com elementos em azul, verde e amarelo.

O projeto possui componentes visuais próprios para:

- Cabeçalho
- Grade de palavras
- Indicador de tentativas
- Mensagens de status
- Teclado
- Botão de iniciar/reiniciar

---

✨ Animações

Para tornar a experiência mais dinâmica, foram implementadas diferentes animações:

Entrada de letra
O bloco aumenta levemente quando uma letra é digitada.

Tentativa inválida
A linha pode realizar uma animação horizontal para indicar que é necessário completar as 5 letras.

Revelação da palavra
As letras são reveladas individualmente com uma animação.

Vitória
Os blocos da linha vencedora realizam uma animação em sequência.

---

🏆 Sistema de vitória

O jogador vence quando a palavra digitada corresponde à palavra escolhida pelo jogo.

Após a vitória, a aplicação apresenta uma mensagem de sucesso e informa em qual tentativa a palavra foi descoberta.

Se todas as 6 tentativas forem utilizadas sem descobrir a palavra, o jogo encerra a partida e apresenta a resposta.

---

🚀 Possíveis melhorias

Algumas funcionalidades que podem ser implementadas futuramente:

- [ ] Sistema de pontuação
- [ ] Estatísticas das partidas
- [ ] Ranking de jogadores
- [ ] Modo diário
- [ ] Níveis de dificuldade
- [ ] Sons e efeitos sonoros
- [ ] Sistema de recordes
- [ ] Histórico de partidas
- [ ] Personalização do tema
- [ ] Versão para navegador

---

👨‍💻 Autor

Alex

Projeto desenvolvido para fins de estudo, prática e desenvolvimento de habilidades em programação Python.

---

⭐ Se você gostou do projeto, deixe uma estrela no repositório!
