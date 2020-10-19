/*
This file is part of OmniDB.
OmniDB is open-source software, distributed "AS IS" under the MIT license in the hope that it will be useful.

The MIT License (MIT)

Portions Copyright (c) 2015-2020, The OmniDB Team
Portions Copyright (c) 2017-2020, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

var v_default_shortcuts = {
  'shortcut_run_query': {
    'windows': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'Q',
    },
    'linux': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'Q',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'Q',
    }
  },
  'shortcut_cancel_query': {
    'windows': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'C',
    },
    'linux': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'C',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'C',
    }
  },
  'shortcut_indent': {
    'windows': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'S',
    },
    'linux': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'S',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'S',
    }
  },
  'shortcut_new_inner_tab': {
    'windows': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'I',
    },
    'linux': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'I',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'I',
    }
  },
  'shortcut_remove_inner_tab': {
    'windows': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'Q',
    },
    'linux': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'Q',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': true,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'Q',
    }
  },
  'shortcut_left_inner_tab': {
    'windows': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'O',
    },
    'linux': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'O',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'O',
    }
  },
  'shortcut_right_inner_tab': {
    'windows': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'P',
    },
    'linux': {
        'ctrl_pressed': false,
        'shift_pressed': false,
        'alt_pressed': true,
        'meta_pressed': false,
        'shortcut_key': 'P',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'P',
    }
  },
  'shortcut_autocomplete': {
    'windows': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'SPACE',
    },
    'linux': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'SPACE',
    },
    'macos': {
        'ctrl_pressed': true,
        'shift_pressed': false,
        'alt_pressed': false,
        'meta_pressed': false,
        'shortcut_key': 'A',
    }
  }
}

//Initializing shortcut buttons
$(function () {

  v_current_os="Unknown OS";
  if (navigator.appVersion.indexOf("Win")!=-1) v_current_os="windows";
  if (navigator.appVersion.indexOf("Mac")!=-1) v_current_os="macos";
  if (navigator.appVersion.indexOf("X11")!=-1) v_current_os="linux";
  if (navigator.appVersion.indexOf("Linux")!=-1) v_current_os="linux";

  //Shortcut actions
  v_shortcut_object.actions = {
    shortcut_run_query: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query')
          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_start.click();
        else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console')
          consoleSQL(false);
        else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='edit')
          queryEditData();
      }
      else if (v_connTabControl.selectedTab.tag.mode=='outer_terminal')
        terminalRun();
    },
    shortcut_cancel_query: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query' || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console')
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_cancel.style.display!='none')
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_cancel.click();
      }
    },
    shortcut_indent: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query' || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console')
          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_indent.click();
      }

    },
    shortcut_new_inner_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='snippets') {
        v_connTabControl.tag.createQueryTab();
      }
      else if (v_connTabControl.selectedTab.tag.mode=='snippets') {
        var v_tabControl = v_connTabControl.selectedTab.tag.tabControl;
        v_tabControl.tabList[v_tabControl.tabList.length - 1].elementLi.click();
      }


    },
    shortcut_remove_inner_tab: function() {
      console.log('ae')

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='snippets') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tabCloseSpan)
          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tabCloseSpan.click();
      }

    },
    shortcut_left_inner_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='snippets') {
        var v_tabControl = v_connTabControl.selectedTab.tag.tabControl;
        var v_actualIndex = v_tabControl.tabList.indexOf(v_tabControl.selectedTab);

        if (v_actualIndex == 0) //avoid triggering click on '+' tab
          v_tabControl.tabList[v_tabControl.tabList.length - 2].elementA.click();
        else
            v_tabControl.tabList[v_actualIndex - 1].elementA.click();
      }

    },
    shortcut_right_inner_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        var v_tabControl = v_connTabControl.selectedTab.tag.tabControl;
        var v_actualIndex = v_tabControl.tabList.indexOf(v_tabControl.selectedTab);

        if (v_actualIndex == v_tabControl.tabList.length - 2) //avoid triggering click on '+' tab
          v_tabControl.tabList[0].elementA.click();
        else
            v_tabControl.tabList[v_actualIndex + 1].elementA.click();
      }

    },
    shortcut_autocomplete: function(e) {
      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query' || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
          var v_editor = null;
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query') {
            v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
            autocomplete_start(v_editor,0,e, true);
          }
          else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
            v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor_input
            autocomplete_start(v_editor,1,e, true);
          }
        }
      }
    }
  }

  // Go over default shortcuts
  for (var default_code in v_default_shortcuts) {
    if (v_default_shortcuts.hasOwnProperty(default_code)) {
        var v_object = v_default_shortcuts[default_code];
        // Find corresponding user defined
        var v_found = false;

        for (var user_code in v_shortcut_object.shortcuts) {
          if (v_shortcut_object.shortcuts.hasOwnProperty(user_code)) {
             if ((default_code == user_code) && (v_current_os == v_shortcut_object.shortcuts[user_code]['os'])) {
               v_found = true;
               break
             }
          }
        }

        if (!v_found) {
          v_shortcut_object.shortcuts[default_code] = v_default_shortcuts[default_code][v_current_os]
          v_shortcut_object.shortcuts[default_code]['shortcut_code'] = default_code
        }
    }
  }

  for (var property in v_shortcut_object.shortcuts) {
    if (v_shortcut_object.shortcuts.hasOwnProperty(property)) {
        var v_object = v_shortcut_object.shortcuts[property];
        var v_button = document.getElementById(property);
        if (v_button)
          buildButtonText(v_object,v_button);
    }
  }

});

function buildButtonText(p_shortcut_object, p_button) {
  var v_text = '';
  if (p_shortcut_object.ctrl_pressed)
    v_text += 'Ctrl+';
  if (p_shortcut_object.shift_pressed)
    v_text += 'Shift+';
  if (p_shortcut_object.alt_pressed)
    v_text += 'Alt+';
  if (p_shortcut_object.meta_pressed)
    v_text += 'Meta+';
  p_button.innerHTML = v_text + p_shortcut_object.shortcut_key;

}

function startSetShortcut(p_button) {
  document.getElementById('div_shortcut_background_dark').style.display = 'block';
  p_button.style['z-index'] = 1002;
  v_shortcut_object.button = p_button;

  document.body.removeEventListener('keydown',v_keyBoardShortcuts);

  document.body.removeEventListener('keydown',setShortcutEvent);
  document.body.addEventListener('keydown',setShortcutEvent);

}

function setShortcutEvent(p_event) {
  p_event.preventDefault();
  p_event.stopPropagation();

  //16 - Shift
  //17 - Ctrl
  //18 - Alt
  //91 - Meta (Windows and Mac)

  if (p_event.keyCode==27) {
    finishSetShortcut();
    return;
  }

  if (p_event.keyCode == 16 || p_event.keyCode == 17 || p_event.keyCode == 18 || p_event.keyCode == 91)
    return;

  var v_shortcut_element = v_shortcut_object.shortcuts[v_shortcut_object.button.id];

  if (v_shortcut_element) {
    v_shortcut_element.ctrl_pressed = 0;
    v_shortcut_element.shift_pressed = 0;
    v_shortcut_element.alt_pressed = 0;
    v_shortcut_element.meta_pressed = 0;
    if (p_event.ctrlKey)
      v_shortcut_element.ctrl_pressed = 1;
    if (p_event.shiftKey)
      v_shortcut_element.shift_pressed = 1;
    if (p_event.altKey)
      v_shortcut_element.alt_pressed = 1;
    if (p_event.metaKey)
      v_shortcut_element.meta_pressed = 1;
    if (p_event.code.toUpperCase()!='SPACE')
      v_shortcut_element.shortcut_key = p_event.key.toUpperCase();
    else
      v_shortcut_element.shortcut_key = 'SPACE'
    buildButtonText(v_shortcut_element,v_shortcut_object.button);
  }

  finishSetShortcut();
}

function finishSetShortcut() {
  v_shortcut_object.button.style['z-index'] = 0;
  v_shortcut_object.button = null;
  document.getElementById('div_shortcut_background_dark').style.display = 'none';

  document.body.removeEventListener('keydown',setShortcutEvent);
  document.body.addEventListener('keydown',v_keyBoardShortcuts);
}

function checkShortcutPressed(p_event, p_shortcut_element) {
  if ((p_event.ctrlKey && p_shortcut_element.ctrl_pressed==0) || (!p_event.ctrlKey && p_shortcut_element.ctrl_pressed==1))
    return false;
  if ((p_event.shiftKey && p_shortcut_element.shift_pressed==0) || (!p_event.shiftKey && p_shortcut_element.shift_pressed==1))
    return false;
  if ((p_event.altKey && p_shortcut_element.alt_pressed==0) || (!p_event.altKey && p_shortcut_element.alt_pressed==1))
    return false;
  if ((p_event.metaKey && p_shortcut_element.meta_pressed==0) || (!p_event.metaKey && p_shortcut_element.meta_pressed==1))
    return false;
  if (p_event.key.toUpperCase() == p_shortcut_element.shortcut_key || p_event.code.toUpperCase() == p_shortcut_element.shortcut_key)
    return true;

  return false;
}


var v_keyBoardShortcuts = function(p_event) {

  //16 - Shift
  //17 - Ctrl
  //18 - Alt
  //91 - Meta (Windows and Mac)
  //27 - Esc

  if (p_event.keyCode == 16 || p_event.keyCode == 17 || p_event.keyCode == 18 || p_event.keyCode == 91 || p_event.keyCode == 27)
    return;

  for (var property in v_shortcut_object.shortcuts) {
    if (v_shortcut_object.shortcuts.hasOwnProperty(property)) {
        var v_element = v_shortcut_object.shortcuts[property];
        if (checkShortcutPressed(p_event,v_element)) {
          p_event.preventDefault();
          p_event.stopPropagation();
          var v_action = v_shortcut_object.actions[property];
          if (v_action)
            v_action(p_event);
        }
    }
  }
}

//Some keyboard shortcuts
document.body.addEventListener('keydown',v_keyBoardShortcuts);
