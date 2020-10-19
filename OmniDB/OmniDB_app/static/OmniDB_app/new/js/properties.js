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

/// <summary>
/// Retrieving Properties.
/// </summary>
function getProperties(p_view, p_data) {

	var v_tab_tag = v_connTabControl.selectedTab.tag;
	$(v_tab_tag.divLoading).fadeIn(100);

	execAjax(p_view,
      JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_tab_id": v_connTabControl.selectedTab.id,
                      "p_data": p_data}),
			function(p_return) {

        v_tab_tag.gridProperties.loadData(p_return.v_data.properties);
				v_tab_tag.ddlEditor.setValue(p_return.v_data.ddl);
				v_tab_tag.ddlEditor.clearSelection();
				v_tab_tag.ddlEditor.gotoLine(0, 0, true);
				$(v_tab_tag.divLoading).fadeOut(100);
        v_tab_tag.gridPropertiesCleared = false;

			},
			function(p_return) {
				$(v_tab_tag.divLoading).fadeOut(100);
				if (p_return.v_data.password_timeout) {
					showPasswordPrompt(
						v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
						function() {
							getProperties(p_view, p_data);
						},
						null,
						p_return.v_data.message
					);
				}
				else {
					showError(p_return.v_data);
				}
			},
			'box',
			false);

}

/// <summary>
/// Clear property grid.
/// </summary>
function clearProperties() {
  var v_tab_tag = v_connTabControl.selectedTab.tag;
  if (!v_tab_tag.gridPropertiesCleared) {
    v_tab_tag.gridProperties.loadData([]);
    v_tab_tag.gridPropertiesCleared = true;

		v_tab_tag.ddlEditor.setValue('');
		v_tab_tag.ddlEditor.clearSelection();
		v_tab_tag.ddlEditor.gotoLine(0, 0, true);
  }
}
