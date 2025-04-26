import tkinter as tk
from tkinter import ttk
import datetime
from CampoItem import CampoItem
from Grupo import GrupoPontuacao

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Pontuação por Grupos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Frame de grupos
        self.grupos_frame = ttk.Frame(root)
        self.grupos_frame.pack(fill="both", expand=True)

        # Controles acima da paginação
        self.controls_frame = ttk.Frame(root)
        self.controls_frame.pack(fill="x", pady=5)
        btn_frame = ttk.Frame(self.controls_frame)
        btn_frame.pack()
        self.btn_adicionar = ttk.Button(btn_frame, text="Adicionar Campo", command=self.adicionar_campo)
        self.btn_adicionar.pack(side="left", padx=5)
        self.btn_calcular = ttk.Button(btn_frame, text="Calcular Total", command=self.calcular_total)
        self.btn_calcular.pack(side="left", padx=5)
        self.btn_remover = ttk.Button(btn_frame, text="Remover Grupo", command=self._remove_current_group)
        self.btn_remover.pack(side="left", padx=5)
        self.btn_remover.config(state="disabled")
        self.lbl_total = ttk.Label(self.controls_frame, text="Total: 0", font=("Arial", 12, "bold"))
        self.lbl_total.pack(pady=3)

        # Paginação
        self.nav_frame = ttk.Frame(root)
        self.nav_frame.pack(fill="x")
        self.prev_btn = ttk.Button(self.nav_frame, text="◀", command=self.prev_page, width=3)
        self.prev_btn.pack(side="left", padx=5)
        


        self.canvas_pages = tk.Canvas(self.nav_frame, height=30, highlightthickness=0)
        self.canvas_pages.pack(side="left", fill="x", expand=True)

        # Frame interno para os botões
        self.scroll_frame = ttk.Frame(self.canvas_pages)
        # anchor nw para posicionar pelo canto superior-esquerdo
        self.canvas_window = self.canvas_pages.create_window((0, 0), window=self.scroll_frame, anchor='nw')

         # Reposiciona o frame no centro horizontalmente quando o canvas for redimensionado
        def center_buttons(event):
            # garante que o Canvas já está desenhado
            self.canvas_pages.update_idletasks()
            bbox = self.canvas_pages.bbox(self.canvas_window)
            if bbox:
                frame_width = bbox[2] - bbox[0]
                canvas_width = event.width
                x = (canvas_width - frame_width) // 2
                # reposiciona canto nw em (x, 0)
                self.canvas_pages.coords(self.canvas_window, x, 0)

        self.canvas_pages.bind("<Configure>", center_buttons)
        # centraliza sempre que o canvas muda de tamanho
        self.canvas_pages.bind("<Configure>", lambda e: self._center_pagination())
        # ... e toda vez que o conteúdo (os botões) muda de tamanho
        self.scroll_frame.bind("<Configure>", lambda e: self._center_pagination())


        self.botoes_paginas = {}
        self.page_btn_defaults = {}
        self.next_btn = ttk.Button(self.nav_frame, text="▶", command=self.next_page, width=3)
        self.next_btn.pack(side="left", padx=5)

        # Novo Grupo
        self.btn_novo_grupo = tk.Button(root, text="+ Novo Grupo", command=self.criar_novo_grupo, bg="#4CAF50", fg="white")
        self.btn_novo_grupo.pack(pady=5, side="bottom", anchor="se", padx=10)

        self.paginas = {}
        self.pagina_atual = None
        self.current_num = None
        self.ultima_pagina = 7

        self._init_pages()
        dia = datetime.datetime.today().weekday()
        self.show_page((dia + 1) % 7 + 1)

    def _init_pages(self):
        for i in range(1, 8):
            self._add_page(i, f"Dia {i}")
            if i == 6:
                page = self.paginas[i]
                page.adicionar_campo(pontuacao_fixa=300, titulo="Engine Frigate")
                page.adicionar_campo(pontuacao_fixa=3000, titulo="Reflit Frigate")
                page.adicionar_campo(pontuacao_fixa=1/100, titulo="Intel")
                page.adicionar_campo(pontuacao_fixa=2000, titulo="UnderSea Cavern")
                page.adicionar_campo(pontuacao_fixa=30, titulo="Diamond")

    def _add_page(self, num, title):
        grp = GrupoPontuacao(self.grupos_frame, nome=title, remove_callback=(lambda g, n=num: self.remove_group(n)))
        grp.frame.pack_forget()
        self.paginas[num] = grp
        btn = tk.Button(self.scroll_frame, text=str(num), width=3, command=lambda n=num: self.show_page(n))
        btn.pack(side="left", padx=2)
        self.botoes_paginas[num] = btn
        self.page_btn_defaults[num] = btn.cget('bg')

    def show_page(self, num):
        if self.pagina_atual:
            self.pagina_atual.frame.pack_forget()
        self.current_num = num
        self.pagina_atual = self.paginas[num]
        self.pagina_atual.frame.pack(fill="both", expand=True)
        # Atualiza total
        self.calcular_total()
        # Atualiza os botões de navegação
        self._update_pagination_buttons()
        # Botão remover grupo
        # Botão remover grupo: cinza e desabilitado se for uma das 7 primeiras
        if num <= 7:
           self.btn_remover.config(state="disabled")
        else:
            self.btn_remover.config(state="normal")


    def _update_pagination_buttons(self):
        # Limpa os botões atuais
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        total = sorted(self.paginas.keys())
        current = self.current_num
        max_display = 10

        def add_btn(num):
            btn = tk.Button(self.scroll_frame, text=str(num), width=3,
                            command=lambda n=num: self.show_page(n))
            if num == current:
                btn.config(bg='blue', fg='white')
            else:
                btn.config(fg='black')
            btn.pack(side="left", padx=2)

        def add_ellipsis():
            lbl = tk.Label(self.scroll_frame, text="...", width=3)
            lbl.pack(side="left", padx=2)

        if len(total) <= max_display:
            for n in total:
                add_btn(n)
        else:
            first = total[0]
            last = total[-1]
            half_range = max_display // 2

            if current <= half_range:
                for n in total[:max_display]:
                    add_btn(n)
                add_ellipsis()
                add_btn(last)
            elif current >= last - half_range + 1:
                add_btn(first)
                add_ellipsis()
                for n in total[-max_display:]:
                    add_btn(n)
            else:
                add_btn(first)
                add_ellipsis()
                mid_range = total[total.index(current) - 4: total.index(current) + 5]
                for n in mid_range:
                    add_btn(n)
                add_ellipsis()
                add_btn(last)
        #Necessario?                
        self._center_pagination()

    def adicionar_campo(self):
        if self.pagina_atual:
            self.pagina_atual.adicionar_campo()

    def calcular_total(self):
        if self.pagina_atual:
            self.pagina_atual.calcular_total()
            self.lbl_total.config(text=self.pagina_atual.total_var.get())

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

    def remove_group(self, num):
        # remove o grupo e o botão
        if num <= 7:
            return
        grp = self.paginas.pop(num)
        grp.frame.destroy()
        btn = self.botoes_paginas.pop(num)
        btn.destroy()

        # se era a página atual, escolhe a “próxima”
        if num == self.current_num:
            # gera offsets 1, 2, 3, ... e testa +offset, -offset
            next_page = None
            offsets = range(1, len(self.paginas) + 2)
            for off in offsets:
                up = num + off
                down = num - off
                if up in self.paginas:
                    next_page = up
                    break
                if down in self.paginas:
                    next_page = down
                    break

            # mostra a página encontrada (se houver)
            if next_page is not None:
                self.show_page(next_page)

    def criar_novo_grupo(self):
        self.ultima_pagina += 1
        num = self.ultima_pagina
        self._add_page(num, f"Grupo {num}")
        self.show_page(num)

    def _remove_current_group(self):
        for numero, grupo in self.paginas.items():
            if grupo == self.pagina_atual:
                self.remove_group(numero)
                break

    def _center_pagination(self):
        # força recálculo de geometria
        self.canvas_pages.update_idletasks()
        # pega bbox do window item
        bbox = self.canvas_pages.bbox(self.canvas_window)
        if not bbox:
            return
        frame_width = bbox[2] - bbox[0]
        canvas_width = self.canvas_pages.winfo_width()
        # centraliza, mas evita x negativo
        x = max((canvas_width - frame_width) // 2, 0)
        # reposiciona NW point em (x, 0)
        self.canvas_pages.coords(self.canvas_window, x, 0)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
