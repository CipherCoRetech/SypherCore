// app.js - SypherCore Token Management Application

// Import necessary libraries and dependencies
const express = require('express');
const Web3 = require('web3');
const bodyParser = require('body-parser');
const cors = require('cors');
const morgan = require('morgan');
const { abi, contractAddress } = require('./SypherTokenContract');
require('dotenv').config(); // For managing private keys securely

// Initialize express app and web3 instance
const app = express();
const web3 = new Web3(new Web3.providers.HttpProvider('https://syphercore-node.network')); // Replace with actual SypherCore node URL

// Set up contract instance
const sypherTokenContract = new web3.eth.Contract(abi, contractAddress);

// Middleware configurations
app.use(cors());
app.use(morgan('combined')); // Log all requests for better visibility
app.use(bodyParser.json());

// Global configurations
const FAUCET_OWNER = '0x123456789abcdef123456789abcdef123456789a'; // Replace with actual owner address
const GAS_LIMIT = 3000000;

// Endpoint to get the token balance of a user
app.get('/balance/:address', async (req, res) => {
    try {
        const address = req.params.address;
        if (!web3.utils.isAddress(address)) {
            return res.status(400).json({ error: 'Invalid Ethereum address.' });
        }

        const balance = await sypherTokenContract.methods.balanceOf(address).call();
        res.status(200).json({ address, balance: web3.utils.fromWei(balance, 'ether') });
    } catch (error) {
        console.error('Error fetching balance:', error);
        res.status(500).json({ error: 'Failed to fetch balance.' });
    }
});

// Endpoint to transfer tokens from the owner to a user
app.post('/transfer', async (req, res) => {
    try {
        const { recipientAddress, amount } = req.body;

        if (!web3.utils.isAddress(recipientAddress)) {
            return res.status(400).json({ error: 'Invalid recipient address.' });
        }

        if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
            return res.status(400).json({ error: 'Invalid transfer amount.' });
        }

        const transferAmount = web3.utils.toWei(amount.toString(), 'ether');

        const tx = {
            from: FAUCET_OWNER,
            to: contractAddress,
            gas: GAS_LIMIT,
            data: sypherTokenContract.methods.transfer(recipientAddress, transferAmount).encodeABI(),
        };

        // Sign the transaction with the faucet owner's private key
        const signedTx = await web3.eth.accounts.signTransaction(tx, process.env.FAUCET_PRIVATE_KEY);

        // Send signed transaction to the network
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        res.status(200).json({ message: 'Tokens transferred successfully.', transactionHash: receipt.transactionHash });
    } catch (error) {
        console.error('Error transferring tokens:', error);
        res.status(500).json({ error: 'Failed to process transfer request.' });
    }
});

// Endpoint to approve token allowance for a spender
app.post('/approve', async (req, res) => {
    try {
        const { spenderAddress, amount } = req.body;

        if (!web3.utils.isAddress(spenderAddress)) {
            return res.status(400).json({ error: 'Invalid spender address.' });
        }

        if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
            return res.status(400).json({ error: 'Invalid approval amount.' });
        }

        const approveAmount = web3.utils.toWei(amount.toString(), 'ether');
        const ownerAddress = FAUCET_OWNER;

        const tx = {
            from: ownerAddress,
            to: contractAddress,
            gas: GAS_LIMIT,
            data: sypherTokenContract.methods.approve(spenderAddress, approveAmount).encodeABI(),
        };

        // Sign the transaction with the owner's private key
        const signedTx = await web3.eth.accounts.signTransaction(tx, process.env.FAUCET_PRIVATE_KEY);

        // Send signed transaction to the network
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        res.status(200).json({ message: 'Allowance approved successfully.', transactionHash: receipt.transactionHash });
    } catch (error) {
        console.error('Error approving allowance:', error);
        res.status(500).json({ error: 'Failed to process approval request.' });
    }
});

// Endpoint to check allowance between owner and spender
app.get('/allowance/:owner/:spender', async (req, res) => {
    try {
        const { owner, spender } = req.params;

        if (!web3.utils.isAddress(owner) || !web3.utils.isAddress(spender)) {
            return res.status(400).json({ error: 'Invalid Ethereum addresses.' });
        }

        const allowance = await sypherTokenContract.methods.allowance(owner, spender).call();
        res.status(200).json({ owner, spender, allowance: web3.utils.fromWei(allowance, 'ether') });
    } catch (error) {
        console.error('Error fetching allowance:', error);
        res.status(500).json({ error: 'Failed to fetch allowance.' });
    }
});

// Endpoint to mint new tokens
app.post('/mint', async (req, res) => {
    try {
        const { recipientAddress, amount } = req.body;

        if (!web3.utils.isAddress(recipientAddress)) {
            return res.status(400).json({ error: 'Invalid recipient address.' });
        }

        if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
            return res.status(400).json({ error: 'Invalid mint amount.' });
        }

        const mintAmount = web3.utils.toWei(amount.toString(), 'ether');

        const tx = {
            from: FAUCET_OWNER,
            to: contractAddress,
            gas: GAS_LIMIT,
            data: sypherTokenContract.methods.mint(mintAmount, recipientAddress).encodeABI(),
        };

        // Sign the transaction with the owner's private key
        const signedTx = await web3.eth.accounts.signTransaction(tx, process.env.FAUCET_PRIVATE_KEY);

        // Send signed transaction to the network
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        res.status(200).json({ message: 'Tokens minted successfully.', transactionHash: receipt.transactionHash });
    } catch (error) {
        console.error('Error minting tokens:', error);
        res.status(500).json({ error: 'Failed to mint tokens.' });
    }
});

// Start the SypherCore app server
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`SypherCore Token Management App running on port ${PORT}`);
});
