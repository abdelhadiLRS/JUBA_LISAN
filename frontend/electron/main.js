const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');

let mainWindow = null;

const isDev = !app.isPackaged;
const FRONTEND_DEV_URL = process.env.ELECTRON_START_URL || 'http://127.0.0.1:3000';

function getRendererPath() {
  return path.join(__dirname, '..', 'out', 'index.html');
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 960,
    minHeight: 640,
    show: false,
    title: 'JUBA LISAN',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
    icon: path.join(__dirname, '..', 'public', 'icon.png'),
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('https://') || url.startsWith('http://')) {
      require('electron').shell.openExternal(url);
    }
    return { action: 'deny' };
  });

  mainWindow.webContents.on('did-fail-load', (_event, errorCode, errorDescription) => {
    if (!isDev && mainWindow && !mainWindow.isDestroyed()) {
      dialog.showErrorBox(
        'JUBA LISAN',
        `Unable to load the application.\n\n${errorDescription} (${errorCode})`,
      );
    }
  });

  const loadPromise = isDev
    ? mainWindow.loadURL(FRONTEND_DEV_URL)
    : mainWindow.loadFile(getRendererPath());

  loadPromise.catch((error) => {
    dialog.showErrorBox('JUBA LISAN', `Application startup failed.\n\n${error.message}`);
  });

  if (isDev) {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
