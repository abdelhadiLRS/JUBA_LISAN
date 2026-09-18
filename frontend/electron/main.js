/* eslint-disable @typescript-eslint/no-require-imports */
const { app, BrowserWindow, dialog, shell, utilityProcess } = require('electron');
const fs = require('fs');
const path = require('path');
const { startBackend, stopBackend } = require('./backend-manager');

let mainWindow = null;
let backend = null;
let renderer = null;

const isDev = !app.isPackaged;
const FRONTEND_DEV_URL = process.env.ELECTRON_START_URL || 'http://127.0.0.1:3000';

function findFreePort(host = '127.0.0.1') {
  return new Promise((resolve, reject) => {
    const server = require('net').createServer();
    server.once('error', reject);
    server.listen(0, host, () => {
      const address = server.address();
      const port = typeof address === 'object' && address ? address.port : 0;
      server.close(() => resolve(port));
    });
  });
}

async function startRendererServer() {
  if (isDev) return { child: null, url: FRONTEND_DEV_URL };

  const port = await findFreePort();
  const serverPath = path.join(process.resourcesPath, 'next-standalone', 'server.js');
  if (!fs.existsSync(serverPath)) {
    throw new Error(
      'Bundled Next.js renderer was not found. Reinstall the application or rebuild the Windows package.',
    );
  }

  const child = utilityProcess.fork(serverPath, [], {
    cwd: path.dirname(serverPath),
    env: {
      ...process.env,
      NODE_ENV: 'production',
      HOSTNAME: '127.0.0.1',
      PORT: String(port),
      NEXT_TELEMETRY_DISABLED: '1',
    },
    stdio: ['ignore', 'pipe', 'pipe'],
    serviceName: 'JUBA LISAN renderer',
  });

  let stderr = '';
  child.stderr?.on('data', (chunk) => {
    stderr += chunk.toString();
    if (stderr.length > 12000) stderr = stderr.slice(-12000);
  });

  const started = Date.now();
  while (Date.now() - started < 30000) {
    try {
      const response = await fetch('http://127.0.0.1:' + port + '/');
      if (response.status < 500) {
        return { child, url: 'http://127.0.0.1:' + port };
      }
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 250));
  }

  try { child.kill(); } catch {}
  throw new Error(
    'JUBA LISAN renderer did not become healthy in time.' +
    (stderr.trim() ? '\n\n' + stderr.trim() : ''),
  );
}

function stopRenderer(renderer) {
  if (!renderer?.child) return;
  try { renderer.child.kill(); } catch {}
}

function createWindow(rendererUrl) {
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
      additionalArguments: ['--juba-backend-url=' + backend.baseUrl],
    },
  });

  mainWindow.once('ready-to-show', () => mainWindow?.show());

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('https://') || url.startsWith('http://')) shell.openExternal(url);
    return { action: 'deny' };
  });

  mainWindow.webContents.on('did-fail-load', (_event, errorCode, errorDescription) => {
    if (!isDev && mainWindow && !mainWindow.isDestroyed()) {
      dialog.showErrorBox(
        'JUBA LISAN',
        'Unable to load the application.\n\n' + errorDescription + ' (' + errorCode + ')',
      );
    }
  });

  const loadPromise = isDev
    ? mainWindow.loadURL(FRONTEND_DEV_URL)
    : mainWindow.loadURL(rendererUrl);

  loadPromise.catch((error) => {
    dialog.showErrorBox('JUBA LISAN', 'Application startup failed.\n\n' + error.message);
  });

  if (isDev) mainWindow.webContents.openDevTools({ mode: 'detach' });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

async function bootstrap() {
  try {
    backend = await startBackend({ app, isDev });
    renderer = await startRendererServer();
    createWindow(renderer.url);
  } catch (error) {
    stopRenderer(renderer);
    if (backend) stopBackend(backend.child);
    dialog.showErrorBox('JUBA LISAN', 'Application startup failed.\n\n' + error.message);
    app.quit();
  }
}

app.whenReady().then(bootstrap);

app.on('before-quit', () => {
  stopRenderer(renderer);
  if (backend) stopBackend(backend.child);
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0 && backend) {
    if (renderer) createWindow(renderer.url);
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
