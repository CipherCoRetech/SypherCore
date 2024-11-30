# main.py

import argparse
from src.blockchain import Blockchain
from wallet.app import Wallet
from faucet.faucet import Faucet
from contracts.privacy_contract import PrivacyContract
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SypherCoreMain:
    def __init__(self):
        self.blockchain = None
        self.wallet = None
        self.faucet = None

    def initialize_blockchain(self):
        """
        Initializes the blockchain, setting up the genesis block and all the nodes.
        """
        logging.info("Initializing SypherCore Blockchain...")
        self.blockchain = Blockchain()
        self.blockchain.create_genesis_block()
        logging.info("Genesis block created successfully.")

    def start_wallet(self):
        """
        Initializes the wallet for user transactions.
        """
        logging.info("Starting Wallet...")
        self.wallet = Wallet()
        logging.info("Wallet setup complete.")

    def start_faucet(self):
        """
        Initializes the faucet for distributing SypherCore tokens.
        """
        logging.info("Starting Faucet Service...")
        self.faucet = Faucet()
        logging.info("Faucet service is ready for token distribution.")

    def deploy_smart_contract(self):
        """
        Deploys a privacy-oriented smart contract to the blockchain.
        """
        logging.info("Deploying Privacy Contract...")
        contract = PrivacyContract()
        contract.deploy(self.blockchain)
        logging.info("Privacy Contract deployed successfully.")

    def run(self):
        """
        Runs the SypherCore blockchain node.
        """
        logging.info("SypherCore Blockchain Node is Running...")
        while True:
            try:
                # Accepting user inputs or processing transactions here.
                user_input = input("Enter command (transaction/mine/quit): ").strip().lower()
                if user_input == "transaction":
                    self.handle_transaction()
                elif user_input == "mine":
                    self.mine_block()
                elif user_input == "quit":
                    logging.info("Shutting down the SypherCore Node...")
                    sys.exit(0)
                else:
                    logging.warning("Unknown command. Available commands: transaction, mine, quit.")
            except KeyboardInterrupt:
                logging.info("Received exit signal. Shutting down the SypherCore Node.")
                sys.exit(0)

    def handle_transaction(self):
        """
        Handles incoming transactions.
        """
        logging.info("Creating a new transaction...")
        sender = input("Enter sender address: ")
        receiver = input("Enter receiver address: ")
        amount = float(input("Enter amount to transfer: "))

        # Create a transaction and add it to the blockchain
        transaction = self.wallet.create_transaction(sender, receiver, amount)
        self.blockchain.add_transaction(transaction)
        logging.info(f"Transaction from {sender} to {receiver} for {amount} Sypher tokens created.")

    def mine_block(self):
        """
        Mines the next block in the blockchain.
        """
        logging.info("Starting mining operation...")
        self.blockchain.mine_pending_transactions()
        logging.info("Block mined and added to the blockchain.")


def parse_arguments():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description="Run SypherCore Blockchain Node")
    parser.add_argument('-w', '--wallet', action='store_true', help="Start with wallet enabled")
    parser.add_argument('-f', '--faucet', action='store_true', help="Start with faucet enabled")
    parser.add_argument('-c', '--contract', action='store_true', help="Deploy smart contract on startup")

    return parser.parse_args()

def main():
    """
    The main entry point for the SypherCore blockchain system.
    """
    # Parse command line arguments
    args = parse_arguments()

    # Initialize the SypherCoreMain instance
    sypher_core = SypherCoreMain()

    # Initialize Blockchain
    sypher_core.initialize_blockchain()

    # Initialize Wallet if specified
    if args.wallet:
        sypher_core.start_wallet()

    # Initialize Faucet if specified
    if args.faucet:
        sypher_core.start_faucet()

    # Deploy Smart Contract if specified
    if args.contract:
        sypher_core.deploy_smart_contract()

    # Run the blockchain node
    sypher_core.run()

if __name__ == "__main__":
    main()
