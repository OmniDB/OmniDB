var jsonfile = require('jsonfile');
var favicon = require('favicon-getter').default;
var path = require('path');
var uuid = require('uuid');
var bookmarks = path.join(__dirname, 'bookmarks.json');

var view = document.getElementById('view');
var loading = document.getElementById('loading');
var loading_interface = document.getElementById('loading_interface');

var ipc = require('electron').ipcRenderer;

ipc.send('invokeAction', null);

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

ipc.on('focus' , function(event , data) {
  view.focus();
});
