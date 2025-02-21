def verify_transaction(public_key_pem, transaction_data, signature):
    """Verifica la firma de una transacción"""
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Crear hash de la transacción
    transaction_hash = hashes.Hash(hashes.SHA256())
    transaction_hash.update(transaction_data.encode())
    hashed_transaction = transaction_hash.finalize()

    try:
        public_key.verify(
            signature,
            hashed_transaction,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# Verificar la transacción
is_valid = verify_transaction(public_key, transaction, signature)
print("✅ Firma válida:", is_valid)
