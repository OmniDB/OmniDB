/*
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

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

/// <summary>
/// Terminal state
/// </summary>
var v_terminalState = {
	Idle: 0,
	Executing: 1,
	Ready: 2
}

function clearTerminal() {
  var v_tag = v_connTabControl.selectedTab.tag;
  v_tag.editor_console.clear();

}

function startTerminal(p_conn_id) {
  var v_tag = v_connTabControl.selectedTab.tag;
  var v_context = {
    tab_tag: v_tag,
    acked: false
  }
  v_tag.context = createContext(v_queryWebSocket,v_context);
	v_tag.editor_console.focus();
	v_tag.editor_console.write('Starting terminal...')
	v_tag.clear_terminal = true;
	terminalRun(true,p_conn_id,'stty rows ' + v_tag.editor_console.rows + ' cols ' + v_tag.editor_console.cols + '\n');
}

function terminalKey(p_key) {
	terminalRun(false,-1, p_key);
}

function terminalContextMenu(p_event) {
	var v_tag = v_connTabControl.selectedTab.tag;
	var v_option_list = [];

	v_option_list.push(
	{
		text: 'Adjust Terminal Dimensions',
		icon: 'fas cm-all fa-window-maximize',
		action: function() {
			terminalRun(false,-1,'stty rows ' + v_tag.editor_console.rows + ' cols ' + v_tag.editor_console.cols + '\n');
			setTimeout(function() {
				v_tag.editor_console.focus();
			},10);
		}
	});

	customMenu(
		{
			x:p_event.clientX+5,
			y:p_event.clientY+5
		},
		v_option_list,
		null);


}

function terminalRun(p_spawn = false, p_ssh_id = -1, p_query = '') {
  var v_tag = v_connTabControl.selectedTab.tag;
	v_tag.tempData = '';
  var v_content = p_query;

		v_tag.last_command = v_content;

    var v_message_data = {
      v_cmd : v_content,
      v_tab_id: v_tag.tab_id,
      v_db_index: null,
      v_spawn: p_spawn,
			v_ssh_id: p_ssh_id
    }

    var d = new Date,
    dformat = [(d.getMonth()+1).padLeft(),
               d.getDate().padLeft(),
               d.getFullYear()].join('/') +' ' +
              [d.getHours().padLeft(),
               d.getMinutes().padLeft(),
               d.getSeconds().padLeft()].join(':');

    sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Terminal, v_message_data, false, v_tag.context.code);

    v_tag.state = v_consoleState.Executing;

		if (p_spawn==true) {
	    setTimeout(function() {
	      if (!v_tag.context.context.acked) {
	        cancelTerminalTab(v_tag.context.context.tab_tag);
	      }
	    },20000);
		}
}

function terminalReturn(p_data,p_context) {
	terminalReturnRender(p_data,p_context);
}

function terminalReturnRender(p_message,p_context) {
	var v_tag = p_context.tab_tag;

	if (p_context.tab_tag.clear_terminal==true) {
		v_tag.editor_console.write('\x1b[H\x1b[2J');
		p_context.tab_tag.clear_terminal = false;
	}

  p_context.tab_tag.state = v_consoleState.Idle;

  v_tag.editor_console.write(p_message.v_data.v_data)
  //appendToEditor(v_tag.editor_console,p_message.v_data.v_data);

  //v_tag.query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
}
