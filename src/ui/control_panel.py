import tkinter as tk
from tkinter import ttk

class ControlPanel(ttk.Frame):
    def __init__(self, parent, add_callback, calculate_callback, remove_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="x", pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack()

        self.btn_add = ttk.Button(btn_frame, text="Add Field", command=add_callback)
        self.btn_add.pack(side="left", padx=5)

        self.btn_calc = ttk.Button(btn_frame, text="Calculate Total", command=calculate_callback)
        self.btn_calc.pack(side="left", padx=5)

        self.btn_remove = ttk.Button(btn_frame, text="Remove Group", command=remove_callback)
        self.btn_remove.pack(side="left", padx=5)
        self.btn_remove.config(state="disabled")

        self.lbl_total = ttk.Label(self, text="Total: 0", font=("Arial", 12, "bold"))
        self.lbl_total.pack(pady=3)

    def update_total(self, total_text):
        """Updates the displayed total text."""
        self.lbl_total.config(text=total_text)

    def update_remove_state(self, enabled):
        """Enables or disables the remove group button."""
        state = "normal" if enabled else "disabled"
        self.btn_remove.config(state=state)
