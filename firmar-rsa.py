from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def sign_transaction(private_key_pem, transaction_data):
    """Firma una transacción con la clave privada"""
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)

    # Crear hash de la transacción
    transaction_hash = hashes.Hash(hashes.SHA256())
    transaction_hash.update(transaction_data.encode())
    hashed_transaction = transaction_hash.finalize()

    # Firmar la transacción
    signature = private_key.sign(
        hashed_transaction,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

# Firmar una transacción de ejemplo
transaction = "Alice envía 2 BTC a Bob"
signature = sign_transaction(private_key, transaction)
print("✅ Transacción firmada!")
