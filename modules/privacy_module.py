import os
import json
import base64
from zokrates_pycrypto import ZkSnark
from ring_signature import RingSignature

class PrivacyModule:
    def __init__(self):
        """
        Initialize the Privacy Module.
        """
        pass

    def verify_zk_snark(self, proof_path, verification_key_path):
        """
        Verify zk-SNARK proof using verification key.
        """
        if not os.path.exists(proof_path) or not os.path.exists(verification_key_path):
            raise FileNotFoundError("Proof or verification key file not found.")

        with open(proof_path, 'rb') as proof_file:
            proof = proof_file.read()

        with open(verification_key_path, 'rb') as verification_key_file:
            verification_key = verification_key_file.read()

        zk_snark = ZkSnark()
        is_verified = zk_snark.verify(proof, verification_key)
        
        return is_verified

    def create_ring_signature(self, private_keys, message):
        """
        Create a ring signature for a given message.
        """
        ring_signature = RingSignature()
        
        # Convert all keys to the correct format (assuming base64 encoding)
        formatted_private_keys = [base64.b64decode(key) for key in private_keys]
        
        signature = ring_signature.generate_signature(formatted_private_keys, message.encode('utf-8'))
        
        return signature

    def verify_ring_signature(self, public_keys, message, signature):
        """
        Verify a ring signature against a given message.
        """
        ring_signature = RingSignature()
        
        formatted_public_keys = [base64.b64decode(key) for key in public_keys]
        is_verified = ring_signature.verify_signature(formatted_public_keys, message.encode('utf-8'), signature)
        
        return is_verified

    def generate_zk_snark_proof(self, inputs_path, proving_key_path, output_proof_path):
        """
        Generate a zk-SNARK proof given an inputs file and proving key.
        """
        if not os.path.exists(inputs_path) or not os.path.exists(proving_key_path):
            raise FileNotFoundError("Inputs or proving key file not found.")

        with open(inputs_path, 'rb') as inputs_file:
            inputs = inputs_file.read()

        with open(proving_key_path, 'rb') as proving_key_file:
            proving_key = proving_key_file.read()

        zk_snark = ZkSnark()
        proof = zk_snark.generate_proof(inputs, proving_key)

        with open(output_proof_path, 'wb') as proof_file:
            proof_file.write(proof)

        print(f"zk-SNARK proof generated at: {output_proof_path}")

