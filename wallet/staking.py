from web3 import Web3
import time

# Connect to the SypherCore blockchain node
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

class Staking:
    def __init__(self, wallet):
        self.wallet = wallet
        self.contract_address = "staking_contract_address_here"  # Replace with the actual staking contract address
        self.gas_price = w3.toWei('50', 'gwei')
        self.gas_limit = 200000

    def _get_nonce(self):
        return w3.eth.getTransactionCount(self.wallet.address)

    def _send_transaction(self, tx):
        signed_tx = w3.eth.account.signTransaction(tx, self.wallet.private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def stake_tokens(self, amount):
        """
        Stake a specific amount of tokens in the staking contract.
        Args:
            amount (float): The amount of tokens to stake.
        Returns:
            tx_hash (str): The transaction hash.
        """
        tx = {
            'nonce': self._get_nonce(),
            'to': self.contract_address,
            'value': Web3.toWei(amount, 'ether'),
            'gas': self.gas_limit,
            'gasPrice': self.gas_price
        }
        tx_hash = self._send_transaction(tx)
        print(f"Staking initiated. Transaction hash: {tx_hash}")
        return tx_hash

    def withdraw_stake(self):
        """
        Withdraw staked tokens along with accumulated rewards.
        Returns:
            tx_hash (str): The transaction hash.
        """
        function_selector = Web3.keccak(text="withdrawStake()").hex()[:10]  # ABI encoded function signature
        tx = {
            'nonce': self._get_nonce(),
            'to': self.contract_address,
            'data': function_selector,
            'gas': self.gas_limit,
            'gasPrice': self.gas_price
        }
        tx_hash = self._send_transaction(tx)
        print(f"Withdrawal of stake initiated. Transaction hash: {tx_hash}")
        return tx_hash

    def get_stake_info(self):
        """
        Check the staking status and current rewards of the user.
        Returns:
            dict: A dictionary containing 'staked_amount' and 'rewards'.
        """
        function_selector = Web3.keccak(text="getStakeInfo(address)").hex()[:10]
        padded_address = self.wallet.address[2:].rjust(64, '0')
        call_data = function_selector + padded_address

        stake_info = w3.eth.call({
            'to': self.contract_address,
            'data': call_data
        })

        # Parsing returned data: Assume that 32 bytes are staked amount and 32 bytes are rewards.
        staked_amount = int(stake_info[0:32].hex(), 16)
        rewards = int(stake_info[32:64].hex(), 16)

        staked_amount_eth = Web3.fromWei(staked_amount, 'ether')
        rewards_eth = Web3.fromWei(rewards, 'ether')

        print(f"Staked Amount: {staked_amount_eth} Sypher, Rewards: {rewards_eth} Sypher")
        return {
            'staked_amount': staked_amount_eth,
            'rewards': rewards_eth
        }

    def calculate_rewards(self, staking_start_time):
        """
        Estimate rewards based on staking duration.
        Args:
            staking_start_time (int): UNIX timestamp of when staking started.
        Returns:
            float: Estimated reward amount.
        """
        current_time = int(time.time())
        duration_in_seconds = current_time - staking_start_time
        reward_rate_per_second = 0.0001  # Example reward rate in Sypher per second

        estimated_rewards = duration_in_seconds * reward_rate_per_second
        print(f"Estimated Rewards: {estimated_rewards} Sypher")
        return estimated_rewards

    def claim_rewards(self):
        """
        Claim accumulated staking rewards without withdrawing the stake.
        Returns:
            tx_hash (str): The transaction hash.
        """
        function_selector = Web3.keccak(text="claimRewards()").hex()[:10]
        tx = {
            'nonce': self._get_nonce(),
            'to': self.contract_address,
            'data': function_selector,
            'gas': self.gas_limit,
            'gasPrice': self.gas_price
        }
        tx_hash = self._send_transaction(tx)
        print(f"Claiming rewards initiated. Transaction hash: {tx_hash}")
        return tx_hash

    def restake_rewards(self):
        """
        Restake accumulated rewards.
        Returns:
            tx_hash (str): The transaction hash.
        """
        function_selector = Web3.keccak(text="restakeRewards()").hex()[:10]
        tx = {
            'nonce': self._get_nonce(),
            'to': self.contract_address,
            'data': function_selector,
            'gas': self.gas_limit,
            'gasPrice': self.gas_price
        }
        tx_hash = self._send_transaction(tx)
        print(f"Restaking rewards initiated. Transaction hash: {tx_hash}")
        return tx_hash

# Example usage:
if __name__ == "__main__":
    from wallet.wallet import Wallet

    # Assume the private key is provided
    user_wallet = Wallet(private_key="0xYOUR_PRIVATE_KEY_HERE")

    staking = Staking(user_wallet)

    # Stake 10 Sypher tokens
    staking.stake_tokens(10)

    # Get current staking information
    staking.get_stake_info()

    # Claim rewards
    staking.claim_rewards()

    # Withdraw staked tokens and rewards
    staking.withdraw_stake()
