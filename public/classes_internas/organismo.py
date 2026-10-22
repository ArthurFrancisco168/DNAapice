from .coracao import Coracao
from .sistema_digestorio import SistemaDigestorio, limitar


class Organismo:
    esforco_andando = 0.22
    esforco_correndo = 0.88

    def __init__(self, nome: str, idade: int, velocidade: float = 155):
        self.nome = nome
        self.idade = idade
        self.velocidade = velocidade
        self.mult_velocidade = 1.0
        self.temperatura = 36.5
        self.stamina = 100.0
        self.coracao = Coracao(idade)
        self.sistemadigestorio = SistemaDigestorio()

    @property
    def comida(self):
        return self.sistemadigestorio.comida

    @property
    def agua(self):
        return self.sistemadigestorio.agua

    @property
    def dejetos(self):
        return self.sistemadigestorio.dejetos

    @property
    def urina(self):
        return self.sistemadigestorio.urina

    def PodeCorrer(self):
        return (self.comida > 15 and self.agua > 15 and self.stamina > 8
                and self.coracao.intensidade < 0.92 and self.temperatura < 38.2)

    def Atualizar(self, dt, andando=False, correndo=False, bioma=None):
        """Recebe dt em segundos do Clock.tick()/1000; retorna se correu."""
        dt = max(0.0, dt)
        correndo = bool(correndo and andando and self.PodeCorrer())
        esforco = self.esforco_correndo if correndo else self.esforco_andando if andando else 0.0
        self.mult_velocidade = 1.75 if correndo else 1.0
        gasto_agua = getattr(bioma, 'gasto_agua', 1.0)
        self.sistemadigestorio.update_tax_alimentacao(getattr(bioma, 'taxa_alimentacao', 1.0))
        self.sistemadigestorio.Consumir(esforco, dt, gasto_agua)
        self.coracao.Atualizar(esforco, dt)
        intensidade = self.coracao.intensidade
        if correndo:
            self.stamina -= (12 + 13 * intensidade) * dt
        else:
            recuperacao = 10 if not andando else 4.5
            self.stamina += recuperacao * (1 - 0.4 * intensidade) * dt
        self.stamina = limitar(self.stamina)
        ambiente = getattr(bioma, 'temperatura', 20.0)
        alvo = 36.5 + max(0, ambiente - 20) * 0.032 + esforco * 0.42
        self.temperatura += (alvo - self.temperatura) * min(1, dt * 0.17)
        return correndo

    def Descansar(self, dt=1, bioma=None):
        self.Atualizar(dt, bioma=bioma)

    def Comer(self) -> str:
        return 'Nham! Energia recuperada.' if self.sistemadigestorio.Comer() else 'Já estou de barriga cheia!'

    def Beber(self) -> str:
        return 'Ahh, água fresquinha!' if self.sistemadigestorio.Beber() else 'Já estou hidratado!'

    def Cagar(self) -> str:
        return 'Que alívio!' if self.sistemadigestorio.Cagar() else 'Ainda não preciso fazer isso.'

    def Mijar(self) -> str:
        return 'Que alívio!' if self.sistemadigestorio.Mijar() else 'Ainda não preciso fazer isso.'

    def MostrarStatus(self) -> str:
        return (f"{self.nome} | {self.coracao.MostrarStatus()}\n"
                f"Temp {self.temperatura:.1f}°C | Energia {self.stamina:.0f}%\n"
                f"{self.sistemadigestorio.MostrarStatus()}")
