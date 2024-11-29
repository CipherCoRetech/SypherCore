// Faucet Service for SypherCore
const express = require('express');
const app = express();

let faucetBalance = 1000000;

app.get('/request/:address', (req, res) => {
    const address = req.params.address;
    if (faucetBalance > 0) {
        faucetBalance -= 100;
        res.json({ address, amount: 100, remainingFaucetBalance: faucetBalance });
    } else {
        res.status(400).json({ error: "Faucet empty" });
    }
});

app.listen(4000, () => console.log('Faucet running on http://localhost:4000'));
