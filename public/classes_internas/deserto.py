from .bioma import Bioma


class Deserto(Bioma):
    def __init__(self):
        super().__init__(
            nome='Deserto do Saara', temperatura=43.0,
            taxa_locomocao=0.91, taxa_alimentacao=0.95, gasto_agua=1.85,
            cor_terreno=(232, 193, 151), cor_detalhe=(215, 170, 121),
            cor_sombra=(194, 145, 100),
            falas=('Que calor!', 'Melhor economizar água!',
                   'Essas dunas parecem infinitas...', 'Olha as pirâmides!'),
            multiplicador_corrida=0.74)
