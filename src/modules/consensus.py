import random
import time
import logging
from hashlib import sha256
from modules.transaction import TransactionPool
from modules.blockchain import Blockchain

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Consensus:
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.stakeholders = {}  # Maps stakeholder public keys to their stake
        self.current_staker = None

    def add_stakeholder(self, stakeholder_public_key, stake_amount):
        """ Add a stakeholder to the list of stakeholders. """
        if stake_amount <= 0:
            raise ValueError("Stake amount must be positive.")
        self.stakeholders[stakeholder_public_key] = self.stakeholders.get(stakeholder_public_key, 0) + stake_amount
        logging.info(f"Added stakeholder {stakeholder_public_key} with stake {stake_amount}.")

    def remove_stakeholder(self, stakeholder_public_key, stake_amount):
        """ Remove a stakeholder or decrease their stake. """
        if stakeholder_public_key in self.stakeholders:
            self.stakeholders[stakeholder_public_key] -= stake_amount
            if self.stakeholders[stakeholder_public_key] <= 0:
                del self.stakeholders[stakeholder_public_key]
            logging.info(f"Removed stakeholder {stakeholder_public_key} or decreased their stake.")

    def select_staker(self):
        """ Select a staker based on weighted random selection. """
        if not self.stakeholders:
            raise Exception("No stakeholders available for staking.")

        total_stake = sum(self.stakeholders.values())
        cumulative_weights = []
        running_sum = 0

        for staker, stake in self.stakeholders.items():
            running_sum += stake
            cumulative_weights.append((staker, running_sum))

        random_point = random.uniform(0, total_stake)
        for staker, weight in cumulative_weights:
            if random_point <= weight:
                logging.info(f"Selected staker {staker}.")
                self.current_staker = staker
                return staker

    def validate_block(self, block):
        """ Validate a block before adding it to the blockchain. """
        previous_block = self.blockchain.get_last_block()
        if block.previous_hash != previous_block.calculate_hash(
