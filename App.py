import customtkinter as ctk
from tkinter import messagebox
import word_processor
import platform

class DocApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.title("Rex")
        self.geometry("800x500")

        self.setup()

    def setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=3)

        label = ctk.CTkLabel(self, text="Rex", font=("", 50))
        label.grid(row=0, column=0)

        def upload_file():
            filename = ctk.filedialog.askopenfilename(
                filetypes=[("Word files", "*.docx")]
            )
            if not filename:
                return

            self.doc = filename

            delimiting_character = '\\'
            if platform.system() == "Linux":
                delimiting_character = '/'

            short_name = filename[filename.rfind(delimiting_character) + 1:]
            if short_name == "":
                doc_title_label.configure(text="")
            else:
                doc_title_label.configure(text=f"Document incarcat: {short_name}")

            return filename

        def process_doc():
            if self.doc is None:
                messagebox.showerror("Eroare", "Nu ati incarcat niciun document")
                return
            
            doc_template, vars = word_processor.get_template_variables(self.doc)
            context = {}

            for v in vars:
                dialog = ctk.CTkInputDialog(text=v)
                value = dialog.get_input()
                context[v] = value
            
            rendered_doc = word_processor.render_docx(doc_template, context)

            path = ctk.filedialog.asksaveasfilename(
                filetypes=[("Word files", "*.docx")]
            )
            if not path:
                messagebox.showerror("Eroare", "Nu ati ales unde sa fie salvat documentul")
                return
            else:
                rendered_doc.save(path)

        upload_button = ctk.CTkButton(self, text="Incarcati document", command=upload_file, width=300, height=80, font=("", 30), fg_color="#911719", hover_color="#560809")
        upload_button.grid(row=1, column=0)

        doc_title_label = ctk.CTkLabel(self, text="", font=("", 20))
        doc_title_label.grid(row=2, column=0)

        process_button = ctk.CTkButton(self, text="Procesati document", command=process_doc, width=300, height=80, font=("", 30), fg_color="#911719", hover_color="#560809")
        process_button.grid(row=3, column=0)

if __name__ == "__main__":
    app = DocApp()
    app.mainloop() 