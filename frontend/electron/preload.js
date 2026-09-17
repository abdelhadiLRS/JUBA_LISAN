const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('jubaDesktop', {
  platform: process.platform,
  isDesktop: true,
  version: process.versions.electron,
});
