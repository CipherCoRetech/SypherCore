# zk_snarks.py
import subprocess
import json
import os

class ZkSnarks:
    def __init__(self, zokrates_path="/usr/local/bin/zokrates"):
        self.zokrates_path = zokrates_path

    def compile_circuit(self, circuit_file_path):
        """Compile the circuit to create proving and verification keys."""
        command = [self.zokrates_path, "compile", "-i", circuit_file_path]
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to compile circuit: " + result.stderr.decode())

        print("Circuit compiled successfully.")

    def setup(self):
        """Generate the trusted setup to produce proving and verification keys."""
        command = [self.zokrates_path, "setup"]
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to generate trusted setup: " + result.stderr.decode())

        print("Trusted setup completed successfully.")

    def generate_proof(self, witness_file):
        """Generate a proof for the given witness."""
        command = [self.zokrates_path, "compute-witness", "-a"] + witness_file.split()
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to compute witness: " + result.stderr.decode())

        command = [self.zokrates_path, "generate-proof"]
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to generate proof: " + result.stderr.decode())

        print("Proof generated successfully.")

    def verify_proof(self):
        """Verify the proof against the verification key."""
        command = [self.zokrates_path, "verify"]
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to verify proof: " + result.stderr.decode())

        print("Proof verified successfully.")
        return True

    def export_verifier(self, verifier_name="Verifier.sol"):
        """Export a verifier smart contract for the generated proof."""
        command = [self.zokrates_path, "export-verifier"]
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to export verifier contract: " + result.stderr.decode())

        with open(verifier_name, "w") as verifier_file:
            verifier_file.write(result.stdout.decode())
        print(f"Verifier smart contract exported as {verifier_name}.")

# Example Usage
if __name__ == "__main__":
    # Example circuit file (replace with your actual circuit)
    zk = ZkSnarks()

    try:
        zk.compile_circuit("example_circuit.zok")
        zk.setup()
        zk.generate_proof("1 2 3")  # Example witness values
        verified = zk.verify_proof()
        if verified:
            print("Proof is valid.")
        zk.export_verifier()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
