"""Personagem jogável: Organismo + movimentação, colisão e animação."""
import math
import pygame
from ..classes_internas.organismo import Organismo
from .animacao import Animacao


class Personagem(Organismo):
    def __init__(self, x: float, y: float, nome='Explorador', idade=25):
        super().__init__(nome, idade, velocidade=158)
        self.x = float(x)
        self.y = float(y)             # ponto chão
        self.direcao = 'frente'
        self.andando = False
        self.correndo = False
        self.animacao = Animacao()
        self.acao = None
        self.tempo_acao = 0.0
        self.duracao_acao = 0.0

    def hitbox(self, x=None, y=None):
        px = self.x if x is None else x
        py = self.y if y is None else y
        return pygame.Rect(round(px) - 12, round(py) - 15, 24, 14)

    def iniciar_necessidade(self, tipo):
        if self.acao:
            return 'Estou ocupado agora.'
        if tipo == 'cagar':
            quantidade = self.dejetos
            pode = self.sistemadigestorio.PodeCagar()
        else:
            quantidade = self.urina
            pode = self.sistemadigestorio.PodeMijar()
        if not pode:
            return 'Ainda não preciso aliviar.'
        self.acao = tipo
        self.tempo_acao = 0.0
        self.duracao_acao = 1.1 + quantidade / 100 * 2.3
        self.direcao = 'costas'
        self.andando = False
        self.correndo = False
        return 'Só um instante...'

    def andar(self, dx, dy, dt, mundo, correndo=False):
        """Move com colisão por eixo; retorna True caso tenha saído do lugar."""
        if not (dx or dy):
            return False
        fator = math.hypot(dx, dy)
        dx, dy = dx / fator, dy / fator
        bioma = mundo.bioma_em(self.x)
        velocidade = self.velocidade * bioma.taxa_locomocao
        if correndo and self.PodeCorrer():
            velocidade *= 1.75 * bioma.multiplicador_corrida
        step_x, step_y = dx * velocidade * dt, dy * velocidade * dt
        movido = False
        if abs(step_x) > 0.0001 and mundo.pode_mover(self.hitbox(self.x + step_x, self.y)):
            self.x += step_x
            movido = True
        if abs(step_y) > 0.0001 and mundo.pode_mover(self.hitbox(self.x, self.y + step_y)):
            self.y += step_y
            movido = True
        return movido

    def correr(self, dx, dy, dt, mundo):
        """Movimento rápido sujeito a stamina, clima e colisões."""
        return self.andar(dx, dy, dt, mundo, correndo=True)

    # Também oferecem nomes compatíveis com os métodos originais.
    Andar = andar
    Correr = correr

    def atualizar(self, dt, teclas, mundo):
        """Retorna mensagem opcional após uma ação concluída."""
        bioma = mundo.bioma_em(self.x)
        if self.acao:
            self.tempo_acao += dt
            self.Atualizar(dt, bioma=bioma)
            self.animacao.atualizar(dt, 'parado', 'costas')
            if self.tempo_acao >= self.duracao_acao:
                tipo = self.acao
                self.acao = None
                return self.Cagar() if tipo == 'cagar' else self.Mijar()
            return None

        dx = (int(teclas[pygame.K_d] or teclas[pygame.K_RIGHT])
              - int(teclas[pygame.K_a] or teclas[pygame.K_LEFT]))
        dy = (int(teclas[pygame.K_s] or teclas[pygame.K_DOWN])
              - int(teclas[pygame.K_w] or teclas[pygame.K_UP]))
        movendo = bool(dx or dy)
        if movendo:
            normalizar = math.hypot(dx, dy)
            dx, dy = dx / normalizar, dy / normalizar
            if abs(dx) > abs(dy):
                self.direcao = 'direita' if dx > 0 else 'esquerda'
            elif dy:
                self.direcao = 'frente' if dy > 0 else 'costas'
        sprint_pedido = bool(teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT])
        sprint = bool(sprint_pedido and movendo and self.PodeCorrer())
        movido = (self.correr(dx,dy,dt,mundo) if sprint else
                  self.andar(dx,dy,dt,mundo))
        self.andando = movido
        self.correndo = sprint and movido
        self.Atualizar(dt, andando=movido, correndo=self.correndo,
                       bioma=mundo.bioma_em(self.x))
        self.animacao.atualizar(dt, 'andando' if movido else 'parado', self.direcao)
        return None

    def desenhar(self, tela, camera):
        quadro = self.animacao.quadro('andando' if self.andando else 'parado', self.direcao)
        tela.blit(quadro, (round(self.x - camera[0] - quadro.get_width()/2),
                           round(self.y - camera[1] - quadro.get_height())))
