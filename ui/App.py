from ui.Paginacao import Paginacao
from ui.PainelControles import PainelControles
from model.GerenciadorGrupos import GerenciadorGrupos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Pontuação")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.gerenciador = GerenciadorGrupos()
        self.paginacao = Paginacao(root, self.on_pagina_trocada)
        self.controles = PainelControles(root, self.adicionar_campo, self.calcular_total, self.remover_grupo)

        self.current_num = None

    def on_pagina_trocada(self, num):
        self.show_page(num)

    def show_page(self, num):
        grupo = self.gerenciador.obter_grupo(num)
        grupo.frame.pack()
        self.current_num = num
