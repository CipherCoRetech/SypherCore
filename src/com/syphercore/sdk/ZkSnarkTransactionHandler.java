package com.syphercore.sdk;

import com.hedera.hashgraph.sdk.*;
import com.hedera.ZkSnarkUtilities;

import java.io.IOException;

public class ZkSnarkTransactionHandler {

    private final Client hederaClient;

    public ZkSnarkTransactionHandler(Client client) {
        this.hederaClient = client;
    }

    /**
     * Verifies the zk-SNARK proof before initiating a transaction.
     * 
     * @param senderId - Sender AccountId
     * @param recipientId - Recipient AccountId
     * @param amount - The amount to transfer
     * @param proofPath - Path to the zk-SNARK proof
     * @param verificationKeyPath - Path to the verification key
     * @throws Exception - if verification fails or transaction is unsuccessful
     */
    public void createZkSnarkTransaction(AccountId senderId, AccountId recipientId, long amount, String proofPath, String verificationKeyPath) throws Exception {
        // Verify the zk-SNARK proof before creating the transaction
        boolean isVerified = verifyZkSnarkProof(proofPath, verificationKeyPath);
        
        if (!isVerified) {
            throw new Exception("zk-SNARK verification failed");
        }

        // Create and sign a transaction after proof verification
        TransferTransaction transferTx = new TransferTransaction()
                .addHbarTransfer(senderId, Hbar.fromTinybars(-amount))
                .addHbarTransfer(recipientId, Hbar.fromTinybars(amount))
                .freezeWith(hederaClient);

        // Execute the transaction on the Hedera network
        TransactionResponse response = transferTx.execute(hederaClient);
        System.out.println("Transaction ID: " + response.transactionId);
    }

    /**
     * Reads zk-SNARK proof and verification key files, and calls the utility to verify them.
     * 
     * @param proofPath - Path to the zk-SNARK proof file
     * @param verificationKeyPath - Path to the verification key file
     * @return boolean indicating whether proof verification was successful or not
     * @throws IOException - if reading the proof or verification key file fails
     */
    private boolean verifyZkSnarkProof(String proofPath, String verificationKeyPath) throws IOException {
        byte[] proof = ZkSnarkUtilities.readProofFromFile(proofPath);
        byte[] verificationKey = ZkSnarkUtilities.readVerificationKeyFromFile(verificationKeyPath);
        return ZkSnarkUtilities.verify(proof, verificationKey);
    }
}
