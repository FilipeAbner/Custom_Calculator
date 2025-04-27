from model.pontuation_group import ScoreGroup
from util.starter_pages import add_default_fields


class GroupManager:
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

        self.pages = {}
        self.current_num = None
        self.current_page = None
        self.last_page = 7

    def init_pages(self):
        for i in range(1, 8):
            self._add_page(i, f"UC Day {i}")
            page = self.pages[i]
            add_default_fields(i, page)

    def _add_page(self, num, title):
        grp = ScoreGroup(
            self.parent_frame,
            name=title,
            remove_callback=(lambda g, n=num: self.remove_group(n))
        )
        grp.frame.pack_forget()
        self.pages[num] = grp

    def show_page(self, num):
        if self.current_page:
            self.current_page.frame.pack_forget()
        self.current_num = num
        self.current_page = self.pages[num]
        self.current_page.frame.pack(fill="both", expand=True)
        self._notify_total()
        self._notify_remove_state()
        self._notify_pagination()

    def add_field(self):
        if self.current_page:
            self.current_page.add_field()

    def calculate_total(self):
        if self.current_page:
            self.current_page.calculate_total()
            if self.total_listener:
                self.total_listener(self.current_page.total_var.get())

    def remove_current_group(self):
        if self.current_num:
            self.remove_group(self.current_num)

    def remove_group(self, num):
        if num <= 7:
            return
        grp = self.pages.pop(num)
        grp.frame.destroy()
        if num == self.current_num:
            pages = sorted(self.pages.keys())
            next_page = None
            for off in range(1, len(pages) + 2):
                for candidate in (num + off, num - off):
                    if candidate in self.pages:
                        next_page = candidate
                        break
                if next_page:
                    break
            if next_page:
                self.show_page(next_page)
        self._notify_pagination()

    def prev_page(self):
        pages = sorted(self.pages.keys())
        idx = pages.index(self.current_num)
        if idx > 0:
            self.show_page(pages[idx - 1])

    def next_page(self):
        pages = sorted(self.pages.keys())
        idx = pages.index(self.current_num)
        if idx < len(pages) - 1:
            self.show_page(pages[idx + 1])

    def create_new_group(self):
        self.last_page += 1
        num = self.last_page
        self._add_page(num, f"Group {num}")
        self.show_page(num)

    def _notify_total(self):
        if self.total_listener:
            self.total_listener(self.current_page.total_var.get())

    def _notify_remove_state(self):
        if self.remove_state_listener:
            enabled = self.current_num > 7
            self.remove_state_listener(enabled)

    def _notify_pagination(self):
        if self.pagination_listener:
            self.pagination_listener(self.pages.keys(), self.current_num)
