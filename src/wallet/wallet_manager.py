import os
import json
from hedera import Client, AccountId, PrivateKey, Hbar, TransferTransaction
from cryptography.fernet import Fernet

class WalletManager:
    def __init__(self, network_type="testnet", operator_id=None, operator_key=None):
        """
        Initialize the WalletManager, set up Hedera client.
        """
        if network_type.lower() == "testnet":
            self.client = Client.for_testnet()
        elif network_type.lower() == "mainnet":
            self.client = Client.for_mainnet()
        else:
            raise ValueError("Unsupported network type: {}".format(network_type))

        if operator_id and operator_key:
            self.client.set_operator(AccountId.from_string(operator_id), PrivateKey.from_string(operator_key))

    def create_wallet(self, password=None):
        """
        Create a new Hedera account and wallet, optionally encrypt keys with a password.
        """
        private_key = PrivateKey.generate()
        public_key = private_key.get_public_key()

        # Create new Hedera account
        transaction_response = self.client.create_account(
            key=public_key,
            initial_balance=Hbar.from_tinybars(1000)  # Set an initial balance
        )
        receipt = transaction_response.get_receipt(self.client)
        account_id = receipt.account_id

        wallet_data = {
            "account_id": str(account_id),
            "private_key": private_key.to_string(),
            "public_key": public_key.to_string()
        }

        # Encrypt wallet data if password is provided
        if password:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            wallet_json = json.dumps(wallet_data)
            encrypted_data = cipher.encrypt(wallet_json.encode())

            wallet_data = {
                "account_id": wallet_data["account_id"],
                "encrypted_data": encrypted_data.decode(),
                "encryption_key": key.decode()
            }

        wallet_filename = f"wallet_{account_id}.json"
        with open(wallet_filename, "w") as wallet_file:
            json.dump(wallet_data, wallet_file)

        return account_id, wallet_filename

    def load_wallet(self, wallet_path, password=None):
        """
        Load wallet information from a file, optionally decrypt if a password is provided.
        """
        if not os.path.exists(wallet_path):
            raise FileNotFoundError(f"Wallet file not found: {wallet_path}")

        with open(wallet_path, "r") as wallet_file:
            wallet_data = json.load(wallet_file)

        if password:
            if "encrypted_data" not in wallet_data or "encryption_key" not in wallet_data:
                raise ValueError("Wallet is encrypted but missing necessary fields.")

            key = wallet_data["encryption_key"].encode()
            cipher = Fernet(key)
            encrypted_data = wallet_data["encrypted_data"].encode()
            decrypted_data = cipher.decrypt(encrypted_data)
            wallet_data = json.loads(decrypted_data)

        private_key = PrivateKey.from_string(wallet_data["private_key"])
        account_id = AccountId.from_string(wallet_data["account_id"])
        
        return account_id, private_key

    def check_balance(self, account_id):
        """
        Check the balance of a Hedera account.
        """
        try:
            balance = self.client.get_account_balance(AccountId.from_string(account_id))
            return balance
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve balance: {e}")

    def transfer_hbar(self, sender_private_key, sender_account_id, recipient_account_id, amount):
        """
        Transfer hbar from one account to another.
        """
        sender_key = PrivateKey.from_string(sender_private_key)

        # Transfer Transaction
        try:
            transfer_tx = TransferTransaction() \
                .add_hbar_transfer(AccountId.from_string(sender_account_id), Hbar.from_tinybars(-amount)) \
                .add_hbar_transfer(AccountId.from_string(recipient_account_id), Hbar.from_tinybars(amount)) \
                .freeze_with(self.client)

            # Sign transaction with the sender's private key
            signed_tx = transfer_tx.sign(sender_key)
            response = signed_tx.execute(self.client)

            receipt = response.get_receipt(self.client)
            return receipt.status
        except Exception as e:
            raise RuntimeError(f"Failed to execute Hbar transfer: {e}")

    def generate_keys(self):
        """
        Generate a new pair of public and private keys.
        """
        private_key = PrivateKey.generate()
        public_key = private_key.get_public_key()
        return {
            "private_key": private_key.to_string(),
            "public_key": public_key.to_string()
        }

if __name__ == "__main__":
    # Example usage
    network_type = "testnet"
    operator_id = "0.0.1234"
    operator_key = "302e020100300506032b657004220420........"

    wallet_manager = WalletManager(network_type, operator_id, operator_key)

    # Create a new wallet with encryption
    account_id, wallet_path = wallet_manager.create_wallet(password="securepassword")
    print(f"Wallet created for account: {account_id}, saved at {wallet_path}")

    # Load wallet information
    loaded_account_id, loaded_private_key = wallet_manager.load_wallet(wallet_path, password="securepassword")
    print(f"Loaded wallet for account: {loaded_account_id}")

    # Check balance
    balance = wallet_manager.check_balance(loaded_account_id)
    print(f"Account balance: {balance.to_tinybars()} tinybars")

    # Transfer HBAR
    recipient_account_id = "0.0.9101"
    transfer_status = wallet_manager.transfer_hbar(loaded_private_key.to_string(), loaded_account_id, recipient_account_id, 500)
    print(f"Transfer status: {transfer_status}")
