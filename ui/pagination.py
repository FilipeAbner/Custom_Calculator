import tkinter as tk
from tkinter import ttk

class Pagination(ttk.Frame):
    def __init__(self, parent, prev_callback, next_callback, select_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="x")

        self.prev_btn = ttk.Button(self, text="◀", command=prev_callback, width=3)
        self.prev_btn.pack(side="left", padx=5)

        self.canvas = tk.Canvas(self, height=30, highlightthickness=0)
        self.canvas.pack(side="left", fill="x", expand=True)

        self.scroll_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Centraliza botões ao redimensionar
        self.canvas.bind("<Configure>", lambda e: self._center_pagination())
        self.scroll_frame.bind("<Configure>", lambda e: self._center_pagination())

        self.next_btn = ttk.Button(self, text="▶", command=next_callback, width=3)
        self.next_btn.pack(side="left", padx=5)

        self.select_callback = select_callback
        self.botoes = {}

    def update_buttons(self, pages, current):
        """Atualiza os botões de paginação de acordo com as páginas disponíveis."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        total = sorted(pages)
        max_display = 10
        last = total[-1]
        half = max_display // 2

        def add_btn(num):
            btn = tk.Button(self.scroll_frame, text=str(num), width=3,
                            command=lambda n=num: self.select_callback(n))
            if num == current:
                btn.config(bg='blue', fg='white')
            else:
                btn.config(fg='black')
            btn.pack(side="left", padx=2)
            self.botoes[num] = btn

        def add_ellipsis():
            lbl = tk.Label(self.scroll_frame, text="...", width=3)
            lbl.pack(side="left", padx=2)

        if len(total) <= max_display:
            for n in total:
                add_btn(n)
        else:
            first = total[0]
            if current <= half:
                for n in total[:max_display]:
                    add_btn(n)
                add_ellipsis()
                add_btn(last)
            elif current >= last - half + 1:
                add_btn(first)
                add_ellipsis()
                for n in total[-max_display:]:
                    add_btn(n)
            else:
                add_btn(first)
                add_ellipsis()
                idx = total.index(current)
                mid = total[idx - half//2 : idx + half//2 + 1]
                for n in mid:
                    add_btn(n)
                add_ellipsis()
                add_btn(last)

        self._center_pagination()

    def _center_pagination(self):
        self.canvas.update_idletasks()
        bbox = self.canvas.bbox(self.canvas_window)
        if not bbox:
            return
        frame_width = bbox[2] - bbox[0]
        canvas_width = self.canvas.winfo_width()
        x = max((canvas_width - frame_width) // 2, 0)
        self.canvas.coords(self.canvas_window, x, 0)