import pygame, random, math

LARGURA_TELA = 1000
ALTURA_TELA = 650

TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("DNA Ápice")

RELOGIO = pygame.time.Clock()

# ----------------------------------------
# CORES
# ----------------------------------------

# PAMPAS

PAMPAS_GRAMA = (160, 175, 95)
PAMPAS_GRAMA_2 = (135, 155, 75)
PAMPAS_FLORES = (230, 210, 140)
PAMPAS_MARROM = (115, 85, 55)
PAMPAS_ARVORE = (90, 115, 55)
PAMPAS_ARVORE_2 = (110, 135, 65)
PAMPAS_PEDRA = (125, 120, 105)
PAMPAS_SOMBRA = (100, 115, 75)


# DESERTO DO SAARA

SAARA_AREIA = (232, 193, 167)
SAARA_AREIA_2 = (218, 169, 125)
SAARA_AREIA_3 = (195, 145, 100)
SAARA_DUNA = (245, 210, 155)
SAARA_MARROM = (125, 80, 45)
SAARA_CACTO = (65, 115, 55)
SAARA_CACTO_2 = (85, 135, 65)
SAARA_PEDRA = (150, 125, 105)
SAARA_SOMBRA = (180, 140, 110)


# TAIGA

TAIGA_NEVE = (235, 242, 250)
TAIGA_NEVE_2 = (210, 225, 240)
TAIGA_GELO = (175, 205, 225)
TAIGA_GRAMA = (190, 210, 195)
TAIGA_MARROM = (90, 65, 45)
TAIGA_TRONCO = (105, 80, 55)
TAIGA_FOLHAS = (35, 75, 65)
TAIGA_FOLHAS_2 = (50, 95, 80)


# ----------------------------------------
# BIOMA LARGURA
# ----------------------------------------

LARGURA_BIOMA = 3000
ALTURA_BIOMA = 2200



# ----------------------------------------
# PERSONAGEM
# ----------------------------------------

from main import Organismo


# ----------------------------------------
# FALAS DO PERSONAGEM
# ----------------------------------------


FALAS = [
    ""
]