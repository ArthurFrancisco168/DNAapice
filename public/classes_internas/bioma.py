from dataclasses import dataclass


@dataclass(frozen=True)
class Bioma:
    nome: str
    temperatura: float
    taxa_locomocao: float
    taxa_alimentacao: float
    gasto_agua: float
    cor_terreno: tuple[int, int, int]
    cor_detalhe: tuple[int, int, int]
    cor_sombra: tuple[int, int, int]
    falas: tuple[str, ...]
    multiplicador_corrida: float = 1.0

    def get_info(self, info):
        return {1: self.nome, 2: self.temperatura,
                3: self.taxa_locomocao, 4: self.taxa_alimentacao}.get(info)
