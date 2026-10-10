class SistemaDigestorio:
    def __init__(self):
        self.comida = 100 #0/100
        self.agua = 100 #0/100
        self.dejetos = 0 #0/100

    def Comer(self):
        if self.comida < 91:
            self.comida += 10
            return True
        else:
            return False
        
    def Beber(self):
        if self.agua < 91:
            self.agua += 10
            return True
        else:
            return False

    def Cagar(self):
        self.comida = 0

    def Mijar(self):
        self.agua = 0

    def MostrarStatus(self):
        return f"Comida: {self.comida}"

class Pulmao:
    def __init__(self):
        pass

class Organismo:
    def __init__(self, nome, idade, velocidade=10):
        self.nome = nome
        self.idade = idade
        self.velocidade = velocidade
        self.mult_velocidade = 1
        self.temperatura = 36.5
        self.stamina = 100
        self.agua = 100
        self.comida = 100
        self.pulmao = Pulmao()
        self.sistemadigestorio = SistemaDigestorio()

    def Correr(self):
        condicoes_ok = (
            self.comida > 30 
            and self.agua > 30 
            and self.stamina > 30 
            and 35.5 < self.temperatura < 37.5
        )   
        if not condicoes_ok:
            print("Não consigo correr!")
            return
        self.stamina -= 1
        self.temperatura += 0.1

    def Descansar(self):
        if self.temperatura > 36.5:
            self.temperatura -= 0.2
        else:
            print("Já descansei o suficiente")

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