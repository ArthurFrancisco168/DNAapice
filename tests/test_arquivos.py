"""Verifica o pacote de assets sem Pygame ou dependências extras."""
import unittest
from pathlib import Path
from public.classes_jogo.config import ASSETS


class TesteArquivos(unittest.TestCase):
    def test_animacoes(self):
        for diretorio, prefixo, minimo in (
            ('animacao_idle_personagens','idle',4),
            ('animacao_andando_personagens','andando',6),
        ):
            for direcao in ('frente','costas','direita','esquerda'):
                imagens=list((ASSETS/diretorio).glob(f'{prefixo}_{direcao}_*.png'))
                self.assertGreaterEqual(len(imagens),minimo,
                                        f'Faltam sprites: {diretorio}/{direcao}')

    def test_marcos(self):
        for bioma,imagem in (
            ('deserto','piramides_de_gizé.png'),
            ('pampas','lake.png'),
            ('taiga','cabana_de_neve.png'),
        ):
            self.assertTrue((ASSETS/'objetos'/bioma/imagem).is_file())


if __name__=='__main__':
    unittest.main()
