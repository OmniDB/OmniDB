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
$(function() {

	var v_fileref = document.createElement("link");
    v_fileref.setAttribute("rel", "stylesheet");
    v_fileref.setAttribute("type", "text/css");
    v_fileref.setAttribute("href", 'css/themes/' + v_theme_type + '.css');
    document.getElementsByTagName("head")[0].appendChild(v_fileref);

	var v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);

	listConversions();

});

/// <summary>
/// Redirects to conversion creation page.
/// </summary>
function newConversion() {

	window.open("CreateConversion.aspx","_self");

}

/// <summary>
/// Retrieves and displays a list o conversions.
/// </summary>
function listConversions() {

	execAjax('Conversions.aspx/GetConversions',
			JSON.stringify({}),
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Source Connection';
				col.renderer = 'html';
				col.width = 200;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Target Connection';
				col.renderer = 'html';
				col.width = 200;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Start';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'End';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Progress';
				col.renderer = 'html';
				col.width = 100;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Status';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Comments';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Duration';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.width = 80;
				col.renderer = 'html';

				columnProperties.push(col);

				var v_div_result = document.getElementById('div_conv_list');

				if (v_div_result.innerHTML!='')
					v_conv_data.ht.destroy();

				if (v_conv_data==null)
				v_conv_data = new Object();
				v_conv_data.v_cellChanges = [];


				var container = v_div_result;
				v_conv_data.ht = new Handsontable(container,
												{
													licenseKey: 'non-commercial-and-evaluation',
													data: p_return.v_data.v_data,
													columns : columnProperties,
													colHeaders : true,
													manualColumnResize: true,
													maxRows: p_return.v_data.v_data.length,
										            cells: function (row, col, prop) {

													    var cellProperties = {};
													    if (p_return.v_data.v_data[row][5]=='E')
													    	cellProperties.renderer = greenHtmlRenderer;
													    else if (p_return.v_data.v_data[row][5]=='C')
													    	cellProperties.renderer = yellowHtmlRenderer;
													    else if (row % 2 == 0)
															cellProperties.renderer = blueHtmlRenderer;

														cellProperties.readOnly = true;

													    return cellProperties;

													}
												});

			},
			null,
			'box');

}

/// <summary>
/// Deletes a conversion.
/// </summary>
/// <param name="p_conv_id">Conversion ID.</param>
function deleteConversion(p_conv_id) {

	showConfirm('Are you sure you want to delete this conversion?',
				function() {

					var input = JSON.stringify({"p_conv_id": p_conv_id});

					execAjax('Conversions.aspx/DeleteConversion',
							input,
							function(p_return) {

								listConversions();

							});

				});

}

/// <summary>
/// Starts a conversion.
/// </summary>
/// <param name="p_conv_id">Conversion ID.</param>
function startConversion(p_conv_id) {

	showConfirm('Are you sure you want to start this conversion?',
				function() {

					var input = JSON.stringify({"p_conv_id": p_conv_id});

					execAjax('Conversions.aspx/StartConversion',
					input,
					function(p_return) {

						listConversions();
						showAlert('A background process was spawned to start the conversion.');

					});

				});

}

/// <summary>
/// Stops a conversion.
/// </summary>
/// <param name="p_conv_id">Conversion ID.</param>
function stopConversion(p_conv_id) {

	showConfirm('Are you sure you want to cancel this conversion?',
	            function() {

	            	var input = JSON.stringify({"p_conv_id": p_conv_id});

	            	execAjax('Conversions.aspx/StopConversion',
					input,
					function(p_return) {

						listConversions();
						showAlert('Conversion was canceled.');

					});

	            });

}

/// <summary>
/// Retrieves and displays window with detailed information about specific conversion.
/// </summary>
/// <param name="p_conv_id">Conversion ID.</param>
function conversionDetails(p_conv_id) {

	v_conv_data.v_conv_id = p_conv_id;

	document.getElementById('sel_details_mode').value = 0;

	var input = JSON.stringify({"p_conv_id": v_conv_data.v_conv_id,"p_mode": document.getElementById('sel_details_mode').value});

	execAjax('Conversions.aspx/GetConversionDetails',
			input,
			function(p_return) {

				$('#div_conv_details').show();

				var v_width = document.getElementById("div_box_details").offsetWidth;

				$('#div_conv_details_data').width(v_width*0.95 + 'px');

				var v_height  = window.innerHeight - $('#div_conv_details_data').offset().top - 120;
				document.getElementById('div_conv_details_data').style.height = v_height + "px";

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Table';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Drop Records';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Table';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Primary Key';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Foreign Keys';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Uniques';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Indexes';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Data';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Filter';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Total Records';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfered Records';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Progress';
				col.renderer = 'html';
				col.width = 100;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Rate';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Estimated Time';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Start';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer End';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Duration';
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_conv_details_data');

				document.getElementById('div_conv_num_items').innerHTML = p_return.v_data.v_data.length + ' items.'

				if (v_div_result.innerHTML!='')
					v_conv_data.ht_details.destroy();

				var container = v_div_result;
				v_conv_data.ht_details = new Handsontable(container,
														{
															licenseKey: 'non-commercial-and-evaluation',
															data: p_return.v_data.v_data,
															columns : columnProperties,
															colHeaders : true,
															manualColumnResize: true,
															maxRows: p_return.v_data.v_data.length,
										                    cells: function (row, col, prop) {

															    var cellProperties = {};
															    if (p_return.v_data.v_data.length>0) {

																	if (p_return.v_data.v_data[row][8]=='E')
																    	cellProperties.renderer = greenHtmlRenderer;
																    else if (row % 2 == 0)
										    							cellProperties.renderer = blueHtmlRenderer;

										    						cellProperties.readOnly = true;

																}

															    return cellProperties;

															}
														});

			},
			null,
			'box');

}

