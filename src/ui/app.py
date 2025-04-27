import tkinter as tk
from tkinter import ttk
import datetime

from ui.control_panel import ControlPanel
from ui.pagination import Pagination
from model.group_manager import GroupManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Group Scoring Calculator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Frame for the groups
        self.groups_frame = ttk.Frame(root)
        self.groups_frame.pack(fill="both", expand=True)

        # Group manager
        self.manager = GroupManager(
            parent_frame=self.groups_frame,
            total_listener=self._on_total_updated,
            remove_state_listener=self._on_remove_state_changed,
            pagination_listener=self._on_pagination_updated
        )

        # Control panel (above the pagination)
        self.control_panel = ControlPanel(
            root,
            add_callback=self.manager.add_field,
            calculate_callback=self.manager.calculate_total,
            remove_callback=self.manager.remove_current_group
        )

        # Pagination
        self.pagination = Pagination(
            root,
            prev_callback=self.manager.prev_page,
            next_callback=self.manager.next_page,
            select_callback=self.manager.show_page
        )

        # Button for new group
        self.btn_new_group = tk.Button(
            root,
            text="+ New Group",
            command=self.manager.create_new_group,
            bg="#4CAF50",
            fg="white"
        )
        self.btn_new_group.pack(pady=5, side="bottom", anchor="se", padx=10)

        # Initialize pages and show the current one
        self.manager.init_pages()
        day = datetime.datetime.today().weekday()
        num = ((day + 1) % 7) + 1
        self.manager.show_page(num)

    def _on_total_updated(self, total_text):
        self.control_panel.update_total(total_text)

    def _on_remove_state_changed(self, enabled):
        self.control_panel.update_remove_state(enabled)

    def _on_pagination_updated(self, pages, current):
        self.pagination.update_buttons(pages, current)
