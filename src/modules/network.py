import socket
import threading
import json
import logging
import time
from modules.node import Node

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Network:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.node = Node(host, port)
        self.peers = set()
        self.lock = threading.Lock()

    def start_network(self):
        """ Start network services for SypherCore. """
        threading.Thread(target=self.node.start_server).start()
        self.auto_discovery()

    def auto_discovery(self):
        """ Automatically discover and connect to other peers. """
        logging.info("Starting auto-discovery of peers.")
        known_peers = [
            ("127.0.0.1", 5001),
            ("127.0.0.1", 5002)
        ]
        for peer_host, peer_port in known_peers:
            self.connect_to_peer(peer_host, peer_port)

    def connect_to_peer(self, peer_host, peer_port):
        """ Connect to a new peer and add them to the peer list. """
        with self.lock:
            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect((peer_host, peer_port))
                self.peers.add((peer_host, peer_port))
                logging.info(f"Successfully connected to peer: {peer_host}:{peer_port}")
                peer_socket.close()
            except Exception as e:
                logging.error(f"Failed to connect to peer {peer_host}:{peer_port} - {e}")

    def listen_for_network_requests(self):
        """ Listen for incoming requests from peers. """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        logging.info(f"Network server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"Received connection from {client_address}")
            threading.Thread(target=self.handle_request, args=(client_socket,)).start()

    def handle_request(self, client_socket):
        """ Handle incoming requests from peers. """
        try:
            data = client_socket.recv(4096).decode()
            if not data:
                return

            request = json.loads(data)
            action = request.get("action")

            if action == "ping":
                self.respond_pong(client_socket)
            elif action == "new_peer":
                self.add_new_peer(request)
            elif action == "sync_chain":
                self.sync_chain_with_peer(request)
            else:
                logging.warning(f"Unknown action received: {action}")

        except Exception as e:
            logging.error(f"Error handling peer request: {e}")
        finally:
            client_socket.close()

    def respond_pong(self, client_socket):
        """ Respond to a ping request from a peer. """
        response = json.dumps({"action": "pong"})
        client_socket.sendall(response.encode())
        logging.info("Responded with PONG to peer.")

    def add_new_peer(self, request):
        """ Add a new peer to the peer list. """
        peer_host = request.get("peer_host")
        peer_port = request.get("peer_port")
        if peer_host and peer_port:
            self.peers.add((peer_host, peer_port))
            logging.info(f"Added new peer to network: {peer_host}:{peer_port}")
            self.broadcast_peer_list()

    def sync_chain_with_peer(self, request):
        """ Sync blockchain with a peer. """
        peer_chain = request.get("chain")
        if peer_chain:
            with self.lock:
                current_chain_length = len(self.node.blockchain.chain)
                if len(peer_chain) > current_chain_length:
                    logging.info("Received longer chain from peer. Attempting synchronization.")
                    self.node.blockchain.replace_chain(peer_chain)
                else:
                    logging.info("Current chain is longer or equal. No replacement needed.")

    def broadcast_peer_list(self):
        """ Broadcast updated peer list to all known peers. """
        message = json.dumps({
            "action": "update_peers",
            "peers": list(self.peers)
        })
        self.broadcast(message)

    def broadcast(self, message):
        """ Send a message to all peers. """
        with self.lock:
            for peer in list(self.peers):
                try:
                    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_socket.connect(peer)
                    peer_socket.sendall(message.encode())
                    peer_socket.close()
                    logging.info(f"Broadcasted message to {peer}")
                except Exception as e:
                    logging.error(f"Failed to send message to {peer} - {e}")
                    self.peers.discard(peer)

    def initiate_ping(self):
        """ Periodically ping all peers to maintain connections. """
        while True:
            time.sleep(30)
            for peer in list(self.peers):
                try:
                    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_socket.connect(peer)
                    ping_message = json.dumps({"action": "ping"})
                    peer_socket.sendall(ping_message.encode())
                    peer_socket.close()
                    logging.info(f"Pinged {peer}")
                except Exception as e:
                    logging.error(f"Failed to ping {peer} - {e}")
                    self.peers.discard(peer)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SypherCore Network")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address for the network")
    parser.add_argument("--port", type=int, default=5000, help="Port for the network")
    args = parser.parse_args()

    network = Network(host=args.host, port=args.port)
    try:
        threading.Thread(target=network.start_network).start()
        network.listen_for_network_requests()
    except KeyboardInterrupt:
        logging.info("Shutting down SypherCore Network...")
