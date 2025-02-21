import json

class Transaction:
    def __init__(self, sender, receiver, amount, signature):
        self.sender = sender  # Clave pública del remitente
        self.receiver = receiver
        self.amount = amount
        self.signature = signature  # Firma digital

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature.hex()  # Convertir firma a formato legible
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

# Crear una transacción firmada
sender_public_key = public_key.decode()
transaction = Transaction(sender_public_key, "Bob", 2, signature)

print("✅ Transacción creada:")
print(transaction)
