import tkinter as tk
from tkinter import ttk
import datetime

from ui.controlPanel import ControlPanel
from ui.pagination import Pagination
from model.groupManager import GerenciadorGrupos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Pontuação por Grupos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Frame para os grupos
        self.grupos_frame = ttk.Frame(root)
        self.grupos_frame.pack(fill="both", expand=True)

        # Gerenciador de grupos
        self.gerenciador = GerenciadorGrupos(
            parent_frame=self.grupos_frame,
            total_listener=self._on_total_updated,
            remove_state_listener=self._on_remove_state_changed,
            pagination_listener=self._on_pagination_updated
        )

        # Painel de controles (acima da paginação)
        self.control_panel = ControlPanel(
            root,
            add_callback=self.gerenciador.adicionar_campo,
            calculate_callback=self.gerenciador.calcular_total,
            remove_callback=self.gerenciador.remove_current_group
        )

        # Paginação
        self.pagination = Pagination(
            root,
            prev_callback=self.gerenciador.prev_page,
            next_callback=self.gerenciador.next_page,
            select_callback=self.gerenciador.show_page
        )

        # Botão para novo grupo
        self.btn_novo_grupo = tk.Button(
            root,
            text="+ Novo Grupo",
            command=self.gerenciador.criar_novo_grupo,
            bg="#4CAF50",
            fg="white"
        )
        self.btn_novo_grupo.pack(pady=5, side="bottom", anchor="se", padx=10)

        # Inicializa páginas e mostra a atual
        self.gerenciador.init_pages()
        dia = datetime.datetime.today().weekday()
        num = ((dia + 1) % 7) + 1
        self.gerenciador.show_page(num)

    def _on_total_updated(self, total_text):
        self.control_panel.update_total(total_text)

    def _on_remove_state_changed(self, enabled):
        self.control_panel.update_remove_state(enabled)

    def _on_pagination_updated(self, pages, current):
        self.pagination.update_buttons(pages, current)