# RobinCrypt 🔐

RobinCrypt es un cofre cifrado portátil que te permite guardar archivos sensibles dentro de una memoria USB. Los datos solo pueden visualizarse tras introducir una contraseña o clave válida.

## Características
- Cifrado con Fernet (AES + HMAC)
- Nombres de archivos ocultos (hash)
- Índice cifrado (`index.enc`)
- Compatible con cientos de archivos
- Totalmente offline y autónomo

## Uso

1. Ejecuta `Robincrypt.py` o `Robincrypt.exe` desde la raíz del USB.
2. Introduce la contraseña o carga la clave.
3. Accede, añade o extrae archivos desde la interfaz.
4. Al cerrar el cofre, todo se recifra automáticamente.

## Requisitos
- Python 3.8+
- `pip install -r requirements.txt`

## Licencia
MIT
