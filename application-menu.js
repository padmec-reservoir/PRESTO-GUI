const {BrowserWindow, Menu, app, shell, dialog} = require('electron')

let template = [{
    label: 'File',
    submenu: [
        {
            label: 'Open',
            accelerator: process.platform == 'darwin' ? 'Command+O' : 'Ctrl+O',
            click() {
                // TODO: Add callback function to save path
                // to selected user file.
                const filePaths = dialog.showOpenDialog({
                    properties: ['openFile'],
                    filters: [
                        {
                            name: 'PRESTO file',
                            extensions: ['presto']
                        },
                        {
                            name: 'All files',
                            extensions: ['*']
                        }
                    ]
                });
                console.log(filePaths);
            }
        },
        {
            label: 'Import mesh',
            click() {
                // TODO: Add callback function.
                console.log(dialog.showOpenDialog({
                    properties: ['openFile'],
                    filters: [
                        {
                            name: 'Mesh file',
                            extensions: ['vtk', 'msh']
                        },
                        {
                            name: 'All files',
                            extensions: ['*']
                        }
                    ]
                }));
            }
        },
        {
            type: 'separator'
        },
        {
            label: 'Save',
            accelerator: process.platform == 'darwin' ? 'Command+S' : 'Ctrl+S',
            // TODO: Handle first save and posterior ones. Add callback function.
            click() {
                console.log(dialog.showSaveDialog({
                    title: 'Save'
                }));
            }
        },
        {
            label: 'Save as...',
            accelerator: process.platform == 'darwin' ? 'Command+Shift+S' : 'Ctrl+Shift+S',
            // TODO: Add callback function.
            click() {
                console.log(dialog.showSaveDialog({
                    title: 'Save as'
                }));
            }
        },
        {
            type: 'separator'
        },
        {
            label: 'Exit',
            accelerator: process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
            click() {
                app.quit();
            }
        }
    ]},
    {
        label: 'Edit',
        submenu: [
            {
                label: 'Undo',
                accelerator: 'CmdOrCtrl+Z',
                role: 'undo'
            },
            {
                label: 'Redo',
                accelerator: 'Shift+CmdOrCtrl+Z',
                role: 'redo'
            },
            {
                type: 'separator'
            },
            {
                label: 'Cut',
                accelerator: 'CmdOrCtrl+X',
                role: 'cut'
            },
            {
                label: 'Copy',
                accelerator: 'CmdOrCtrl+C',
                role: 'copy'
            },
            {
                label: 'Paste',
                accelerator: 'CmdOrCtrl+V',
                role: 'paste'
            },
            {
                label: 'Select All',
                accelerator: 'CmdOrCtrl+A',
                role: 'selectall'
            }
        ]
    },
    {
        label: 'View',
        submenu: [
            {
                label: 'Reload',
                accelerator: 'CmdOrCtrl+R',
                click: (item, focusedWindow) => {
                    if (focusedWindow) {
                        // on reload, start fresh and close any old
                        // open secondary windows
                        if (focusedWindow.id === 1) {
                            BrowserWindow.getAllWindows().forEach(win => {
                                if (win.id > 1) win.close()
                            })
                        }
                        focusedWindow.reload()
                    }
                }
            },
            {
                label: 'Toggle Full Screen',
                accelerator: process.platform == 'darwin' ? 'Ctrl+Command+F' : 'F11',
                click: (item, focusedWindow) => {
                    if (focusedWindow) {
                        focusedWindow.setFullScreen(!focusedWindow.isFullScreen())
                    }
                }
            },
            {
                label: 'Toggle Developer Tools',
                accelerator: process.platform == 'darwin' ? 'Alt+Command+I' : 'Ctrl+Shift+I',
                click: (item, focusedWindow) => {
                    if (focusedWindow) {
                        focusedWindow.toggleDevTools()
                    }
                }
            }]
    },
    {
        label: 'Window',
        role: 'window',
        submenu: [
            {
                label: 'Minimize',
                accelerator: 'CmdOrCtrl+M',
                role: 'minimize'
            },
            {
                label: 'Close',
                accelerator: 'CmdOrCtrl+W',
                role: 'close'
            },
            {
                type: 'separator'
            },
            {
                label: 'Reopen Window',
                accelerator: 'CmdOrCtrl+Shift+T',
                enabled: false,
                key: 'reopenMenuItem',
                click: () => {
                    app.emit('activate')
                }
            }]
    },
    {
        label: 'Help',
        submenu: [
            {
                label: 'Help',
                accelerator: process.platform == 'darwin' ? 'Command+H' : 'Ctrl+H',
                click() {
                    createHelpWindow();
                }
            },
            {
                label: 'About',
                click() {
                    createAboutWindow();
                }
            }
        ]
}]

