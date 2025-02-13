import os
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP

# -------------------- Generación y Gestión de Claves --------------------

def generar_claves():
    """Genera claves AES y RSA y las guarda en archivos."""
    clave_aes = get_random_bytes(32)
    clave_rsa = RSA.generate(4096)
    clave_publica = clave_rsa.publickey()

    # Guardar claves en archivos
    with open("clave_aes.bin", "wb") as f:
        f.write(clave_aes)
    
    with open("clave_rsa.pem", "wb") as f:
        f.write(clave_rsa.export_key())

    with open("clave_publica.pem", "wb") as f:
        f.write(clave_publica.export_key())

    print("✅ Claves generadas y guardadas correctamente.")

def cargar_claves():
    """Carga las claves AES y RSA desde archivos."""
    try:
        with open("clave_aes.bin", "rb") as f:
            clave_aes = f.read()

        with open("clave_rsa.pem", "rb") as f:
            clave_rsa = RSA.import_key(f.read())

        with open("clave_publica.pem", "rb") as f:
            clave_publica = RSA.import_key(f.read())

        print("✅ Claves cargadas correctamente.")
        return clave_aes, clave_rsa, clave_publica
    except FileNotFoundError:
        print("❌ No se encontraron las claves. Genera nuevas claves primero.")
        return None, None, None

# -------------------- Cifrado y Descifrado --------------------

def cifrar_mensaje(mensaje, clave_aes):
    """Cifra un mensaje con AES-256 en modo GCM."""
    cipher = AES.new(clave_aes, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(mensaje.encode())

    # Guardar datos cifrados en archivo
    with open("mensaje_cifrado.bin", "wb") as f:
        f.write(cipher.nonce + ciphertext + tag)

    print("✅ Mensaje cifrado y guardado en 'mensaje_cifrado.bin'.")
    return cipher.nonce, ciphertext, tag

def descifrar_mensaje(clave_aes):
    """Descifra un mensaje cifrado con AES-256 GCM."""
    try:
        with open("mensaje_cifrado.bin", "rb") as f:
            data = f.read()

        nonce = data[:16]
        ciphertext = data[16:-16]
        tag = data[-16:]

        cipher = AES.new(clave_aes, AES.MODE_GCM, nonce=nonce)
        mensaje_descifrado = cipher.decrypt_and_verify(ciphertext, tag)

        print("✅ Mensaje descifrado:", mensaje_descifrado.decode())
    except FileNotFoundError:
        print("❌ No se encontró el archivo de mensaje cifrado.")
    except ValueError:
        print("❌ Error en la verificación del mensaje. Clave incorrecta o mensaje alterado.")

# -------------------- Menú Interactivo --------------------

def menu():
    """Muestra el menú interactivo para cifrar y descifrar mensajes."""
    while True:
        print("\n📌 Menú de Cifrado AES y RSA")
        print("1. Generar claves")
        print("2. Cargar claves")
        print("3. Cifrar un mensaje")
        print("4. Descifrar un mensaje")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            generar_claves()
        elif opcion == "2":
            global clave_aes, clave_rsa, clave_publica
            clave_aes, clave_rsa, clave_publica = cargar_claves()
        elif opcion == "3":
            if clave_aes:
                mensaje = input("Escribe el mensaje a cifrar: ")
                cifrar_mensaje(mensaje, clave_aes)
            else:
                print("❌ Carga las claves primero.")
        elif opcion == "4":
            if clave_aes:
                descifrar_mensaje(clave_aes)
            else:
                print("❌ Carga las claves primero.")
        elif opcion == "5":
            print("👋 Saliendo del programa.")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

# -------------------- Ejecución --------------------

if __name__ == "__main__":
    clave_aes, clave_rsa, clave_publica = None, None, None
    menu()
