import hashlib
import json
import time
from uuid import uuid4


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the genesis block and add it to the chain.
        The genesis block is the first block in the blockchain.
        """
        genesis_block = self.create_block(previous_hash='1', proof=100)
        self.chain.append(genesis_block)

    def create_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain.
        :param proof: The proof given by the Proof of Work algorithm.
        :param previous_hash: Hash of the previous block.
        :return: A dictionary representing the new block.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        return block

    def add_block_to_chain(self, block):
        """
        Add the block to the chain.
        :param block: Block to be added.
        """
        self.chain.append(block)

    def new_transaction(self, sender, recipient, amount):
        """
        Add a new transaction to the list of transactions.
        :param sender: Address of the sender.
        :param recipient: Address of the recipient.
        :param amount: Amount to be transferred.
        :return: The index of the block that will hold this transaction.
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes
        - p is the previous proof, and p' is the new proof.
        :param last_proof: <int> Previous proof
        :return: <int> New proof
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    def valid_proof(self, last_proof, proof):
        """
        Validates the Proof.
        :param last_proof: <int> Previous proof.
        :param proof: <int> Current proof.
        :return: <bool> True if correct, False otherwise.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Add a new node to the list of nodes.
        :param address: <str> Address of node. E.g. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid.
        :param chain: <list> A blockchain.
        :return: <bool> True if valid, False if not.
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Consensus Algorithm, resolves conflicts by replacing the chain with the longest one.
        :return: <bool> True if the chain was replaced, False if not.
        """
        neighbours = self.nodes
        new_chain = None

        # Look for chains longer than ours
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Replace our chain if we find a longer, valid chain
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block.
        :param block: <dict> Block
        :return: <str>
        """
        # Ensure that the Dictionary is Ordered, or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Returns the last block in the chain.
        """
        return self.chain[-1]


# Instantiate our node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# Example Usage:
# Register transactions, mine blocks, etc.

blockchain.new_transaction(sender="sender_address", recipient="recipient_address", amount=50)
last_proof = blockchain.last_block['proof']
proof = blockchain.proof_of_work(last_proof)
block = blockchain.create_block(proof)
blockchain.add_block_to_chain(block)

print("Blockchain successfully initialized and Genesis Block created.")
