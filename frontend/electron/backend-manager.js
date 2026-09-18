/* eslint-disable @typescript-eslint/no-require-imports */
const { spawn } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const net = require('net');
const path = require('path');

function findFreePort(host = '127.0.0.1') {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.once('error', reject);
    server.listen(0, host, () => {
      const address = server.address();
      const port = typeof address === 'object' && address ? address.port : 0;
      server.close(() => resolve(port));
    });
  });
}

function getDesktopSecretKey(dataDir) {
  const secretPath = path.join(dataDir, '.secret_key');

  try {
    const existing = fs.readFileSync(secretPath, 'utf8').trim();
    if (existing.length >= 32) return existing;
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }

  const generated = crypto.randomBytes(32).toString('base64url');
  try {
    fs.writeFileSync(secretPath, generated, { encoding: 'utf8', flag: 'wx' });
    return generated;
  } catch (error) {
    if (error.code === 'EEXIST') {
      const existing = fs.readFileSync(secretPath, 'utf8').trim();
      if (existing.length >= 32) return existing;
    }
    throw error;
  }
}

function waitForHealth(url, timeoutMs = 30000) {
  const started = Date.now();
  return new Promise((resolve, reject) => {
    const retry = () => {
      if (Date.now() - started >= timeoutMs) {
        reject(new Error('JUBA LISAN backend did not become healthy in time.'));
        return;
      }
      setTimeout(check, 250);
    };
    const check = () => {
      const http = require('http');
      const request = http.get(url, (response) => {
        response.resume();
        // /health is an application readiness endpoint. Treat only an explicit
        // 200 response as healthy; a 3xx/4xx response must not unblock startup.
        if (response.statusCode === 200) {
          resolve();
          return;
        }
        retry();
      });
      request.on('error', retry);
      request.setTimeout(2000, () => {
        request.destroy();
        retry();
      });
    };
    check();
  });
}

async function startBackend({ app, isDev }) {
  // Development keeps the backend on the conventional port so Next.js
  // server-side requests and its /api rewrites resolve to the same service.
  // Packaged Desktop uses an ephemeral port to avoid collisions.
  const port = isDev
    ? Number(process.env.JUBA_BACKEND_PORT || 8000)
    : await findFreePort();
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error('JUBA_BACKEND_PORT must be a valid TCP port.');
  }

  const dataDir = path.join(app.getPath('userData'), 'data');
  fs.mkdirSync(dataDir, { recursive: true });

  const packagedExe = path.join(
    process.resourcesPath,
    'backend',
    'juba-lisan-backend.exe',
  );

  let command;
  let args;

  if (!isDev) {
    if (!fs.existsSync(packagedExe)) {
      throw new Error(
        'Bundled JUBA LISAN backend was not found. Reinstall the application or rebuild the Windows package.',
      );
    }
    command = packagedExe;
    args = ['--host', '127.0.0.1', '--port', String(port)];
  } else {
    command = process.platform === 'win32' ? 'python' : 'python3';
    args = [
      '-m', 'uvicorn', 'app.main:app',
      '--host', '127.0.0.1', '--port', String(port), '--workers', '1',
    ];
  }

  const cwd = isDev
    ? path.resolve(__dirname, '../../backend')
    : path.join(process.resourcesPath, 'backend');

  const env = {
    ...process.env,
    DESKTOP_MODE: 'true',
    DATA_DIR: dataDir,
    DATABASE_URL: 'sqlite+aiosqlite:///' + path.join(dataDir, 'database', 'juba_lisan.db'),
    REDIS_ENABLED: 'false',
    REDIS_URL: '',
    SECRET_KEY: process.env.SECRET_KEY || getDesktopSecretKey(dataDir),
    AUDIO_STORAGE_PATH: path.join(dataDir, 'audio'),
    CORS_ORIGINS: '["http://127.0.0.1","http://localhost","null"]',
  };

  const child = spawn(command, args, {
    cwd,
    env,
    stdio: isDev ? 'inherit' : ['ignore', 'pipe', 'pipe'],
    windowsHide: true,
  });

  let stderr = '';
  let exitedBeforeReady = false;
  let exitCode = null;
  let exitSignal = null;
  if (child.stderr) {
    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
      if (stderr.length > 12000) stderr = stderr.slice(-12000);
    });
  }

  child.on('error', (error) => {
    child.startupError = error;
  });
  child.on('exit', (code, signal) => {
    exitedBeforeReady = true;
    exitCode = code;
    exitSignal = signal;
  });

  try {
    await waitForHealth('http://127.0.0.1:' + port + '/health');
  } catch (error) {
    try { child.kill(); } catch {}
    const detail = stderr.trim() ? '\n\n' + stderr.trim() : '';
    const processDetail = exitedBeforeReady
      ? '\n\nBackend process exited before becoming healthy (code=' + exitCode + ', signal=' + (exitSignal || 'none') + ').'
      : '';
    throw new Error(error.message + processDetail + detail);
  }

  return {
    child,
    port,
    baseUrl: 'http://127.0.0.1:' + port,
    dataDir,
  };
}

function stopBackend(child) {
  if (!child || child.killed) return;
  try {
    child.kill();
  } catch {}
}

module.exports = { startBackend, stopBackend };
