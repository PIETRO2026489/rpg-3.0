# rpg-3.0
atualização final# rpg-3.0
atualização final
Reino de Elementaria

Um RPG 2D desenvolvido em Python com Pygame, no qual o jogador explora ilhas elementais, enfrenta monstros, evolui de nível, compra equipamentos e conquista masmorras para avançar na aventura.

Sobre o jogo

Você começa sua aventura com 100 de vida, 100 de mana e algumas moedas. No início, escolha seu elemento entre:

🔥 Fogo

💧 Água

⚡ Elétrico

🌿 Planta

Cada elemento possui ataques próprios, com diferentes valores de dano e custo de mana.

Durante a aventura, você pode explorar as ilhas, enfrentar monstros escolhidos pelo jogo, ganhar experiência e moedas, comprar equipamentos e completar missões.

Principais recursos

Evolução do personagem

Ao derrotar monstros, você recebe:

XP para aumentar o nível do personagem;

XP elemental para evoluir os ataques do elemento escolhido;

Moedas para comprar equipamentos e poções.

Ao subir de nível, sua vida máxima e sua mana máxima aumentam.

Combate

Nas batalhas existem quatro ações principais:

1 — Ataque elemental 1

2 — Ataque elemental 2

3 — Ataque elemental 3

4 — Ataque físico com punho ou espada

Os ataques elementais possuem requisitos de nível elemental e gastam mana.

Existe também uma relação de forças e fraquezas entre os elementos. Usar o elemento correto contra determinado inimigo pode aumentar o dano.

Equipamentos

Na loja, o jogador pode adquirir:

Armadura de Ferro

Armadura de Escamas

Cajado Arcano

Espada de Ferro

Escudo Elemental

Cada equipamento possui uma função diferente, como aumentar defesa, dano físico ou dano elemental.

Poções

Durante a aventura e nas batalhas é possível utilizar:

Poção de Regeneração — recupera vida;

Poção de Mana — recupera mana.

Ilhas

O jogo possui 10 ilhas, cada uma com seu próprio tema elemental:

Ilha Inicial

Ilha Vulcânica

Ilha Aquática

Ilha Eletrônica

Ilha Sombria

Ilha de Terra

Ilha Voadora

Ilha de Gelo

Ilha Fantasmagórica

Ilha Venenosa

As ilhas ficam progressivamente mais difíceis.

Masmorras

Cada ilha possui uma masmorra.

Ao entrar em uma masmorra:

existem exatamente 3 monstros;

o jogador precisa derrotar os 3;

depois das três vitórias, recebe um pergaminho;

o pergaminho libera a próxima ilha;

a masmorra concluída não precisa ser repetida.

A masmorra também possui regras próprias para impedir que o jogador simplesmente abandone o desafio.

Chefão final

Depois de avançar pelas ilhas e cumprir os requisitos da aventura, o jogador pode chegar ao portão do chefe.

O chefe final é o Dragão Guardião de Elementaria.

Ao derrotá-lo, o jogador recebe a tela de vitória e o reino é salvo da ameaça.

Missões

O jogo possui missões relacionadas à progressão da aventura, incluindo:

derrotar o primeiro monstro;

derrotar pelo menos cinco monstros diferentes;

derrotar o chefe final.

Controles

No mapa

Tecla

Ação

W A S D

Mover o personagem

Setas

Mover o personagem

M

Abrir mapa das ilhas

I

Abrir inventário

E

Interagir

F

Entrar na masmorra

B

Ir para o portão do chefe

F5

Salvar o jogo

Durante a batalha

Tecla

Ação

1

Ataque elemental 1

2

Ataque elemental 2

3

Ataque elemental 3

4

Punho/Espada

H

Usar poção de vida

P

Usar poção de mana

ESC

Sair da batalha, quando permitido

Menus

Use as teclas numéricas para selecionar opções quando elas forem exibidas na tela.

Salvamento

O jogo possui sistema de salvamento automático por arquivo.

O progresso é armazenado no arquivo:

elementaria_save.json

O salvamento pode ser realizado pressionando:

F5

Requisitos

É necessário ter:

Python 3

Pygame

Instale o Pygame com:

pip install pygame

Como executar

Abra um terminal na pasta do jogo e execute:

python jogo.py

Em alguns computadores, pode ser necessário usar:

python3 jogo.py

Estrutura básica

RPG-2.0/
├── jogo.py
├── elementaria_save.json
└── README.md

O arquivo elementaria_save.json pode ser criado pelo próprio jogo quando o progresso for salvo.

Objetivo

O objetivo principal é evoluir seu personagem, explorar as ilhas, derrotar os monstros, conquistar as masmorras, coletar os pergaminhos, desbloquear novas regiões e finalmente derrotar o Dragão Guardião de Elementaria.

Tecnologias utilizadas

Python

Pygame

JSON para o sistema de salvamento

Autor

Projeto de RPG 2D desenvolvido para estudo e prática de programação em Python.
Feito por Pietro Ferreira, Lincoln Martins e Rafael Ribeiro.
obrigado pela leitura.
