import socket
import threading
import json
import time
import logging
from modules.blockchain import Blockchain
from modules.transaction import Transaction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.blockchain = Blockchain()
        self.peers = set()  # Set of known peer nodes
        self.running = True

    def start_node(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
        self.connect_to_network()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        logging.info(f"Node server started on {self.host}:{self.port}")

        while self.running:
            client_socket, client_address = server_socket.accept()
            logging.info(f"Connection established with {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(4096).decode()
            if not data:
                return

            message = json.loads(data)
            action = message.get("action")

            if action == "new_transaction":
                self.handle_new_transaction(message)
            elif action == "new_block":
                self.handle_new_block(message)
            elif action == "get_chain":
                self.send_chain(client_socket)
            elif action == "get_peers":
                self.send_peers(client_socket)
            else:
                logging.warning(f"Unknown action received: {action}")

        except Exception as e:
            logging.error(f"Error handling client: {e}")

        finally:
            client_socket.close()

    def handle_new_transaction(self, message):
        try:
            transaction_data = message.get("transaction")
            transaction = Transaction(
                sender=transaction_data["sender"],
                receiver=transaction_data["receiver"],
                amount=transaction_data["amount"],
                signature=transaction_data["signature"]
            )
            if self.blockchain.validate_transaction(transaction):
                self.blockchain.add_transaction(transaction)
                logging.info(f"New transaction added: {transaction}")
                self.broadcast_transaction(transaction)
            else:
                logging.warning("Transaction validation failed")
        except Exception as e:
            logging.error(f"Failed to handle new transaction: {e}")

    def handle_new_block(self, message):
        try:
            block_data = message.get("block")
            block = self.blockchain.create_block_from_data(block_data)
            if self.blockchain.add_block(block):
                logging.info(f"New block added to the chain: {block.index}")
                self.broadcast_block(block)
            else:
                logging.warning("Block validation failed")
        except Exception as e:
            logging.error(f"Failed to handle new block: {e}")

    def send_chain(self, client_socket):
        try:
            chain_data = json.dumps(self.blockchain.to_dict())
            client_socket.sendall(chain_data.encode())
            logging.info("Blockchain sent to requesting node")
        except Exception as e:
            logging.error(f"Failed to send blockchain: {e}")

    def send_peers(self, client_socket):
        try:
            peers_data = json.dumps(list(self.peers))
            client_socket.sendall(peers_data.encode())
            logging.info("List of peers sent to requesting node")
        except Exception as e:
            logging.error(f"Failed to send peers: {e}")

    def connect_to_network(self):
        while True:
            try:
                peer_host = input("Enter peer host to connect (or 'done' to finish): ").strip()
                if peer_host.lower() == 'done':
                    break
                peer_port = int(input("Enter peer port: "))

                self.connect_peer(peer_host, peer_port)
            except ValueError:
                logging.error("Invalid port. Please enter a valid number.")
            except Exception as e:
                logging.error(f"Failed to connect to peer: {e}")

    def connect_peer(self, peer_host, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            self.peers.add((peer_host, peer_port))
            logging.info(f"Connected to peer: {peer_host}:{peer_port}")
            peer_socket.close()
        except Exception as e:
            logging.error(f"Failed to connect to peer {peer_host}:{peer_port} - {e}")

    def broadcast_transaction(self, transaction):
        message = json.dumps({
            "action": "new_transaction",
            "transaction": transaction.to_dict()
        })
        self.broadcast(message)

    def broadcast_block(self, block):
        message = json.dumps({
            "action": "new_block",
            "block": block.to_dict()
        })
        self.broadcast(message)

    def broadcast(self, message):
        for peer in list(self.peers):
            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect(peer)
                peer_socket.sendall(message.encode())
                peer_socket.close()
                logging.info(f"Message broadcasted to {peer}")
            except Exception as e:
                logging.error(f"Failed to send message to {peer} - {e}")
                self.peers.discard(peer)

    def stop_node(self):
        logging.info("Stopping SypherCore Node...")
        self.running = False
        for peer in list(self.peers):
            self.peers.discard(peer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SypherCore Node")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address of the node")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the node on")
    args = parser.parse_args()

    node = Node(host=args.host, port=args.port)
    try:
        node.start_node()
    except KeyboardInterrupt:
        node.stop_node()
