# Core Blockchain Node for SypherCore
from modules.blockchain import Blockchain

def main():
    print("Starting SypherCore Node...")
    blockchain = Blockchain()
    blockchain.start()

if __name__ == "__main__":
    main()