/// <summary>
/// Refreshes window with detailed information about specific conversion.
/// </summary>
function refreshConvDetails() {

	var input = JSON.stringify({"p_conv_id": v_conv_data.v_conv_id,"p_mode": document.getElementById('sel_details_mode').value});

	execAjax('Conversions.aspx/GetConversionDetails',
			input,
			function(p_return) {

				var columnProperties = [];

				var col = new Object();
				col.title =  'Table';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Drop Records';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Table';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Primary Key';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Foreign Keys';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Uniques';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Create Indexes';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Data';
				col.renderer = 'html';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Filter';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Total Records';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfered Records';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Progress';
				col.renderer = 'html';
				col.width = 100;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Rate';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Estimated Time';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Start';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer End';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Transfer Duration';
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_conv_details_data');

				document.getElementById('div_conv_num_items').innerHTML = p_return.v_data.v_data.length + ' items.'

				if (v_div_result.innerHTML!='')
					v_conv_data.ht_details.destroy();

				var container = v_div_result;
				v_conv_data.ht_details = new Handsontable(container,
														{
															licenseKey: 'non-commercial-and-evaluation',
															data: p_return.v_data.v_data,
															columns : columnProperties,
															colHeaders : true,
															manualColumnResize: true,
															maxRows: p_return.v_data.v_data.length,
										                    cells: function (row, col, prop) {

															    var cellProperties = {};

															    if (p_return.v_data.v_data.length>0) {

																	if (p_return.v_data.v_data[row][8]=='E')
																    	cellProperties.renderer = greenHtmlRenderer;
																    else if (row % 2 == 0)
										    							cellProperties.renderer = blueHtmlRenderer;

										    						cellProperties.readOnly = true;

																}

															    return cellProperties;

															}
														});

			},
			null,
			'box');

}

/// <summary>
/// Hides window with conversion details.
/// </summary>
function hideConvDetails() {

	$('#div_conv_details').hide();

}

/// <summary>
/// Retrieves and displays conversion log.
/// </summary>
/// <param name="p_conv_id">Conversion ID.</param>
function viewLog(p_conv) {

	var input = JSON.stringify({"p_conv_id": p_conv});

	execAjax('Conversions.aspx/GetConvLog',
			input,
			function(p_return) {

				if (v_logObject!=null)
				if (v_logObject.editor!=null) {
					 v_logObject.editor.destroy();
					 document.getElementById('txt_log').innerHTML = '';
				}

				var langTools = ace.require("ace/ext/language_tools");
				var v_editor = ace.edit('txt_log');
				v_editor.setTheme("ace/theme/" + v_editor_theme);
				v_editor.session.setMode("ace/mode/text");

				v_editor.setFontSize(Number(v_editor_font_size));

				v_editor.setOptions({enableBasicAutocompletion: true});

				document.getElementById('txt_log').onclick = function() {
			  		v_editor.focus();
			    };

				v_editor.setValue(p_return.v_data);

				v_editor.clearSelection();

				v_editor.setReadOnly(true);

				//Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
				v_editor.commands.bindKey("Cmd-,", null)
				v_editor.commands.bindKey("Ctrl-,", null)
				v_editor.commands.bindKey("Cmd-Delete", null)
				v_editor.commands.bindKey("Ctrl-Delete", null)

				v_logObject = new Object();
				v_logObject.editor = v_editor;

				$('#div_log').show();

			},
			null,
			'box');

}

/// <summary>
/// Hides conversion log.
/// </summary>
/// <param name="p_conv_id">Conversion ID.</param>
function hideLog() {

	$('#div_log').hide();

	v_logObject.editor.setValue('');

}
