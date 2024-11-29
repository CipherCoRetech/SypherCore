// Simple Node.js Wallet Server
const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.json());

let wallets = {};

// Create a new wallet
app.post('/create', (req, res) => {
    const walletId = `wallet-${Date.now()}`;
    wallets[walletId] = { balance: 0 };
    res.json({ walletId, balance: wallets[walletId].balance });
});

// Check wallet balance
app.get('/balance/:walletId', (req, res) => {
    const walletId = req.params.walletId;
    if (wallets[walletId]) {
        res.json({ balance: wallets[walletId].balance });
    } else {
        res.status(404).json({ error: "Wallet not found" });
    }
});

// Transfer funds
app.post('/transfer', (req, res) => {
    const { fromWallet, toWallet, amount } = req.body;
    if (wallets[fromWallet] && wallets[toWallet]) {
        wallets[fromWallet].balance -= amount;
        wallets[toWallet].balance += amount;
        res.json({ success: true });
    } else {
        res.status(400).json({ error: "Invalid wallet IDs" });
    }
});

app.listen(3000, () => console.log('Wallet service running on http://localhost:3000'));
