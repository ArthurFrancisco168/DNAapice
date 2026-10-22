from .bioma import Bioma


class Pampas(Bioma):
    def __init__(self):
        super().__init__(
            nome='Pampas', temperatura=23.0, taxa_locomocao=1.0,
            taxa_alimentacao=1.0, gasto_agua=1.0,
            cor_terreno=(155, 179, 101), cor_detalhe=(120, 154, 82),
            cor_sombra=(103, 132, 73),
            falas=('Que brisa agradável!', 'Esse campo é tão tranquilo...',
                   'Perfeito para correr!', 'Um lago no meio do campo!'))
