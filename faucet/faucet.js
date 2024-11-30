// faucet.js - SypherCore Token Faucet

// Import necessary libraries and dependencies
const Web3 = require('web3');
const express = require('express');
const bodyParser = require('body-parser');
const { abi, contractAddress } = require('./SypherTokenContract');
const fs = require('fs');

// Initialize express app and web3 instance
const app = express();
const web3 = new Web3(new Web3.providers.HttpProvider('https://syphercore-node.network')); // Replace with actual SypherCore node URL

// Set up contract instance
const sypherTokenContract = new web3.eth.Contract(abi, contractAddress);

// Faucet configurations
const FAUCET_OWNER = '0x123456789abcdef123456789abcdef123456789a'; // Replace with actual owner address
const FAUCET_PRIVATE_KEY = 'YOUR_PRIVATE_KEY_HERE'; // Replace with the private key of the faucet owner
const TOKEN_AMOUNT = web3.utils.toWei('10', 'ether'); // Amount of tokens to distribute per request
const GAS_LIMIT = 3000000;

// Middleware for parsing JSON requests
app.use(bodyParser.json());

// Endpoint to request tokens from the faucet
app.post('/request-tokens', async (req, res) => {
    try {
        // Extract recipient address from request body
        const { recipientAddress } = req.body;

        // Validate the recipient address
        if (!web3.utils.isAddress(recipientAddress)) {
            return res.status(400).json({ error: 'Invalid recipient address.' });
        }

        // Check if the recipient has already received tokens in the past 24 hours
        const lastRequest = await getLastRequest(recipientAddress);
        if (lastRequest && isRequestWithin24Hours(lastRequest)) {
            return res.status(429).json({ error: 'Tokens have already been claimed in the past 24 hours.' });
        }

        // Create transaction to transfer tokens from faucet owner to recipient
        const tx = {
            from: FAUCET_OWNER,
            to: contractAddress,
            gas: GAS_LIMIT,
            data: sypherTokenContract.methods.transfer(recipientAddress, TOKEN_AMOUNT).encodeABI(),
        };

        // Sign the transaction with faucet owner's private key
        const signedTx = await web3.eth.accounts.signTransaction(tx, FAUCET_PRIVATE_KEY);

        // Send signed transaction to the network
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);

        // Log the request
        await logRequest(recipientAddress);

        // Respond with transaction receipt
        res.status(200).json({ message: 'Tokens transferred successfully.', transactionHash: receipt.transactionHash });
    } catch (error) {
        console.error('Error transferring tokens:', error);
        res.status(500).json({ error: 'Failed to process token request.' });
    }
});

// Function to log the request in a simple database (using a JSON file)
const LOG_FILE = './requests_log.json';

// Load requests log from file
function loadRequestLog() {
    if (fs.existsSync(LOG_FILE)) {
        return JSON.parse(fs.readFileSync(LOG_FILE));
    } else {
        return {};
    }
}

// Save requests log to file
function saveRequestLog(requests) {
    fs.writeFileSync(LOG_FILE, JSON.stringify(requests, null, 2));
}

// Function to log the request in a JSON file database
async function logRequest(recipientAddress) {
    const currentTimestamp = Date.now();
    let requests = loadRequestLog();
    requests[recipientAddress] = currentTimestamp;
    saveRequestLog(requests);
}

// Function to get the last request time of a specific address
async function getLastRequest(recipientAddress) {
    let requests = loadRequestLog();
    return requests[recipientAddress] || null;
}

// Function to check if a request was made within the last 24 hours
function isRequestWithin24Hours(lastRequestTimestamp) {
    const ONE_DAY = 24 * 60 * 60 * 1000;
    return Date.now() - lastRequestTimestamp < ONE_DAY;
}

// Endpoint to check the balance of the faucet
app.get('/faucet-balance', async (req, res) => {
    try {
        const balance = await sypherTokenContract.methods.balanceOf(FAUCET_OWNER).call();
        res.status(200).json({ balance: web3.utils.fromWei(balance, 'ether') });
    } catch (error) {
        console.error('Error fetching faucet balance:', error);
        res.status(500).json({ error: 'Failed to fetch faucet balance.' });
    }
});

// Endpoint to get request history
app.get('/request-history', async (req, res) => {
    try {
        const requests = loadRequestLog();
        res.status(200).json({ requests });
    } catch (error) {
        console.error('Error fetching request history:', error);
        res.status(500).json({ error: 'Failed to fetch request history.' });
    }
});

// Start the faucet server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`SypherCore Token Faucet running on port ${PORT}`);
});
