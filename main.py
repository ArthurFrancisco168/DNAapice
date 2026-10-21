def limitar(valor, minimo=0, maximo=100):
    return max(minimo, min(maximo, valor))


class SistemaDigestorio:
    def __init__(self):
        self.comida = 100   # 100 = cheio, 0 = faminto
        self.agua = 100     # 100 = hidratado, 0 = desidratado
        self.dejetos = 0    # 0 = vazio, 100 = precisa cagar
        self.urina = 0      # 0 = vazio, 100 = precisa mijar

    def Comer(self):
        if self.comida < 91:
            self.comida += 10
            self.dejetos = limitar(self.dejetos + 5)
            return True
        return False

    def Beber(self):
        if self.agua < 91:
            self.agua += 10
            self.urina = limitar(self.urina + 5)
            return True
        return False

    def Cagar(self):
        self.dejetos = 0

    def Mijar(self):
        self.urina = 0

    def Consumir(self, esforco, dt):
        # gasta comida e água, mais rápido com esforço.
        self.comida = limitar(self.comida - (0.05 + 0.4 * esforco) * dt)
        self.agua = limitar(self.agua - (0.08 + 0.6 * esforco) * dt)

    def MostrarStatus(self):
        return (f"Comida: {self.comida:.0f} | Água: {self.agua:.0f} | "
                f"Dejetos: {self.dejetos:.0f} | Urina: {self.urina:.0f}")


class Coracao:
    def __init__(self, idade, bpm_repouso=60):
        self.bpm_repouso = bpm_repouso
        self.bpm_max = 220 - idade
        self.bpm = bpm_repouso

    @property
    def intensidade(self):
        return (self.bpm - self.bpm_repouso) / (self.bpm_max - self.bpm_repouso) # 0.0 = repouso, 1.0 = BPM máximo

    def Atualizar(self, esforco, dt):
        alvo = self.bpm_repouso + esforco * (self.bpm_max - self.bpm_repouso)
        # sobe rápido, desce devagar
        taxa = 40 if alvo > self.bpm else 12
        passo = taxa * dt
        if abs(alvo - self.bpm) <= passo:
            self.bpm = alvo
        else:
            self.bpm += passo if alvo > self.bpm else -passo

    def MostrarStatus(self):
        return f"BPM: {self.bpm:.0f}/{self.bpm_max}"


class Organismo:
    esforco_andando = 0.2
    esforco_correndo = 1.0

    def __init__(self, nome, idade, velocidade=10):
        self.nome = nome
        self.idade = idade
        self.velocidade = velocidade
        self.mult_velocidade = 1
        self.temperatura = 36.5
        self.stamina = 100
        self.coracao = Coracao(idade)
        self.sistemadigestorio = SistemaDigestorio()

    # estado único: comida e água vivem só no sistema digestório
    @property
    def comida(self):
        return self.sistemadigestorio.comida

    @property
    def agua(self):
        return self.sistemadigestorio.agua

    def PodeCorrer(self):
        return (
            self.comida > 30
            and self.agua > 30
            and self.stamina > 10
            and self.coracao.intensidade < 0.9
            and self.temperatura < 38.0
        )

    def Atualizar(self, dt, andando=False, correndo=False): # Chame a cada frame. 'correndo' = Shift pressionado (dash).
        dash = correndo and self.PodeCorrer()
        if correndo and not dash:
            print("Não consigo correr!")

        if dash:
            esforco = self.esforco_correndo
            self.mult_velocidade = 2
        elif andando:
            esforco = self.esforco_andando
            self.mult_velocidade = 1
        else:
            esforco = 0
            self.mult_velocidade = 1

        self.coracao.Atualizar(esforco, dt)
        self.sistemadigestorio.Consumir(esforco, dt)

        # stamina: com coração acelerado, cansa mais rápido e recupera mais devagar
        i = self.coracao.intensidade
        if dash:
            self.stamina -= 15 * (0.5 + i) * dt
        else:
            self.stamina += 10 * (1 - i) * dt
        self.stamina = limitar(self.stamina)

        # temperatura: esquenta com esforço, esfria sozinha
        self.temperatura += esforco * 0.15 * dt
        self.temperatura -= (self.temperatura - 36.5) * 0.05 * dt

    def Descansar(self, dt=1.0):
        self.Atualizar(dt)

    def Comer(self):
        if self.sistemadigestorio.Comer():
            print("Nham-Nham, que delicia!")
        else:
            print("Já estou de barriga cheia!")

    def Beber(self):
        if self.sistemadigestorio.Beber():
            print("Glub-glub, que delicia!")
        else:
            print("Já estou de bexiga cheia!")

    def Cagar(self):
        self.sistemadigestorio.Cagar()
        print("Que alívio!")

    def Mijar(self):
        self.sistemadigestorio.Mijar()
        print("Que alívio!")

    def MostrarStatus(self):
        return (
            f"[{self.nome}] {self.coracao.MostrarStatus()} | "
            f"Temp: {self.temperatura:.1f}°C | Stamina: {self.stamina:.0f}\n    "
            f"{self.sistemadigestorio.MostrarStatus()}"
        )

o = Organismo("Joao", 25)
dt = 0.5

print("Dash por 10s")
for t in range(20):
    o.Atualizar(dt, andando=True, correndo=True)
    if t % 5 == 0:
        print(o.MostrarStatus())

print("Descansando por 20s")
for t in range(40):
    o.Atualizar(dt)
    if t % 10 == 0:
        print(o.MostrarStatus())