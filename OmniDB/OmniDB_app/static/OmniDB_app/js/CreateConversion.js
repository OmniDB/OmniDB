/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function () {

	var v_fileref = document.createElement("link");
    v_fileref.setAttribute("rel", "stylesheet");
    v_fileref.setAttribute("type", "text/css");
    v_fileref.setAttribute("href", 'css/themes/' + v_theme_type + '.css');
    document.getElementsByTagName("head")[0].appendChild(v_fileref);

	var v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);

	getDatabaseList('sl_database1','div_select_db1');

});

/// <summary>
/// Retrieves database list.
/// </summary>
/// <param name="p_sel_id">Selection tag ID.</param>
/// <param name="p_div">Div.</param>
/// <param name="p_filter">Filtering a specific database technology.</param>
function getDatabaseList(p_sel_id,p_div) {

	execAjax('MainDB.aspx/GetDatabaseList',
			JSON.stringify({}),
			function(p_return) {
				
				document.getElementById(p_div).innerHTML = p_return.v_data.v_select_html;

				document.getElementById(p_div).childNodes[0].id = p_sel_id;
				$(document.getElementById(p_div).childNodes[0]).msDropDown();


			},
			null,
			'box');

}

function changeDatabase() {

}

/// <summary>
/// Retrieves a grid full of checkboxes to select conversion info.
/// </summary>
function conversionData() {
	execAjax('CreateConversion.aspx/ConversionData',
			JSON.stringify({"p_database_index": document.getElementById('sl_database1').value}),
			function(p_return) {

				v_tables = p_return.v_data.v_tables;

				document.getElementById('div_conversion_data').innerHTML = p_return.v_data.v_html;

				$('#div_execute').show();

				getDatabaseList('sl_database2','div_select_db2');

			},
			null,
			'box');

}

/// <summary>
/// Selects/Deselects all checkboxes in one column.
/// </summary>
/// <param name="p_element">Current checkbox element.</param>
/// <param name="p_mode">Mode.</param>
function changeAllCheckboxes(p_element,p_mode) {

	var v_sufix;

	if (p_mode==0)
		v_sufix = '_drop_records';
	else if (p_mode==1)
		v_sufix = '_create_table';
	else if (p_mode==2)
		v_sufix = '_transfer_data';
	else if (p_mode==3)
		v_sufix = '_create_pks';
	else if (p_mode==4)
		v_sufix = '_create_fks';
	else if (p_mode==5)
		v_sufix = '_create_uniques';
	else if (p_mode==6)
		v_sufix = '_create_indexes';

	for (var i = 0; i < v_tables.length; i++) {
		document.getElementById('cb_' + v_tables[i] + v_sufix).checked = p_element.checked;
	}

}

/// <summary>
/// Inserts conversion info into OmniDBs database.
/// </summary>
function startConversion() {

	var v_tables_data = [];

	for (var i = 0; i < v_tables.length; i++) {
		var v_table_data = {
			v_table: v_tables[i],
			v_drop_records: document.getElementById('cb_' + v_tables[i] + '_drop_records').checked,
			v_create_table: document.getElementById('cb_' + v_tables[i] + '_create_table').checked,
			v_transfer_data : document.getElementById('cb_' + v_tables[i] + '_transfer_data').checked,
			v_create_pks: document.getElementById('cb_' + v_tables[i] + '_create_pks').checked,
			v_create_fks: document.getElementById('cb_' + v_tables[i] + '_create_fks').checked,
			v_create_uniques: document.getElementById('cb_' + v_tables[i] + '_create_uniques').checked,
			v_create_indexes: document.getElementById('cb_' + v_tables[i] + '_create_indexes').checked,
			v_transferfilter: document.getElementById('txt_' + v_tables[i] + '_transferfilter').value
		};

		v_tables_data.push(v_table_data);
	}

	execAjax('CreateConversion.aspx/StartConversion',
			JSON.stringify({"p_src_index": document.getElementById('sl_database1').value, "p_dst_index": document.getElementById('sl_database2').value, "p_tables_data": v_tables_data}),
			function(p_return) {

				window.open("Conversions.aspx","_self");

			},
			null,
			'box');

}