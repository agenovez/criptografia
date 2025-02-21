import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, data, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), previous_block.hash, data)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Simulación del blockchain
blockchain = Blockchain(difficulty=3)

print("Minando bloque 1...")
blockchain.add_block("Transacción: Alice envía 2 BTC a Bob")

print("Minando bloque 2...")
blockchain.add_block("Transacción: Bob envía 1 BTC a Charlie")

# Verificación de la cadena
print("¿El blockchain es válido?", blockchain.is_chain_valid())

# Imprimir la blockchain
for block in blockchain.chain:
    print(f"\nBloque {block.index}")
    print(f"Hash: {block.hash}")
    print(f"Hash anterior: {block.previous_hash}")
    print(f"Datos: {block.data}")
    print(f"Nonce: {block.nonce}")
