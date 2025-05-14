import os
import shutil
import json
from hashlib import sha256
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

VAULT_ENC = "VaultEncrypted"
VAULT_DEC = "VaultDecrypted"
KEY_FILE = "clave.key"
INDEX_FILE = "index.json"


def derive_key_from_password(password: str) -> bytes:
    salt = b"vault_salt"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))


def load_key_or_ask_password():
    import tkinter as tk
    from tkinter import simpledialog
    from cryptography.fernet import Fernet, InvalidToken

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        root = tk.Tk()
        root.withdraw()
        pwd = simpledialog.askstring("Key", "Introduce tu contraseña:", show="*")
        if not pwd:
            raise Exception("Contraseña no proporcionada")

        key = derive_key_from_password(pwd)

        # ✅ Validar clave intentando descifrar index.enc (si existe)
        if os.path.exists("index.enc"):
            try:
                with open("index.enc", "rb") as fidx:
                    encrypted_index = fidx.read()
                f = Fernet(key)
                f.decrypt(encrypted_index)  # prueba de clave
            except InvalidToken:
                raise Exception("❌ Contraseña incorrecta.")
            except Exception as e:
                raise Exception(f"Error al validar clave: {e}")

        # ✅ Si todo va bien, ahora sí guardamos la clave
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key


def decrypt_all(key: bytes):
    from cryptography.fernet import InvalidToken

    if not os.path.exists("index.enc"):
        # Primer uso: no hay archivos que descifrar
        print("[INFO] Primer uso: no se encontró index.json, nada que descifrar.")
        return

    f = Fernet(key)

    try:
        with open("index.enc", "rb") as fidx:
            encrypted_index = fidx.read()
        decrypted_index = f.decrypt(encrypted_index)
        index = json.loads(decrypted_index)
    except InvalidToken:
        raise Exception("❌ Contraseña incorrecta o clave inválida.")
    except Exception as e:
        raise Exception(f"Error al leer index.enc: {e}")

    for file_id, original_name in index.items():
        enc_path = os.path.join(VAULT_ENC, file_id + ".bin")
        if not os.path.exists(enc_path):
            continue
        try:
            with open(enc_path, "rb") as infile:
                encrypted = infile.read()
            decrypted = f.decrypt(encrypted)
            with open(os.path.join(VAULT_DEC, original_name), "wb") as outfile:
                outfile.write(decrypted)
        except InvalidToken:
            raise Exception(
                "❌ Contraseña incorrecta o la clave no coincide con los archivos cifrados."
            )


def encrypt_all(key: bytes):
    f = Fernet(key)
    index = {}

    if not os.path.exists(VAULT_DEC):
        return

    os.makedirs(VAULT_ENC, exist_ok=True)

    for filename in os.listdir(VAULT_DEC):
        filepath = os.path.join(VAULT_DEC, filename)
        with open(filepath, "rb") as infile:
            content = infile.read()

        encrypted = f.encrypt(content)

        file_id = sha256(filename.encode()).hexdigest()
        index[file_id] = filename

        with open(os.path.join(VAULT_ENC, file_id + ".bin"), "wb") as outfile:
            outfile.write(encrypted)

    with open(INDEX_FILE, "w") as fidx:
        json.dump(index, fidx)

    # Cifrar el index.json
    with open(INDEX_FILE, "rb") as raw_index:
        encrypted_index = f.encrypt(raw_index.read())
    with open("index.enc", "wb") as enc_index:
        enc_index.write(encrypted_index)

    os.remove(INDEX_FILE)

    shutil.rmtree(VAULT_DEC)
