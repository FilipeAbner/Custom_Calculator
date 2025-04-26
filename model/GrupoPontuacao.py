import tkinter as tk
from tkinter import ttk
from model.CampoItem import CampoItem

class GrupoPontuacao:
    def __init__(self, parent, nome, remove_callback):
        self.frame = ttk.LabelFrame(parent, text=nome)
        self.campos = []
        self.total_var = tk.StringVar(value="Total: 0")
        self.remove_callback = remove_callback

        # Área rolável de campos
        self.canvas = tk.Canvas(self.frame, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='n')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.canvas_window, width=e.width)
        )
        # Bind mouse wheel only on overflow
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="y", side="right")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def adicionar_campo(self, pontuacao_fixa=None, titulo="Novo item", quantidade=0):
        campo = CampoItem(
            self.scrollable_frame,
            remove_callback=self.remover_campo,
            pontuacao_fixa=pontuacao_fixa,
            titulo=titulo,
            quantidade=quantidade
        )
        campo.pack(pady=2, anchor='center')
        self.campos.append(campo)

    def remover_campo(self, campo):
        self.campos.remove(campo)
        self.calcular_total()

    def calcular_total(self):
        total = sum(c.calcular() for c in self.campos)
        if total == int(total):
            self.total_var.set(f"Total: {int(total):,}".replace(",", "."))
        else:
            self.total_var.set(
                f"Total: {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

    def remover_grupo(self):
        self.frame.destroy()
        if self.remove_callback:
            self.remove_callback(self)

    def _on_mousewheel(self, event):
        region = self.canvas.bbox("all")
        if region and (region[3] - region[1] > self.canvas.winfo_height()):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _linux_scroll(self, event):
        region = self.canvas.bbox("all")
        if region and (region[3] - region[1] > self.canvas.winfo_height()):
            delta = -1 if event.num == 5 else 1
            self.canvas.yview_scroll(delta, "units")

    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._linux_scroll)
        self.canvas.bind_all("<Button-5>", self._linux_scroll)

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
