const { app, BrowserWindow, ipcMain, shell } = require('electron')
const path = require('path')
const http = require('http');
const { spawn } = require('child_process');

// TODO: find better ports
const PORT_FRONTEND = 3001;
const PORT_BACKEND = 3002;
let backend = null;

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js')
    }, 
    show: false
  })

  win.maximize();
  win.show();

  win.loadFile('index.html')

  const forwardMsgToUser = ({ msg, sender }) => {
    console.log("forwarding " + msg + "from user " + sender + " to user!");
    win.webContents.send('user-receive-msg', msg, sender);
  };

  const disableSTT = () => {
    console.log("disabling stt");
    win.webContents.send('set-state-stt', false);
  }

  // setup server to monitor for POST requests from back-end
  http.createServer((req, res) => {
    if (req.method === 'POST') {
      let msg = '';
      req.on('data', chunk => {
        msg += chunk;
      })

      req.on('end', () => {
        res.statusCode = 200;
        res.end('received');
        console.log("message:", msg);
        
        let json = JSON.parse(msg);
        
        switch (JSON.stringify(Object.keys(json))) {
          case JSON.stringify(['msg', 'sender']):
            forwardMsgToUser(json);
            break;
          case JSON.stringify(['stt']):
            disableSTT();
            break;
          default:
            console.log('message not recognized');
        }
        
      })
    } else {
      res.statusCode = 400;
      res.end('invalid request');
    }
  }).listen(PORT_FRONTEND, '127.0.0.1'); /* should specify that it only receives messages on port PORT_FRONTEND from its own ip address*/
}

const forwardMsgToJade = (event, msg) => {
  console.log('sending "' + msg + '" to jade!');

  // Sends POST request
  const url = `http://127.0.0.1:${PORT_BACKEND}`;
  fetch(url, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json'
    },   
    body: JSON.stringify({
      'msg': msg,
      'sender': 'user'
    }
    )})
    // .then(response => response.json())
    .then(responseData => {
    // Handle the response data
    // console.log(responseData);
    })
    .catch(error => {
      // Handle any errors
      console.error('error:', error);
    })
};

const forwardSTTToggle = (event, enabled) => {
  console.log("sending stt enabled state =", enabled, "to jade!");
  const url = `http://127.0.0.1:${PORT_BACKEND}`;

  fetch(url, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json'
    },   
    body: JSON.stringify({
      // 'msg': msg,
      // 'sender': 'user'
      'stt_enabled': enabled
    }
    )})
    // .then(response => response.json())
    .then(responseData => {
    // Handle the response data
    // console.log(responseData);
    })
    .catch(error => {
      // Handle any errors
      console.error('error:', error);
    })
};

app.whenReady().then(() => {
  // setup backend
  backend = spawn('python', ['./../backend/__main__.py'], { env: {...process.env }});

  // backend output for debugging
  backend.stdout.on('data', (data) => {
    console.log(`PowerShell Output: ${data}`);
  });
  backend.stderr.on('data', (data) => {
    console.log(`PowerShell Output: ${data}`);
  });

  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  })

  ipcMain.on('user-send-msg', forwardMsgToJade);
  ipcMain.on('stt-toggle', forwardSTTToggle);
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (backend) {
      backend.kill();
    }
    app.quit()
  }
})