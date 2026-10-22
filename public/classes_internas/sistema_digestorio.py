def limitar(valor: float, minimo: float = 0, maximo: float = 100) -> float:
    return max(minimo, min(maximo, valor))


class SistemaDigestorio:
    def __init__(self):
        self.comida = 100.0
        self.agua = 100.0
        self.dejetos = 0.0
        self.urina = 0.0
        self.tax_eficiencia = 1.0

    def update_tax_alimentacao(self, taxa: float) -> None:
        self.tax_eficiencia = limitar(taxa, 0.25, 2.0)

    def Comer(self) -> bool:
        if self.comida >= 99:
            return False
        self.comida = limitar(self.comida + 23 * self.tax_eficiencia)
        self.dejetos = limitar(self.dejetos + 14)
        return True

    def Beber(self) -> bool:
        if self.agua >= 99:
            return False
        self.agua = limitar(self.agua + 27 * self.tax_eficiencia)
        self.urina = limitar(self.urina + 15)
        return True

    def PodeCagar(self) -> bool:
        return self.dejetos >= 20

    def PodeMijar(self) -> bool:
        return self.urina >= 20

    def Cagar(self) -> bool:
        if not self.PodeCagar():
            return False
        self.dejetos = 0
        return True

    def Mijar(self) -> bool:
        if not self.PodeMijar():
            return False
        self.urina = 0
        return True

    def Consumir(self, esforco: float, dt: float, gasto_agua: float = 1.0) -> None:
        dt = max(0.0, dt)
        esforco = limitar(esforco, 0, 1)
        self.comida = limitar(self.comida - (0.045 + 0.23 * esforco) * dt)
        self.agua = limitar(self.agua - (0.075 + 0.44 * esforco) * gasto_agua * dt)
        # Os resíduos se acumulam lentamente mesmo entre refeições.
        self.dejetos = limitar(self.dejetos + (0.012 + 0.025 * esforco) * dt)
        self.urina = limitar(self.urina + (0.030 + 0.018 * esforco) * dt)

    def MostrarStatus(self) -> str:
        return (f"Comida {self.comida:.0f}% | Água {self.agua:.0f}%\n"
                f"Dejetos {self.dejetos:.0f}% | Urina {self.urina:.0f}%")
