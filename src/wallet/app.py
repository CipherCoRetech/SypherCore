from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)

# Define the blockchain RPC URL to interact with
BLOCKCHAIN_RPC_URL = "http://localhost:8545"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    # Create a new wallet address
    response = requests.post(f"{BLOCKCHAIN_RPC_URL}/create_wallet")
    return jsonify(response.json())

@app.route('/wallet/balance', methods=['GET'])
def get_balance():
    # Get balance of a given wallet address
    address = request.args.get('address')
    response = requests.get(f"{BLOCKCHAIN_RPC_URL}/get_balance?address={address}")
    return jsonify(response.json())

@app.route('/wallet/transfer', methods=['POST'])
def transfer():
    data = request.json
    response = requests.post(f"{BLOCKCHAIN_RPC_URL}/transfer", json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
