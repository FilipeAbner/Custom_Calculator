import tkinter as tk
from tkinter import ttk

class CampoItem:
    def __init__(
        self,
        parent,
        remove_callback=None,
        pontuacao_fixa=None,
        titulo=None,
        quantidade=0
    ):
        self.frame = ttk.Frame(parent)
        self.score_var = tk.StringVar(value=str(pontuacao_fixa) if pontuacao_fixa is not None else "")
        self.qty_var = tk.StringVar(value=str(quantidade))

        ttk.Label(self.frame, text=titulo, width=25, anchor="w").grid(row=0, column=0, padx=5, pady=2)
        self.score_entry = ttk.Entry(
            self.frame,
            width=8,
            textvariable=self.score_var,
            justify="center"
        )
        self.score_entry.grid(row=0, column=1, padx=5)
        if pontuacao_fixa is not None:
            self.score_entry.configure(state="readonly")

        ttk.Label(self.frame, text="x").grid(row=0, column=2)
        self.qty_entry = ttk.Entry(
            self.frame,
            width=12,
            textvariable=self.qty_var,
            justify="center"
        )
        self.qty_entry.grid(row=0, column=3, padx=5)
        self.qty_entry.bind("<FocusIn>", self._clear_qty)

        if remove_callback:
            ttk.Button(
                self.frame,
                text="Remover",
                command=self._remove
            ).grid(row=0, column=4, padx=5)
            self.remove_callback = remove_callback
        else:
            self.remove_callback = None

    def _clear_qty(self, event):
        if self.qty_var.get() == "0":
            self.qty_var.set("")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def _remove(self):
        if self.remove_callback:
            self.remove_callback(self)
            self.frame.destroy()

    def calcular(self):
        try:
            score = float(self.score_var.get())
            qty = float(self.qty_var.get())
            return score * qty
        except ValueError:
            return 0