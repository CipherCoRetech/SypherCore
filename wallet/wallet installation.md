### Instructions on How to Install the SypherCore Wallet

To facilitate the use and management of SypherCore tokens, follow these instructions to set up the wallet on your machine:

#### **1. Prerequisites**

Before installing the wallet, ensure you have:

- **Node.js** (latest LTS version recommended) and **npm** installed.
- **Git** to clone the wallet repository.
- A **stable internet connection**.

#### **2. Installation Steps for the SypherCore Wallet**

##### Step 1: Clone the Wallet Repository

First, clone the SypherCore wallet repository from GitHub:

```sh
git clone https://github.com/SypherCoRe/SypherCore-Wallet.git
cd SypherCore-Wallet
```

##### Step 2: Install Dependencies

Once inside the cloned directory, install all necessary dependencies by running:

```sh
npm install
```

This command installs all the dependencies required for running the SypherCore wallet.

##### Step 3: Start the Wallet

To start the SypherCore wallet application in development mode, use the command:

```sh
npm start
```

The wallet interface should now be accessible from your browser at:

```
http://localhost:3000
```

##### Step 4: Build for Production

If you wish to build the wallet for production (e.g., to run it on a server or as a standalone application), run:

```sh
npm run build
```

This will create a `build/` directory containing all the static files to serve for a production wallet.

### **Creating a Windows Wallet Application for SypherCore**

#### **1. Prerequisites for Creating a Windows Executable Wallet**

- **Node.js** and **npm** should be installed.
- **Electron**: This will allow us to create a desktop application from the wallet.
- **Windows Operating System**: For packaging a Windows-specific version.

#### **2. Converting the SypherCore Wallet into a Windows Application**

##### Step 1: Install Electron

Electron allows you to package your wallet as a Windows application. You can install Electron globally using npm:

```sh
npm install -g electron
```

##### Step 2: Configure Electron for Wallet Application

Create an `electron.js` file at the root of the `SypherCore-Wallet` directory:

```javascript
// electron.js - Main File for Electron Integration

const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 1280,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    // Load the wallet interface.
    win.loadFile('build/index.html');
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
```

This script initializes an Electron instance that will load the SypherCore wallet in a standalone desktop window.

##### Step 3: Update Package.json

Add a script to start Electron in your `package.json`:

```json
"scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "electron": "electron electron.js"
}
```

This will allow you to run `npm run electron` to launch the Electron app.

##### Step 4: Build the Electron Windows Application

Run the following commands to build the wallet for production:

1. **Build the React Wallet**:

    ```sh
    npm run build
    ```

2. **Run Electron** to package the wallet:

    ```sh
    npm run electron
    ```

##### Step 5: Package the Application for Windows

To create an executable for the wallet, you will need **electron-packager** or **electron-builder**. For example, to use **electron-packager**:

Install electron-packager:

```sh
npm install -g electron-packager
```

Run the packager:

```sh
electron-packager . SypherCoreWallet --platform=win32 --arch=x64 --out=release-builds
```

This will create an executable in the `release-builds` directory.

### **Optional - Cross-Platform Builds**

For users who would like a cross-platform wallet, use **electron-builder**, which simplifies the process:

```sh
npm install -g electron-builder
```

Add the `build` script in `package.json`:

```json
"build": {
    "appId": "com.syphercore.wallet",
    "productName": "SypherCoreWallet",
    "directories": {
        "buildResources": "assets"
    },
    "files": [
        "build/**/*",
        "electron.js"
    ],
    "win": {
        "target": [
            "nsis"
        ]
    }
}
```

Build the Windows executable:

```sh
electron-builder build --win
```

### **Summary**

- **Install Dependencies**: Clone and install the SypherCore wallet dependencies using `npm install`.
- **Run Locally**: Start the wallet using `npm start`.
- **Build Electron App**: Add Electron configurations to create a standalone wallet.
- **Package for Windows**: Use **electron-packager** or **electron-builder** to package the wallet as a `.exe` file.

This provides you with a complete, standalone Windows application for managing SypherCore tokens, offering users a familiar and easy-to-use interface. Let me know if you need additional guidance or want any more features included in the wallet!
