import re
import pygame
from .config import ASSETS, SPRITE_ALTURA


class Animacao:
    DIRECOES = ('frente', 'costas', 'esquerda', 'direita')

    def __init__(self):
        self.quadros = {}
        for estado, pasta, prefixo in (
            ('parado', 'animacao_idle_personagens', 'idle'),
            ('andando', 'animacao_andando_personagens', 'andando'),
        ):
            for direcao in self.DIRECOES:
                arquivos = list((ASSETS / pasta).glob(f'{prefixo}_{direcao}_*.png'))
                arquivos.sort(key=lambda p: int(re.search(r'_(\d+)\.png$', p.name).group(1)))
                if not arquivos:
                    raise FileNotFoundError(f'Faltam sprites: {pasta}/{prefixo}_{direcao}_*.png')
                originais = [pygame.image.load(str(p)).convert_alpha() for p in arquivos]
                altura_max = max(frame.get_height() for frame in originais)
                fator = SPRITE_ALTURA / altura_max
                quadros = [pygame.transform.scale(frame, (
                    max(1, round(frame.get_width() * fator)),
                    max(1, round(frame.get_height() * fator)))) for frame in originais]
                self.quadros[(estado, direcao)] = quadros
        self.tempo = 0.0
        self.indice = 0
        self.estado_anterior = None

    def atualizar(self, dt, estado, direcao):
        chave = (estado, direcao)
        if chave != self.estado_anterior:
            self.tempo, self.indice = 0.0, 0
            self.estado_anterior = chave
        duracao = 0.11 if estado == 'andando' else 0.20
        self.tempo += dt
        if self.tempo >= duracao:
            passos = int(self.tempo / duracao)
            self.tempo %= duracao
            self.indice = (self.indice + passos) % len(self.quadros[chave])

    def quadro(self, estado, direcao):
        return self.quadros[(estado, direcao)][self.indice % len(self.quadros[(estado, direcao)])]
