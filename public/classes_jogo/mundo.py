from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
import random
import pygame
from ..classes_internas import Deserto, Pampas, Taiga
from .config import (ASSETS, LARGURA_BIOMA, MAPA_LARGURA, MAPA_ALTURA,
                     CHUNK, TRANSICAO, LARGURA_TELA, ALTURA_TELA)


@dataclass
class Objeto:
    x: int
    y: int
    imagem: pygame.Surface | None
    colisao: pygame.Rect
    tipo: str = 'arvore'
    tamanho_pedra: tuple[int, int] = (0, 0)

    @property
    def profundidade(self):
        return self.y

    def desenhar(self, tela, camera):
        cx, cy = camera
        if self.imagem is not None:
            tela.blit(self.imagem, (round(self.x - cx - self.imagem.get_width()/2),
                                   round(self.y - cy - self.imagem.get_height())))
        else:
            w, h = self.tamanho_pedra
            r = pygame.Rect(round(self.x - cx - w/2), round(self.y - cy - h), w, h)
            pygame.draw.ellipse(tela, (97, 101, 95), r.move(0, 3))
            pygame.draw.ellipse(tela, (134, 137, 128), r)
            pygame.draw.ellipse(tela, (177, 172, 151), r.inflate(-max(4,w//3), -max(3,h//3)).move(-3,-2))


class Mundo:
    def __init__(self):
        self.biomas = (Deserto(), Pampas(), Taiga())
        self.chunks = OrderedDict()
        self.objetos = []
        self.colisores = []
        self.sprites_objetos = {}
        self._carregar_objetos()
        self._gerar_objetos()
        self.objetos.sort(key=lambda o: o.profundidade)

    def indice_bioma(self, x):
        return min(2, max(0, int(x) // LARGURA_BIOMA))

    def bioma_em(self, x):
        return self.biomas[self.indice_bioma(x)]

    @staticmethod
    def _interpolar(a, b, t):
        t = max(0.0, min(1.0, t))
        return tuple(round(i * (1-t) + j*t) for i,j in zip(a,b))

    def cor_em(self, x, atributo='cor_terreno'):
        indice = self.indice_bioma(x)
        cor = getattr(self.biomas[indice], atributo)
        for borda, anterior, seguinte in ((LARGURA_BIOMA, 0, 1),
                                          (2 * LARGURA_BIOMA, 1, 2)):
            if borda - TRANSICAO <= x <= borda + TRANSICAO:
                t = (x - (borda - TRANSICAO)) / (2 * TRANSICAO)
                cor = self._interpolar(getattr(self.biomas[anterior], atributo),
                                        getattr(self.biomas[seguinte], atributo), t)
                break
        return cor

    def _carregar_png(self, categoria: str, nome: str, tamanho: tuple[int, int]):
        caminho = ASSETS / 'objetos' / categoria / nome
        if not caminho.is_file():
            raise FileNotFoundError(f'Asset não encontrado: {caminho}')
        original = pygame.image.load(str(caminho)).convert_alpha()
        recorte = original.get_bounding_rect(min_alpha=2)
        if recorte.width and recorte.height:
            original = original.subsurface(recorte).copy()
        return pygame.transform.scale(original, tamanho)

    def _carregar_objetos(self):
        # adicionar árvore = incluir entrada no dicionário.
        registros = {
            'deserto': {
                'arvores': [('palmeira_tree1.png',(82,96)),
                            ('palmeira_tree2_1.png',(88,98)),
                            ('palmeira_tree2_2.png',(75,85)),
                            ('Burned_tree3.png',(64,76))],
                'marco': ('piramides_de_gizé.png',(510,370))},
            'pampas': {
                'arvores': [('Tree1.png',(83,96)), ('Tree2.png',(78,90))],
                'marco': ('lake.png',(380,315))},
            'taiga': {
                'arvores': [('pinheiro_tree1.png',(85,108)),
                            ('pinheiro_tree2.png',(77,95))],
                'marco': ('cabana_de_neve.png',(310,295))},
        }
        self.registros = registros
        for categoria, bloco in registros.items():
            for nome, tamanho in bloco['arvores'] + [bloco['marco']]:
                self.sprites_objetos[(categoria, nome)] = self._carregar_png(categoria,nome,tamanho)

    def _adicionar(self, objeto):
        self.objetos.append(objeto)
        self.colisores.append(objeto.colisao)

    def _gerar_objetos(self):
        rng = random.Random(20261021)
        categorias = ('deserto', 'pampas', 'taiga')
        # O corredor horizontal (y=520) é deliberadamente livre, inclusive nas fronteiras.
        for idx, categoria in enumerate(categorias):
            x0 = idx * LARGURA_BIOMA
            centro_x, centro_y = x0 + LARGURA_BIOMA // 2, MAPA_ALTURA // 2
            nome, tamanho = self.registros[categoria]['marco']
            imagem = self.sprites_objetos[(categoria, nome)]
            larg, alt = (290, 110) if categoria == 'deserto' else (
                (280, 140) if categoria == 'pampas' else (155, 90))
            colisao = pygame.Rect(centro_x - larg//2, centro_y - alt, larg, alt)
            self._adicionar(Objeto(centro_x, centro_y, imagem, colisao, 'marco'))

            qtd, distancia = {'deserto':(41,118), 'pampas':(29,155), 'taiga':(132,86)}[categoria]
            arv = self.registros[categoria]['arvores']
            tentativas = 0
            incluidos = 0
            while incluidos < qtd and tentativas < qtd * 65:
                tentativas += 1
                x = rng.randint(x0 + 95, x0 + LARGURA_BIOMA - 95)
                y = rng.randint(135, MAPA_ALTURA - 110)
                if abs(y - 520) < 180:
                    continue
                if abs(x - centro_x) < 380 and abs(y - centro_y) < 320:
                    continue
                if any(abs(x - obj.x) < distancia and abs(y - obj.y) < distancia
                       for obj in self.objetos if x0 <= obj.x < x0 + LARGURA_BIOMA):
                    continue
                nome, _ = rng.choice(arv)
                img = self.sprites_objetos[(categoria, nome)]
                # Colisões ocorrem no tronco/pé, não na copa da árvore.
                colisao = pygame.Rect(x-15, y-21, 30, 20)
                self._adicionar(Objeto(x,y,img,colisao))
                incluidos += 1

            for _ in range(22):
                x = rng.randint(x0 + 40, x0 + LARGURA_BIOMA - 40)
                y = rng.randint(75, MAPA_ALTURA - 50)
                if abs(y - 520) < 150:
                    continue
                w, h = rng.randint(16,29), rng.randint(12,20)
                rect = pygame.Rect(x-w//2, y-h+3, w, h-3)
                if any(rect.inflate(25,25).colliderect(c) for c in self.colisores):
                    continue
                self._adicionar(Objeto(x,y,None,rect,'pedra',(w,h)))

    def pode_mover(self, hitbox):
        if (hitbox.left < 0 or hitbox.right > MAPA_LARGURA or
                hitbox.top < 0 or hitbox.bottom > MAPA_ALTURA):
            return False
        return not any(hitbox.colliderect(c) for c in self.colisores)

    def _criar_chunk(self, ix, iy):
        surf = pygame.Surface((CHUNK, CHUNK)).convert()
        x0, y0 = ix * CHUNK, iy * CHUNK

        # 16 faixas por bloco | transição de cores 
        for faixa in range(0, CHUNK, 16):
            cor = self.cor_em(x0 + faixa + 8)
            pygame.draw.rect(surf, cor, (faixa, 0, 16, CHUNK))
        rng = random.Random((ix + 941) * 152443 + (iy+793) * 96791)

        for _ in range(90):
            x, y = rng.randrange(CHUNK), rng.randrange(CHUNK)
            world_x = x0 + x
            cor = self.cor_em(world_x, 'cor_detalhe' if rng.random() < .68 else 'cor_sombra')
            biome = self.indice_bioma(world_x)
            if biome == 0:
                w = rng.choice([3,5,8,13])
                pygame.draw.rect(surf, cor, (x,y,w,rng.choice([2,3,4])))
            elif biome == 1:
                # Tufo de grama pixelado (somente nos pampas).
                pygame.draw.line(surf, cor, (x,y+5), (x-2,y), 2)
                pygame.draw.line(surf, cor, (x,y+5), (x+2,y+1), 2)
            else:
                # Tons de gelo e micro-sombras na neve.
                pygame.draw.rect(surf, cor, (x,y,rng.randrange(3,9),2))
        return surf

    def desenhar_chao(self, tela, camera):
        camera_x, camera_y = camera
        ix0 = max(0, int(camera_x) // CHUNK)
        iy0 = max(0, int(camera_y) // CHUNK)
        ix1 = min((MAPA_LARGURA-1)//CHUNK, int(camera_x + LARGURA_TELA)//CHUNK)
        iy1 = min((MAPA_ALTURA-1)//CHUNK, int(camera_y + ALTURA_TELA)//CHUNK)
        for iy in range(iy0, iy1+1):
            for ix in range(ix0, ix1+1):
                chave = (ix,iy)
                if chave not in self.chunks:
                    self.chunks[chave] = self._criar_chunk(ix,iy)
                self.chunks.move_to_end(chave)
                tela.blit(self.chunks[chave], (ix*CHUNK-round(camera_x),
                                              iy*CHUNK-round(camera_y)))
        while len(self.chunks) > 90:
            self.chunks.popitem(last=False)

    def objetos_visiveis(self, camera):
        cx,cy = camera
        tela = pygame.Rect(cx-540,cy-400,LARGURA_TELA+1080,ALTURA_TELA+800)
        return [obj for obj in self.objetos if tela.collidepoint(obj.x,obj.y)]
