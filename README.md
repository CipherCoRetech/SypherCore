To launch the SypherCore blockchain, you need to go through the following steps to initialize the genesis block, configure the nodes, and start the network. This guide will walk you through the process in detail to get your blockchain up and running.

### **1. Prerequisites**

Ensure you have the following installed on your system:

- **Docker**: Required to containerize the blockchain node environment.
- **Node.js** and **npm**: Required for developing and running smart contracts.
- **Git**: To clone necessary repositories.
- **Python 3.8+**: For compiling SypherLang and executing scripts.
  
### **2. Set Up Docker**

If Docker is not already installed, you can install it using:

```sh
# For Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y docker.io
```

Ensure that Docker is running:

```sh
sudo systemctl start docker
sudo systemctl enable docker
```

### **3. Clone SypherCore Repository**

Clone the SypherCore blockchain repository:

```sh
git clone https://github.com/SypherCoRe/SypherCore.git
cd SypherCore
```

This repository contains all the configurations, Docker scripts, and files needed to launch the blockchain.

### **4. Configure the Genesis Block**

The **genesis block** is the first block of your blockchain. You will need to create a `genesis.json` file that defines the initial configuration, including initial accounts and balances.

Create a `genesis.json` file in the root directory of the SypherCore repository with the following content:

```json
{
  "config": {
    "chainId": 1234,
    "homesteadBlock": 0,
    "eip150Block": 0,
    "eip155Block": 0,
    "eip158Block": 0
  },
  "difficulty": "0x20000",
  "gasLimit": "0x8000000",
  "alloc": {
    "0xYourAccountAddressHere": { "balance": "1000000000000000000000" }
  }
}
```

- **ChainId**: This identifies your blockchain network and is used to prevent cross-chain replay attacks.
- **Alloc**: Allocates initial balances to specified accounts.

### **5. Initialize the Genesis Block**

After creating the `genesis.json` file, initialize the blockchain:

```sh
geth init genesis.json --datadir ./sypherdata
```

This command initializes the genesis block for the blockchain and stores the chain data in `./sypherdata`.

### **6. Create Account(s) for Nodes**

To create a new account for your node, run:

```sh
geth account new --datadir ./sypherdata
```

This command will prompt you to create a password for your new account and provide you with an address. Note the address, as it will be required later.

### **7. Create and Run Docker Containers**

To create a scalable network with multiple nodes, use Docker. Create a `docker-compose.yml` file with the following content:

```yaml
version: '3'
services:
  node1:
    image: ethereum/client-go:alltools-stable
    volumes:
      - ./sypherdata:/root/.ethereum
    ports:
      - "8545:8545"
      - "30303:30303"
    command: >
      --networkid 1234
      --nodiscover
      --http
      --http.addr "0.0.0.0"
      --http.port 8545
      --http.api "eth,net,web3,personal"
      --datadir /root/.ethereum
      --allow-insecure-unlock
```

- **Ports**:
  - `8545`: This is for JSON-RPC, which allows you to interact with the blockchain.
  - `30303`: This is the default peer-to-peer communication port.
  
Run Docker to create and start the nodes:

```sh
docker-compose up -d
```

This command will launch the blockchain nodes in the background.

### **8. Mining the Genesis Block**

To start mining the genesis block and subsequent blocks, run:

```sh
geth --datadir ./sypherdata --mine --miner.threads=1 --http
```

The `--mine` flag enables mining, and the `--miner.threads` flag allows you to control how many threads are allocated for mining.

### **9. Connecting to the Blockchain**

To connect to your blockchain, you can use **geth console** or the **JSON-RPC API** via the HTTP port (8545):

```sh
geth attach http://127.0.0.1:8545
```

This command will connect you to your local blockchain, where you can interact with it using JavaScript commands.

### **10. Deploying Smart Contracts**

Once the blockchain is running, you can deploy SypherCore smart contracts.

1. **Compile Your Contract**:

   Use the SypherLang compiler to compile your smart contract into bytecode:

   ```sh
   python compiler/compiler.py contracts/PrivacyContract.sypher
   ```

2. **Deploy Contract Using Web3.js**:

   Use the Web3.js library to deploy your contract:

   ```javascript
   const Web3 = require('web3');
   const fs = require('fs');

// Set up web3 provider to connect to SypherCore blockchain
const web3 = new Web3('http://localhost:8545');

// Define account to deploy the contract
const deployAccount = '0xYourAccountAddressHere';
const privateKey = '0xYourPrivateKeyHere'; // Use environment variables in production!

// Compile contract
const compiledContract = JSON.parse(fs.readFileSync('./contracts/PrivacyContract.json'));
const contractAbi = compiledContract.abi;
const contractBytecode = compiledContract.bytecode;

const deployContract = async () => {
    const myContract = new web3.eth.Contract(contractAbi);

    const deployOptions = {
        data: contractBytecode,
        arguments: []
    };

    const deployTx = myContract.deploy(deployOptions);

    const gas = await deployTx.estimateGas();
    const gasPrice = await web3.eth.getGasPrice();

    const tx = {
        from: deployAccount,
        gas,
        gasPrice,
        data: deployTx.encodeABI()
    };

    const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);
    const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);

    console.log(`Contract deployed at address: ${receipt.contractAddress}`);
};

deployContract();
   ```

### **11. Start Wallet for Interaction**

The SypherCore wallet can be used to interact with your blockchain and deployed contracts. Follow the wallet installation instructions (provided earlier) to set it up.

### **Summary Steps to Launch SypherCore Blockchain**:

1. **Install Prerequisites**: Docker, Geth, Git, Node.js.
2. **Clone the Repository**: Clone SypherCore from GitHub.
3. **Create Genesis Block**: Define and initialize the genesis block.
4. **Create Accounts**: Use `geth` to create blockchain accounts.
5. **Use Docker**: Launch nodes using Docker for scalability.
6. **Mine Genesis Block**: Start mining using Geth.
7. **Connect**: Connect using Geth or JSON-RPC API.
8. **Deploy Contracts**: Compile and deploy SypherCore contracts.
9. **Use Wallet**: Set up and use the SypherCore wallet to interact with your blockchain.
