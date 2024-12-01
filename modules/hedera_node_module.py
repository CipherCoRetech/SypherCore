import json
import os
from hedera import Hbar, Client, AccountId, PrivateKey, TransferTransaction

class HederaNodeModule:
    def __init__(self, network_type, operator_id, operator_key):
        """
        Initialize the HederaNodeModule with a client for testnet or mainnet.
        """
        if network_type.lower() == "testnet":
            self.client = Client.for_testnet()
        elif network_type.lower() == "mainnet":
            self.client = Client.for_mainnet()
        else:
            raise ValueError("Unsupported network type: {}".format(network_type))
        
        self.client.set_operator(AccountId.from_string(operator_id), PrivateKey.from_string(operator_key))
    
    def transfer_hbar(self, sender_id, recipient_id, amount):
        """
        Transfer hbar between two accounts on the Hedera network.
        """
        try:
            transaction = TransferTransaction().add_hbar_transfer(
                AccountId.from_string(sender_id), Hbar.from_tinybars(-amount)
            ).add_hbar_transfer(
                AccountId.from_string(recipient_id), Hbar.from_tinybars(amount)
            ).freeze_with(self.client)

            response = transaction.execute(self.client)
            receipt = response.get_receipt(self.client)
            return receipt.status
        except Exception as e:
            raise RuntimeError("Failed to execute Hbar transfer: {}".format(e))

    def create_account(self, initial_balance):
        """
        Create a new Hedera account with an initial Hbar balance.
        """
        private_key = PrivateKey.generate()
        public_key = private_key.get_public_key()

        try:
            transaction_response = (
                self.client.create_account(
                    key=public_key, initial_balance=Hbar.from_tinybars(initial_balance)
                )
            )
            receipt = transaction_response.get_receipt(self.client)
            account_id = receipt.account_id
            return account_id, private_key
        except Exception as e:
            raise RuntimeError("Failed to create Hedera account: {}".format(e))

    def close_client(self):
        """
        Close the Hedera client connection.
        """
        self.client.close()

