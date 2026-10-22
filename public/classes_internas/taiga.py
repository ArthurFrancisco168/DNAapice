from .bioma import Bioma


class Taiga(Bioma):
    def __init__(self):
        super().__init__(
            nome='Taiga', temperatura=-8.0, taxa_locomocao=0.88,
            taxa_alimentacao=0.95, gasto_agua=1.30,
            cor_terreno=(228, 235, 240), cor_detalhe=(201, 215, 225),
            cor_sombra=(169, 195, 205),
            falas=('Que frio!', 'Será que há alguém na cabana?',
                   'A neve deixa tudo silencioso...', 'Preciso me aquecer!'),
            multiplicador_corrida=0.77)
