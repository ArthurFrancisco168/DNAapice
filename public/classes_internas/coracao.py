import random


class Coracao:
    def __init__(self, idade: int, bpm_repouso: int = 68, rng=None):
        self.bpm_repouso = bpm_repouso
        self.bpm_max = max(bpm_repouso + 30, 220 - idade)
        self.bpm = float(bpm_repouso)
        self._rng = rng if rng is not None else random.Random()
        self._relogio = 0.0
        self._ruido = 0.0

    @property
    def intensidade(self) -> float:
        return max(0.0, min(1.0, (self.bpm - self.bpm_repouso) /
                            (self.bpm_max - self.bpm_repouso)))

    def Atualizar(self, esforco: float, dt: float) -> None:
        dt = max(0.0, dt)
        self._relogio += dt
        if self._relogio >= 0.8:
            self._relogio %= 0.8
            self._ruido = self._rng.uniform(-2.0, 2.0)
        alvo = self.bpm_repouso + max(0.0, min(1, esforco)) * (self.bpm_max - self.bpm_repouso) * 0.78
        alvo += self._ruido
        
        velocidade = 55.0 if alvo > self.bpm else 17.0
        passo = min(abs(alvo - self.bpm), velocidade * dt)
        self.bpm += passo if alvo > self.bpm else -passo
        self.bpm = min(self.bpm_max, max(45.0, self.bpm))

    def MostrarStatus(self) -> str:
        return f"BPM: {self.bpm:.0f}/{self.bpm_max}"
