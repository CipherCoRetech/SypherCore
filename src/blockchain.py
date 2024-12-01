import hashlib
import time
import json
from collections import deque

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash}, previous_hash={self.previous_hash}, transactions={self.transactions})"

class Blockchain:
    difficulty = 4  # Number of leading zeros required in hash for proof of work

    def __init__(self):
        self.chain = []
        self.pending_transactions = deque()
        self.mining_reward = 50
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.get("sender") or not transaction.get("receiver") or not transaction.get("amount"):
            raise ValueError("Transaction must include sender, receiver, and amount")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        if len(self.pending_transactions) == 0:
            print("No transactions to mine.")
            return False

        # Create a new block with all pending transactions
        new_block = Block(len(self.chain), list(self.pending_transactions), time.time(), self.get_latest_block().hash)

        # Perform proof of work
        new_block = self.proof_of_work(new_block)

        # Add the newly mined block to the blockchain
        self.chain.append(new_block)
        print(f"Block mined: {new_block.hash}")

        # Clear pending transactions and reward the miner
        self.pending_transactions = deque([{
            "sender": "Network",
            "receiver": miner_address,
            "amount": self.mining_reward
        }])

        return True

    def proof_of_work(self, block):
        block.nonce = 0
        calculated_hash = block.calculate_hash()
        while not calculated_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            calculated_hash = block.calculate_hash()
        block.hash = calculated_hash
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the block is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash for block {current_block.index}")
                return False

            # Check if the block points to the correct previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash for block {current_block.index}")
                return False

        return True
