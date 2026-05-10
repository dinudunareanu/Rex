import customtkinter as ctk


class MultiLineInputDialog(ctk.CTkToplevel):
    """Dialog cu text box multi-line pentru valori de tip paragraf.
    Se închide doar la click pe OK (sau Ctrl+Enter)."""

    def __init__(self, text="", parent=None):
        super().__init__(parent)

        self._value = None

        self.title(f"Introduceți valoarea pentru: {text}")
        self.geometry("600x400")
        self.minsize(400, 250)

        # Centrăm dialogul deasupra părintelui
        self.after(100, lambda: self._center_on_parent())

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Etichetă cu numele variabilei
        label = ctk.CTkLabel(self, text=f"Valoare pentru «{text}»:", font=("", 16))
        label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Câmp text multi-line
        self.textbox = ctk.CTkTextbox(self, font=("", 14))
        self.textbox.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.textbox.focus_set()

        # Buton OK
        ok_button = ctk.CTkButton(
            self, text="OK", command=self._on_ok,
            width=200, height=40, font=("", 16),
            fg_color="#911719", hover_color="#560809"
        )
        ok_button.grid(row=2, column=0, padx=20, pady=(0, 20))

        # Ctrl+Enter confirmă
        self.bind("<Control-Return>", lambda e: self._on_ok())

        # Blocăm interacțiunea cu fereastra părinte cât timp dialogul e deschis
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _center_on_parent(self):
        """Plasează dialogul în centrul ferestrei principale."""
        if self.master:
            x = self.master.winfo_x() + (self.master.winfo_width() - self.winfo_width()) // 2
            y = self.master.winfo_y() + (self.master.winfo_height() - self.winfo_height()) // 2
            self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _on_ok(self):
        self._value = self.textbox.get("1.0", "end-1c")
        self.grab_release()
        self.destroy()

    def _on_close(self):
        """La închidere cu X, returnăm string gol."""
        self._value = ""
        self.grab_release()
        self.destroy()

    def get_input(self):
        """Așteaptă till dialogul e închis și returnează textul."""
        self.wm_protocol("WM_DELETE_WINDOW", self._on_close)
        self.wait_window(self)
        return self._value
