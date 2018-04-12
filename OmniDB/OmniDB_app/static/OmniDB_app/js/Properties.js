/// <summary>
/// Retrieving Properties.
/// </summary>
function getProperties(p_view, p_data) {

	var v_tab_tag = v_connTabControl.selectedTab.tag;
  v_tab_tag.divLoading.style.display = 'block';

	execAjax(p_view,
      JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_tab_id": v_connTabControl.selectedTab.id,
                      "p_data": p_data}),
			function(p_return) {

        v_tab_tag.gridProperties.loadData(p_return.v_data.properties);
				v_tab_tag.ddlEditor.setValue(p_return.v_data.ddl);
				v_tab_tag.ddlEditor.clearSelection();
				v_tab_tag.ddlEditor.gotoLine(0, 0, true);
        v_tab_tag.divLoading.style.display = 'none';
        v_tab_tag.gridPropertiesCleared = false;

			},
			function(p_return) {
        v_tab_tag.divLoading.style.display = 'none';
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
