/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

//Initializing shortcut buttons
$(function () {

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
    shortcut_previous_console_command: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
          getConsoleHistoryCommand('previous');
        }
      }
    },
    shortcut_next_console_command: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
          getConsoleHistoryCommand('next');
        }
      }
    },
    shortcut_indent: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query' || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console')
          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_indent.click();
      }

    },
    shortcut_explain: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query') {
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_explain.style.display!='none')
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_explain.click();
        }
      }

    },
    shortcut_analyze: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query') {
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_analyze.style.display!='none')
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.bt_analyze.click();
        }
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
    shortcut_new_outer_tab: function() {

      var v_tabControl = v_connTabControl;
      v_tabControl.tabList[v_tabControl.tabList.length - 1].elementLi.click();

    },
    shortcut_remove_inner_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='snippets') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tabCloseSpan)
          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tabCloseSpan.click();
      }

    },
    shortcut_remove_outer_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='website_outer')
        v_connTabControl.selectedTab.tag.tabCloseSpan.click();

    },
    shortcut_left_inner_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='snippets') {
        var v_tabControl = v_connTabControl.selectedTab.tag.tabControl;
        var v_actualIndex = v_tabControl.tabList.indexOf(v_tabControl.selectedTab);

        if (v_actualIndex == 0) //avoid triggering click on '+' tab
          v_tabControl.tabList[v_tabControl.tabList.length - 2].elementLi.click();
        else
            v_tabControl.tabList[v_actualIndex - 1].elementLi.click();
      }

    },
    shortcut_left_outer_tab: function() {

        var v_tabControl = v_connTabControl;
        var v_actualIndex = v_tabControl.tabList.indexOf(v_tabControl.selectedTab);

        if (v_actualIndex == 0) //avoid triggering click on '+' tab
          v_tabControl.tabList[v_tabControl.tabList.length - 2].elementLi.click();
        else
            v_tabControl.tabList[v_actualIndex - 1].elementLi.click();

    },
    shortcut_right_inner_tab: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection' || v_connTabControl.selectedTab.tag.mode=='snippets') {
        var v_tabControl = v_connTabControl.selectedTab.tag.tabControl;
        var v_actualIndex = v_tabControl.tabList.indexOf(v_tabControl.selectedTab);

        if (v_actualIndex == v_tabControl.tabList.length - 2) //avoid triggering click on '+' tab
          v_tabControl.tabList[0].elementLi.click();
        else
            v_tabControl.tabList[v_actualIndex + 1].elementLi.click();
      }

    },
    shortcut_right_outer_tab: function() {

      var v_tabControl = v_connTabControl;
      var v_actualIndex = v_tabControl.tabList.indexOf(v_tabControl.selectedTab);

      if (v_actualIndex == v_tabControl.tabList.length - 2) //avoid triggering click on '+' tab
        v_tabControl.tabList[0].elementLi.click();
      else
          v_tabControl.tabList[v_actualIndex + 1].elementLi.click();

    },
    shortcut_autocomplete: function() {

      if (v_connTabControl.selectedTab.tag.mode=='connection') {
        if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query' || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
          var v_editor = null;
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query') {
            v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
            autocomplete_start(v_editor,0);
          }
          else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
            v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor_input
            autocomplete_start(v_editor,1);
          }
        }
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
            v_action();
        }
    }
  }
}

//Some keyboard shortcuts
document.body.addEventListener('keydown',v_keyBoardShortcuts);
