import pygame
import random
import math

# ============================================================
# CONFIGURAÇÕES
# ============================================================

pygame.init()

LARGURA_TELA = 1000
ALTURA_TELA = 650

TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("DNA Apce")

RELOGIO = pygame.time.Clock()

# Cores
VERDE_GRAMA = (240, 150, 50)
VERDE_GRAMA_2 = (82, 160, 80)
MARROM = (110, 75, 45)
CINZA = (100, 100, 100)
CINZA_ESCURO = (65, 65, 65)
BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
AZUL = (60, 130, 230)
PELE = (255, 200, 160)
VERMELHO = (200, 60, 60)
AMARELO = (255, 220, 60)

# ============================================================
# MAPA
# ============================================================

MAPA_LARGURA = 3000
MAPA_ALTURA = 2200

# ============================================================
# PERSONAGEM
# ============================================================

personagem = pygame.Rect(
    MAPA_LARGURA // 2,
    MAPA_ALTURA // 2,
    40,
    55
)

VELOCIDADE = 5

# ============================================================
# PEDRAS
# ============================================================

random.seed(10)

pedras = []

for i in range(100):
    x = random.randint(50, MAPA_LARGURA - 80)
    y = random.randint(50, MAPA_ALTURA - 80)

    pedra = pygame.Rect(
        x,
        y,
        random.randint(25, 60),
        random.randint(20, 45)
    )

    # Não colocar pedra inicialmente em cima do personagem
    if not pedra.colliderect(personagem.inflate(250, 250)):
        pedras.append(pedra)

# ============================================================
# ÁRVORES
# ============================================================

arvores = []

for i in range(45):
    x = random.randint(50, MAPA_LARGURA - 80)
    y = random.randint(50, MAPA_ALTURA - 100)

    arvore = pygame.Rect(x, y, 45, 70)

    if not arvore.colliderect(personagem.inflate(250, 250)):
        arvores.append(arvore)

# ============================================================
# FALAS
# ============================================================

falas = [
    "DNA Apice",
    "CHICO Arthur Francisco",
    "Tung Tung Sahur",
    "Cachorro Ouvido Au Au",
    "Ai meu cu"
]

fala_atual = 0
tempo_ultima_fala = pygame.time.get_ticks()

DURACAO_FALA = 5000       # fala fica visível por 5 segundos
INTERVALO_FALA = 10000     # nova fala a cada 10 segundos

fala_visivel = True
tempo_inicio_fala = pygame.time.get_ticks()

# ============================================================
# CÂMERA
# ============================================================

camera_x = 0
camera_y = 0

# ============================================================
# FONTES
# ============================================================

fonte = pygame.font.SysFont("arial", 22)
fonte_pequena = pygame.font.SysFont("arial", 18)
fonte_titulo = pygame.font.SysFont("arial", 28, bold=True)

# ============================================================
# FUNÇÕES
# ============================================================

def desenhar_personagem():
    """
    Desenha um personagem simples.
    """

    # Posição na tela
    x = personagem.x - camera_x
    y = personagem.y - camera_y

    # Pernas
    pygame.draw.rect(TELA, (40, 60, 150), (x + 7, y + 35, 10, 20))
    pygame.draw.rect(TELA, (40, 60, 150), (x + 23, y + 35, 10, 20))

    # Corpo
    pygame.draw.rect(
        TELA,
        AZUL,
        (x + 5, y + 18, 30, 25),
        border_radius=5
    )

    # Cabeça
    pygame.draw.circle(
        TELA,
        PELE,
        (x + 20, y + 12),
        13
    )

    # Cabelo
    pygame.draw.arc(
        TELA,
        (50, 30, 20),
        (x + 7, y - 2, 26, 20),
        math.pi,
        2 * math.pi,
        5
    )

    # Olhos
    pygame.draw.circle(TELA, PRETO, (x + 15, y + 10), 2)
    pygame.draw.circle(TELA, PRETO, (x + 25, y + 10), 2)


