/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Debug state
/// </summary>
var v_debugState = {
	Starting: 0,
	Ready: 1,
  Step: 2,
  Finished: 3
}

function startDebugging(p_node) {

  //console.log(p_node);
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  v_tab_tag.state = v_debugState.Starting;

  //Instantiate grid
  var columnProperties = [];
  var col = new Object();
  col.readOnly = true;
  col.title =  'Variable';
  columnProperties.push(col);
  var col = new Object();
  col.readOnly = true;
  col.title =  'Type';
  columnProperties.push(col);
  var col = new Object();
  col.readOnly = true;
  col.title =  'Value';
  columnProperties.push(col);
  v_tab_tag.div_result.innerHTML = '';

  v_tab_tag.ht = new Handsontable(v_tab_tag.div_result,
  {
    data: [],
    columns : columnProperties,
    colHeaders : true,
    rowHeaders : true,
    copyRowsLimit : 1000000000,
    copyColsLimit : 1000000000,
    manualColumnResize: true,
    fillHandle:false,
        cells: function (row, col, prop) {
        var cellProperties = {};
        if (row % 2 == 0)
        cellProperties.renderer = blueRenderer;
      else
        cellProperties.renderer = whiteRenderer;
        return cellProperties;
    }
  });






  v_tab_tag.database_index = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;

  var v_message_data = {
    v_db_index: v_tab_tag.database_index,
    v_state: v_tab_tag.state,
    v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
    v_function: p_node.tag.id
  }

  var v_context = {
    tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
    acked: false
  }
  v_context.tab_tag.context = v_context;

  sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Debug, v_message_data, false, v_context);

}

function stepDebug() {
  var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;
  if (v_state==v_debugState.Starting) {
    showAlert('Debugger still starting.');
  }
  else if (v_state==v_debugState.Step) {
    showAlert('Step in progress.');
  }
  else if (v_state==v_debugState.Finished) {
    showAlert('Function already finished.');
  }
  //Ready to step
  else {

    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.state = v_debugState.Step;

    var v_message_data = {
      v_db_index: v_tab_tag.database_index,
      v_state: v_tab_tag.state,
      v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id
    }

    var v_context = {
      tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
    }
    v_context.tab_tag.context = v_context;

    sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Debug, v_message_data, false, v_context);


  }
}

function debugResponse(p_message, p_context) {
  //console.log(p_message.v_data)
  p_context.tab_tag.state = p_message.v_data.v_state;

  var Range = ace.require('ace/range').Range;
  if (p_message.v_data.v_lineno) {
    if (p_context.tab_tag.markerId)
      p_context.tab_tag.editor.session.removeMarker(p_context.tab_tag.markerId);
    p_context.tab_tag.markerId = p_context.tab_tag.editor.session.addMarker(new Range(p_message.v_data.v_lineno+2,0,p_message.v_data.v_lineno+2,200),"editorMarker","fullLine");
  }

  if (p_message.v_data.v_variables) {
    p_context.tab_tag.ht.loadData(p_message.v_data.v_variables);


  }

  if (p_context.tab_tag.state==v_debugState.Finished)
    showAlert('Function finished.');
}
