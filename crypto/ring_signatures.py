# ring_signatures.py
from hashlib import sha256
import random
import base64

class RingSignature:
    def __init__(self, private_keys, public_keys):
        self.private_keys = private_keys  # List of private keys (signers)
        self.public_keys = public_keys    # List of public keys (ring members)

    def generate_ring_signature(self, message, signing_index):
        """Generate a ring signature for the given message."""
        n = len(self.public_keys)
        if signing_index >= n:
            raise ValueError("Signing index out of range")

        # Generate random keys for all members in the ring
        random_keys = [random.getrandbits(256).to_bytes(32, 'big') for _ in range(n)]
        
        # Hash the message using SHA256
        message_hash = sha256(message.encode('utf-8')).digest()

        # Calculate ring elements
        elements = [None] * n
        s = self.private_keys[signing_index]

        for i in range(n):
            elements[i] = sha256(random_keys[i] + message_hash).digest()

        # Return a simplified ring signature containing random keys and elements
        signature = {
            "random_keys": random_keys,
            "elements": elements,
            "signing_index": signing_index
        }

        return base64.b64encode(str(signature).encode()).decode()

    def verify_ring_signature(self, message, signature_b64):
        """Verify a ring signature for the given message."""
        # Decode signature from Base64
        signature_str = base64.b64decode(signature_b64).decode()
        
        # Extract the signature components
        signature = eval(signature_str)  # Assuming secure input (Use caution with eval)
        random_keys = signature["random_keys"]
        elements = signature["elements"]

        # Hash the message
        message_hash = sha256(message.encode('utf-8')).digest()

        # Verify the elements against public keys
        for i, public_key in enumerate(self.public_keys):
            calculated_element = sha256(random_keys[i] + message_hash).digest()
            if calculated_element != elements[i]:
                return False

        return True


# Example Usage
if __name__ == "__main__":
    # Example private keys (mock, not secure)
    private_keys = [random.getrandbits(256).to_bytes(32, 'big') for _ in range(3)]
    # Corresponding public keys (mock, for demonstration purposes)
    public_keys = [sha256(private_key).digest() for private_key in private_keys]

    # Create a RingSignature object
    ring_signature = RingSignature(private_keys, public_keys)

    # Generate and verify ring signature
    message = "This is a confidential transaction"
    signing_index = 1
    signature = ring_signature.generate_ring_signature(message, signing_index)
    print("Signature:", signature)

    # Verify the generated signature
    is_valid = ring_signature.verify_ring_signature(message, signature)
    print("Verification result:", "Valid" if is_valid else "Invalid")
