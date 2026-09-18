/* eslint-disable @typescript-eslint/no-require-imports */
const { contextBridge } = require('electron');

const backendArg = process.argv.find((arg) => arg.startsWith('--juba-backend-url='));
const backendUrl = backendArg ? backendArg.slice('--juba-backend-url='.length) : '';

contextBridge.exposeInMainWorld('jubaDesktop', {
  platform: process.platform,
  isDesktop: true,
  version: process.versions.electron,
  backendUrl,
});
