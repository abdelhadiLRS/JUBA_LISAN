/* eslint-disable @typescript-eslint/no-require-imports */
const { app, BrowserWindow, dialog, shell } = require('electron');
const fs = require('fs');
const http = require('http');
const path = require('path');
const { startBackend, stopBackend } = require('./backend-manager');

let mainWindow = null;
let backend = null;
let rendererServer = null;

const isDev = !app.isPackaged;
const FRONTEND_DEV_URL = process.env.ELECTRON_START_URL || 'http://127.0.0.1:3000';

function getRendererRoot() {
  return path.join(__dirname, '..', 'out');
}

function getContentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return {
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.wasm': 'application/wasm',
  }[ext] || 'application/octet-stream';
}

function startStaticRenderer() {
  const root = getRendererRoot();

  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      try {
        const requestPath = decodeURIComponent((req.url || '/').split('?')[0]);
        const normalized = path.normalize(requestPath).replace(/^([.][.][/\\])+/, '');
        let filePath = path.join(root, normalized);

        if (!filePath.startsWith(root)) {
          res.writeHead(403);
          res.end('Forbidden');
          return;
        }

        if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
          filePath = path.join(filePath, 'index.html');
        }

        if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
          if (!path.extname(filePath)) {
            filePath = path.join(root, 'index.html');
          } else {
            res.writeHead(404);
            res.end('Not found');
            return;
          }
        }

        res.writeHead(200, {
          'Content-Type': getContentType(filePath),
          'Cache-Control': path.basename(filePath) === 'index.html'
            ? 'no-store'
            : 'public, max-age=31536000, immutable',
          'X-Content-Type-Options': 'nosniff',
          'X-Frame-Options': 'DENY',
          'Referrer-Policy': 'strict-origin-when-cross-origin',
          'Permissions-Policy': 'camera=(), microphone=(self), geolocation=()',
          'Content-Security-Policy': [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'",
            "style-src 'self' 'unsafe-inline'",
            "connect-src 'self' http://127.0.0.1:* ws: wss:",
            "img-src 'self' data: blob:",
            "media-src 'self' blob:",
            "worker-src 'self' blob:",
            "font-src 'self'",
            "object-src 'none'",
            "base-uri 'self'",
          ].join('; '),
        });
        fs.createReadStream(filePath).pipe(res);
      } catch (error) {
        res.writeHead(500);
        res.end('Renderer error');
      }
    });

    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      if (!address || typeof address === 'string') {
        server.close();
        reject(new Error('Unable to allocate the desktop renderer port.'));
        return;
      }
      rendererServer = server;
      resolve('http://127.0.0.1:' + address.port);
    });
  });
}

function stopRenderer() {
  if (!rendererServer) return;
  try { rendererServer.close(); } catch {}
  rendererServer = null;
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
    const rendererUrl = isDev ? FRONTEND_DEV_URL : await startStaticRenderer();
    createWindow(rendererUrl);
  } catch (error) {
    stopRenderer();
    if (backend) stopBackend(backend.child);
    dialog.showErrorBox('JUBA LISAN', 'Application startup failed.\n\n' + error.message);
    app.quit();
  }
}

app.whenReady().then(bootstrap);

app.on('before-quit', () => {
  stopRenderer();
  if (backend) stopBackend(backend.child);
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0 && backend) {
    const rendererUrl = isDev ? FRONTEND_DEV_URL : (
      rendererServer ? 'http://127.0.0.1:' + rendererServer.address().port : null
    );
    if (rendererUrl) createWindow(rendererUrl);
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
