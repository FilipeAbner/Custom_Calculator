from model.pontuation_group import GrupoPontuacao
from util.starter_pages import add_default_fields


class GerenciadorGrupos:
    def __init__(
        self,
        parent_frame,
        total_listener=None,
        remove_state_listener=None,
        pagination_listener=None
    ):
        self.parent_frame = parent_frame
        self.total_listener = total_listener
        self.remove_state_listener = remove_state_listener
        self.pagination_listener = pagination_listener

        self.paginas = {}
        self.current_num = None
        self.pagina_atual = None
        self.ultima_pagina = 7

    def init_pages(self):
        for i in range(1, 8):
            self._add_page(i, f"UC Day {i}")
            page = self.paginas[i]
            add_default_fields(i, page)

    def _add_page(self, num, title):
        grp = GrupoPontuacao(
            self.parent_frame,
            nome=title,
            remove_callback=(lambda g, n=num: self.remove_group(n))
        )
        grp.frame.pack_forget()
        self.paginas[num] = grp

    def show_page(self, num):
        if self.pagina_atual:
            self.pagina_atual.frame.pack_forget()
        self.current_num = num
        self.pagina_atual = self.paginas[num]
        self.pagina_atual.frame.pack(fill="both", expand=True)
        self._notify_total()
        self._notify_remove_state()
        self._notify_pagination()

    def adicionar_campo(self):
        if self.pagina_atual:
            self.pagina_atual.adicionar_campo()

    def calcular_total(self):
        if self.pagina_atual:
            self.pagina_atual.calcular_total()
            if self.total_listener:
                self.total_listener(self.pagina_atual.total_var.get())

    def remove_current_group(self):
        if self.current_num:
            self.remove_group(self.current_num)

    def remove_group(self, num):
        if num <= 7:
            return
        grp = self.paginas.pop(num)
        grp.frame.destroy()
        if num == self.current_num:
            pages = sorted(self.paginas.keys())
            next_page = None
            for off in range(1, len(pages) + 2):
                for candidate in (num + off, num - off):
                    if candidate in self.paginas:
                        next_page = candidate
                        break
                if next_page:
                    break
            if next_page:
                self.show_page(next_page)
        self._notify_pagination()

    def prev_page(self):
        pages = sorted(self.paginas.keys())
        idx = pages.index(self.current_num)
        if idx > 0:
            self.show_page(pages[idx - 1])

    def next_page(self):
        pages = sorted(self.paginas.keys())
        idx = pages.index(self.current_num)
        if idx < len(pages) - 1:
            self.show_page(pages[idx + 1])

    def criar_novo_grupo(self):
        self.ultima_pagina += 1
        num = self.ultima_pagina
        self._add_page(num, f"Grupo {num}")
        self.show_page(num)

    def _notify_total(self):
        if self.total_listener:
            self.total_listener(self.pagina_atual.total_var.get())

    def _notify_remove_state(self):
        if self.remove_state_listener:
            enabled = self.current_num > 7
            self.remove_state_listener(enabled)

    def _notify_pagination(self):
        if self.pagination_listener:
            self.pagination_listener(self.paginas.keys(), self.current_num)