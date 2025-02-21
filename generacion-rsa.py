from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keys():
    """Genera un par de claves RSA (privada y pública)"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Guardar clave privada
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Guardar clave pública
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

# Generar claves para un usuario
private_key, public_key = generate_rsa_keys()

# Guardar claves en archivos
with open("private_key.pem", "wb") as f:
    f.write(private_key)

with open("public_key.pem", "wb") as f:
    f.write(public_key)

print("✅ Claves generadas y guardadas!")
