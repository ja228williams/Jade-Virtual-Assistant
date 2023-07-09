const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    sendMsgToJade: msg => ipcRenderer.send('user-send-msg', msg), 
    receiveJadeMsg: (msg, user) => ipcRenderer.on('user-receive-msg', msg, user),
    sttToggle: enabled => ipcRenderer.send('stt-toggle', enabled),
    sttSetState: (state) => ipcRenderer.on('set-state-stt', state)
});