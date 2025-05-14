import os
import tkinter as tk
from tkinter import filedialog
from vault_core import VAULT_DEC


def open_vault_window(on_close):
    root = tk.Tk()
    root.title("Robincrypt v0.3")
    root.geometry("300x150")

    def open_folder():
        os.startfile(os.path.abspath(VAULT_DEC))

    def add_file():
        filepath = filedialog.askopenfilename(title="Seleccionar archivo para agregar")
        if filepath:
            filename = os.path.basename(filepath)
            dest = os.path.join(VAULT_DEC, filename)
            with open(filepath, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())

    # Crear botones con ancho completo
    btn_open = tk.Button(root, text="📂 Abrir carpeta", command=open_folder)
    btn_add = tk.Button(root, text="➕ Añadir archivo", command=add_file)
    btn_exit = tk.Button(
        root, text="🔐 Cerrar cofre", command=lambda: (on_close(), root.destroy())
    )

    # Organizar botones con relleno horizontal completo
    btn_open.pack(fill="x", padx=20, pady=10)
    btn_add.pack(fill="x", padx=20, pady=10)
    btn_exit.pack(fill="x", padx=20, pady=10)

    root.mainloop()
