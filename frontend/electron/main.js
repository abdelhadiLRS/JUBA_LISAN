/* eslint-disable @typescript-eslint/no-require-imports */
const { app, BrowserWindow, dialog, shell, utilityProcess } = require('electron');
const fs = require('fs');
const path = require('path');
const { startBackend, stopBackend } = require('./backend-manager');

let mainWindow = null;
let backend = null;
let renderer = null;
let isQuitting = false;

const isDev = !app.isPackaged;
const FRONTEND_DEV_URL = process.env.ELECTRON_START_URL || 'http://127.0.0.1:3000';

function writeDesktopLog(message) {
  if (isDev) return;
  try {
    const logDir = app.getPath('userData');
    fs.mkdirSync(logDir, { recursive: true });
    const logPath = path.join(logDir, 'juba-lisan-desktop.log');
    const line = new Date().toISOString() + ' ' + message + '\\n';
    fs.appendFileSync(logPath, line, { encoding: 'utf8' });
  } catch {}
}

// SQLite desktop mode is a single-user local application. Prevent two Electron
// instances from opening the same database and data directory concurrently.
const gotSingleInstanceLock = app.requestSingleInstanceLock();
if (!gotSingleInstanceLock) {
  app.quit();
}

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

async function startRendererServer(backendUrl) {
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
      BACKEND_URL: backendUrl,
    },
    stdio: ['ignore', 'pipe', 'pipe'],
    serviceName: 'JUBA LISAN renderer',
  });

  // Keep a reference to an unexpected renderer exit so the packaged app does
  // not remain open on a permanently blank window after Next.js crashes.
  let rendererExited = false;
  let rendererExitCode = null;
  child.once('exit', (code) => {
    rendererExited = true;
    rendererExitCode = code;
    if (isQuitting) return;
    if (!mainWindow || mainWindow.isDestroyed()) return;
    const detail = 'exit code ' + code;
    writeDesktopLog('Renderer stopped unexpectedly: ' + detail);
    dialog.showErrorBox(
      'JUBA LISAN',
      'The application renderer stopped unexpectedly (' + detail + ').\n\nPlease restart JUBA LISAN.',
    );
    isQuitting = true;
    try { mainWindow.close(); } catch {}
    app.quit();
  });

  // Consume both child streams so verbose Next.js startup logs cannot fill a pipe.
  let stdout = '';
  child.stdout?.on('data', (chunk) => {
    stdout += chunk.toString();
    if (stdout.length > 12000) stdout = stdout.slice(-12000);
  });

  let stderr = '';
  child.stderr?.on('data', (chunk) => {
    stderr += chunk.toString();
    if (stderr.length > 12000) stderr = stderr.slice(-12000);
  });

  const failStartup = (message) => {
    try { child.kill(); } catch {}
    throw new Error(
      message + (stderr.trim() ? '\n\n' + stderr.trim() : ''),
    );
  };

  const started = Date.now();
  while (Date.now() - started < 30000) {
    if (rendererExited) {
      failStartup(
        'JUBA LISAN renderer exited during startup (exit code ' + rendererExitCode + ').',
      );
    }

    try {
      const response = await fetch('http://127.0.0.1:' + port + '/');
      if (response.status === 200) {
        return { child, url: 'http://127.0.0.1:' + port };
      }
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 250));
  }

  failStartup('JUBA LISAN renderer did not become healthy in time.');
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
    writeDesktopLog('Application startup failed: ' + error.message);
    dialog.showErrorBox('JUBA LISAN', 'Application startup failed.\n\n' + error.message);
  });

  if (isDev) mainWindow.webContents.openDevTools({ mode: 'detach' });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function monitorBackendProcess(child) {
  if (!child || isDev) return;

  child.once('exit', (code, signal) => {
    if (isQuitting) return;

    const detail = code === null
      ? 'signal ' + (signal || 'unknown')
      : 'exit code ' + code;

    if (mainWindow && !mainWindow.isDestroyed()) {
      writeDesktopLog('Backend stopped unexpectedly: ' + detail);
      dialog.showErrorBox(
        'JUBA LISAN',
        'The local backend stopped unexpectedly (' + detail + ').\n\nPlease restart JUBA LISAN.',
      );
    }

    isQuitting = true;
    try { mainWindow?.close(); } catch {}
    app.quit();
  });
}

async function bootstrap() {
  try {
    backend = await startBackend({ app, isDev });
    writeDesktopLog('Backend ready at ' + backend.baseUrl);
    monitorBackendProcess(backend.child);
    renderer = await startRendererServer(backend.baseUrl);
    writeDesktopLog('Renderer ready at ' + renderer.url);
    createWindow(renderer.url);
  } catch (error) {
    stopRenderer(renderer);
    if (backend) stopBackend(backend.child);
    dialog.showErrorBox('JUBA LISAN', 'Application startup failed.\n\n' + error.message);
    app.quit();
  }
}

app.on('second-instance', () => {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  if (mainWindow.isMinimized()) mainWindow.restore();
  mainWindow.focus();
});

if (gotSingleInstanceLock) {
  app.whenReady().then(bootstrap);
}

app.on('before-quit', () => {
  isQuitting = true;
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
