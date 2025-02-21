#Como ejecutar P2P
#Iniciar nodo:
#python nombre_del_script.py
#Iniciar en un nodo
#curl -X POST http://127.0.0.1:5001/connect -H "Content-Type: application/json" -d '{"host":"127.0.0.1", "port":5000}'
#Minar
#curl -X POST http://127.0.0.1:5001/mine -H "Content-Type: application/json" -d '{"data":"Nuevo bloque de prueba"}'
import hashlib
import time
import json
import socket
import threading
from flask import Flask, request, jsonify

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
    def __init__(self, difficulty=3):
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

# ---------------------- Red P2P ----------------------

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []  # Lista de nodos conectados
        self.blockchain = Blockchain()

    def start_server(self):
        """Inicia el servidor P2P en un hilo separado."""
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def run_server(self):
        """Servidor que escucha nuevas conexiones."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"🌐 Nodo en marcha en {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            print(f"📡 Conexión entrante de {address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client):
        """Maneja la comunicación con otros nodos."""
        try:
            data = client.recv(1024).decode("utf-8")
            if data == "REQUEST_CHAIN":
                chain_data = json.dumps([block.__dict__ for block in self.blockchain.chain])
                client.send(chain_data.encode("utf-8"))
            elif data.startswith("NEW_BLOCK:"):
                block_data = json.loads(data.split("NEW_BLOCK:")[1])
                new_block = Block(**block_data)
                if self.validate_and_add_block(new_block):
                    print("✅ Nuevo bloque agregado a la blockchain!")
                else:
                    print("⚠️ Bloque inválido recibido.")
        except Exception as e:
            print(f"Error al manejar cliente: {e}")
        finally:
            client.close()

    def connect_to_peer(self, peer_host, peer_port):
        """Conecta este nodo a otro nodo en la red."""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((peer_host, peer_port))
            self.peers.append((peer_host, peer_port))
            print(f"🔗 Conectado a {peer_host}:{peer_port}")
        except Exception as e:
            print(f"❌ No se pudo conectar con {peer_host}:{peer_port}: {e}")

    def broadcast_block(self, block):
        """Envia el nuevo bloque a todos los nodos conectados."""
        for peer_host, peer_port in self.peers:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((peer_host, peer_port))
                block_data = json.dumps(block.__dict__)
                client.send(f"NEW_BLOCK:{block_data}".encode("utf-8"))
                client.close()
            except Exception as e:
                print(f"⚠️ No se pudo enviar el bloque a {peer_host}:{peer_port}: {e}")

    def validate_and_add_block(self, block):
        """Verifica si un bloque recibido es válido y lo agrega."""
        latest_block = self.blockchain.get_latest_block()
        if block.previous_hash == latest_block.hash and block.calculate_hash() == block.hash:
            self.blockchain.chain.append(block)
            return True
        return False

# ---------------------- Interfaz REST con Flask ----------------------

app = Flask(__name__)
node = P2PNode("127.0.0.1", 5000)
node.start_server()

@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.json.get("data", "Bloque vacío")
    node.blockchain.add_block(data)
    new_block = node.blockchain.get_latest_block()
    node.broadcast_block(new_block)
    return jsonify({"message": "Bloque minado y transmitido", "block": new_block.__dict__}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in node.blockchain.chain]
    return jsonify(chain_data), 200

@app.route('/connect', methods=['POST'])
def connect_peer():
    peer_host = request.json.get("host")
    peer_port = request.json.get("port")
    node.connect_to_peer(peer_host, peer_port)
    return jsonify({"message": f"Conectado a {peer_host}:{peer_port}"}), 200

if __name__ == '__main__':
    app.run(port=5001)
