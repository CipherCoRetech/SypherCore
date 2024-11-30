from wallet.wallet import Wallet

def send_tokens(sender_private_key, recipient, amount):
    wallet = Wallet(sender_private_key)
    tx_hash = wallet.send_transaction(recipient, amount)
    return tx_hash
