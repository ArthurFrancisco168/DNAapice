import argparse
import os
import random
import pygame
from .config import (LARGURA_TELA, ALTURA_TELA, FPS, MAPA_LARGURA,
                     MAPA_ALTURA, FALA_INTERVALO_MS)
from .mundo import Mundo
from .personagem import Personagem
from .interface import Interface, Balao


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
        pygame.display.set_caption('DNA Ápice • Deserto → Pampas → Taiga')
        self.relogio = pygame.time.Clock()
        self.mundo = Mundo()
        self.personagem = Personagem(180,520)
        self.interface = Interface()
        self.balao = Balao()
        self.camera = (0.,0.)
        self.rodando = True
        self.tempo = 0
        self.ultimo_bioma = self.mundo.indice_bioma(self.personagem.x)
        self.balao.dizer('Bem-vindo ao DNA Ápice! Aperte F1 para ajuda.', 0,9000)

    def usar_tecla(self, tecla):
        p, b, t = self.personagem, self.balao, self.tempo
        if tecla == pygame.K_ESCAPE:
            self.rodando = False
        elif tecla == pygame.K_F1:
            self.interface.mostrar_ajuda = not self.interface.mostrar_ajuda
        elif tecla == pygame.K_TAB:
            b.dizer(p.MostrarStatus(),t,9000)
        elif tecla == pygame.K_c:
            b.dizer(p.Comer() if not p.acao else 'Agora estou ocupado!',t)
        elif tecla == pygame.K_v:
            b.dizer(p.Beber() if not p.acao else 'Agora estou ocupado!',t)
        elif tecla == pygame.K_b:
            b.dizer(p.iniciar_necessidade('cagar'),t)
        elif tecla == pygame.K_m:
            b.dizer(p.iniciar_necessidade('mijar'),t)

    def atualizar(self, dt):
        # dt em segundos, limitado para não atravessar obstáculos após uma pausa.
        dt = min(0.05,max(0.0,dt))
        teclas = pygame.key.get_pressed()
        mensagem = self.personagem.atualizar(dt,teclas,self.mundo)
        if mensagem:
            self.balao.dizer(mensagem,self.tempo)
        idx = self.mundo.indice_bioma(self.personagem.x)
        if idx != self.ultimo_bioma:
            self.ultimo_bioma = idx
            self.balao.dizer('Cheguei ao bioma: '+self.mundo.biomas[idx].nome,self.tempo,6000)
        self.balao.atualizar(self.tempo,self.mundo.biomas[idx],self.personagem)
        self.camera=(max(0,min(self.personagem.x-LARGURA_TELA/2,MAPA_LARGURA-LARGURA_TELA)),
                     max(0,min(self.personagem.y-ALTURA_TELA/2,MAPA_ALTURA-ALTURA_TELA)))

    def desenhar(self):
        self.mundo.desenhar_chao(self.tela,self.camera)
        # Profundidade por posição dos pés: personagem passa atrás / à frente de árvores.
        lista=self.mundo.objetos_visiveis(self.camera)
        personagem_renderizado=False
        for obj in lista:
            if not personagem_renderizado and obj.profundidade >= self.personagem.y:
                self.personagem.desenhar(self.tela,self.camera)
                personagem_renderizado=True
            obj.desenhar(self.tela,self.camera)
        if not personagem_renderizado:
            self.personagem.desenhar(self.tela,self.camera)
        self.balao.desenhar(self.tela,self.camera,self.personagem,
                           self.interface.fonte,self.tempo)
        self.interface.desenhar(self.tela,self.personagem,
                                self.mundo.bioma_em(self.personagem.x),self.tempo)
        pygame.display.flip()

    def executar(self, limite_frames=0, captura=None):
        frames=0
        try:
            while self.rodando:
                dt=self.relogio.tick(FPS)/1000
                self.tempo+=round(dt*1000)
                for ev in pygame.event.get():
                    if ev.type==pygame.QUIT:
                        self.rodando=False
                    elif ev.type==pygame.KEYDOWN:
                        self.usar_tecla(ev.key)
                if not self.rodando:
                    break
                self.atualizar(dt)
                self.desenhar()
                frames+=1
                if limite_frames and frames>=limite_frames:
                    break
            if captura:
                pygame.image.save(self.tela,captura)
        finally:
            pygame.quit()


def main(argv=None):
    parser=argparse.ArgumentParser(description='DNA Ápice — jogo de exploração e sobrevivência')
    parser.add_argument('--frames',type=int,default=0,help='Executa N frames e termina (teste)')
    parser.add_argument('--screenshot',default=None,help='Salva imagem da tela no fim da execução')
    argumentos=parser.parse_args(argv)
    Jogo().executar(limite_frames=argumentos.frames,captura=argumentos.screenshot)


if __name__=='__main__':
    main()
