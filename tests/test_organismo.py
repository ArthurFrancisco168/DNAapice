"""Testes de comportamento independentes do pygame. Execute: python -m unittest discover -s tests -v"""
import unittest
from public.classes_internas import Organismo, Coracao, SistemaDigestorio, Deserto, Pampas, Taiga


class TesteOrganismo(unittest.TestCase):
    def test_atributos_no_intervalo(self):
        p = Organismo('Teste',25)
        for _ in range(900):
            p.Atualizar(0.05,andando=True,correndo=True,bioma=Deserto())
        for valor in (p.comida,p.agua,p.dejetos,p.urina,p.stamina):
            self.assertGreaterEqual(valor,0)
            self.assertLessEqual(valor,100)

    def test_corrida_gasta_mais_agua_que_caminhada(self):
        a,b = Organismo('A',25),Organismo('B',25)
        for _ in range(50):
            a.Atualizar(.05,andando=True,correndo=False,bioma=Pampas())
            b.Atualizar(.05,andando=True,correndo=True,bioma=Pampas())
        self.assertLess(b.agua,a.agua)
        self.assertLess(b.stamina,a.stamina)
        self.assertGreater(b.coracao.bpm,a.coracao.bpm)

    def test_deserto_gasta_mais_agua(self):
        p,q = Organismo('P',25),Organismo('Q',25)
        for _ in range(120):
            p.Atualizar(.05,andando=True,bioma=Deserto())
            q.Atualizar(.05,andando=True,bioma=Pampas())
        self.assertLess(p.agua,q.agua)

    def test_refeicoes_e_necessidades(self):
        p = Organismo('Teste',25)
        self.assertIn('cheia',p.Comer())
        p.sistemadigestorio.comida = 50
        self.assertIn('Nham',p.Comer())
        self.assertGreater(p.dejetos,0)
        self.assertIn('não preciso',p.Cagar())
        p.sistemadigestorio.dejetos = 50
        self.assertIn('alívio',p.Cagar())
        self.assertEqual(p.dejetos,0)
        p.sistemadigestorio.urina = 35
        self.assertIn('alívio',p.Mijar())
        self.assertEqual(p.urina,0)

    def test_descanso_recupera_stamina(self):
        p=Organismo('Teste',25)
        p.stamina=20
        p.Descansar(5,Pampas())
        self.assertGreater(p.stamina,20)

    def test_biomas_e_api(self):
        self.assertEqual(Deserto().get_info(1),'Deserto do Saara')
        self.assertEqual(Taiga().get_info(2),-8)
        self.assertLess(Deserto().taxa_locomocao,Pampas().taxa_locomocao)
        self.assertGreater(Deserto().gasto_agua,Taiga().gasto_agua)

    def test_coracao_bpm_limitado(self):
        c=Coracao(25)
        for i in range(900):
            c.Atualizar(1,0.04)
        self.assertGreater(c.bpm,c.bpm_repouso)
        self.assertLessEqual(c.bpm,c.bpm_max)
        for i in range(900):
            c.Atualizar(0,0.04)
        self.assertLess(c.bpm,100)


if __name__=='__main__':
    unittest.main()
