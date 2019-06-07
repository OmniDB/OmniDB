const electron = require('electron')
const child_process = require('child_process')

const app = electron.app
const BrowserWindow = electron.BrowserWindow

const path = require('path')
const url = require('url')

const Menu = electron.Menu;

var template = [{
    label: "Application",
    submenu: [
        { label: "About Application", selector:
"orderFrontStandardAboutPanel:" },
        { type: "separator" },
        { label: "Quit", accelerator: "Command+Q", click: function() {
app.quit(); }}
    ]}, {
    label: "Edit",
    submenu: [
        { label: "Undo", accelerator: "CmdOrCtrl+Z", selector: "undo:" },
        { label: "Redo", accelerator: "Shift+CmdOrCtrl+Z", selector: "redo:" },
        { type: "separator" },
        { label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:" },
        { label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:" },
        { label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:" },
        { label: "Select All", accelerator: "CmdOrCtrl+A", selector:
"selectAll:" }
    ]}
];

var ipc = require('electron').ipcMain;
let django;
let callback_started = false;

let mainWindow

function createWindow () {
  mainWindow = new BrowserWindow({width: 800, height: 600, icon:
path.join(__dirname, 'images/omnidb.png'), title: 'OmniDB'});
  mainWindow.setMenu(null);
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
  mainWindow.maximize();

  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  ipc.on('invokeAction', function(event, data){
    callback_started = true;

    //Starting the server
    django = child_process.spawn(path.join(__dirname,
'omnidb-server/omnidb-server'),['-A'],{detached: true});

    django.stdout.on('data', (data) => {
      v_data_list = data.toString('utf8').split("\n");
      mainWindow.webContents.send('info' , v_data_list);
    });

  });

  mainWindow.on('closed', function () {
    mainWindow = null
  })

  mainWindow.on('focus', function () {
    mainWindow.webContents.send('focus' , null);
  })
}

app.on('ready', createWindow)

app.on('will-quit', function () {
  if (callback_started) {
    while (django==null)
      null;
    try {
      process.kill(django.pid);
    }
    catch (e) {
    }
  }
  app.quit();
})

app.on('window-all-closed', function () {
  if (callback_started) {
    while (django==null)
      null;
    try {
      process.kill(django.pid);
    }
    catch (e) {
    }
  }
  app.quit();
})

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow()
  }
})
