import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from vault_core import (
    load_key_or_ask_password,
    decrypt_all,
    encrypt_all,
    VAULT_ENC,
    VAULT_DEC,
)
from vault_gui import open_vault_window


def main():
    os.makedirs(VAULT_ENC, exist_ok=True)
    os.makedirs(VAULT_DEC, exist_ok=True)

    # Cargar clave o pedir contraseña
    try:
        key = load_key_or_ask_password()
    except Exception as e:
        messagebox.showerror("Error de clave", str(e))
        return

    # Descifrar el contenido
    decrypt_all(key)

    # Abrir la ventana de explorador
    open_vault_window(on_close=lambda: encrypt_all(key))


if __name__ == "__main__":
    main()
