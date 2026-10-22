# DNA Ápice

Jogo 2D de exploração em **Python e Pygame**. Explore um mundo longo com três biomas: **Deserto do Saara → Pampas → Taiga**. O personagem tem um organismo simulado, com fome, sede, frequência cardíaca, energia e necessidades fisiológicas. Os gráficos utilizam os **sprites PNG originais** do projeto.

## Como instalar e jogar

1. Instale Python **3.10+**.
2. Abra o terminal na pasta `DNAapice` (onde está `main.py`).
3. Instale o Pygame: `python -m pip install -r requirements.txt`.
4. Inicie o jogo: `python main.py` (ou `python game.py`).

O jogo abre em uma janela de **1000 × 650**. Não precisa instalar Pillow nem baixar assets adicionais. Os caminhos dos sprites são resolvidos a partir da pasta do projeto, portanto é possível executar `main.py` de outro diretório.

### Controles

| Tecla | Ação |
| --- | --- |
| **W A S D** ou setas | Caminhar (inclusive na diagonal) |
| **Shift** + movimento | Correr, se tiver energia e hidratação suficientes |
| **C** | Comer |
| **V** | Beber água |
| **B** | Evacuar (se tiver dejetos suficientes) |
| **M** | Urinar (se tiver urina suficiente) |
| **Tab** | Mostrar status completo no balão |
| **F1** | Mostrar ou esconder ajuda |
| **Esc** | Sair |

Ao aliviar as necessidades, o personagem fica **virado de costas**, parado, por alguns segundos; o tempo depende da quantidade acumulada. Não há animação específica para isso nos assets. O aviso **“Que alívio!”** surge quando termina.

### Interface e mecânicas

- **Canto inferior esquerdo:** barras de **Água** (azul), **Comida** (verde) e **Necessidades** (amarela, a maior entre urina e dejetos). Durante o alívio, uma linha amarela acompanha o progresso.
- **Canto superior direito:** frequência cardíaca aproximada em **BPM**, ícone pulsante e energia (stamina).
- **Canto superior esquerdo:** nome e temperatura do bioma atual.
- **Balão acima do personagem:** feedback das ações, status ao pressionar **Tab**, alertas de necessidades, comentários aleatórios do bioma **a cada 3 minutos** e aviso quando entra em outro bioma.
- O mundo tem **9000 × 2200** unidades (três biomas de 3000 × 2200); a câmera acompanha o personagem e não ultrapassa o mapa.
- A passagem entre biomas usa **mistura gradual de cores do terreno**, sem uma parede entre eles.
- **Deserto:** água se esgota mais rápido e a corrida é mais lenta. Marco principal: **Pirâmides de Gizé**.
- **Pampas:** terreno ideal para correr e árvores mais espaçadas. Marco principal: **lago**.
- **Taiga:** neve reduz a velocidade e a corrida consome mais água que nos Pampas. Marco principal: **cabana**. Pinheiros mais agrupados.
- Árvores e pedras bloqueiam o personagem por meio de colisão **próxima do chão**, não pela copa. Um corredor horizontal livre permite atravessar todos os biomas sem ficar preso.
- Os recursos usados nos controles **C/V são ilimitados** nesta versão: ainda não existe sistema de inventário/coleta no escopo do projeto.

### Atributos internos

O código utiliza um **modelo simplificado para gameplay, não uma simulação médica**:

| Atributo | Como funciona |
| --- | --- |
| Comida | Diminui aos poucos e mais rapidamente quando há esforço. Comer recupera até 23 pontos. |
| Água | Diminui com o tempo, esforço e multiplicador climático. Beber recupera até 27 pontos. |
| Stamina | Corrida consome; parada ou caminhada recuperam. |
| Coração | BPM acompanha esforço e tem pequenas variações pseudoaleatórias; desacelera durante o descanso. |
| Temperatura corporal | Tende gradualmente ao valor correspondente ao clima e ao esforço. |
| Dejetos e urina | Acumulam com o tempo e ao comer/beber. Para eliminar, devem estar em pelo menos 20%. |

**Correr é bloqueado** quando água/comida/energia estão muito baixas ou o organismo está muito exigido. A velocidade depende do bioma. O jogo atualiza tudo usando `Clock.tick(FPS) / 1000`, em segundos (e limita `dt` de cada frame para evitar atravessar obstáculos após travamento da janela).

## Organização do projeto

```text
DNAapice/
├── main.py                    
├── game.py                     
├── requirements.txt          
├── README.md
├── assets/
│   └── sprites/
│       ├── animacao_idle_personagens/  
│       ├── animacao_andando_personagens/  
│       └── objetos/
│           ├── deserto/      
│           ├── pampas/        
│           └── taiga/         
├── public/
│   ├── classes_internas/
│   │   ├── organismo.py
│   │   ├── coracao.py
│   │   ├── sistema_digestorio.py
│   │   ├── bioma.py
│   │   ├── deserto.py
│   │   ├── pampas.py
│   │   └── taiga.py
│   └── classes_jogo/
│       ├── config.py
│       ├── personagem.py
│       ├── animacao.py
│       ├── mundo.py
│       ├── interface.py
│       └── game.py
├── tests/
│   └── test_organismo.py
└── legado/
    ├── aa_original.py
    ├── classes_original.py
    └── README_original.txt
```