def desenhar_pedra(pedra):
    """
    Desenha uma pedra com sombra.
    """

    x = pedra.x - camera_x
    y = pedra.y - camera_y

    # sombra
    pygame.draw.ellipse(
        TELA,
        (60, 110, 60),
        (x - 4, y + pedra.height - 5,
         pedra.width + 8, 12)
    )

    # pedra
    pygame.draw.ellipse(
        TELA,
        CINZA,
        (x, y, pedra.width, pedra.height)
    )

    # parte clara
    pygame.draw.ellipse(
        TELA,
        (125, 125, 125),
        (
            x + pedra.width // 5,
            y + 4,
            pedra.width // 3,
            pedra.height // 3
        )
    )


def desenhar_arvore(arvore):
    x = arvore.x - camera_x
    y = arvore.y - camera_y

    # tronco
    pygame.draw.rect(
        TELA,
        MARROM,
        (x + 15, y + 30, 15, 40)
    )

    # copa
    pygame.draw.circle(
        TELA,
        (35, 120, 45),
        (x + 22, y + 25),
        28
    )

    pygame.draw.circle(
        TELA,
        (45, 140, 50),
        (x + 10, y + 30),
        20
    )

    pygame.draw.circle(
        TELA,
        (40, 130, 45),
        (x + 35, y + 30),
        20
    )


def desenhar_balao():
    """
    Desenha o balão de fala acima do personagem.
    """

    if not fala_visivel:
        return

    texto = fonte_pequena.render(falas[fala_atual], True, PRETO)

    largura = texto.get_width() + 30
    altura = 45

    personagem_x = personagem.x - camera_x
    personagem_y = personagem.y - camera_y

    # Posicionar o balão acima do personagem
    balao_x = personagem_x + 20 - largura // 2
    balao_y = personagem_y - 70

    # Não deixar o balão sair da tela
    balao_x = max(10, min(balao_x, LARGURA_TELA - largura - 10))

    # Sombra
    pygame.draw.rect(
        TELA,
        (80, 80, 80),
        (balao_x + 3, balao_y + 3, largura, altura),
        border_radius=12
    )

    # Balão
    pygame.draw.rect(
        TELA,
        BRANCO,
        (balao_x, balao_y, largura, altura),
        border_radius=12
    )

    # Borda
    pygame.draw.rect(
        TELA,
        PRETO,
        (balao_x, balao_y, largura, altura),
        2,
        border_radius=12
    )

    # Triângulo apontando para o personagem
    pontos = [
        (personagem_x - 8, balao_y + altura),
        (personagem_x + 8, balao_y + altura),
        (personagem_x, balao_y + altura + 12)
    ]

    pygame.draw.polygon(TELA, BRANCO, pontos)
    pygame.draw.lines(TELA, PRETO, False, pontos + [pontos[0]], 2)

    TELA.blit(
        texto,
        (balao_x + 15, balao_y + 12)
    )


def pode_mover(novo_retangulo):
    """
    Verifica se o personagem pode ocupar a nova posição.
    """

    # Limites do mapa
    if novo_retangulo.left < 0:
        return False

    if novo_retangulo.right > MAPA_LARGURA:
        return False

    if novo_retangulo.top < 0:
        return False

    if novo_retangulo.bottom > MAPA_ALTURA:
        return False

    # Colisão com pedras
    for pedra in pedras:
        if novo_retangulo.colliderect(pedra):
            return False

    # Colisão com árvores
    for arvore in arvores:
        if novo_retangulo.colliderect(arvore):
            return False

    return True


# ============================================================
# LOOP PRINCIPAL
# ============================================================

rodando = True

