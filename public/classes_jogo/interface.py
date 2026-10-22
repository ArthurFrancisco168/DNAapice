"""HUD, relógio de falas, avisos e balão usado como pequeno console."""
import random
import pygame
from .config import (LARGURA_TELA, ALTURA_TELA, FALA_INTERVALO_MS,
                     FALA_DURACAO_MS)


class Balao:
    def __init__(self):
        self.fala = ''
        self.expira_em = 0
        self.proxima_fala = FALA_INTERVALO_MS
        self._rng = random.Random(1024)
        self._ultimo_aviso = {}

    def dizer(self, texto, agora, duracao=FALA_DURACAO_MS):
        self.fala = str(texto)
        self.expira_em = agora + duracao

    def avisar(self, chave, mensagem, agora, intervalo=24_000):
        if agora >= self._ultimo_aviso.get(chave, -intervalo):
            self._ultimo_aviso[chave] = agora
            self.dizer(mensagem, agora)

    def atualizar(self, agora, bioma, personagem):
        if agora >= self.proxima_fala:
            self.proxima_fala = agora + FALA_INTERVALO_MS
            self.dizer(self._rng.choice(bioma.falas), agora)
        if personagem.agua <= 22:
            self.avisar('agua','Estou com muita sede! [V] para beber.',agora)
        elif personagem.comida <= 22:
            self.avisar('comida','Estou com fome! [C] para comer.',agora)
        if personagem.urina >= 80:
            self.avisar('urina','Preciso urinar! Aperte [M].',agora)
        elif personagem.dejetos >= 80:
            self.avisar('dejetos','Preciso ir ao banheiro! [B].',agora)
        if personagem.stamina <= 12:
            self.avisar('fadiga','Sem fôlego! Preciso descansar.',agora)

    @staticmethod
    def _quebrar(texto, fonte, limite):
        linhas = []
        for paragrafo in texto.split('\n'):
            palavras = paragrafo.split()
            linha = ''
            for palavra in palavras:
                tentativa = (linha + ' ' + palavra).strip()
                if fonte.size(tentativa)[0] > limite and linha:
                    linhas.append(linha)
                    linha = palavra
                else:
                    linha = tentativa
            linhas.append(linha)
        return linhas[:5]

    def desenhar(self, tela, camera, personagem, fonte, agora):
        if not self.fala or agora >= self.expira_em:
            return
        linhas = self._quebrar(self.fala, fonte, 380)
        largura = min(420, max(140,max(fonte.size(l)[0] for l in linhas)+30))
        altura = len(linhas)*23+22
        # Balão ancorado acima da cabeça, limitado às bordas da tela.
        px = round(personagem.x-camera[0])
        py = round(personagem.y-camera[1]-66)
        bx = max(10, min(px-largura//2, LARGURA_TELA-largura-10))
        by = max(8, min(py-altura-20, ALTURA_TELA-altura-25))
        sombra = pygame.Rect(bx+3,by+3,largura,altura)
        fundo = pygame.Rect(bx,by,largura,altura)
        pygame.draw.rect(tela,(55,63,69),sombra,border_radius=10)
        pygame.draw.rect(tela,(250,248,231),fundo,border_radius=10)
        pygame.draw.rect(tela,(49,48,48),fundo,2,border_radius=10)
        ponta = [(max(bx+12,min(px,bx+largura-12))-8,by+altura),
                 (max(bx+12,min(px,bx+largura-12))+8,by+altura),
                 (max(bx+12,min(px,bx+largura-12)),by+altura+10)]
        pygame.draw.polygon(tela,(250,248,231),ponta)
        pygame.draw.lines(tela,(49,48,48),False,ponta,2)
        for i,linha in enumerate(linhas):
            tela.blit(fonte.render(linha, True,(39,43,40)),(bx+15,by+12+i*23))


class Interface:
    def __init__(self):
        self.fonte = pygame.font.SysFont('dejavusans,arial',17)
        self.fonte_pequena = pygame.font.SysFont('dejavusans,arial',15)
        self.fonte_titulo = pygame.font.SysFont('dejavusans,arial',22,bold=True)
        self.mostrar_ajuda = True

    def barra(self, tela, x, y, label, valor, cor, largura=210):
        valor = max(0,min(100,valor))
        texto = self.fonte_pequena.render(f'{label}  {valor:.0f}%',True,(248,249,250))
        tela.blit(texto,(x,y))
        fundo = pygame.Rect(x,y+21,largura,12)
        pygame.draw.rect(tela,(35,43,51),fundo,border_radius=4)
        if valor > 0:
            pygame.draw.rect(tela,cor,(x+1,y+22,round((largura-2)*valor/100),10),border_radius=3)
        pygame.draw.rect(tela,(209,217,212),fundo,1,border_radius=4)

    def desenhar(self,tela,personagem,bioma,agora):
        x,y = 14,ALTURA_TELA-164
        painel = pygame.Surface((255,153),pygame.SRCALPHA)
        pygame.draw.rect(painel,(20,30,37,208),painel.get_rect(),border_radius=11)
        tela.blit(painel,(x-8,y-8))
        self.barra(tela,x,y,'Água',personagem.agua,(65,166,244))
        self.barra(tela,x,y+44,'Comida',personagem.comida,(100,216,105))
        qtd=max(personagem.dejetos,personagem.urina)
        self.barra(tela,x,y+88,'Necessidades',qtd,(248,211,66))
        if personagem.acao:
            progresso=personagem.tempo_acao/max(.01,personagem.duracao_acao)
            pygame.draw.rect(tela,(244,194,56),(x,y+132,round(210*min(1,progresso)),4))

        painel_bpm = pygame.Surface((200,77),pygame.SRCALPHA)
        pygame.draw.rect(painel_bpm,(20,30,37,205),painel_bpm.get_rect(),border_radius=12)
        tela.blit(painel_bpm,(LARGURA_TELA-215,13))
        bpm=personagem.coracao.bpm
        # Pulso representado pelo ícone que varia de tamanho, sem alegações médicas.
        pulso = int(1+2*(1-(agora%(max(350,int(60000/max(45,bpm)))))/max(350,int(60000/max(45,bpm)))))
        cx,cy=LARGURA_TELA-191,39
        pygame.draw.polygon(tela,(233,91,100),[(cx-11-pulso,cy-2),(cx-8,cy-9-pulso),
             (cx,cy-3),(cx+8,cy-9-pulso),(cx+11+pulso,cy-2),
             (cx,cy+12+pulso)])
        tela.blit(self.fonte_titulo.render(f'{bpm:.0f} BPM',True,(255,245,244)),
                  (LARGURA_TELA-169,24))
        tela.blit(self.fonte_pequena.render(f'Energia {personagem.stamina:.0f}%',True,(205,224,234)),
                  (LARGURA_TELA-168,54))

        topo = pygame.Surface((325,66),pygame.SRCALPHA)
        pygame.draw.rect(topo,(20,30,37,180),topo.get_rect(),border_radius=10)
        tela.blit(topo,(10,10))
        tela.blit(self.fonte_titulo.render(bioma.nome,True,(245,244,218)),(22,15))
        tela.blit(self.fonte_pequena.render(f'{bioma.temperatura:.0f}°C (ambiente)  |  DNA Ápice',True,(232,235,234)),(22,48))

        if self.mostrar_ajuda:
            ajuda = ['WASD / Setas  Mover   |   Shift  Correr',
                     'C  Comer   |   V  Beber   |   B  Evacuar   |   M  Urinar',
                     'TAB  Status   |   F1  Ajuda   |   ESC  Sair']
            caixa = pygame.Surface((510,88),pygame.SRCALPHA)
            pygame.draw.rect(caixa,(20,30,37,192),caixa.get_rect(),border_radius=10)
            tela.blit(caixa,(LARGURA_TELA-525,ALTURA_TELA-102))
            for i,linha in enumerate(ajuda):
                tela.blit(self.fonte_pequena.render(linha,True,(244,247,246)),
                          (LARGURA_TELA-514,ALTURA_TELA-96+i*26))