function createHelpWindow () {
    helpWindow = new BrowserWindow({
        width: 300,
        height: 400,
        autoHideMenuBar: true
    });
    // helpWindow.loadURL(url.format({
    //     pathname: path.join(__dirname, 'help.html'),
    //     protocol: 'file:',
    //     slashes: true
    // }));

    helpWindow.on('closed', () => {
        helpWindow = null;
    });
}

function createAboutWindow () {
    aboutWindow = new BrowserWindow({
        width: 400,
        height: 400,
        autoHideMenuBar: true
    });
    // aboutWindow.loadURL(url.format({
    //     pathname: path.join(__dirname, 'about.html'),
    //     protocol: 'file:',
    //     slashes: true
    // }));

    aboutWindow.on('closed', () => {
        aboutWindow = null;
    });
}

function addUpdateMenuItems (items, position) {
  if (process.mas) return

  const version = app.getVersion()
  let updateItems = [{
    label: `Version ${version}`,
    enabled: false
  }, {
    label: 'Checking for Update',
    enabled: false,
    key: 'checkingForUpdate'
  }, {
    label: 'Check for Update',
    visible: false,
    key: 'checkForUpdate',
    click: () => {
      require('electron').autoUpdater.checkForUpdates()
    }
  }, {
    label: 'Restart and Install Update',
    enabled: true,
    visible: false,
    key: 'restartToUpdate',
    click: () => {
      require('electron').autoUpdater.quitAndInstall()
    }
  }]

  items.splice.apply(items, [position, 0].concat(updateItems))
}

function findReopenMenuItem () {
  const menu = Menu.getApplicationMenu()
  if (!menu) return

  let reopenMenuItem
  menu.items.forEach(item => {
    if (item.submenu) {
      item.submenu.items.forEach(item => {
        if (item.key === 'reopenMenuItem') {
          reopenMenuItem = item
        }
      })
    }
  })
  return reopenMenuItem
}

if (process.platform === 'darwin') {
  const name = app.getName()
  template.unshift({
    label: name,
    submenu: [{
      label: `About ${name}`,
      role: 'about'
    }, {
      type: 'separator'
    }, {
      label: 'Services',
      role: 'services',
      submenu: []
    }, {
      type: 'separator'
    }, {
      label: `Hide ${name}`,
      accelerator: 'Command+H',
      role: 'hide'
    }, {
      label: 'Hide Others',
      accelerator: 'Command+Alt+H',
      role: 'hideothers'
    }, {
      label: 'Show All',
      role: 'unhide'
    }, {
      type: 'separator'
    }, {
      label: 'Quit',
      accelerator: 'Command+Q',
      click: () => {
        app.quit()
      }
    }]
  })

  // Window menu.
  template[3].submenu.push({
    type: 'separator'
  }, {
    label: 'Bring All to Front',
    role: 'front'
  })

  addUpdateMenuItems(template[0].submenu, 1)
}

if (process.platform === 'win32') {
  const helpMenu = template[template.length - 1].submenu
  addUpdateMenuItems(helpMenu, 0)
}

app.on('ready', () => {
  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
  console.log("Menu created");
})

app.on('browser-window-created', () => {
  let reopenMenuItem = findReopenMenuItem()
  if (reopenMenuItem) reopenMenuItem.enabled = false
})

app.on('window-all-closed', () => {
  let reopenMenuItem = findReopenMenuItem()
  if (reopenMenuItem) reopenMenuItem.enabled = true
})
