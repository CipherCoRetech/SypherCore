from web3 import Web3
from wallet.keys import generate_key_pair

# Connect to the SypherCore blockchain
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = private_key
            self.address = w3.eth.account.privateKeyToAccount(private_key).address
        else:
            self.private_key, self.address = generate_key_pair()

    def get_balance(self):
        return w3.eth.get_balance(self.address)

    def send_transaction(self, recipient, amount):
        tx = {
            'nonce': w3.eth.getTransactionCount(self.address),
            'to': recipient,
            'value': w3.toWei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': w3.toWei('50', 'gwei')
        }
        signed_tx = w3.eth.account.signTransaction(tx, self.private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash.hex()
