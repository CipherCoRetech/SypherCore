from eth_keys import keys
import os

def generate_key_pair():
    private_key_bytes = os.urandom(32)
    private_key = keys.PrivateKey(private_key_bytes)
    public_key = private_key.public_key
    address = public_key.to_checksum_address()
    return private_key.to_hex(), address
