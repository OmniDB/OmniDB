// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

var ById = function (id) {
    return document.getElementById(id);
}
var jsonfile = require('jsonfile');
var favicon = require('favicon-getter').default;
var path = require('path');
var uuid = require('uuid');
var bookmarks = path.join(__dirname, 'bookmarks.json');

var view = ById('view');
var loading = ById('loading');
var loading_interface = ById('loading_interface');

var ipc = require('electron').ipcRenderer;

ipc.on('info' , function(event , data) {
  for (var i=0; i<data.length-1; i++) {
    if (data[i].substring(0, 4)!='http')
      loading.innerHTML += data[i] + '<br/>';
    else {
      loading.innerHTML += 'Opening OmniDB...<br/>';
      (function(value) { setTimeout( function() {
        loading_interface.style.display = 'none';
        view.style.display = '';
        view.src = value;
      },2000);
    })(data[i]);
    }
  }
});
