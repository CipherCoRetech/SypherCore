import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
from src.blockchain import Blockchain
from wallet.app import Wallet
from faucet.faucet import Faucet
from contracts.privacy_contract import PrivacyContract
import logging
import sys
import socket
import threading

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SypherCoreMain:
    def __init__(self):
        self.blockchain = None
        self.wallet = None
        self.faucet = None
        self.peers = []

    def initialize_blockchain(self):
        logging.info("Initializing SypherCore Blockchain...")
        self.blockchain = Blockchain()
        self.blockchain.create_genesis_block()
        logging.info("Genesis block created successfully.")

    def start_wallet(self):
        logging.info("Starting Wallet...")
        self.wallet = Wallet()
        logging.info("Wallet setup complete.")

    def start_faucet(self):
        logging.info("Starting Faucet Service...")
        self.faucet = Faucet()
        logging.info("Faucet service is ready for token distribution.")

    def deploy_smart_contract(self):
        logging.info("Deploying Privacy Contract...")
        contract = PrivacyContract()
        contract.deploy(self.blockchain)
        logging.info("Privacy Contract deployed successfully.")

    def run(self):
        logging.info("SypherCore Blockchain Node is Running...")
        while True:
            try:
                user_input = input("Enter command (transaction/mine/quit/peers/connect): ").strip().lower()
                if user_input == "transaction":
                    self.handle_transaction()
                elif user_input == "mine":
                    self.mine_block()
                elif user_input == "peers":
                    self.show_peers()
                elif user_input == "connect":
                    self.connect_peer()
                elif user_input == "quit":
                    logging.info("Shutting down the SypherCore Node...")
                    sys.exit(0)
                else:
                    logging.warning("Unknown command. Available commands: transaction, mine, peers, connect, quit.")
            except KeyboardInterrupt:
                logging.info("Received exit signal. Shutting down the SypherCore Node.")
                sys.exit(0)

    def handle_transaction(self):
        logging.info("Creating a new transaction...")
        sender = input("Enter sender address: ")
        receiver = input("Enter receiver address: ")
        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            logging.error("Invalid amount. Please enter a valid number.")
            return

        transaction = self.wallet.create_transaction(sender, receiver, amount)
        if transaction:
            self.blockchain.add_transaction(transaction)
            logging.info(f"Transaction from {sender} to {receiver} for {amount} Sypher tokens created.")
        else:
            logging.error("Transaction failed. Please check your balance or addresses.")

    def mine_block(self):
        logging.info("Starting mining operation...")
        if self.blockchain.mine_pending_transactions():
            logging.info("Block mined and added to the blockchain.")
        else:
            logging.error("Mining failed. Make sure there are transactions to include in the block.")

    def show_peers(self):
        if not self.peers:
            logging.info("No peers connected.")
        else:
            logging.info(f"Connected peers: {', '.join(self.peers)}")

    def connect_peer(self):
        logging.info("Connecting to a new peer...")
        peer_address = input("Enter peer address (IP:Port): ").strip()
        if self.validate_peer_address(peer_address):
            if peer_address not in self.peers:
                self.peers.append(peer_address)
                logging.info(f"Successfully connected to peer {peer_address}.")
            else:
                logging.warning("Peer is already connected.")
        else:
            logging.error("Invalid peer address. Please provide a valid IP and port.")

    @staticmethod
    def validate_peer_address(peer_address):
        try:
            host, port = peer_address.split(':')
            socket.inet_aton(host)
            int(port)  # Make sure port is a valid integer
            return True
        except (socket.error, ValueError):
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SypherCore Blockchain Node")
    parser.add_argument("--genesis", action="store_true", help="Initialize the blockchain with the genesis block")
    args = parser.parse_args()

    main_app = SypherCoreMain()

    if args.genesis:
        main_app.initialize_blockchain()

    main_app.start_wallet()
    main_app.start_faucet()
    main_app.deploy_smart_contract()
    main_app.run()