while rodando:

    RELOGIO.tick(60)

    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # ESC fecha o jogo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

    # --------------------------------------------------------
    # MOVIMENTO
    # --------------------------------------------------------

    teclas = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        dx -= VELOCIDADE

    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        dx += VELOCIDADE

    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        dy -= VELOCIDADE

    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        dy += VELOCIDADE

    # Movimento diagonal normalizado
    if dx != 0 and dy != 0:
        fator = 0.707
        dx = int(dx * fator)
        dy = int(dy * fator)

    # Movimento horizontal
    novo_x = personagem.copy()
    novo_x.x += dx

    if pode_mover(novo_x):
        personagem.x = novo_x.x

    # Movimento vertical
    novo_y = personagem.copy()
    novo_y.y += dy

    if pode_mover(novo_y):
        personagem.y = novo_y.y

    # --------------------------------------------------------
    # CÂMERA
    # --------------------------------------------------------

    camera_x = personagem.centerx - LARGURA_TELA // 2
    camera_y = personagem.centery - ALTURA_TELA // 2

    # Limites da câmera
    camera_x = max(0, min(camera_x, MAPA_LARGURA - LARGURA_TELA))
    camera_y = max(0, min(camera_y, MAPA_ALTURA - ALTURA_TELA))

    # --------------------------------------------------------
    # SISTEMA DE FALA
    # --------------------------------------------------------

    agora = pygame.time.get_ticks()

    if agora - tempo_ultima_fala >= INTERVALO_FALA:

        fala_atual += 1

        if fala_atual >= len(falas):
            fala_atual = 0

        tempo_ultima_fala = agora
        tempo_inicio_fala = agora
        fala_visivel = True

    # Esconder depois de alguns segundos
    if fala_visivel and agora - tempo_inicio_fala >= DURACAO_FALA:
        fala_visivel = False

    # --------------------------------------------------------
    # DESENHAR MAPA
    # --------------------------------------------------------

    TELA.fill(VERDE_GRAMA)

    # Pequenos detalhes no chão
    # São desenhados usando a posição da câmera
    random.seed(20)

    for i in range(500):

        x = random.randint(0, MAPA_LARGURA)
        y = random.randint(0, MAPA_ALTURA)

        tela_x = x - camera_x
        tela_y = y - camera_y

        if -10 < tela_x < LARGURA_TELA + 10 and \
           -10 < tela_y < ALTURA_TELA + 10:

            pygame.draw.circle(
                TELA,
                VERDE_GRAMA_2,
                (tela_x, tela_y),
                2
            )

    # --------------------------------------------------------
    # DESENHAR ÁRVORES
    # --------------------------------------------------------

    for arvore in arvores:

        # Só desenhar se estiver na tela
        area_tela = pygame.Rect(
            arvore.x - camera_x,
            arvore.y - camera_y,
            arvore.width,
            arvore.height
        )

        if area_tela.colliderect(
            pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA)
        ):
            desenhar_arvore(arvore)

    # --------------------------------------------------------
    # DESENHAR PEDRAS
    # --------------------------------------------------------

    for pedra in pedras:

        area_tela = pygame.Rect(
            pedra.x - camera_x,
            pedra.y - camera_y,
            pedra.width,
            pedra.height
        )

        if area_tela.colliderect(
            pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA)
        ):
            desenhar_pedra(pedra)

    # --------------------------------------------------------
    # PERSONAGEM
    # --------------------------------------------------------

    desenhar_personagem()

    # --------------------------------------------------------
    # BALÃO DE FALA
    # --------------------------------------------------------

    desenhar_balao()

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    pygame.draw.rect(
        TELA,
        (0, 0, 0, 120),
        (10, 10, 240, 75),
        border_radius=10
    )

    texto_controle = fonte_pequena.render(
        "WASD / Setas: mover",
        True,
        BRANCO
    )

    texto_sair = fonte_pequena.render(
        "ESC: sair",
        True,
        BRANCO
    )

    TELA.blit(texto_controle, (25, 25))
    TELA.blit(texto_sair, (25, 52))

    # --------------------------------------------------------
    # ATUALIZAR TELA
    # --------------------------------------------------------

    pygame.display.flip()


pygame.quit()
