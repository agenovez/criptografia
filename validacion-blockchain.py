class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")

    def add_transaction(self, transaction):
        """Verifica la firma y añade una transacción pendiente"""
        sender_public_key = transaction.sender.encode()
        is_valid = verify_transaction(sender_public_key, f"{transaction.sender}{transaction.receiver}{transaction.amount}", bytes.fromhex(transaction.signature))

        if is_valid:
            self.pending_transactions.append(transaction)
            print("✅ Transacción añadida!")
        else:
            print("⚠️ Transacción inválida!")

    def mine_block(self):
        """Mina un bloque con las transacciones pendientes"""
        if len(self.pending_transactions) == 0:
            print("⚠️ No hay transacciones para minar!")
            return

        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, json.dumps([tx.to_dict() for tx in self.pending_transactions]))
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        self.pending_transactions = []  # Limpiar transacciones

        print("✅ Bloque minado con transacciones!")
