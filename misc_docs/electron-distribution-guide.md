# Complete Guide: Making Your Django-Electron App Distributable

## 1. Preparing Your Project

### 1.1 Create a Python Virtual Environment Package
First, we need to bundle Python with your application:
```bash
# Create requirements.txt if you haven't already
pip freeze > requirements.txt

# Install pyinstaller
pip install pyinstaller

# Create a standalone Python bundle
pyinstaller --name django_backend --add-data "my_project;my_project" --add-data "static;static" --add-data "templates;templates" python_server.py
```

### 1.2 Update Project Structure
Your project should look like:
```
your-app/
├── dist/
│   └── django_backend/  # PyInstaller output
├── build/              # PyInstaller build files
├── static/
├── templates/
├── my_project/
├── python_server.py
├── main.js
├── package.json
└── icon.ico           # Your app icon (256x256 recommended)
```

### 1.3 Configure package.json
```json
{
  "name": "arabic-diacriticizer",
  "version": "1.0.0",
  "description": "Arabic Text Diacritization App",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "dev": "electron . --debug",
    "build": "electron-builder",
    "make": "electron-builder"
  },
  "dependencies": {
    "alpinejs": "^3.14.8",
    "hotkeys-js": "^3.13.9"
  },
  "devDependencies": {
    "electron": "^29.1.0",
    "electron-builder": "^24.12.0"
  },
  "build": {
    "appId": "com.diacriticizer.app",
    "productName": "Arabic Diacriticizer",
    "copyright": "Copyright © 2024",
    "win": {
      "target": ["nsis"],
      "icon": "icon.ico",
      "extraResources": [
        {
          "from": "dist/django_backend",
          "to": "django_backend",
          "filter": ["**/*"]
        }
      ]
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true,
      "createStartMenuShortcut": true,
      "shortcutName": "Arabic Diacriticizer"
    }
  }
}
```

### 1.4 Update main.js to Use Bundled Python
```javascript
const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
let pyProc = null;
let mainWindow = null;

// Get correct path whether in development or production
const getPythonScriptPath = () => {
  const isDev = require('electron-is-dev');
  if (isDev) {
    return path.join(__dirname, 'python_server.py');
  }
  return path.join(process.resourcesPath, 'django_backend', 'django_backend.exe');
};

const startPython = () => {
  const scriptPath = getPythonScriptPath();
  pyProc = spawn(scriptPath, {
    stdio: ['pipe', 'pipe', 'pipe']
  });
  
  pyProc.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });
  
  pyProc.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });
};

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: path.join(__dirname, 'icon.ico'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // Wait a bit for Django to start
  setTimeout(() => {
    mainWindow.loadURL('http://localhost:8000');
  }, 2000);
};

app.on('ready', () => {
  startPython();
  createWindow();
});

app.on('window-all-closed', () => {
  if (pyProc) {
    pyProc.kill();
    pyProc = null;
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
```

## 2. Building the Application

### 2.1 Install Required Tools
```bash
# Install electron-builder globally
npm install -g electron-builder

# Install project dependencies
npm install
```

### 2.2 Build the Application
```bash
# Build for Windows
npm run build
```

This will create a `dist` folder containing your installer.

## 3. Distribution Checklist

### 3.1 Test Installation Package
Before distributing:
1. Test on a clean Windows machine
2. Verify all features work
3. Check startup time
4. Verify uninstallation process

### 3.2 Prepare Distribution Assets
- README file with installation instructions
- License file if applicable
- Change log
- Support contact information

## 4. Common Issues and Solutions

### 4.1 Python Not Found
If Python executable isn't found:
```javascript
// In main.js
const getPythonScriptPath = () => {
  const isDev = require('electron-is-dev');
  if (isDev) {
    return path.join(__dirname, 'python_server.py');
  }
  // Add error handling
  const exePath = path.join(process.resourcesPath, 'django_backend', 'django_backend.exe');
  if (!require('fs').existsSync(exePath)) {
    throw new Error(`Python executable not found at: ${exePath}`);
  }
  return exePath;
};
```

### 4.2 Port Already in Use
Add port checking:
```javascript
const checkPort = (port) => {
  return new Promise((resolve, reject) => {
    const net = require('net');
    const server = net.createServer();
    
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        resolve(false);
      }
      reject(err);
    });
    
    server.once('listening', () => {
      server.close();
      resolve(true);
    });
    
    server.listen(port);
  });
};

// Use in startPython
const startPython = async () => {
  const portAvailable = await checkPort(8000);
  if (!portAvailable) {
    throw new Error('Port 8000 is already in use');
  }
  // Rest of the code...
};
```

### 4.3 Antivirus Issues
Some antiviruses might block the Python executable. Add these to your build config:
```json
{
  "build": {
    "win": {
      "signAndEditExecutable": true,
      "publisherName": "Your Name",
      "requestedExecutionLevel": "asInvoker"
    }
  }
}
```

## 5. Additional Features to Consider

### 5.1 Auto Updates
Add electron-updater for automatic updates:
```javascript
const { autoUpdater } = require('electron-updater');

autoUpdater.checkForUpdatesAndNotify();
```

### 5.2 Error Reporting
Add error logging:
```javascript
const log = require('electron-log');

log.transports.file.level = 'info';
autoUpdater.logger = log;
```

### 5.3 Splash Screen
Add a splash screen while Django loads:
```javascript
const createSplashScreen = () => {
  let splash = new BrowserWindow({
    width: 500,
    height: 300,
    transparent: true,
    frame: false,
    alwaysOnTop: true
  });
  
  splash.loadFile('splash.html');
  return splash;
};
```

## 6. Post-Distribution Support

### 6.1 User Support
1. Create documentation for common issues
2. Set up a support email
3. Consider adding a bug report feature

### 6.2 Monitoring
1. Add basic analytics (with user consent)
2. Monitor error reports
3. Track usage patterns for improvements

Remember to always test the final package thoroughly on a clean machine before distribution.
