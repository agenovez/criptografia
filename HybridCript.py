from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# Generación de clave AES y RSA
clave_aes = get_random_bytes(32)
clave_rsa = RSA.generate(4096)
clave_publica = clave_rsa.publickey()

# Cifrar mensaje con AES
def cifrar_mensaje(mensaje, clave_aes):
    cipher = AES.new(clave_aes, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(mensaje.encode())
    return cipher.nonce, ciphertext, tag

mensaje = "Mensaje secreto"
nonce, cifrado, tag = cifrar_mensaje(mensaje, clave_aes)
print("Mensaje cifrado:", cifrado)
