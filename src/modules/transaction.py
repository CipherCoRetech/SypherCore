import hashlib
import json
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

class Transaction:
    def __init__(self, sender, receiver, amount, timestamp=None, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.signature = signature

    def to_dict(self):
        """ Convert transaction data to a dictionary format. """
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

    def to_json(self):
        """ Convert transaction data to JSON format. """
        return json.dumps(self.to_dict(), sort_keys=True)

    def calculate_hash(self):
        """ Calculate a SHA-256 hash of the transaction. """
        transaction_json = self.to_json()
        return hashlib.sha256(transaction_json.encode()).hexdigest()

    def sign_transaction(self, private_key_pem):
        """ Sign the transaction using the sender's private key (in PEM format). """
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None,
                backend=default_backend()
            )
            transaction_hash = self.calculate_hash()
            self.signature = private_key.sign(
                transaction_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            self.signature = self.signature.hex()  # Convert to hex for easy storage and transmission
        except Exception as e:
            raise Exception(f"Transaction signing failed: {str(e)}")

    def verify_signature(self, public_key_pem):
        """ Verify the signature of the transaction using the sender's public key. """
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode(),
                backend=default_backend()
            )
            transaction_hash = self.calculate_hash()
            public_key.verify(
                bytes.fromhex(self.signature),
                transaction_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
        except Exception as e:
            raise Exception(f"Transaction verification failed: {str(e)}")

    @staticmethod
    def create_key_pair():
        """ Create a new RSA key pair for transaction signing and verification. """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        public_key_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        return private_key_pem, public_key_pem

    @staticmethod
    def from_dict(data):
        """ Create a transaction instance from a dictionary. """
        return Transaction(
            sender=data['sender'],
            receiver=data['receiver'],
            amount=data['amount'],
            timestamp=data['timestamp'],
            signature=data['signature']
        )

    @staticmethod
    def from_json(data):
        """ Create a transaction instance from a JSON string. """
        data_dict = json.loads(data)
        return Transaction.from_dict(data_dict)

    @staticmethod
    def validate_transaction(transaction):
        """ Validate transaction structure and integrity. """
        if not transaction.sender or not transaction.receiver or not transaction.amount:
            raise ValueError("Transaction must have a sender, receiver, and an amount.")
        if transaction.amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")
        if not transaction.signature:
            raise ValueError("Transaction must be signed.")
        return True


class TransactionPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        """ Add a new transaction to the pool after validation. """
        if Transaction.validate_transaction(transaction):
            self.transactions.append(transaction)
            return True
        else:
            return False

    def get_transactions(self):
        """ Retrieve all transactions in the pool. """
        return [transaction.to_dict() for transaction in self.transactions]

    def clear_transactions(self):
        """ Clear all transactions from the pool. """
        self.transactions = []

    def remove_transaction(self, transaction):
        """ Remove a specific transaction from the pool. """
        for tx in self.transactions:
            if tx.calculate_hash() == transaction.calculate_hash():
                self.transactions.remove(tx)
                return True
        return False


if __name__ == "__main__":
    # Demonstrate transaction signing and verification.
    private_key, public_key = Transaction.create_key_pair()

    # Create a transaction
    transaction = Transaction(
        sender="sender_public_key_placeholder",
        receiver="receiver_public_key_placeholder",
        amount=100
    )

    # Sign the transaction
    transaction.sign_transaction(private_key)

    # Verify the transaction signature
    verification_result = transaction.verify_signature(public_key)
    print("Transaction verification:", "Passed" if verification_result else "Failed")

    # Serialize and Deserialize example
    transaction_json = transaction.to_json()
    deserialized_transaction = Transaction.from_json(transaction_json)
    print("Deserialized Transaction:", deserialized_transaction.to_dict())

    # Add transaction to pool
    pool = TransactionPool()
    pool.add_transaction(transaction)
    print("Transactions in pool:", pool.get_transactions())
