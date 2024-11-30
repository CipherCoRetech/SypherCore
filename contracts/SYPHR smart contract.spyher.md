// TokenContract.sypher

contract SypherToken {
    // Define the token properties
    public string name = "SypherCore Token";
    public string symbol = "SYPR";
    public uint256 totalSupply;
    private map<string, uint256> balances;
    private map<string, map<string, uint256>> allowances;

    // Events to log transfers and approvals
    event Transfer(string from, string to, uint256 value);
    event Approval(string owner, string spender, uint256 value);

    // Initialize the contract with initial supply and assign all tokens to the owner
    function initialize(uint256 initialSupply, string owner) {
        totalSupply = initialSupply;
        balances[owner] = initialSupply;
        emit Transfer("0x0", owner, initialSupply); // Log the initial distribution
    }

    // Function to get the balance of a particular account
    public function balanceOf(string account) returns (uint256) {
        return balances[account];
    }

    // Transfer tokens from the caller to another account
    public function transfer(string to, uint256 value) returns (bool) {
        string sender = msg.sender();
        require(balances[sender] >= value, "Insufficient balance");
        
        balances[sender] -= value;
        balances[to] += value;
        
        emit Transfer(sender, to, value);
        return true;
    }

    // Approve another account to spend tokens on behalf of the caller
    public function approve(string spender, uint256 value) returns (bool) {
        string owner = msg.sender();
        allowances[owner][spender] = value;
        
        emit Approval(owner, spender, value);
        return true;
    }

    // Transfer tokens from one account to another, if approved
    public function transferFrom(string from, string to, uint256 value) returns (bool) {
        string spender = msg.sender();
        require(balances[from] >= value, "Insufficient balance");
        require(allowances[from][spender] >= value, "Allowance exceeded");
        
        balances[from] -= value;
        balances[to] += value;
        allowances[from][spender] -= value;
        
        emit Transfer(from, to, value);
        return true;
    }

    // Get the remaining allowance that a spender has from a particular owner
    public function allowance(string owner, string spender) returns (uint256) {
        return allowances[owner][spender];
    }

    // Mint new tokens and add to the total supply
    public function mint(uint256 amount, string to) returns (bool) {
        require(msg.sender() == "owner", "Only the contract owner can mint tokens");
        totalSupply += amount;
        balances[to] += amount;
        
        emit Transfer("0x0", to, amount);
        return true;
    }

    // Burn tokens to reduce the total supply
    public function burn(uint256 amount) returns (bool) {
        string owner = msg.sender();
        require(balances[owner] >= amount, "Insufficient balance to burn");
        
        balances[owner] -= amount;
        totalSupply -= amount;
        
        emit Transfer(owner, "0x0", amount);
        return true;
    }
}
