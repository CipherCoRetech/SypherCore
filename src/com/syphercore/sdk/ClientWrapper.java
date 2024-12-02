package com.syphercore.sdk;

import com.hedera.hashgraph.sdk.AccountId;
import com.hedera.hashgraph.sdk.Client;
import com.hedera.hashgraph.sdk.PrivateKey;

public class ClientWrapper {

    private Client client;

    public ClientWrapper(String networkType, String operatorId, String operatorKey) {
        if (networkType.equalsIgnoreCase("testnet")) {
            client = Client.forTestnet();
        } else if (networkType.equalsIgnoreCase("mainnet")) {
            client = Client.forMainnet();
        } else {
            throw new IllegalArgumentException("Unsupported network type: " + networkType);
        }

        setOperator(operatorId, operatorKey);
    }

    /**
     * Set the operator account and private key for the Hedera client.
     * 
     * @param operatorId - Hedera Account ID of the operator
     * @param operatorKey - Hedera Private Key of the operator
     */
    public void setOperator(String operatorId, String operatorKey) {
        try {
            AccountId accountId = AccountId.fromString(operatorId);
            PrivateKey privateKey = PrivateKey.fromString(operatorKey);
            client.setOperator(accountId, privateKey);
        } catch (Exception e) {
            throw new RuntimeException("Failed to set operator for client: " + e.getMessage(), e);
        }
    }

    /**
     * Returns the Hedera client instance to interact with the network.
     * 
     * @return Hedera Client instance
     */
    public Client getClient() {
        return client;
    }

    /**
     * Set maximum transaction fee for transactions.
     * 
     * @param feeInHbars - Maximum fee in HBARs
     */
    public void setMaxTransactionFee(long feeInHbars) {
        client.setMaxTransactionFee(Hbar.from(feeInHbars));
    }

    /**
     * Set default timeout for network requests.
     * 
     * @param timeoutInSeconds - Timeout value in seconds
     */
    public void setRequestTimeout(int timeoutInSeconds) {
        client.setRequestTimeout(java.time.Duration.ofSeconds(timeoutInSeconds));
    }

    /**
     * Close the client instance, releasing any resources it uses.
     */
    public void close() {
        client.close();
    }
}
