# ring_signatures.py
from hashlib import sha256
import random
import base64

class RingSignature:
    def __init__(self, private_keys, public_keys):
        self.private_keys = private_keys  # List of private keys (signers)
        self.public_keys = public_keys    # List of public keys (ring members)

    def generate_ring_signature(self, message, signing_index):
        n = len(self.public_keys)
        if signing_index >= n:
            raise ValueError("Signing index out of range")

        random_keys = [random.getrandbits(256).to_bytes(32, 'big') for _ in range(n)]
        message_hash = sha256(message.encode('utf-8')).digest()

        elements = [None] * n
        s = self.private_keys[signing_index]

        for i in range(n):
            elements[i] = sha256(random_keys[i] + message_hash).digest()

        signature = {
            "random_keys": random_keys,
            "elements": elements,
            "signing_index": signing_index
        }

        return base64.b64encode(str(signature).encode()).decode()

    def verify_ring_signature(self, message, signature_b64):
        signature_str = base64.b64decode(signature_b64).decode()
        signature = eval(signature_str)  # Use caution with eval (secure input)
        random_keys = signature["random_keys"]
        elements = signature["elements"]
        message_hash = sha256(message.encode('utf-8')).digest()

        for i, public_key in enumerate(self.public_keys):
            calculated_element = sha256(random_keys[i] + message_hash).digest()
            if calculated_element != elements[i]:
                return False

        return True
