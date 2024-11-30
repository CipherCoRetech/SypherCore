import tkinter as tk
from wallet.wallet import Wallet

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SypherCore Wallet")

        # Create wallet instance
        self.wallet = Wallet()

        # Display wallet address
        self.address_label = tk.Label(root, text=f"Address: {self.wallet.address}")
        self.address_label.pack()

        # Display balance
        self.balance_label = tk.Label(root, text="Balance: 0 Sypher")
        self.balance_label.pack()
        self.update_balance()

        # Send tokens section
        self.recipient_label = tk.Label(root, text="Recipient Address:")
        self.recipient_label.pack()
        self.recipient_entry = tk.Entry(root)
        self.recipient_entry.pack()

        self.amount_label = tk.Label(root, text="Amount (Sypher):")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.send_button = tk.Button(root, text="Send", command=self.send_tokens)
        self.send_button.pack()

    def update_balance(self):
        balance = self.wallet.get_balance()
        self.balance_label.config(text=f"Balance: {balance} Sypher")

    def send_tokens(self):
        recipient = self.recipient_entry.get()
        amount = float(self.amount_entry.get())
        tx_hash = self.wallet.send_transaction(recipient, amount)
        tk.messagebox.showinfo("Transaction", f"Transaction successful! Hash: {tx_hash}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()
