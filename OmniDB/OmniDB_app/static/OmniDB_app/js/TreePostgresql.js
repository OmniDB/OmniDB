/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function tabSQLTemplate(p_tab_name, p_template, p_showTip=true) {
    v_connTabControl.tag.createQueryTab(p_tab_name);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(
        p_template);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(
        0, 0, true);

    if(p_showTip) {
      var v_instance = new Tooltip($(v_connTabControl.selectedTab.tag.tabControl.selectedLi),{
        title: 'Adjust command and run!',
        placement: "bottom",
        container: 'body',
        offset: 100
      });
      v_instance.show();
      window.setTimeout(function() {
          v_instance.dispose();
      }, 4000);
    }
}

function tabDataMining(node) {
    var v_name = 'Advanced Object Search';

    v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl
        .selectedTab.tag.tabControl.tabList.length - 1);

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
        '<span id="tab_title">' + v_name +
        '</span><span id="tab_stub"><img style="width: 16px;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i>',
        false,
        null,
        renameTab,
        null,
        null,
        true,
        function() {
            if (this.tag != null) {
                refreshHeights();
            }

            if (this.tag != null) {
                checkDataMiningStatus(this);
            }
        }
    );
    v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

    //Adding unique names to spans
    var v_tab_title_span = document.getElementById('tab_title');
    v_tab_title_span.id = 'tab_title_' + v_tab.id;

    var v_tab_loading_span = document.getElementById('tab_loading');
    v_tab_loading_span.id = 'tab_loading_' + v_tab.id;

    var v_tab_close_span = document.getElementById('tab_close');
    v_tab_close_span.id = 'tab_close_' + v_tab.id;

    v_tab_close_span.onclick = function(e) {
        var v_current_tab = v_tab;
        customMenu({
                x: e.clientX + 5,
                y: e.clientY + 5
            }, [{
                text: 'Confirm',
                icon: 'fas cm-all fa-check',
                action: function() {
                    removeTab(v_current_tab);
                }
            }, {
                text: 'Cancel',
                icon: 'fas cm-all fa-times',
                action: function() {}
            }],
            null);
    };

    var v_tab_check_span = document.getElementById('tab_check');
    v_tab_check_span.id = 'tab_check_' + v_tab.id;

    var v_tab_stub_span = document.getElementById('tab_stub');
    v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

    var v_html =
        "<div id='txt_query_" + v_tab.id +
        "' style=' width: 100%; height: 400px; border: 1px solid #c3c3c3;'></div>" +
        "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
        "<button id='bt_start_" + v_tab.id +
        "' class='bt_execute bt_icon_only' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block; vertical-align: middle;'><i class='fas fa-play fa-light'></i></button>" +
        "<button id='bt_cancel_" + v_tab.id +
        "' class='bt_red' title='Cancel' style='margin-bottom: 5px; margin-left: 5px; display: none; vertical-align: middle;' onclick='cancelSQL();'>Cancel</button>" +
        "<div id='div_query_info_" + v_tab.id +
        "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +

        "        <div id='query_result_tabs_" + v_tab.id + "'>" +
        "            <ul>" +
        "            <li id='query_result_tabs_" + v_tab.id +
        "_tab1'>Data</li>" +
        "			</ul>" +
        "			<div id='div_query_result_tabs_" + v_tab.id + "_tab1'>" +
        "<div id='div_result_" + v_tab.id +
        "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
        "			</div>";

    var v_div = document.getElementById('div_' + v_tab.id);
    v_div.innerHTML = v_html;

    var v_ = document.createElement('div');

    var v_containerDiv = document.getElementById('txt_query_' + v_tab.id);
    v_containerDiv.style.display = 'flex';
    v_containerDiv.className = 'query_info';
    v_containerDiv.style.flexDirection = 'column';
    v_containerDiv.style.overflow = 'auto';

    var v_filterHeader = document.createElement('h3');
    v_filterHeader.innerHTML = 'Text Filter';
    v_filterHeader.style.marginLeft = '10px';
    v_filterHeader.className = 'query_info';
    v_filterHeader.style.marginBottom = '0px';
    v_filterHeader.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_filterHeader);

    var v_filterContainerDiv = document.createElement('div');
    v_filterContainerDiv.style.display = 'flex';
    v_filterContainerDiv.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_filterContainerDiv);

    var v_inputFilter = document.createElement('input');
    v_inputFilter.type = 'text';
    v_inputFilter.placeholder = 'Type the pattern to be searched...';
    v_inputFilter.style.margin = '10px';
    v_inputFilter.style.flex = '1 0 auto';
    v_inputFilter.classList.add('data-mining-input-text');
    v_filterContainerDiv.appendChild(v_inputFilter);

    var v_divCase = document.createElement('div');
    v_divCase.style.margin = '10px';
    v_divCase.style.flex = '0 0 auto';
    v_filterContainerDiv.appendChild(v_divCase);

    var v_inputCase = document.createElement('input');
    v_inputCase.type = 'checkbox';
    v_inputCase.style.margin = '10px';
    v_inputCase.classList.add('data-mining-input-case');
    v_divCase.appendChild(v_inputCase);

    var v_spanCase = document.createElement('span');
    v_spanCase.innerHTML = 'Case-sensitive';
    v_spanCase.className = 'query_info';
    v_divCase.appendChild(v_spanCase);

    var v_divRegex = document.createElement('div');
    v_divRegex.style.margin = '10px';
    v_divRegex.style.flex = '0 0 auto';
    v_filterContainerDiv.appendChild(v_divRegex);

    var v_inputRegex = document.createElement('input');
    v_inputRegex.type = 'checkbox';
    v_inputRegex.style.margin = '10px';
    v_inputRegex.classList.add('data-mining-input-regex');
    v_divRegex.appendChild(v_inputRegex);

    /*v_inputRegex.addEventListener(
        'click',
        function(p_inputCase, p_spanCase, p_event) {
            p_inputCase.disabled = this.checked;

            if (this.checked) {
                p_spanCase.style.opacity = '0.5';
            } else {
                p_spanCase.style.opacity = '';
            }
        }.bind(v_inputRegex, v_inputCase, v_spanCase)
    );*/

    var v_spanRegex = document.createElement('span');
    v_spanRegex.innerHTML = 'Regular Expression';
    v_divRegex.appendChild(v_spanRegex);

    var v_optionsHeader = document.createElement('h3');
    v_optionsHeader.innerHTML = 'Categories Filter';
    v_optionsHeader.style.marginLeft = '10px';
    v_optionsHeader.style.marginBottom = '0px';
    v_optionsHeader.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_optionsHeader);

    var v_optionsContainerDiv = document.createElement('div');
    v_optionsContainerDiv.style.display = 'grid';
    v_optionsContainerDiv.style.gridTemplateColumns = '1fr 1fr 1fr 1fr';
    v_optionsContainerDiv.style.gridRowGap = '10px';
    v_optionsContainerDiv.style.gridColumnGap = '10px';
    v_optionsContainerDiv.style.justifyItems = 'start';
    v_optionsContainerDiv.style.boxSizing = 'border-box';
    v_optionsContainerDiv.style.padding = '10px';
    v_containerDiv.appendChild(v_optionsContainerDiv);

    if (parseInt(getMajorVersionPostgresql(node.tree.tag.version)) >= 10) {
      var v_optionList = [{
              'text': 'Data',
              'value': 1
          }, {
              'text': 'FK Name',
              'value': 2
          }, {
              'text': 'Function Definition',
              'value': 3
          }, {
              'text': 'Function Name',
              'value': 4
          }, {
              'text': 'Index Name',
              'value': 5
          }, {
              'text': 'Materialized View Column Name',
              'value': 6
          }, {
              'text': 'Materialized View Name',
              'value': 7
          }, {
              'text': 'PK Name',
              'value': 8
          }, {
              'text': 'Schema Name',
              'value': 9
          }, {
              'text': 'Sequence Name',
              'value': 10
          }, {
              'text': 'Table Column Name',
              'value': 11
          }, {
              'text': 'Table Name',
              'value': 12
          }, {
              'text': 'Trigger Name',
              'value': 13
          }, {
              'text': 'Trigger Source',
              'value': 14
          }, {
              'text': 'Unique Name',
              'value': 15
          }, {
              'text': 'View Column Name',
              'value': 16
          }, {
              'text': 'View Name',
              'value': 17
          }, {
              'text': 'Check Name',
              'value': 18
          }, {
              'text': 'Rule Name',
              'value': 19
          }, {
              'text': 'Rule Definition',
              'value': 20
          }, {
              'text': 'Inherited Table Name',
              'value': 21
          }, {
              'text': 'Partition Name',
              'value': 22
          }, {
              'text': 'Role Name',
              'value': 23
          }, {
              'text': 'Tablespace Name',
              'value': 24
          }, {
              'text': 'Extension Name',
              'value': 25
          }, {
              'text': 'FK Column Name',
              'value': 26
          }, {
              'text': 'PK Column Name',
              'value': 27
          }, {
              'text': 'Unique Column Name',
              'value': 28
          }, {
              'text': 'Index Column Name',
              'value': 29
          }, {
              'text': 'Check Definition',
              'value': 30
          }, {
              'text': 'Table Trigger Name',
              'value': 31
          }, {
              'text': 'Materialized View Definition',
              'value': 32
          }, {
              'text': 'View Definition',
              'value': 33
          }
      ];
    } else {
      var v_optionList = [{
              'text': 'Data',
              'value': 1
          }, {
              'text': 'FK Name',
              'value': 2
          }, {
              'text': 'Function Definition',
              'value': 3
          }, {
              'text': 'Function Name',
              'value': 4
          }, {
              'text': 'Index Name',
              'value': 5
          }, {
              'text': 'Materialized View Column Name',
              'value': 6
          }, {
              'text': 'Materialized View Name',
              'value': 7
          }, {
              'text': 'PK Name',
              'value': 8
          }, {
              'text': 'Schema Name',
              'value': 9
          }, {
              'text': 'Sequence Name',
              'value': 10
          }, {
              'text': 'Table Column Name',
              'value': 11
          }, {
              'text': 'Table Name',
              'value': 12
          }, {
              'text': 'Trigger Name',
              'value': 13
          }, {
              'text': 'Trigger Source',
              'value': 14
          }, {
              'text': 'Unique Name',
              'value': 15
          }, {
              'text': 'View Column Name',
              'value': 16
          }, {
              'text': 'View Name',
              'value': 17
          }, {
              'text': 'Check Name',
              'value': 18
          }, {
              'text': 'Rule Name',
              'value': 19
          }, {
              'text': 'Rule Definition',
              'value': 20
          }, {
              'text': 'Inherited Table Name',
              'value': 21
          }, {
              'text': 'Role Name',
              'value': 22
          }, {
              'text': 'Tablespace Name',
              'value': 23
          }, {
              'text': 'Extension Name',
              'value': 24
          }, {
              'text': 'FK Column Name',
              'value': 25
          }, {
              'text': 'PK Column Name',
              'value': 26
          }, {
              'text': 'Unique Column Name',
              'value': 27
          }, {
              'text': 'Index Column Name',
              'value': 28
          }, {
              'text': 'Check Definition',
              'value': 29
          }, {
              'text': 'Table Trigger Name',
              'value': 30
          }, {
              'text': 'Materialized View Definition',
              'value': 31
          }, {
              'text': 'View Definition',
              'value': 32
          }
      ];
    }

    var v_compare = function(a, b) {
        if (a.text < b.text) {
            return -1;
        } else if (a.text > b.text) {
            return 1;
        } else {
            return 0;
        }
    }

    v_optionList.sort(v_compare);

    var v_inputDataFilter = document.createElement('input');
    var v_dataFilterHeader = document.createElement('h3');

    for (var i = 0; i < v_optionList.length; i++) {
        var v_divOption = document.createElement('div');
        v_optionsContainerDiv.appendChild(v_divOption);

        var v_inputOption = document.createElement('input');
        v_inputOption.type = 'checkbox';
        v_inputOption.value = v_optionList[i].text;
        v_inputOption.classList.add('data-mining-input-option');
        v_divOption.appendChild(v_inputOption);

        if(v_optionList[i].text == 'Data') {
            v_inputOption.addEventListener(
                'click',
                function(p_inputDataFilter, p_dataFilterHeader, p_event) {
                    p_inputDataFilter.disabled = !this.checked;

                    if(!this.checked) {
                        p_dataFilterHeader.style.opacity = '0.5';
                    }
                    else {
                        p_dataFilterHeader.style.opacity = '';
                    }
                }.bind(v_inputOption, v_inputDataFilter, v_dataFilterHeader)
            );
        }

        var v_spanOption = document.createElement('span');
        v_spanOption.innerHTML = v_optionList[i].text;
        v_divOption.appendChild(v_spanOption);
    }

    var v_categoriesButtonsContainer = document.createElement('div');
    v_categoriesButtonsContainer.style.display = 'flex';
    v_categoriesButtonsContainer.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_categoriesButtonsContainer);

    var v_buttonSelectAllCategories = document.createElement('button');
    v_buttonSelectAllCategories.style.margin = '10px';
    v_buttonSelectAllCategories.innerHTML = 'Select All';

    v_buttonSelectAllCategories.addEventListener(
        'click',
        function(p_event) {
            var v_grandParent = this.parentElement.parentElement;

            var v_categoryList = v_grandParent.querySelectorAll(
                '.data-mining-input-option');

            for (var i = 0; i < v_categoryList.length; i++) {
                if (!v_categoryList[i].checked) {
                    v_categoryList[i].click();
                }
            }
        }
    );

    v_categoriesButtonsContainer.appendChild(v_buttonSelectAllCategories);

    var v_buttonUnselectAllCategories = document.createElement('button');
    v_buttonUnselectAllCategories.style.margin = '10px';
    v_buttonUnselectAllCategories.innerHTML = 'Unselect All';

    v_buttonUnselectAllCategories.addEventListener(
        'click',
        function(p_event) {
            var v_grandParent = this.parentElement.parentElement;

            var v_categoryList = v_grandParent.querySelectorAll(
                '.data-mining-input-option');

            for (var i = 0; i < v_categoryList.length; i++) {
                if (v_categoryList[i].checked) {
                    v_categoryList[i].click();
                }
            }
        }
    );

    v_categoriesButtonsContainer.appendChild(v_buttonUnselectAllCategories);

    var v_schemasHeader = document.createElement('h3');
    v_schemasHeader.innerHTML = 'Schemas Filter';
    v_schemasHeader.style.marginLeft = '10px';
    v_schemasHeader.style.marginBottom = '0px';
    v_schemasHeader.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_schemasHeader);

    var v_schemasContainerDiv = document.createElement('div');
    v_schemasContainerDiv.style.display = 'grid';
    v_schemasContainerDiv.style.gridTemplateColumns = '1fr 1fr 1fr 1fr 1fr';
    v_schemasContainerDiv.style.gridRowGap = '10px';
    v_schemasContainerDiv.style.gridColumnGap = '10px';
    v_schemasContainerDiv.style.justifyItems = 'start';
    v_schemasContainerDiv.style.boxSizing = 'border-box';
    v_schemasContainerDiv.style.padding = '10px';
    v_containerDiv.appendChild(v_schemasContainerDiv);

    execAjax('/get_schemas_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_schemasContainerDiv, p_return) {
            var v_schemaList = p_return.v_data;

            var v_compare = function(a, b) {
                if (a.v_name < b.v_name) {
                    return -1;
                } else if (a.v_name > b.v_name) {
                    return 1;
                } else {
                    return 0;
                }
            }

            v_schemaList.sort(v_compare);

            v_disconsiderSchemas = {
                'information_schema': 1,
                'omnidb': 1,
                'pg_catalog': 1,
                'pg_toast': 1
            }

            for (var i = 0; i < v_schemaList.length; i++) {
                if (!(v_schemaList[i].v_name in v_disconsiderSchemas) && (
                        v_schemaList[i].v_name.search(/pg.*temp.*/) == -1)) {
                    var v_divSchema = document.createElement('div');
                    p_schemasContainerDiv.appendChild(v_divSchema);

                    var v_inputSchema = document.createElement('input');
                    v_inputSchema.type = 'checkbox';
                    v_inputSchema.value = v_schemaList[i].v_name;
                    v_inputSchema.classList.add('data-mining-input-schema');
                    v_divSchema.appendChild(v_inputSchema);

                    var v_spanSchema = document.createElement('span');
                    v_spanSchema.innerHTML = v_schemaList[i].v_name;
                    v_divSchema.appendChild(v_spanSchema);
                }
            }
        }.bind(null, v_schemasContainerDiv),
        function(p_return) {
            showAlert(p_return.v_data);
        },
        'box',
        false
    );

    var v_schemasButtonsContainer = document.createElement('div');
    v_schemasButtonsContainer.style.display = 'flex';
    v_schemasButtonsContainer.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_schemasButtonsContainer);

    var v_buttonSelectAllSchemas = document.createElement('button');
    v_buttonSelectAllSchemas.style.margin = '10px';
    v_buttonSelectAllSchemas.innerHTML = 'Select All';

    v_buttonSelectAllSchemas.addEventListener(
        'click',
        function(p_event) {
            var v_grandParent = this.parentElement.parentElement;

            var v_schemaList = v_grandParent.querySelectorAll(
                '.data-mining-input-schema');

            for (var i = 0; i < v_schemaList.length; i++) {
                if (!v_schemaList[i].checked) {
                    v_schemaList[i].click();
                }
            }
        }
    );

    v_schemasButtonsContainer.appendChild(v_buttonSelectAllSchemas);

    var v_buttonUnselectAllSchemas = document.createElement('button');
    v_buttonUnselectAllSchemas.style.margin = '10px';
    v_buttonUnselectAllSchemas.innerHTML = 'Unselect All';

    v_buttonUnselectAllSchemas.addEventListener(
        'click',
        function(p_event) {
            var v_grandParent = this.parentElement.parentElement;

            var v_schemaList = v_grandParent.querySelectorAll(
                '.data-mining-input-schema');

            for (var i = 0; i < v_schemaList.length; i++) {
                if (v_schemaList[i].checked) {
                    v_schemaList[i].click();
                }
            }
        }
    );

    v_schemasButtonsContainer.appendChild(v_buttonUnselectAllSchemas);

    v_dataFilterHeader.innerHTML = 'Data Category Filter';
    v_dataFilterHeader.style.opacity = '0.5'
    v_dataFilterHeader.style.marginLeft = '10px';
    v_dataFilterHeader.style.marginBottom = '0px';
    v_dataFilterHeader.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_dataFilterHeader);

    var v_dataFilterContainerDiv = document.createElement('div');
    v_dataFilterContainerDiv.style.display = 'flex';
    v_dataFilterContainerDiv.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_dataFilterContainerDiv);

    v_inputDataFilter.type = 'text';
    v_inputDataFilter.disabled = true;
    v_inputDataFilter.placeholder = 'Type the filter to be applied to data category...';
    v_inputDataFilter.style.margin = '10px';
    v_inputDataFilter.style.flex = '1 0 auto';
    v_inputDataFilter.classList.add('data-mining-data-input-text');
    v_dataFilterContainerDiv.appendChild(v_inputDataFilter);

    var v_buttonStart = document.getElementById('bt_start_' + v_tab.id);

    v_buttonStart.addEventListener(
        'click',
        function(p_event) {
            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state != v_queryState.Idle) {
        		showAlert('Tab with activity in progress.');
        	}
            else {
                var v_parent = this.parentElement;

                var v_data = {
                    text: '',
                    regex: false,
                    caseSensitive: false,
                    categoryList: [],
                    schemaList: [],
                    dataCategoryFilter: ''
                };

                var v_inputFilter = v_parent.querySelector('.data-mining-input-text');

                if (v_inputFilter != null) {
                    v_data.text = v_inputFilter.value;
                }

                if (v_data.text.trim() == '') {
                    showAlert('Please, provide a string in order to search.');
                    return;
                }

                var v_inputCase = v_parent.querySelector('.data-mining-input-case');

                if (v_inputCase != null) {
                    v_data.caseSensitive = v_inputCase.checked;
                }

                var v_inputRegex = v_parent.querySelector('.data-mining-input-regex');

                if (v_inputRegex != null) {
                    v_data.regex = v_inputRegex.checked;
                }

                var v_categoryList = v_parent.querySelectorAll('.data-mining-input-option');

                for (var i = 0; i < v_categoryList.length; i++) {
                    if (v_categoryList[i].checked) {
                        v_data.categoryList.push(v_categoryList[i].value);

                        if (v_categoryList[i].value == 'Data') {
                            var v_dataInputFilter = v_parent.querySelector('.data-mining-data-input-text');

                            if (v_dataInputFilter != null) {
                                v_data.dataCategoryFilter = v_dataInputFilter.value;
                            }
                        }
                    }
                }

                if (v_data.categoryList.length == 0) {
                    showAlert('Please, select at least one category to search.');
                    return;
                }

                var v_schemaList = v_parent.querySelectorAll('.data-mining-input-schema');

                for (var i = 0; i < v_schemaList.length; i++) {
                    if (v_schemaList[i].checked) {
                        v_data.schemaList.push(v_schemaList[i].value);
                    }
                }

                if (v_data.schemaList.length == 0) {
                    showAlert('Please, select at least one schema to search.');
                    return;
                }

                if (v_data.categoryList.indexOf('Data') != -1) {
                    showConfirm(
                        'You have selected the category "Data". Please, be aware that it can consume a considerable amount of time, depending on selected schemas size. Do you want to proceed?',
                        function(p_data) {
                            queryDataMining(p_data);
                        }.bind(null, v_data)
                    );
                } else {
                    queryDataMining(v_data);
                }
            }
        }
    );

    var v_curr_tabs = createTabControl('query_result_tabs_' + v_tab.id, 0, null);

    var v_tab_db_id = null;

    var v_tag = {
        tab_id: v_tab.id,
        mode: 'data_mining',
        editorDivId: 'txt_query_' + v_tab.id,
        query_info: document.getElementById('div_query_info_' + v_tab.id),
        div_result: document.getElementById('div_result_' + v_tab.id),
        div_notices: document.getElementById('div_notices_' + v_tab.id),
        div_count_notices: document.getElementById(
            'query_result_tabs_count_notices_' + v_tab.id),
        sel_filtered_data: document.getElementById('sel_filtered_data_' +
            v_tab.id),
        sel_export_type: document.getElementById('sel_export_type_' + v_tab
            .id),
        tab_title_span: v_tab_title_span,
        tab_loading_span: v_tab_loading_span,
        tab_close_span: v_tab_close_span,
        tab_check_span: v_tab_check_span,
        tab_stub_span: v_tab_stub_span,
        bt_start: document.getElementById('bt_start_' + v_tab.id),
        bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
        state: 0,
        context: null,
        tabControl: v_connTabControl.selectedTab.tag.tabControl,
        queryTabControl: v_curr_tabs,
        currQueryTab: null,
        connTab: v_connTabControl.selectedTab,
        currDatabaseIndex: null,
        tab_db_id: v_tab_db_id
    };

    v_tab.tag = v_tag;

    var v_selectDataTabFunc = function() {
        v_curr_tabs.selectTabIndex(0);
        v_tag.currQueryTab = 'data';
        refreshHeights();
    }

    var v_selectMessageTabFunc = function() {
        v_curr_tabs.selectTabIndex(1);
        v_tag.currQueryTab = 'message';
        v_tag.div_count_notices.style.display = 'none';
        refreshHeights();
    }

    v_tag.selectDataTabFunc = v_selectDataTabFunc;
    v_curr_tabs.tabList[0].elementLi.onclick = v_selectDataTabFunc;

    v_selectDataTabFunc();

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);

    v_add_tab.tag = {
        mode: 'add'
    }

    setTimeout(
        function() {
            refreshHeights();
        },
        10
    );

    var v_instance1 = new Tooltip($(v_connTabControl.selectedTab.tag.tabControl.selectedLi),{
      title: 'Adjust parameters and run!',
      placement: 'top',
      container: 'body'
    });
    v_instance1.show();
    window.setTimeout(function() {
        v_instance1.dispose();
    }, 4000);

    var v_instance2 = new Tooltip($('.data-mining-input-text'),{
      title: '<div style="text-align: left;">If Regular Expression is not selected, the pattern will work as follows:<br /><br />' +
      '- if it does not contain sql % wildcard, it will put your pattern between two % <br /><br />' +
      '- else it will consider your pattern as it is.</div>',
      placement: "bottom",
      container: 'body',
      html: true
    });

    var v_instance3 = new Tooltip($('.data-mining-data-input-text'),{
      title: '<div style="text-align: left;">If Data category is selected you can use it to filter search space and get a faster response.<br /><br />' +
      'If you want to filter you must fill it with a | separeted list of patterns that may use % wildcard.<br /><br />' +
      'For example: public.%mytable%|mysch%ema.% will search for data just in tables that match given patterns.</div>',
      placement: "top",
      container: 'body',
      html: true
    });

}

/// <summary>
/// Retrieving tree.
/// </summary>
function getTreePostgresql(p_div) {

    var context_menu = {
        'cm_server': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }]
        },
        'cm_databases': {
            elements: [{
                    text: 'Refresh',
                    icon: 'fas cm-all fa-sync-alt',
                    action: function(node) {
                        if (node.childNodes == 0)
                            refreshTreePostgresql(node);
                        else {
                            node.collapseNode();
                            node.expandNode();
                        }
                    }
                }, {
                    text: 'Create Database',
                    icon: 'fas cm-all fa-edit',
                    action: function(node) {
                        tabSQLTemplate('Create Database', node.tree
                            .tag.create_database);
                    }
                }
                , {
                    text: 'Doc: Databases',
                    icon: 'fas cm-all fa-globe-americas',
                    action: function(node) {
                        v_connTabControl.tag.createWebsiteTab(
                            'Documentation: Databases',
                            'https://www.postgresql.org/docs/' +
                            getMajorVersionPostgresql(node.tree.tag.version) +
                            '/static/managing-databases.html');
                    }
                }
            ]
        },
        'cm_database': {
            elements: [{
                text: 'Alter Database',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Database', node.tree.tag
                        .alter_database.replace(
                            '#database_name#', node.text));
                }
            }, {
                text: 'Drop Database',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Database', node.tree.tag
                        .drop_database.replace(
                            '#database_name#', node.text));
                }
            }, {
                text: 'Advanced Object Search',
                icon: 'fas cm-all fa-search',
                action: function(node) {
                  checkCurrentDatabase(node, true, function() {
                      tabDataMining(node);
                  }, function() {
                      node.collapseNode();
                  })
                }
            }]
        },
        'cm_tablespaces': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Tablespace',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Tablespace', node.tree
                        .tag.create_tablespace);
                }
            }, {
                text: 'Doc: Tablespaces',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Tablespaces',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/manage-ag-tablespaces.html'
                    );
                }
            }]
        },
        'cm_tablespace': {
            elements: [{
                text: 'Alter Tablespace',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Tablespace', node.tree
                        .tag.alter_tablespace.replace(
                            '#tablespace_name#', node.text)
                    );
                }
            }, {
                text: 'Drop Tablespace',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Tablespace', node.tree
                        .tag.drop_tablespace.replace(
                            '#tablespace_name#', node.text)
                    );
                }
            }]
        },
        'cm_roles': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Role',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Role', node.tree.tag
                        .create_role);
                }
            }, {
                text: 'Doc: Roles',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Roles',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/user-manag.html');
                }
            }]
        },
        'cm_role': {
            elements: [{
                text: 'Alter Role',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Role', node.tree.tag.alter_role
                        .replace('#role_name#', node.text));
                }
            }, {
                text: 'Drop Role',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Role', node.tree.tag.drop_role
                        .replace('#role_name#', node.text));
                }
            }]
        },
        'cm_extensions': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Extension',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Extension', node.tree
                        .tag.create_extension);
                }
            }, {
                text: 'Doc: Extensions',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Extensions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/extend-extensions.html');
                }
            }]
        },
        'cm_extension': {
            elements: [{
                text: 'Alter Extension',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Extension', node.tree
                        .tag.alter_extension.replace(
                            '#extension_name#', node.text));
                }
            }, {
                text: 'Drop Extension',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Role', node.tree.tag.drop_extension
                        .replace('#extension_name#', node.text)
                    );
                }
            }]
        },
        'cm_schemas': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Schema',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Schema', node.tree.tag
                        .create_schema);
                }
            }, {
                text: 'Doc: Schemas',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Schemas',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/ddl-schemas.html');
                }
            }]
        },
        'cm_schema': {
            elements: [{
                text: 'Render Graph',
                icon: 'fab cm-all fa-hubspot',
                action: function(node) {

                },
                submenu: {
                    elements: [{
                        text: 'Simple Graph',
                        icon: 'fab cm-all fa-hubspot',
                        action: function(node) {
                            v_connTabControl.tag.createGraphTab(
                                node.text)
                            drawGraph(false, node.text);
                        }
                    }, {
                        text: 'Complete Graph',
                        icon: 'fab cm-all fa-hubspot',
                        action: function(node) {
                            v_connTabControl.tag.createGraphTab(
                                node.text)
                            drawGraph(true, node.text);
                        }
                    }]
                }
            }, {
                text: 'Alter Schema',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Schema', node.tree.tag
                        .alter_schema.replace(
                            '#schema_name#', node.text));
                }
            }, {
                text: 'Drop Schema',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Schema', node.tree.tag
                        .drop_schema.replace(
                            '#schema_name#', node.text));
                }
            }]
        },
        'cm_tables': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Table (GUI)',
                icon: 'fas cm-all fa-plus-square',
                action: function(node) {
                    startAlterTable(true, 'new', null, node.parent
                        .text);
                }
            }, {
                text: 'Create Table (SQL)',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Table', node.tree.tag
                        .create_table.replace(
                            '#schema_name#', node.parent.text));
                }
            }, {
                text: 'Doc: Basics',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Table Basics',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/ddl-basics.html');
                }
            }, {
                text: 'Doc: Constraints',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Table Constraints',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/ddl-constraints.html');
                }
            }, {
                text: 'Doc: Modifying',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Modifying Tables',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/ddl-alter.html');
                }
            }]
        },
        'cm_table': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Data Actions',
                icon: 'fas cm-all fa-list',
                submenu: {
                    elements: [{
                        text: 'Query Data',
                        icon: 'fas cm-all fa-search',
                        action: function(node) {
                            TemplateSelectPostgresql(node.parent
                              .parent.text, node.text, 't');
                        }
                    }, {
                        text: 'Edit Data',
                        icon: 'fas cm-all fa-table',
                        action: function(node) {
                            startEditData(node.text,
                                node.parent.parent.text
                            );
                        }
                    }, {
                        text: 'Insert Record',
                        icon: 'fas cm-all fa-edit',
                        action: function(node) {
                            TemplateInsertPostgresql(node.parent
                              .parent.text, node.text);
                        }
                    }, {
                        text: 'Update Records',
                        icon: 'fas cm-all fa-edit',
                        action: function(node) {
                            TemplateUpdatePostgresql(node.parent
                              .parent.text, node.text);
                        }
                    }, {
                        text: 'Count Records',
                        icon: 'fas cm-all fa-sort-numeric-down',
                        action: function(node) {

                            var v_table_name = '';
                            if (node.parent.parent.parent
                                .parent != null)
                                v_table_name = node.parent
                                .parent.text + '.' +
                                node.text;
                            else
                                v_table_name = node.text;

                            v_connTabControl.tag.createQueryTab(
                                node.text);

                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    "-- Counting Records\nSELECT count(*) AS count\nFROM " +
                                    v_table_name + " t"
                                );
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            renameTabConfirm(
                                v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab,
                                node.text);

                            querySQL(0);
                        }
                    }, {
                        text: 'Delete Records',
                        icon: 'fas cm-all fa-times',
                        action: function(node) {
                          tabSQLTemplate(
                              'Delete Records',
                              node.tree.tag.delete
                              .replace(
                                  '#table_name#',
                                  node.parent.parent
                                  .text + '.' +
                                  node.text));
                        }
                    }, {
                        text: 'Truncate Table',
                        icon: 'fas cm-all fa-cut',
                        action: function(node) {
                            tabSQLTemplate(
                                'Truncate Table',
                                node.tree.tag.truncate
                                .replace(
                                    '#table_name#',
                                    node.parent.parent
                                    .text + '.' +
                                    node.text));
                        }
                    }]
                }
            }, {
                text: 'Table Actions',
                icon: 'fas cm-all fa-list',
                submenu: {
                    elements: [{
                        text: 'Vacuum Table',
                        icon: 'fas cm-all fa-broom',
                        action: function(node) {
                            tabSQLTemplate(
                                'Vacuum Table',
                                node.tree.tag.vacuum_table
                                .replace(
                                    '#table_name#',
                                    node.parent.parent
                                    .text + '.' +
                                    node.text));
                        }
                    }, {
                        text: 'Analyze Table',
                        icon: 'fas cm-all fa-search-plus',
                        action: function(node) {
                            tabSQLTemplate(
                                'Analyze Table',
                                node.tree.tag.analyze_table
                                .replace(
                                    '#table_name#',
                                    node.parent.parent
                                    .text + '.' +
                                    node.text));
                        }
                    }, {
                        text: 'Alter Table (GUI)',
                        icon: 'fas cm-all fa-table',
                        action: function(node) {
                            startAlterTable(true,
                                'alter', node.text,
                                node.parent.parent.text
                            );
                        }
                    }, {
                        text: 'Alter Table (SQL)',
                        icon: 'fas cm-all fa-edit',
                        action: function(node) {
                            tabSQLTemplate('Alter Table', node.tree.tag
                                .alter_table.replace(
                                    '#table_name#', node.parent.parent.text
                                    + '.' + node.text));
                        }
                    }, {
                        text: 'Drop Table',
                        icon: 'fas cm-all fa-times',
                        action: function(node) {
                            tabSQLTemplate('Drop Table',
                                node.tree.tag.drop_table
                                .replace(
                                    '#table_name#',
                                    node.parent.parent
                                    .text + '.' +
                                    node.text));
                        }
                    }]
                }
            }]
        },
        'cm_columns': {
            elements: [{
                text: 'Create Column',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Column', node.tree.tag
                        .create_column.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_column': {
            elements: [{
                text: 'Alter Column',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Column', node.tree.tag
                        .alter_column.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            /#column_name#/g, node.text));
                }
            }, {
                text: 'Drop Column',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Column', node.tree.tag
                        .drop_column.replace('#table_name#',
                            node.parent.parent.parent.parent
                            .text + '.' + node.parent.parent
                            .text).replace(/#column_name#/g,
                            node.text));
                }
            }]
        },
        'cm_pks': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Primary Key',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Primary Key', node.tree
                        .tag.create_primarykey.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_pk': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Drop Primary Key',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Primary Key', node.tree
                        .tag.drop_primarykey.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_fks': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Foreign Key',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Foreign Key', node.tree
                        .tag.create_foreignkey.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_fk': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Drop Foreign Key',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Foreign Key', node.tree
                        .tag.drop_foreignkey.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_uniques': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Unique',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Unique', node.tree.tag
                        .create_unique.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_unique': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Drop Unique',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Unique', node.tree.tag
                        .drop_unique.replace('#table_name#',
                            node.parent.parent.parent.parent
                            .text + '.' + node.parent.parent
                            .text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_indexes': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Index',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Index', node.tree.tag
                        .create_index.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Indexes',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Indexes',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/indexes.html');
                }
            }]
        },
        'cm_index': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Alter Index',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Index', node.tree.tag
                        .alter_index.replace('#index_name#',
                            node.parent.parent.parent.parent
                            .text + '.' +
                            node.text.replace(' (Unique)',
                                '').replace(' (Non Unique)',
                                '')));
                }
            }, {
                text: 'Drop Index',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Index', node.tree.tag.drop_index
                        .replace('#index_name#', node.parent
                            .parent.parent
                            .parent.text + '.' + node.text.replace(
                                ' (Unique)', '').replace(
                                ' (Non Unique)', '')));
                }
            }]
        },
        'cm_checks': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Check',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Check', node.tree.tag
                        .create_check.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_check': {
            elements: [{
                text: 'Drop Check',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Check', node.tree.tag.drop_check
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_excludes': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Exclude',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Exclude', node.tree.tag
                        .create_exclude.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_exclude': {
            elements: [{
                text: 'Drop Exclude',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Exclude', node.tree.tag
                        .drop_exclude
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_rules': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Rule',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Rule', node.tree.tag
                        .create_rule.replace('#table_name#',
                            node.parent.parent.parent.text +
                            '.' + node.parent.text));
                }
            }, {
                text: 'Doc: Rules',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Rules',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/rules.html');
                }
            }]
        },
        'cm_rule': {
            elements: [{
                text: 'Alter Rule',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Rule', node.tree.tag.alter_rule
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text).replace(
                            '#rule_name#', node.text));
                }
            }, {
                text: 'Edit Rule',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getRuleDefinitionPostgresql(node);
                }
            }, {
                text: 'Drop Rule',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Rule', node.tree.tag.drop_rule
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text).replace(
                            '#rule_name#', node.text));
                }
            }]
        },
        'cm_triggers': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                },
            }, {
                text: 'Create Trigger',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Trigger', node.tree.tag
                        .create_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Triggers',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Triggers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/trigger-definition.html');
                }
            }]
        },
        'cm_view_triggers': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                },
            }, {
                text: 'Create Trigger',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Trigger', node.tree.tag
                        .create_view_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Triggers',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Triggers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/trigger-definition.html');
                }
            }]
        },
        'cm_trigger': {
            elements: [{
                text: 'Alter Trigger',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Trigger', node.tree.tag
                        .alter_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }, {
                text: 'Enable Trigger',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Enable Trigger', node.tree.tag
                        .enable_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }, {
                text: 'Disable Trigger',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Disable Trigger', node.tree
                        .tag.disable_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }, {
                text: 'Drop Trigger',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Trigger', node.tree.tag
                        .drop_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }]
        },
        'cm_inheriteds': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Inherited',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Inherited', node.tree
                        .tag.create_inherited.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Partitioning',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Partitioning',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/ddl-partitioning.html');
                }
            }]
        },
        'cm_inherited': {
            elements: [{
                text: 'No Inherit Table',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('No Inherit Partition', node
                        .tree.tag.noinherit_partition.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#partition_name#', node.text));
                }
            }, {
                text: 'Drop Inherited',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Partition', node.tree.tag
                        .drop_partition.replace(
                            '#partition_name#', node.text));
                }
            }]
        },
        'cm_partitions': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Partition',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Partition', node.tree
                        .tag.create_partition.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Partitioning',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Partitioning',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/ddl-partitioning.html');
                }
            }]
        },
        'cm_partition': {
            elements: [{
                text: 'Detach Partition',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Detach Partition', node
                        .tree.tag.detach_partition.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#partition_name#', node.text));
                }
            }, {
                text: 'Drop Partition',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Partition', node.tree.tag
                        .drop_partition.replace(
                            '#partition_name#', node.text));
                }
            }]
        },
        'cm_functions': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Function',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Function', node.tree
                        .tag.create_function.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Functions',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-createfunction.html');
                }
            }]
        },
        'cm_function': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Select Function',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    TemplateSelectFunctionPostgresql(node.parent
                      .parent.text, node.text, node.tag.id);
                }
            }, {
                text: 'Edit Function',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getFunctionDefinitionPostgresql(node);
                }
            }, {
                text: 'Debug Function',
                icon: 'fas cm-all fa-bug',
                action: function(node) {
                    v_connTabControl.tag.createDebuggerTab(
                        node.text);
                    setupDebug(node, 'f');
                }
            }, {
                text: 'Drop Function',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Function', node.tree.tag
                        .drop_function.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_procedures': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Procedure',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Procedure', node.tree
                        .tag.create_procedure.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Procedures',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Procedures',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-createprocedure.html');
                }
            }]
        },
        'cm_procedure': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Call Procedure',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    TemplateCallProcedurePostgresql(node.parent
                      .parent.text, node.text, node.tag.id);
                }
            }, {
                text: 'Edit Procedure',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getProcedureDefinitionPostgresql(node);
                }
            }, {
                text: 'Debug Procedure',
                icon: 'fas cm-all fa-bug',
                action: function(node) {
                    v_connTabControl.tag.createDebuggerTab(
                        node.text);
                    setupDebug(node, 'p');
                }
            }, {
                text: 'Drop Procedure',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Procedure', node.tree.tag
                        .drop_procedure.replace(
                            '#procedure_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_triggerfunctions': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Trigger Function',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Trigger Function',
                        node.tree.tag.create_triggerfunction
                        .replace('#schema_name#', node.parent
                            .text));
                }
            }, {
                text: 'Doc: Trigger Functions',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Trigger Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/plpgsql-trigger.html');
                }
            }]
        },
        'cm_triggerfunction': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Edit Trigger Function',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getTriggerFunctionDefinitionPostgresql(node);
                }
            }, {
                text: 'Drop Trigger Function',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Trigger Function',
                        node.tree.tag.drop_triggerfunction.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_direct_triggerfunction': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Edit Trigger Function',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getTriggerFunctionDefinitionPostgresql(node);
                }
            }, {
                text: 'Drop Trigger Function',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Trigger Function',
                        node.tree.tag.drop_triggerfunction.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_sequences': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Sequence',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Sequence', node.tree
                        .tag.create_sequence.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Sequences',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Sequences',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-createsequence.html');
                }
            }]
        },
        'cm_sequence': {
            elements: [{
                text: 'Alter Sequence',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Sequence', node.tree.tag
                        .alter_sequence.replace(
                            '#sequence_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }, {
                text: 'Drop Sequence',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Sequence', node.tree.tag
                        .drop_sequence.replace(
                            '#sequence_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }]
        },
        'cm_views': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create View',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create View', node.tree.tag
                        .create_view.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Views',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Views',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-createview.html');
                }
            }]
        },
        'cm_view': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Query Data',
                icon: 'fas cm-all fa-search',
                action: function(node) {
                    TemplateSelectPostgresql(node.parent
                      .parent.text, node.text, 'v');
                }
            }, {
                text: 'Count Records',
                icon: 'fas cm-all fa-sort-numeric-down',
                action: function(node) {

                    var v_table_name = '';
                    if (node.parent.parent.parent
                        .parent != null)
                        v_table_name = node.parent
                        .parent.text + '.' +
                        node.text;
                    else
                        v_table_name = node.text;

                    v_connTabControl.tag.createQueryTab(
                        node.text);

                    v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab
                        .tag.editor.setValue(
                            "-- Counting Records\nSELECT count(*) AS count\nFROM " +
                            v_table_name + " t"
                        );
                    v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab
                        .tag.editor.clearSelection();
                    renameTabConfirm(
                        v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab,
                        node.text);

                    querySQL(0);
                }
            }, {
                text: 'Edit View',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getViewDefinitionPostgresql(node);
                }
            }, {
                text: 'Drop View',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop View', node.tree.tag.drop_view
                        .replace('#view_name#', node.parent
                            .parent.text + '.' + node.text)
                    );
                }
            }]
        },
        'cm_mviews': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Mat. View',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Materialized View',
                        node.tree.tag
                        .create_mview.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Mat. Views',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Materialized Views',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-creatematerializedview.html'
                    );
                }
            }]
        },
        'cm_mview': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Query Data',
                icon: 'fas cm-all fa-search',
                action: function(node) {
                    TemplateSelectPostgresql(node.parent
                      .parent.text, node.text, 'm');
                }
            }, {
                text: 'Count Records',
                icon: 'fas cm-all fa-sort-numeric-down',
                action: function(node) {

                    var v_table_name = '';
                    if (node.parent.parent.parent
                        .parent != null)
                        v_table_name = node.parent
                        .parent.text + '.' +
                        node.text;
                    else
                        v_table_name = node.text;

                    v_connTabControl.tag.createQueryTab(
                        node.text);

                    v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab
                        .tag.editor.setValue(
                            "-- Counting Records\nSELECT count(*) AS count\nFROM " +
                            v_table_name + " t"
                        );
                    v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab
                        .tag.editor.clearSelection();
                    renameTabConfirm(
                        v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab,
                        node.text);

                    querySQL(0);
                }
            }, {
                text: 'Edit Mat. View',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getMaterializedViewDefinitionPostgresql(
                        node);
                }
            }, {
                text: 'Refresh Mat. View',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Refresh Materialized View',
                        node.tree.tag.refresh_mview
                        .replace('#view_name#', node.parent
                            .parent.text + '.' + node.text)
                    );
                }
            }, {
                text: 'Analyze Mat. View',
                icon: 'fas cm-all fa-search-plus',
                action: function(node) {
                    tabSQLTemplate(
                        'Analyze Mat. View',
                        node.tree.tag.analyze_table
                        .replace(
                            '#table_name#',
                            node.parent.parent
                            .text + '.' +
                            node.text));
                }
            }, {
                text: 'Drop Mat. View',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Materialized View',
                        node.tree.tag.drop_mview
                        .replace('#view_name#', node.parent
                            .parent.text + '.' + node.text)
                    );
                }
            }]
        },
        'cm_physicalreplicationslots': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Slot',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate(
                        'Create Physical Replication Slot',
                        node.tree.tag
                        .create_physicalreplicationslot);
                }
            }, {
                text: 'Doc: Replication Slots',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Physical Replication Slots',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/warm-standby.html#streaming-replication-slots'
                    );
                }
            }]
        },
        'cm_physicalreplicationslot': {
            elements: [{
                text: 'Drop Slot',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate(
                        'Drop Physical Replication Slot',
                        node.tree.tag
                        .drop_physicalreplicationslot.replace(
                            '#slot_name#', node.text));
                }
            }]
        },
        'cm_logicalreplicationslots': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Slot',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate(
                        'Create Logical Replication Slot',
                        node.tree.tag
                        .create_logicalreplicationslot);
                }
            }, {
                text: 'Doc: Replication Slots',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Logical Replication Slots',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/logicaldecoding-explanation.html#logicaldecoding-replication-slots'
                    );
                }
            }]
        },
        'cm_logicalreplicationslot': {
            elements: [{
                text: 'Drop Slot',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate(
                        'Drop Logical Replication Slot',
                        node.tree.tag
                        .drop_logicalreplicationslot.replace(
                            '#slot_name#', node.text));
                }
            }]
        },
        'cm_publications': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Publication',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Publication', node.tree
                        .tag.create_publication);
                }
            }, {
                text: 'Doc: Publications',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Publications',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/logical-replication-publication.html'
                    );
                }
            }]
        },
        'cm_publication': {
            elements: [{
                text: 'Alter Publication',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Publication', node.tree
                        .tag.alter_publication
                        .replace('#pub_name#', node.text));
                }
            }, {
                text: 'Drop Publication',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Publication', node.tree
                        .tag.drop_publication
                        .replace('#pub_name#', node.text));
                }
            }]
        },
        'cm_pubtables': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Add Table',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Add Table', node.tree.tag.add_pubtable
                        .replace('#pub_name#', node.parent.text)
                    );
                }
            }]
        },
        'cm_pubtable': {
            elements: [{
                text: 'Drop Table',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Table', node.tree.tag.drop_pubtable
                        .replace('#pub_name#', node.parent.parent
                            .text)
                        .replace('#table_name#', node.text)
                    );
                }
            }]
        },
        'cm_subscriptions': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Subscription',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Subscription', node.tree
                        .tag.create_subscription);
                }
            }, {
                text: 'Doc: Subscriptions',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Subscriptions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/logical-replication-subscription.html'
                    );
                }
            }]
        },
        'cm_subscription': {
            elements: [{
                text: 'Alter Subscription',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Subscription', node.tree
                        .tag.alter_subscription
                        .replace('#sub_name#', node.text));
                }
            }, {
                text: 'Drop Subscription',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Subscription', node.tree
                        .tag.drop_subscription
                        .replace('#sub_name#', node.text));
                }
            }]
        },
        'cm_fdws': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Foreign Data Wrapper',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Foreign Data Wrapper', node.tree
                        .tag.create_fdw);
                }
            }, {
                text: 'Doc: Foreign Data Wrappers',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Foreign Data Wrappers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/postgres-fdw.html'
                    );
                }
            }]
        },
        'cm_fdw': {
            elements: [{
                text: 'Alter Foreign Data Wrapper',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Foreign Data Wrapper', node.tree
                        .tag.alter_fdw
                        .replace('#fdwname#', node.text));
                }
            }, {
                text: 'Drop Foreign Data Wrapper',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Foreign Data Wrapper', node.tree
                        .tag.drop_fdw
                        .replace('#fdwname#', node.text));
                }
            }]
        },
        'cm_foreign_servers': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Foreign Server',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Foreign Server', node.tree
                        .tag.create_foreign_server
                        .replace('#fdwname#', node.parent.text));
                }
            }]
        },
        'cm_foreign_server': {
            elements: [{
                text: 'Alter Foreign Server',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Foreign Server', node.tree
                        .tag.alter_foreign_server
                        .replace('#srvname#', node.text));
                }
            }, {
                text: 'Import Foreign Schema',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Import Foreign Schema', node.tree
                        .tag.import_foreign_schema
                        .replace('#srvname#', node.text));
                }
            }, {
                text: 'Drop Foreign Server',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Foreign Server', node.tree
                        .tag.drop_foreign_server
                        .replace('#srvname#', node.text));
                }
            }]
        },
        'cm_user_mappings': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create User Mapping',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create User Mapping', node.tree
                        .tag.create_user_mapping
                        .replace('#srvname#', node.parent.text));
                }
            }]
        },
        'cm_user_mapping': {
            elements: [{
                text: 'Alter User Mapping',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter User Mapping', node.tree
                        .tag.alter_user_mapping
                        .replace('#user_name#', node.text)
                        .replace('#srvname#', node.parent.parent.text));
                }
            }, {
                text: 'Drop User Mapping',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop User Mapping', node.tree
                        .tag.drop_user_mapping
                        .replace('#user_name#', node.text)
                        .replace('#srvname#', node.parent.parent.text));
                }
            }]
        },
        'cm_foreign_tables': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Foreign Table',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Foreign Table', node.tree
                        .tag.create_foreign_table
                        .replace('#schema_name#', node.parent.text));
                }
            }]
        },
        'cm_foreign_table': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Data Actions',
                icon: 'fas cm-all fa-list',
                submenu: {
                    elements: [{
                        text: 'Query Data',
                        icon: 'fas cm-all fa-search',
                        action: function(node) {
                            TemplateSelectPostgresql(node.parent
                              .parent.text, node.text, 'f');
                        }
                    }, {
                        text: 'Edit Data',
                        icon: 'fas cm-all fa-table',
                        action: function(node) {
                            startEditData(node.text,
                                node.parent.parent.text
                            );
                        }
                    }, {
                        text: 'Insert Record',
                        icon: 'fas cm-all fa-edit',
                        action: function(node) {
                            TemplateInsertPostgresql(node.parent
                              .parent.text, node.text);
                        }
                    }, {
                        text: 'Update Records',
                        icon: 'fas cm-all fa-edit',
                        action: function(node) {
                            TemplateUpdatePostgresql(node.parent
                              .parent.text, node.text);
                        }
                    }, {
                        text: 'Count Records',
                        icon: 'fas cm-all fa-sort-numeric-down',
                        action: function(node) {

                            var v_table_name = '';
                            if (node.parent.parent.parent
                                .parent != null)
                                v_table_name = node.parent
                                .parent.text + '.' +
                                node.text;
                            else
                                v_table_name = node.text;

                            v_connTabControl.tag.createQueryTab(
                                node.text);

                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    "-- Counting Records\nSELECT count(*) AS count\nFROM " +
                                    v_table_name + " t"
                                );
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            renameTabConfirm(
                                v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab,
                                node.text);

                            querySQL(0);
                        }
                    }, {
                        text: 'Delete Records',
                        icon: 'fas cm-all fa-times',
                        action: function(node) {
                          tabSQLTemplate(
                              'Delete Records',
                              node.tree.tag.delete
                              .replace(
                                  '#table_name#',
                                  node.parent.parent
                                  .text + '.' +
                                  node.text));
                        }
                    }, {
                        text: 'Truncate Foreign Table',
                        icon: 'fas cm-all fa-times',
                        action: function(node) {
                            tabSQLTemplate(
                                'Truncate Foreign Table',
                                node.tree.tag.truncate
                                .replace(
                                    '#table_name#',
                                    node.parent.parent
                                    .text + '.' +
                                    node.text));
                        }
                    }]
                }
            }, {
                text: 'Table Actions',
                icon: 'fas cm-all fa-list',
                submenu: {
                    elements: [{
                        text: 'Analyze Foreign Table',
                        icon: 'fas cm-all fa-table',
                        action: function(node) {
                            tabSQLTemplate(
                                'Analyze Foreign Table',
                                node.tree.tag.analyze_table
                                .replace(
                                    '#table_name#',
                                    node.parent.parent
                                    .text + '.' +
                                    node.text));
                        }
                    }, {
                        text: 'Alter Foreign Table',
                        icon: 'fas cm-all fa-edit',
                        action: function(node) {
                            tabSQLTemplate('Alter Foreign Table', node.tree
                                .tag.alter_foreign_table
                                .replace('#table_name#', node.parent.parent
                                  .text + '.' + node.text));
                        }
                    }, {
                        text: 'Drop Foreign Table',
                        icon: 'fas cm-all fa-times',
                        action: function(node) {
                            tabSQLTemplate('Drop Foreign Table', node.tree
                                .tag.drop_foreign_table
                                .replace('#table_name#', node.parent.parent
                                  .text + '.' + node.text));
                        }
                    }]
                }
            }]
        },
        'cm_foreign_columns': {
            elements: [{
                text: 'Create Foreign Column',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Foreign Column', node.tree.tag
                        .create_foreign_column.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_foreign_column': {
            elements: [{
                text: 'Alter Foreign Column',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Foreign Column', node.tree.tag
                        .alter_foreign_column.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            /#column_name#/g, node.text));
                }
            }, {
                text: 'Drop Foreign Column',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Foreign Column', node.tree.tag
                        .drop_foreign_column.replace('#table_name#',
                            node.parent.parent.parent.parent
                            .text + '.' + node.parent.parent
                            .text).replace(/#column_name#/g,
                            node.text));
                }
            }]
        },
        'cm_types': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Type',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Type', node.tree
                        .tag.create_type.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Types',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Types',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-createtype.html');
                }
            }]
        },
        'cm_type': {
            elements: [{
                text: 'Alter Type',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Type', node.tree.tag
                        .alter_type.replace(
                            '#type_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }, {
                text: 'Drop Type',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Type', node.tree.tag
                        .drop_type.replace(
                            '#type_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }]
        },
        'cm_domains': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Domain',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Create Domain', node.tree
                        .tag.create_domain.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Domains',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Domains',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-createdomain.html');
                }
            }]
        },
        'cm_domain': {
            elements: [{
                text: 'Alter Domain',
                icon: 'fas cm-all fa-edit',
                action: function(node) {
                    tabSQLTemplate('Alter Domain', node.tree.tag
                        .alter_domain.replace(
                            '#domain_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }, {
                text: 'Drop Domain',
                icon: 'fas cm-all fa-times',
                action: function(node) {
                    tabSQLTemplate('Drop Domain', node.tree.tag
                        .drop_domain.replace(
                            '#domain_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }]
        },
        'cm_refresh': {
            elements: [{
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }]
        }
    };
    var tree = createTree(p_div, '#fcfdfd', context_menu);
    v_connTabControl.selectedTab.tag.tree = tree;
    v_connTabControl.selectedTab.tag.divDetails.innerHTML =
        'Active database: <b>' + v_connTabControl.selectedTab.tag.selectedDatabase +
        '</b>';

    tree.nodeAfterOpenEvent = function(node) {
        refreshTreePostgresql(node);
    }

    tree.clickNodeEvent = function(node) {
        getPropertiesPostgresql(node);
    }

    tree.beforeContextMenuEvent = function(node, callback) {

        var v_elements = [];
        //Hooks
        if (v_connTabControl.tag.hooks.postgresqlTreeContextMenu.length>0) {
          for (var i=0; i<v_connTabControl.tag.hooks.postgresqlTreeContextMenu.length; i++)
            v_elements = v_elements.concat(v_connTabControl.tag.hooks.postgresqlTreeContextMenu[i](node));
        }

        var v_customCallback = function() {
          callback(v_elements);
        }
        checkCurrentDatabase(node, false, v_customCallback);
    }

    var node_server = tree.createNode('PostgreSQL', false,
        'node-postgresql', null, {
            type: 'server'
        }, 'cm_server');
    node_server.createChildNode('', true, 'node-spin',
        null, null);
    tree.drawTree();

}

function checkCurrentDatabase(p_node, p_complete_check, p_callback_continue,
    p_callback_stop) {
    if ((p_node.tag != null && p_node.tag.database != null && p_node.tag.database !=
            v_connTabControl.selectedTab.tag.selectedDatabase) && (
            p_complete_check || (!p_complete_check && p_node.tag.type !=
                'database'))) {

        showConfirm3(
            'This node belongs to another database, change active database to <b>' +
            p_node.tag.database + '</b>?',
            function() {
                var v_call_back_continue = p_callback_continue;
                var v_call_back_stop = p_callback_stop;

                checkBeforeChangeDatabase(
                    function() {
                        if (p_callback_stop)
                            p_callback_stop();
                    },
                    function() {
                        execAjax('/change_active_database/',
                            JSON.stringify({
                                "p_database_index": v_connTabControl
                                    .selectedTab.tag.selectedDatabaseIndex,
                                "p_tab_id": v_connTabControl.selectedTab
                                    .id,
                                "p_database": p_node.tag.database
                            }),
                            function(p_return) {

                                v_connTabControl.selectedTab.tag.divDetails
                                    .innerHTML =
                                    'Active database: <b>' + p_node
                                    .tag.database + '</b>';

                                v_connTabControl.selectedTab.tag.selectedDatabaseNode
                                    .clearNodeBold();
                                //searching new selected database node
                                var v_list_database_nodes = p_node.tree
                                    .childNodes[0].childNodes[0].childNodes;
                                for (var i = 0; i <
                                    v_list_database_nodes.length; i++
                                ) {
                                    if (p_node.tag.database ==
                                        v_list_database_nodes[i].text
                                        .replace(/"/g, '')) {
                                        v_list_database_nodes[i].setNodeBold();
                                        v_connTabControl.selectedTab
                                            .tag.selectedDatabase =
                                            p_node.tag.database;
                                        v_connTabControl.selectedTab
                                            .tag.selectedDatabaseNode =
                                            v_list_database_nodes[i];

                                        if (v_connTabControl.selectedTab.tag.selectedTitle!='')
                                  				v_connTabControl.selectedTab.tag.tabTitle.innerHTML = '<img src="/static/OmniDB_app/images/' + v_connTabControl.selectedTab.tag.selectedDBMS + '_medium.png"/> ' + v_connTabControl.selectedTab.tag.selectedTitle + ' - ' + v_connTabControl.selectedTab.tag.selectedDatabase;
                                  			else
                                  				v_connTabControl.selectedTab.tag.tabTitle.innerHTML = '<img src="/static/OmniDB_app/images/' + v_connTabControl.selectedTab.tag.selectedDBMS + '_medium.png"/> ' + v_connTabControl.selectedTab.tag.selectedDatabase;
                                    }

                                }
                                if (p_callback_continue)
                                    p_callback_continue();

                            },
                            function(p_return) {
                                nodeOpenError(p_return, node);
                            },
                            'box');
                    })


            },
            function() {
                if (p_callback_stop)
                    p_callback_stop();
            });

    } else
        p_callback_continue();
}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreePostgresql(p_node) {
    checkCurrentDatabase(p_node, true, function() {
        refreshTreePostgresqlConfirm(p_node);
    }, function() {
        p_node.collapseNode();
    })
}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function getPropertiesPostgresql(p_node) {
    checkCurrentDatabase(p_node, false, function() {
        getPropertiesPostgresqlConfirm(p_node);
    })
}

/// <summary>
/// Retrieving properties.
/// </summary>
/// <param name="node">Node object.</param>
function getPropertiesPostgresqlConfirm(node) {
    if (node.tag != undefined)
        if (node.tag.type == 'role') {
            getProperties('/get_properties_postgresql/', {
                p_schema: null,
                p_table: null,
                p_object: node.text,
                p_type: node.tag.type
            });
        } else if (node.tag.type == 'tablespace') {
        getProperties('/get_properties_postgresql/', {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'database') {
        getProperties('/get_properties_postgresql/', {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'extension') {
        getProperties('/get_properties_postgresql/', {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'schema') {
        getProperties('/get_properties_postgresql/', {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'table') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'sequence') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'view') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'mview') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'function') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.tag.id,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'procedure') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.tag.id,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'trigger') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'triggerfunction') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.tag.id,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'direct_triggerfunction') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.parent.text,
            p_table: null,
            p_object: node.tag.id,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'index') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text.replace(' (Non Unique)', '').replace(
                ' (Unique)', ''),
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'pk') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'foreign_key') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'unique') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'check') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'exclude') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'rule') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.parent.parent.text,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'foreign_table') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'user_mapping') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'foreign_server') {
        getProperties('/get_properties_postgresql/', {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'fdw') {
        getProperties('/get_properties_postgresql/', {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'type') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else if (node.tag.type == 'domain') {
        getProperties('/get_properties_postgresql/', {
            p_schema: node.parent.parent.text,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
        });
    } else {
        clearProperties();
    }

    //Hooks
    if (v_connTabControl.tag.hooks.postgresqlTreeNodeClick.length>0) {
      for (var i=0; i<v_connTabControl.tag.hooks.postgresqlTreeNodeClick.length; i++)
        v_connTabControl.tag.hooks.postgresqlTreeNodeClick[i](node);
    }
}

/// <summary>
/// Refreshing tree node confirm.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreePostgresqlConfirm(node) {
  if (node.tag != undefined)
    if (node.tag.type == 'schema_list') {
        getSchemasPostgresql(node);
    } else if (node.tag.type == 'table_list') {
        getTablesPostgresql(node);
    } else if (node.tag.type == 'table') {
        getColumnsPostgresql(node);
    } else if (node.tag.type == 'primary_key') {
        getPKPostgresql(node);
    } else if (node.tag.type == 'pk') {
        getPKColumnsPostgresql(node);
    } else if (node.tag.type == 'uniques') {
        getUniquesPostgresql(node);
    } else if (node.tag.type == 'unique') {
        getUniquesColumnsPostgresql(node);
    } else if (node.tag.type == 'foreign_keys') {
        getFKsPostgresql(node);
    } else if (node.tag.type == 'foreign_key') {
        getFKsColumnsPostgresql(node);
    } else if (node.tag.type == 'view_list') {
        getViewsPostgresql(node);
    } else if (node.tag.type == 'view') {
        getViewsColumnsPostgresql(node);
    } else if (node.tag.type == 'mview_list') {
        getMaterializedViewsPostgresql(node);
    } else if (node.tag.type == 'mview') {
        getMaterializedViewsColumnsPostgresql(node);
    } else if (node.tag.type == 'indexes') {
        getIndexesPostgresql(node);
    } else if (node.tag.type == 'index') {
        getIndexesColumnsPostgresql(node);
    } else if (node.tag.type == 'function_list') {
        getFunctionsPostgresql(node);
    } else if (node.tag.type == 'function') {
        getFunctionFieldsPostgresql(node);
    } else if (node.tag.type == 'procedure_list') {
        getProceduresPostgresql(node);
    } else if (node.tag.type == 'procedure') {
        getProcedureFieldsPostgresql(node);
    } else if (node.tag.type == 'sequence_list') {
        getSequencesPostgresql(node);
    } else if (node.tag.type == 'database_list') {
        getDatabasesPostgresql(node);
    } else if (node.tag.type == 'database') {
        getDatabaseObjectsPostgresql(node);
    } else if (node.tag.type == 'tablespace_list') {
        getTablespacesPostgresql(node);
    } else if (node.tag.type == 'role_list') {
        getRolesPostgresql(node);
    } else if (node.tag.type == 'extension_list') {
        getExtensionsPostgresql(node);
    } else if (node.tag.type == 'check_list') {
        getChecksPostgresql(node);
    } else if (node.tag.type == 'exclude_list') {
        getExcludesPostgresql(node);
    } else if (node.tag.type == 'rule_list') {
        getRulesPostgresql(node);
    } else if (node.tag.type == 'trigger_list') {
        getTriggersPostgresql(node);
    } else if (node.tag.type == 'triggerfunction_list') {
        getTriggerFunctionsPostgresql(node);
    } else if (node.tag.type == 'inherited_list') {
        getInheritedsPostgresql(node);
    } else if (node.tag.type == 'partition_list') {
        getPartitionsPostgresql(node);
    } else if (node.tag.type == 'server') {
        getTreeDetailsPostgresql(node);
    } else if (node.tag.type == 'physicalreplicationslot_list') {
        getPhysicalReplicationSlotsPostgresql(node);
    } else if (node.tag.type == 'logicalreplicationslot_list') {
        getLogicalReplicationSlotsPostgresql(node);
    } else if (node.tag.type == 'publication_list') {
        getPublicationsPostgresql(node);
    } else if (node.tag.type == 'subscription_list') {
        getSubscriptionsPostgresql(node);
    } else if (node.tag.type == 'publication_table_list') {
        getPublicationTablesPostgresql(node);
    } else if (node.tag.type == 'subscription_table_list') {
        getSubscriptionTablesPostgresql(node);
    } else if (node.tag.type == 'fdw_list') {
        getForeignDataWrappersPostgresql(node);
    } else if (node.tag.type == 'foreign_server_list') {
        getForeignServersPostgresql(node);
    } else if (node.tag.type == 'user_mapping_list') {
        getUserMappingsPostgresql(node);
    } else if (node.tag.type == 'foreign_table_list') {
        getForeignTablesPostgresql(node);
    } else if (node.tag.type == 'foreign_table') {
        getForeignColumnsPostgresql(node);
    } else if (node.tag.type == 'type_list') {
        getTypesPostgresql(node);
    } else if (node.tag.type == 'domain_list') {
        getDomainsPostgresql(node);
    }
    else {
      afterNodeOpenedCallbackPostgreSQL(node);
    }
}

function afterNodeOpenedCallbackPostgreSQL(node) {
  //Hooks
  if (v_connTabControl.tag.hooks.postgresqlTreeNodeOpen.length>0) {
    for (var i=0; i<v_connTabControl.tag.hooks.postgresqlTreeNodeOpen.length; i++)
      v_connTabControl.tag.hooks.postgresqlTreeNodeOpen[i](node);
  }
}

/// <summary>
/// Retrieving tree details.
/// </summary>
/// <param name="node">Node object.</param>
function getTreeDetailsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_tree_info_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            node.tree.contextMenu.cm_server.elements = []
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Refresh',
                icon: 'fas cm-all fa-sync-alt',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Monitoring',
                icon: 'fas cm-all fa-chart-line',
                action: function(node) {},
                submenu: {
                    elements: [{
                        text: 'Dashboard',
                        icon: 'fas cm-all fa-chart-line',
                        action: function(node) {
                            v_connTabControl.tag.createMonitorDashboardTab();
                            startMonitorDashboard();
                        }
                    }, {
                        text: 'Backends',
                        icon: 'fas cm-all fa-tasks',
                        action: function(node) {
                            v_connTabControl.tag.createMonitoringTab(
                                'Backends',
                                'SELECT * FROM pg_stat_activity', [{
                                    icon: 'fas cm-all fa-times',
                                    title: 'Terminate',
                                    action: 'postgresqlTerminateBackend'
                                }]);
                        }
                    }, {
                        text: 'Replication',
                        icon: 'fas cm-all fa-tasks',
                        action: function(node) {
                            v_connTabControl.tag.createMonitoringTab(
                                'Replication',
                                'SELECT * FROM pg_stat_replication',
                                null);
                        }
                    }]
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: PostgreSQL',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: PostgreSQL',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/');
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: SQL Language',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: SQL Language',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql.html');
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: SQL Commands',
                icon: 'fas cm-all fa-globe-americas',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: SQL Commands',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersionPostgresql(node.tree.tag.version) +
                        '/static/sql-commands.html');
                }
            });

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tree.tag = {
                version: p_return.v_data.v_database_return.version,
                //superuser: p_return.v_data.v_database_return.superuser,
                create_role: p_return.v_data.v_database_return.create_role,
                alter_role: p_return.v_data.v_database_return.alter_role,
                drop_role: p_return.v_data.v_database_return.drop_role,
                create_tablespace: p_return.v_data.v_database_return.create_tablespace,
                alter_tablespace: p_return.v_data.v_database_return.alter_tablespace,
                drop_tablespace: p_return.v_data.v_database_return.drop_tablespace,
                create_database: p_return.v_data.v_database_return.create_database,
                alter_database: p_return.v_data.v_database_return.alter_database,
                drop_database: p_return.v_data.v_database_return.drop_database,
                create_extension: p_return.v_data.v_database_return.create_extension,
                alter_extension: p_return.v_data.v_database_return.alter_extension,
                drop_extension: p_return.v_data.v_database_return.drop_extension,
                create_schema: p_return.v_data.v_database_return.create_schema,
                alter_schema: p_return.v_data.v_database_return.alter_schema,
                drop_schema: p_return.v_data.v_database_return.drop_schema,
                create_sequence: p_return.v_data.v_database_return.create_sequence,
                alter_sequence: p_return.v_data.v_database_return.alter_sequence,
                drop_sequence: p_return.v_data.v_database_return.drop_sequence,
                create_function: p_return.v_data.v_database_return.create_function,
                drop_function: p_return.v_data.v_database_return.drop_function,
                create_procedure: p_return.v_data.v_database_return.create_procedure,
                drop_procedure: p_return.v_data.v_database_return.drop_procedure,
                create_triggerfunction: p_return.v_data.v_database_return
                    .create_triggerfunction,
                drop_triggerfunction: p_return.v_data.v_database_return
                    .drop_triggerfunction,
                create_view: p_return.v_data.v_database_return.create_view,
                drop_view: p_return.v_data.v_database_return.drop_view,
                create_mview: p_return.v_data.v_database_return.create_mview,
                refresh_mview: p_return.v_data.v_database_return.refresh_mview,
                drop_mview: p_return.v_data.v_database_return.drop_mview,
                create_table: p_return.v_data.v_database_return.create_table,
                alter_table: p_return.v_data.v_database_return.alter_table,
                drop_table: p_return.v_data.v_database_return.drop_table,
                create_column: p_return.v_data.v_database_return.create_column,
                alter_column: p_return.v_data.v_database_return.alter_column,
                drop_column: p_return.v_data.v_database_return.drop_column,
                create_primarykey: p_return.v_data.v_database_return.create_primarykey,
                drop_primarykey: p_return.v_data.v_database_return.drop_primarykey,
                create_unique: p_return.v_data.v_database_return.create_unique,
                drop_unique: p_return.v_data.v_database_return.drop_unique,
                create_foreignkey: p_return.v_data.v_database_return.create_foreignkey,
                drop_foreignkey: p_return.v_data.v_database_return.drop_foreignkey,
                create_index: p_return.v_data.v_database_return.create_index,
                alter_index: p_return.v_data.v_database_return.alter_index,
                drop_index: p_return.v_data.v_database_return.drop_index,
                create_check: p_return.v_data.v_database_return.create_check,
                drop_check: p_return.v_data.v_database_return.drop_check,
                create_exclude: p_return.v_data.v_database_return.create_exclude,
                drop_exclude: p_return.v_data.v_database_return.drop_exclude,
                create_rule: p_return.v_data.v_database_return.create_rule,
                alter_rule: p_return.v_data.v_database_return.alter_rule,
                drop_rule: p_return.v_data.v_database_return.drop_rule,
                create_trigger: p_return.v_data.v_database_return.create_trigger,
                create_view_trigger: p_return.v_data.v_database_return.create_view_trigger,
                alter_trigger: p_return.v_data.v_database_return.alter_trigger,
                enable_trigger: p_return.v_data.v_database_return.enable_trigger,
                disable_trigger: p_return.v_data.v_database_return.disable_trigger,
                drop_trigger: p_return.v_data.v_database_return.drop_trigger,
                create_inherited: p_return.v_data.v_database_return.create_inherited,
                noinherit_partition: p_return.v_data.v_database_return.noinherit_partition,
                create_partition: p_return.v_data.v_database_return.create_partition,
                detach_partition: p_return.v_data.v_database_return.detach_partition,
                drop_partition: p_return.v_data.v_database_return.drop_partition,
                vacuum: p_return.v_data.v_database_return.vacuum,
                vacuum_table: p_return.v_data.v_database_return.vacuum_table,
                analyze: p_return.v_data.v_database_return.analyze,
                analyze_table: p_return.v_data.v_database_return.analyze_table,
                delete: p_return.v_data.v_database_return.delete,
                truncate: p_return.v_data.v_database_return.truncate,
                create_physicalreplicationslot: p_return.v_data.v_database_return
                    .create_physicalreplicationslot,
                drop_physicalreplicationslot: p_return.v_data.v_database_return
                    .drop_physicalreplicationslot,
                create_logicalreplicationslot: p_return.v_data.v_database_return
                    .create_logicalreplicationslot,
                drop_logicalreplicationslot: p_return.v_data.v_database_return
                    .drop_logicalreplicationslot,
                create_publication: p_return.v_data.v_database_return.create_publication,
                alter_publication: p_return.v_data.v_database_return.alter_publication,
                drop_publication: p_return.v_data.v_database_return.drop_publication,
                add_pubtable: p_return.v_data.v_database_return.add_pubtable,
                drop_pubtable: p_return.v_data.v_database_return.drop_pubtable,
                create_subscription: p_return.v_data.v_database_return.create_subscription,
                alter_subscription: p_return.v_data.v_database_return.alter_subscription,
                drop_subscription: p_return.v_data.v_database_return.drop_subscription,
                create_fdw: p_return.v_data.v_database_return.create_fdw,
                alter_fdw: p_return.v_data.v_database_return.alter_fdw,
                drop_fdw: p_return.v_data.v_database_return.drop_fdw,
                create_foreign_server: p_return.v_data.v_database_return.create_foreign_server,
                alter_foreign_server: p_return.v_data.v_database_return.alter_foreign_server,
                import_foreign_schema: p_return.v_data.v_database_return.import_foreign_schema,
                drop_foreign_server: p_return.v_data.v_database_return.drop_foreign_server,
                create_foreign_table: p_return.v_data.v_database_return.create_foreign_table,
                alter_foreign_table: p_return.v_data.v_database_return.alter_foreign_table,
                drop_foreign_table: p_return.v_data.v_database_return.drop_foreign_table,
                create_foreign_column: p_return.v_data.v_database_return.create_foreign_column,
                alter_foreign_column: p_return.v_data.v_database_return.alter_foreign_column,
                drop_foreign_column: p_return.v_data.v_database_return.drop_foreign_column,
                create_user_mapping: p_return.v_data.v_database_return.create_user_mapping,
                alter_user_mapping: p_return.v_data.v_database_return.alter_user_mapping,
                drop_user_mapping: p_return.v_data.v_database_return.drop_user_mapping,
                create_type: p_return.v_data.v_database_return.create_type,
                alter_type: p_return.v_data.v_database_return.alter_type,
                drop_type: p_return.v_data.v_database_return.drop_type,
                create_domain: p_return.v_data.v_database_return.create_domain,
                alter_domain: p_return.v_data.v_database_return.alter_domain,
                drop_domain: p_return.v_data.v_database_return.drop_domain
            }

            node.setText(p_return.v_data.v_database_return.version);

            var node_databases = node.createChildNode('Databases', false,
                'fas node-all fa-database node-database-list', {
                    type: 'database_list',
                    num_databases: 0
                }, 'cm_databases');
            node_databases.createChildNode('', true,
                'node-spin', null, null);
            var node_tablespaces = node.createChildNode('Tablespaces',
                false, 'fas node-all fa-folder-open node-tablespace-list', {
                    type: 'tablespace_list',
                    num_tablespaces: 0
                }, 'cm_tablespaces');
            node_tablespaces.createChildNode('', true,
                'node-spin', null, null);
            var node_roles = node.createChildNode('Roles', false,
                'fas node-all fa-users node-user-list', {
                    type: 'role_list',
                    num_roles: 0
                }, 'cm_roles');
            node_roles.createChildNode('', true,
                'node-spin', null, null);
            if (parseFloat(getMajorVersionPostgresql(node.tree.tag.version)) >= 9.4) {
                var node_replication = node.createChildNode(
                    'Replication Slots', false,
                    'fas node-all fa-sitemap node-repslot-list', {
                        type: 'replication',
                    }, null);
                var node_phyrepslots = node_replication.createChildNode(
                    'Physical Replication Slots', false,
                    'fas node-all fa-sitemap node-repslot-list', {
                        type: 'physicalreplicationslot_list',
                        num_repslots: 0
                    }, 'cm_physicalreplicationslots');
                node_phyrepslots.createChildNode('', true,
                    'node-spin', null, null);
                var node_logrepslots = node_replication.createChildNode(
                    'Logical Replication Slots', false,
                    'fas node-all fa-sitemap node-repslot-list', {
                        type: 'logicalreplicationslot_list',
                        num_repslots: 0
                    }, 'cm_logicalreplicationslots');
                node_logrepslots.createChildNode('', true,
                    'node-spin', null, null);
            }

            if (v_connTabControl.selectedTab.tag.firstTimeOpen) {
                v_connTabControl.selectedTab.tag.firstTimeOpen = false;
                //v_connTabControl.tag.createMonitorDashboardTab();
                //startMonitorDashboard();
            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);

}

/// <summary>
/// Retrieving database objects.
/// </summary>
/// <param name="node">Node object.</param>
function getDatabaseObjectsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_database_objects_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tag.database_data = p_return.v_data;

            var node_schemas = node.createChildNode('Schemas',
                false, 'fas node-all fa-layer-group node-schema-list', {
                    type: 'schema_list',
                    num_schemas: 0,
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, 'cm_schemas');
            node_schemas.createChildNode('', true,
                'node-spin', null, null);
            var node_extensions = node.createChildNode(
                'Extensions', false,
                'fas node-all fa-cubes node-extension-list', {
                    type: 'extension_list',
                    num_extensions: 0,
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, 'cm_extensions');
            node_extensions.createChildNode('', true,
                'node-spin', null, null);
            var node_fdws = node.createChildNode(
                'Foreign Data Wrappers', false,
                'fas node-all fa-cube node-fdw-list', {
                    type: 'fdw_list',
                    num_fdws: 0,
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, 'cm_fdws');
            node_fdws.createChildNode('', true,
                'node-spin', null, null);
            if (parseInt(getMajorVersionPostgresql(node.tree.tag.version)) >= 10) {
                var node_replication = node.createChildNode(
                    'Logical Replication', false,
                    'fas node-all fa-sitemap node-logrep', {
                        type: 'replication',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null);
                var node_publications = node_replication.createChildNode(
                    'Publications', false,
                    'fas node-all fa-arrow-alt-circle-down node-publication-list', {
                        type: 'publication_list',
                        num_pubs: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_publications');
                node_publications.createChildNode('', true,
                    'node-spin', null, null);
                var node_subscriptions = node_replication.createChildNode(
                    'Subscriptions', false,
                    'fas node-all fa-arrow-alt-circle-up node-subscription-list', {
                        type: 'subscription_list',
                        num_subs: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_subscriptions');
                node_subscriptions.createChildNode('', true,
                    'node-spin', null, null);
            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving databases.
/// </summary>
/// <param name="node">Node object.</param>
function getDatabasesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_databases_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Databases (' + p_return.v_data.length + ')');

            node.tag.num_databases = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-database node-database', {
                        type: 'database',
                        database: p_return.v_data[i].v_name.replace(
                            /"/g, '')
                    }, 'cm_database', null, false);

                if (v_connTabControl.selectedTab.tag.selectedDatabase ==
                    p_return.v_data[i].v_name.replace(/"/g, '')) {
                    v_node.setNodeBold();
                    v_connTabControl.selectedTab.tag.selectedDatabaseNode =
                        v_node;
                }

                v_node.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving tablespaces.
/// </summary>
/// <param name="node">Node object.</param>
function getTablespacesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);


    execAjax('/get_tablespaces_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tablespaces (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-folder node-tablespace', {
                        type: 'tablespace'
                    }, 'cm_tablespace', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving roles.
/// </summary>
/// <param name="node">Node object.</param>
function getRolesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_roles_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Roles (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-user node-user', {
                        type: 'role'
                    }, 'cm_role', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving roles.
/// </summary>
/// <param name="node">Node object.</param>
function getExtensionsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_extensions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Extensions (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-cubes node-extension', {
                        type: 'extension',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_extension', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving tables.
/// </summary>
/// <param name="node">Node object.</param>
function getTablesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false,'fas node-all fa-table node-' + p_return.v_data[i].v_icon, {
                        type: 'table',
                        has_primary_keys: p_return.v_data[i].v_has_primary_keys,
                        has_foreign_keys: p_return.v_data[i].v_has_foreign_keys,
                        has_uniques: p_return.v_data[i].v_has_uniques,
                        has_indexes: p_return.v_data[i].v_has_indexes,
                        has_checks: p_return.v_data[i].v_has_checks,
                        has_excludes: p_return.v_data[i].v_has_excludes,
                        has_rules: p_return.v_data[i].v_has_rules,
                        has_triggers: p_return.v_data[i].v_has_triggers,
                        has_partitions: p_return.v_data[i].v_has_partitions,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_table', null, false);

                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'table_field'
                    }, null, null, false);

            }
            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving tables.
/// </summary>
/// <param name="node">Node object.</param>
function getSchemasPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_schemas_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Schemas (' + p_return.v_data.length + ')');

            node.tag.num_schemas = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-layer-group node-schema', {
                        type: 'schema',
                        num_tables: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_schema', null, false);

                var node_tables = v_node.createChildNode('Tables', false,
                    'fas node-all fa-th node-table-list', {
                        type: 'table_list',
                        schema: p_return.v_data[i].v_name,
                        num_tables: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_tables', null, false);
                node_tables.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                var node_foreign_tables = v_node.createChildNode('Foreign Tables', false,
                    'fas node-all fa-th node-ftable-list', {
                        type: 'foreign_table_list',
                        schema: p_return.v_data[i].v_name,
                        num_tables: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_foreign_tables', null, false);
                node_foreign_tables.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                var node_sequences = v_node.createChildNode('Sequences',
                    false,
                    'fas node-all fa-sort-numeric-down node-sequence-list', {
                        type: 'sequence_list',
                        schema: p_return.v_data[i].v_name,
                        num_sequences: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_sequences', null, false);
                node_sequences.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                var node_views = v_node.createChildNode('Views', false,
                    'fas node-all fa-eye node-view-list', {
                        type: 'view_list',
                        schema: p_return.v_data[i].v_name,
                        num_views: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_views', null, false);
                node_views.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                if (parseFloat(getMajorVersionPostgresql(node.tree.tag.version)) >=
                    9.3) {
                    var node_views = v_node.createChildNode(
                        'Materialized Views', false,
                        'fas node-all fa-eye node-mview-list', {
                            type: 'mview_list',
                            schema: p_return.v_data[i].v_name,
                            num_views: 0,
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_mviews', null, false);
                    node_views.createChildNode('', true,
                        'node-spin', null,
                        null, null, false);
                }

                var node_functions = v_node.createChildNode('Functions',
                    false, 'fas node-all fa-cog node-function-list', {
                        type: 'function_list',
                        schema: p_return.v_data[i].v_name,
                        num_functions: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_functions', null, false);
                node_functions.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                var node_triggerfunctions = v_node.createChildNode(
                    'Trigger Functions', false,
                    'fas node-all fa-cog node-tfunction-list', {
                        type: 'triggerfunction_list',
                        schema: p_return.v_data[i].v_name,
                        num_triggerfunctions: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_triggerfunctions', null, false);
                node_triggerfunctions.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                if (parseInt(getMajorVersionPostgresql(node.tree.tag.version)) >= 11) {
                    var node_procedures = v_node.createChildNode('Procedures',
                        false, 'fas node-all fa-cog node-procedure-list', {
                            type: 'procedure_list',
                            schema: p_return.v_data[i].v_name,
                            num_procedures: 0,
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_procedures', null, false);
                    node_procedures.createChildNode('', true,
                        'node-spin', null, null,
                        null, false);
                }

                var node_types = v_node.createChildNode('Types',
                    false,
                    'fas node-all fa-square node-type-list', {
                        type: 'type_list',
                        schema: p_return.v_data[i].v_name,
                        num_types: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_types', null, false);
                node_types.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);

                var node_domains = v_node.createChildNode('Domains',
                    false,
                    'fas node-all fa-square node-domain-list', {
                        type: 'domain_list',
                        schema: p_return.v_data[i].v_name,
                        num_domains: 0,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_domains', null, false);
                node_domains.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving sequences.
/// </summary>
/// <param name="node">Node object.</param>
function getSequencesPostgresql(node) {
    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null, null, false);

    execAjax('/get_sequences_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            node.setText('Sequences (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_sequence_name,
                    false,
                    'fas node-all fa-sort-numeric-down node-sequence', {
                        type: 'sequence',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_sequence', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving views.
/// </summary>
/// <param name="node">Node object.</param>
function getViewsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_views_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Views (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-eye node-view', {
                        type: 'view',
                        has_rules: p_return.v_data[i].v_has_rules,
                        has_triggers: p_return.v_data[i].v_has_triggers,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_view', null, false);
                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'view_field'
                    }, null, null, false);
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);
        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving View Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getViewsColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_views_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, 'fas node-all fa-columns node-column', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                },
                null, null, false);

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, 'fas node-all fa-columns node-column', {
                        type: 'table_field',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

            }

            if (node.tag.has_rules) {
                v_node = node.createChildNode('Rules', false,
                    'fas node-all fa-lightbulb node-rule', {
                        type: 'rule_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_rules', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_triggers) {
                v_node = node.createChildNode('Triggers', false,
                    'fas node-all fa-bolt node-trigger', {
                        type: 'trigger_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_view_triggers', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving view definition.
/// </summary>
/// <param name="node">Node object.</param>
function getViewDefinitionPostgresql(node) {

    execAjax('/get_view_definition_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_view": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
            }

            v_div_result.innerHTML = '';

            maximizeEditor();

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving materialized views.
/// </summary>
/// <param name="node">Node object.</param>
function getMaterializedViewsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_mviews_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Materialized Views (' + p_return.v_data.length +
                ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-eye node-mview', {
                        type: 'mview',
                        has_indexes: p_return.v_data[i].v_has_indexes,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_mview', null, false);
                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'mview_field'
                    }, null, null, false);
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);
        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Materialized View Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getMaterializedViewsColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_mviews_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, 'fas node-all fa-columns node-column', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                },
                null, null, false);

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, 'fas node-all fa-columns node-column', {
                        type: 'table_field',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

            }

            if (node.tag.has_indexes) {
                v_node = node.createChildNode('Indexes', false,
                    'fas node-all fa-thumbtack node-index', {
                        type: 'indexes',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_indexes', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);

}

/// <summary>
/// Retrieving materialized view definition.
/// </summary>
/// <param name="node">Node object.</param>
function getMaterializedViewDefinitionPostgresql(node) {

    execAjax('/get_mview_definition_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_view": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
            }

            v_div_result.innerHTML = '';

            maximizeEditor();

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving columns.
/// </summary>
/// <param name="node">Node object.</param>
function getColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, 'fas node-all fa-columns node-column', {
                    type: 'column_list',
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, 'cm_columns', null, false);

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, 'fas node-all fa-columns node-column', {
                        type: 'table_field',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_column', null, false);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Nullable: ' + p_return.v_data[i].v_nullable,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

            }

            if (node.tag.has_primary_keys) {
                v_node = node.createChildNode('Primary Key', false,
                    'fas node-all fa-key node-pkey', {
                        type: 'primary_key',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_pks', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_foreign_keys) {
                v_node = node.createChildNode('Foreign Keys', false,
                    'fas node-all fa-key node-fkey', {
                        type: 'foreign_keys',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_fks', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_uniques) {
                v_node = node.createChildNode('Uniques', false,
                    'fas node-all fa-key node-unique', {
                        type: 'uniques',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_uniques', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_checks) {
                v_node = node.createChildNode('Checks', false,
                    'fas node-all fa-check-square node-check', {
                        type: 'check_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_checks', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_excludes) {
                v_node = node.createChildNode('Excludes', false,
                    'fas node-all fa-times-circle node-exclude', {
                        type: 'exclude_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_excludes', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_indexes) {
                v_node = node.createChildNode('Indexes', false,
                    'fas node-all fa-thumbtack node-index', {
                        type: 'indexes',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_indexes', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_rules) {
                v_node = node.createChildNode('Rules', false,
                    'fas node-all fa-lightbulb node-rule', {
                        type: 'rule_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_rules', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_triggers) {
                v_node = node.createChildNode('Triggers', false,
                    'fas node-all fa-bolt node-trigger', {
                        type: 'trigger_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_triggers', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);
            }

            if (node.tag.has_partitions) {
                v_node = node.createChildNode('Inherited Tables', false,
                    'fas node-all fa-table node-inherited', {
                        type: 'inherited_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_inheriteds', null, false);
                v_node.createChildNode('', false,
                    'node-spin', null, null,
                    null, false);

                if (parseInt(getMajorVersionPostgresql(node.tree.tag.version)) >= 10) {
                    v_node = node.createChildNode('Partitions', false,
                        'fas node-all fa-table node-partition', {
                            type: 'partition_list',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_partitions', null, false);
                    v_node.createChildNode('', false,
                        'node-spin', null,
                        null, null, false);
                }
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving PKs.
/// </summary>
/// <param name="node">Node object.</param>
function getPKPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_pk_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Primary Key (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0) {
                node.removeChildNodes();
                //node.contextMenu = 'cm_refresh'
            } else {
                //node.contextMenu = 'cm_pks'
            }

            if (p_return.v_data.length > 0) {
                v_node = node.createChildNode(p_return.v_data[0][0], false,
                    'fas node-all fa-key node-pkey', {
                        type: 'pk',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_pk');
                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'pk_field'
                    }, null);
            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving PKs Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getPKColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_pk_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_key": node.text,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node.createChildNode(p_return.v_data[i][0], false,
                    'fas node-all fa-columns node-column', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Uniques.
/// </summary>
/// <param name="node">Node object.</param>
function getUniquesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_uniques_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Uniques (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false,
                        'fas node-all fa-key node-unique', {
                            type: 'unique',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_unique', null, false);

                    v_node.createChildNode('', false,
                        'node-spin', {
                            type: 'unique_field'
                        }, null, null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Uniques Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getUniquesColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_uniques_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_unique": node.text,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node.createChildNode(p_return.v_data[i][0], false,
                        'fas node-all fa-columns node-column', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false
                    );

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Indexes.
/// </summary>
/// <param name="node">Node object.</param>
function getIndexesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_indexes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Indexes (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0] +
                        ' (' + p_return.v_data[i][1] + ')', false,
                        'fas node-all fa-thumbtack node-index', {
                            type: 'index',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_index', null, false);

                    v_node.createChildNode('', false,
                        'node-spin', {
                            type: 'index_field',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Indexes Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getIndexesColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_indexes_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_index": node.text.replace(' (Non Unique)', '').replace(
                ' (Unique)', ''),
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    node.createChildNode(p_return.v_data[i][0], false,
                        'fas node-all fa-columns node-column', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false
                    );

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving FKs.
/// </summary>
/// <param name="node">Node object.</param>
function getFKsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_fks_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Foreign Keys (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i][0],
                    false,
                    'fas node-all fa-key node-fkey', {
                        type: 'foreign_key',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_fk', null, false);
                v_node.createChildNode('Referenced Table: ' + p_return.v_data[
                        i][1], false,
                    'fas node-all fa-table node-table', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    },
                    null, null, false);
                v_node.createChildNode('Delete Rule: ' + p_return.v_data[
                        i][2], false,
                    'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Update Rule: ' + p_return.v_data[
                        i][3], false,
                    'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

                v_curr_fk = p_return.v_data[i][0];

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving FKs Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getFKsColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_fks_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_fkey": node.text,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.createChildNode('Referenced Table: ' + p_return.v_data[
                    0][0], false,
                'fas node-all fa-table node-table', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                },
                null, null, false);
            node.createChildNode('Delete Rule: ' + p_return.v_data[
                    0][1], false,
                'fas node-all fa-ellipsis-h node-bullet', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, null, null, false);
            node.createChildNode('Update Rule: ' + p_return.v_data[
                    0][2], false,
                'fas node-all fa-ellipsis-h node-bullet', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, null, null, false);

            for (i = 0; i < p_return.v_data.length; i++) {

                node.createChildNode(p_return.v_data[i][3] +
                    " <i class='fas node-all fa-arrow-right'></i> " +
                    p_return.v_data[i][4], false,
                    'fas node-all fa-columns node-column', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Checks.
/// </summary>
/// <param name="node">Node object.</param>
function getChecksPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_checks_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Checks (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false, 'fas node-all fa-check-square node-check', {
                            type: 'check',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_check', null, false);
                    v_node.createChildNode(p_return.v_data[i][1], false,
                        'fas node-all fa-edit node-check-value', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        },
                        null, null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Excludes.
/// </summary>
/// <param name="node">Node object.</param>
function getExcludesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_excludes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Excludes (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false, 'fas node-all fa-times-circle node-exclude', {
                            type: 'exclude',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_exclude', null, false);
                    v_node.createChildNode('Attributes: ' + p_return.v_data[
                            i][1],
                        false,
                        'fas node-all fa-ellipsis-h node-bullet', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);
                    v_node.createChildNode('Operators: ' + p_return.v_data[
                            i][2],
                        false,
                        'fas node-all fa-ellipsis-h node-bullet', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Rules.
/// </summary>
/// <param name="node">Node object.</param>
function getRulesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_rules_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Rules (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false, 'fas node-all fa-lightbulb node-rule', {
                            type: 'rule',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_rule', null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving rule definition.
/// </summary>
/// <param name="node">Node object.</param>
function getRuleDefinitionPostgresql(node) {

    execAjax('/get_rule_definition_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_rule": node.text,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
            }

            v_div_result.innerHTML = '';

            maximizeEditor();

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving Triggers.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggersPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_triggers_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Triggers (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    var v_node = node.createChildNode(p_return.v_data[i].v_name,
                        false, 'fas node-all fa-bolt node-trigger', {
                            type: 'trigger',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_trigger', null, true);
                    v_node.createChildNode('Enabled: ' + p_return.v_data[i]
                        .v_enabled, false,
                        'fas node-all fa-ellipsis-h node-bullet', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);

                    /*v_node.createChildNode('Function: ' + p_return.v_data[i]
                        .v_function, false,
                        'fas node-all fa-ellipsis-h node-bullet', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);*/

                    v_node.createChildNode(p_return.v_data[i].v_function, false,
                        'fas node-all fa-cog node-tfunction', {
                            type: 'direct_triggerfunction',
                            id: p_return.v_data[i].v_id,
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_direct_triggerfunction', null, true);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Partitions.
/// </summary>
/// <param name="node">Node object.</param>
function getInheritedsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_inheriteds_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Inherited Tables (' + p_return.v_data.length +
                ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false,
                        'fas node-all fa-table node-inherited', {
                            type: 'inherit',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_inherit', null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Partitions.
/// </summary>
/// <param name="node">Node object.</param>
function getPartitionsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_partitions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Partitions (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false,
                        'fas node-all fa-table node-partition', {
                            type: 'partition',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_partition', null, false);

                }

                node.drawChildNodes();

            }

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving functions.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_functions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Functions (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-cog node-function', {
                        type: 'function',
                        id: p_return.v_data[i].v_id,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_function', null, false);
                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'function_field'
                    }, null, null, false);

            }
            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving function fields.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionFieldsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_function_fields_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_function": node.tag.id,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                if (p_return.v_data[i].v_type == 'O')
                    v_node = node.createChildNode(p_return.v_data[i].v_name,
                        false, 'fas node-all fa-arrow-right node-function-field', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        },
                        null, null, false);
                else {
                    if (p_return.v_data[i].v_type == 'I')
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false, 'fas node-all fa-arrow-left node-function-field', {
                                database: v_connTabControl.selectedTab.tag.selectedDatabase
                            }, null, null, false);
                    else
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false,
                            'fas node-all fa-exchange-alt node-function-field', {
                                database: v_connTabControl.selectedTab.tag.selectedDatabase
                            }, null, null, false);
                }

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getDebugFunctionDefinitionPostgresql(node) {

    execAjax('/get_function_debug_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionDefinitionPostgresql(node) {

    execAjax('/get_function_definition_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
            }

            v_div_result.innerHTML = '';

            maximizeEditor();

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving procedures.
/// </summary>
/// <param name="node">Node object.</param>
function getProceduresPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_procedures_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Procedures (' + p_return.v_data.length + ')');

            node.tag.num_procedures = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-cog node-procedure', {
                        type: 'procedure',
                        id: p_return.v_data[i].v_id,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_procedure', null, false);
                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'procedure_field'
                    }, null, null, false);

            }
            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving procedure fields.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedureFieldsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_procedure_fields_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_procedure": node.tag.id,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tag.num_fields = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                if (p_return.v_data[i].v_type == 'O')
                    v_node = node.createChildNode(p_return.v_data[i].v_name,
                        false, 'fas node-all fa-arrow-right node-function-field', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        },
                        null, null, false);
                else {
                    if (p_return.v_data[i].v_type == 'I')
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false, 'fas node-all fa-arrow-left node-function-field', {
                                database: v_connTabControl.selectedTab.tag.selectedDatabase
                            }, null, null, false);
                    else
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false,
                            'fas node-all fa-exchange-alt node-function-field', {
                                database: v_connTabControl.selectedTab.tag.selectedDatabase
                            }, null, null, false);
                }

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving procedure definition.
/// </summary>
/// <param name="node">Node object.</param>
function getDebugProcedureDefinitionPostgresql(node) {

    execAjax('/get_procedure_debug_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_procedure": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving procedure definition.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedureDefinitionPostgresql(node) {

    execAjax('/get_procedure_definition_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_procedure": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
            }

            v_div_result.innerHTML = '';

            maximizeEditor();

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving trigger functions.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggerFunctionsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_triggerfunctions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Trigger Functions (' + p_return.v_data.length +
                ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                node.createChildNode(p_return.v_data[i].v_name, false,
                    'fas node-all fa-cog node-tfunction', {
                        type: 'triggerfunction',
                        id: p_return.v_data[i].v_id,
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_triggerfunction', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving trigger function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggerFunctionDefinitionPostgresql(node) {

    execAjax('/get_triggerfunction_definition_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
            }

            v_div_result.innerHTML = '';

            maximizeEditor();

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}

/// <summary>
/// Retrieving Physical Replication Slots.
/// </summary>
/// <param name="node">Node object.</param>
function getPhysicalReplicationSlotsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_physicalreplicationslots_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Physical Replication Slots (' + p_return.v_data.length +
                ')');

            node.tag.num_repslots = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-sitemap node-repslot', {
                        type: 'physicalreplicationslot',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_physicalreplicationslot', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Logical Replication Slots.
/// </summary>
/// <param name="node">Node object.</param>
function getLogicalReplicationSlotsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_logicalreplicationslots_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Logical Replication Slots (' + p_return.v_data.length +
                ')');

            node.tag.num_repslots = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-sitemap node-repslot', {
                        type: 'logicalreplicationslot',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_logicalreplicationslot', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Publications.
/// </summary>
/// <param name="node">Node object.</param>
function getPublicationsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_publications_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Publications (' + p_return.v_data.length + ')');

            node.tag.num_pubs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-arrow-alt-circle-down node-publication', {
                        type: 'publication',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_publication', null, false);
                v_node.createChildNode('All Tables: ' + p_return.v_data[i].v_alltables,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Insert: ' + p_return.v_data[i].v_insert,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Update: ' + p_return.v_data[i].v_update,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Delete: ' + p_return.v_data[i].v_delete,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Truncate: ' + p_return.v_data[i].v_truncate,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                if (p_return.v_data[i].v_alltables == 'False') {
                    v_tables = v_node.createChildNode('Tables',
                        false,
                        'fas node-all fa-th node-table-list', {
                            type: 'publication_table_list',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, 'cm_pubtables', null, false);
                    v_tables.createChildNode('', true,
                        'node-spin', null,
                        null, null, false);
                }

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Publication Tables.
/// </summary>
/// <param name="node">Node object.</param>
function getPublicationTablesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_publication_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_pub": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-table node-table', {
                        type: 'pubtable',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_pubtable', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Subscriptions.
/// </summary>
/// <param name="node">Node object.</param>
function getSubscriptionsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_subscriptions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Subscriptions (' + p_return.v_data.length + ')');

            node.tag.num_subs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-arrow-alt-circle-up node-subscription', {
                        type: 'subscription',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_subscription', null, false);
                v_node.createChildNode('Enabled: ' + p_return.v_data[i].v_enabled,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('ConnInfo: ' + p_return.v_data[i].v_conninfo,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_publications = v_node.createChildNode(
                    'Referenced Publications',
                    false, 'fas node-all fa-arrow-alt-circle-down node-publication', {
                        type: 'subpubs',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                tmp = p_return.v_data[i].v_publications.split(',')
                for (j = 0; j < tmp.length; j++) {
                    v_publications.createChildNode(tmp[j],
                        false,
                        'fas node-all fa-arrow-alt-circle-down node-publication', {
                            type: 'subpub',
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);
                }
                v_tables = v_node.createChildNode('Tables',
                    false,
                    'fas node-all fa-th node-table-list', {
                        type: 'subscription_table_list',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_tables.createChildNode('', true,
                    'node-spin', null, null,
                    null, false);
            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Subscription Tables.
/// </summary>
/// <param name="node">Node object.</param>
function getSubscriptionTablesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_subscription_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_sub": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-table node-table', {
                        type: 'subtable',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Foreign Data Wrappers.
/// </summary>
/// <param name="node">Node object.</param>
function getForeignDataWrappersPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_foreign_data_wrappers_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Foreign Data Wrappers (' + p_return.v_data.length + ')');

            node.tag.num_fdws = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

              v_node = node.createChildNode(p_return.v_data[i].v_name,
                  false, 'fas node-all fa-cube node-fdw', {
                      type: 'fdw',
                      database: v_connTabControl.selectedTab.tag.selectedDatabase
                  }, 'cm_fdw', null, false);
              v_node = v_node.createChildNode('Foreign Servers',
                  false, 'fas node-all fa-server node-server', {
                      type: 'foreign_server_list',
                      database: v_connTabControl.selectedTab.tag.selectedDatabase
                  }, 'cm_foreign_servers', null, false);
              v_node.createChildNode('', true,
                  'node-spin', null, null, null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Foreign Servers.
/// </summary>
/// <param name="node">Node object.</param>
function getForeignServersPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_foreign_servers_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_fdw": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Foreign Servers (' + p_return.v_data.length + ')');

            node.tag.num_foreign_servers = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

              v_node = node.createChildNode(p_return.v_data[i].v_name,
                  false, 'fas node-all fa-server node-server', {
                      type: 'foreign_server',
                      database: v_connTabControl.selectedTab.tag.selectedDatabase
                  }, 'cm_foreign_server', null, false);

              if (p_return.v_data[i].v_type != null) {
                  v_node.createChildNode('Type: ' + p_return.v_data[i].v_type,
                      true, 'fas node-all fa-ellipsis-h node-bullet', {
                          database: v_connTabControl.selectedTab.tag.selectedDatabase
                      }, null, null, false);
              }

              if (p_return.v_data[i].v_version != null) {
                  v_node.createChildNode('Version: ' + p_return.v_data[i].v_version,
                      true, 'fas node-all fa-ellipsis-h node-bullet', {
                          database: v_connTabControl.selectedTab.tag.selectedDatabase
                      }, null, null, false);
              }

              if (p_return.v_data[i].v_options != null) {
                v_options = p_return.v_data[i].v_options.split(',');
                if (v_options[0] != '') {
                  for (j = 0; j < v_options.length; j++) {
                      v_node.createChildNode(v_options[j],
                          true, 'fas node-all fa-ellipsis-h node-bullet', {
                              database: v_connTabControl.selectedTab.tag.selectedDatabase
                          }, null, null, false);
                  }
                }
              }

              v_node = v_node.createChildNode('User Mappings',
                  false, 'fas node-all fa-user-friends node-user', {
                      type: 'user_mapping_list',
                      database: v_connTabControl.selectedTab.tag.selectedDatabase
                  }, 'cm_user_mappings', null, false);
              v_node.createChildNode('', true,
                  'node-spin', null, null, null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving User Mappings.
/// </summary>
/// <param name="node">Node object.</param>
function getUserMappingsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_user_mappings_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_foreign_server": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('User Mappings (' + p_return.v_data.length + ')');

            node.tag.num_user_mappings = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

              v_node = node.createChildNode(p_return.v_data[i].v_name,
                  false, 'fas node-all fa-user-friends node-user', {
                      type: 'user_mapping',
                      database: v_connTabControl.selectedTab.tag.selectedDatabase
                  }, 'cm_user_mapping', null, false);

              if (p_return.v_data[i].v_options != null) {
                v_options = p_return.v_data[i].v_options.split(',');
                if (v_options[0] != '') {
                  for (j = 0; j < v_options.length; j++) {
                      v_node.createChildNode(v_options[j],
                          true, 'fas node-all fa-ellipsis-h node-bullet', {
                              database: v_connTabControl.selectedTab.tag.selectedDatabase
                          }, null, null, false);
                  }
                }
              }

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving foreign tables.
/// </summary>
/// <param name="node">Node object.</param>
function getForeignTablesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_foreign_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Foreign Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, 'fas node-all fa-table node-' + p_return.v_data[i].v_icon, {
                        type: 'foreign_table',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_foreign_table', null, false);

                v_node.createChildNode('', false,
                    'node-spin', {
                        type: 'foreign_table_field'
                    }, null, null, false);

            }
            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving columns.
/// </summary>
/// <param name="node">Node object.</param>
function getForeignColumnsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_foreign_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, 'fas node-all fa-columns node-column', {
                    type: 'foreign_column_list',
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, 'cm_foreign_columns', null, false);

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, 'fas node-all fa-columns node-column', {
                        type: 'foreign_table_field',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_foreign_column', null, false);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);
                v_node.createChildNode('Nullable: ' + p_return.v_data[i].v_nullable,
                    false, 'fas node-all fa-ellipsis-h node-bullet', {
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, null, null, false);

                if (p_return.v_data[i].v_options != null) {
                  v_options = p_return.v_data[i].v_options.split(',');
                  if (v_options[0] != '') {
                    for (j = 0; j < v_options.length; j++) {
                        v_node.createChildNode(v_options[j],
                            true, 'fas node-all fa-ellipsis-h node-bullet', {
                                database: v_connTabControl.selectedTab.tag.selectedDatabase
                            }, null, null, false);
                    }
                  }
                }

            }

            if (p_return.v_data[0].v_tableoptions != null) {
              v_options = p_return.v_data[0].v_tableoptions.split(',');
              if (v_options[0] != '') {
                for (j = 0; j < v_options.length; j++) {
                    node.createChildNode(v_options[j],
                        true, 'fas node-all fa-ellipsis-h node-bullet', {
                            database: v_connTabControl.selectedTab.tag.selectedDatabase
                        }, null, null, false);
                }
              }
            }

            node.createChildNode(p_return.v_data[0].v_server,
                true, 'fas node-all fa-server node-server', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, null, null, false);

            node.createChildNode(p_return.v_data[0].v_fdw,
                true, 'fas node-all fa-cube node-fdw', {
                    database: v_connTabControl.selectedTab.tag.selectedDatabase
                }, null, null, false);

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving types.
/// </summary>
/// <param name="node">Node object.</param>
function getTypesPostgresql(node) {
    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_types_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            node.setText('Types (' + p_return.v_data.length + ')');

            node.tag.num_types = p_return.v_data.length;

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_type_name,
                    false,
                    'fas node-all fa-square node-type', {
                        type: 'type',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_type', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving domains.
/// </summary>
/// <param name="node">Node object.</param>
function getDomainsPostgresql(node) {
    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    execAjax('/get_domains_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            node.setText('Domains (' + p_return.v_data.length + ')');

            node.tag.num_domains = p_return.v_data.length;

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_domain_name,
                    false,
                    'fas node-all fa-square node-domain', {
                        type: 'domain',
                        database: v_connTabControl.selectedTab.tag.selectedDatabase
                    }, 'cm_domain', null, false);

            }

            node.drawChildNodes();

            afterNodeOpenedCallbackPostgreSQL(node);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving SELECT SQL template.
/// </summary>
function TemplateSelectPostgresql(p_schema, p_table, p_kind) {

    execAjax('/template_select_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": p_table,
            "p_schema": p_schema,
            "p_kind": p_kind
        }),
        function(p_return) {
            v_connTabControl.tag.createQueryTab(
                p_schema + '.' + p_table);

            v_connTabControl.selectedTab
                .tag.tabControl.selectedTab
                .tag.editor.setValue(p_return.v_data.v_template);
            v_connTabControl.selectedTab
                .tag.tabControl.selectedTab
                .tag.editor.clearSelection();
            renameTabConfirm(
                v_connTabControl.selectedTab
                .tag.tabControl.selectedTab,
                p_schema + '.' + p_table);

            //minimizeEditor();

            querySQL(0);
        },
        function(p_return) {
            showError(p_return.v_data);
            return '';
        },
        'box',
        true);
}

/// <summary>
/// Retrieving INSERT SQL template.
/// </summary>
function TemplateInsertPostgresql(p_schema, p_table) {

    execAjax('/template_insert_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": p_table,
            "p_schema": p_schema
        }),
        function(p_return) {
          tabSQLTemplate(
              'Insert ' + p_schema + '.' + p_table,
              p_return.v_data.v_template);
        },
        function(p_return) {
            showError(p_return.v_data);
            return '';
        },
        'box',
        true);
}

/// <summary>
/// Retrieving UPDATE SQL template.
/// </summary>
function TemplateUpdatePostgresql(p_schema, p_table) {

    execAjax('/template_update_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_table": p_table,
            "p_schema": p_schema
        }),
        function(p_return) {
          tabSQLTemplate(
              'Update ' + p_schema + '.' + p_table,
              p_return.v_data.v_template);
        },
        function(p_return) {
            showError(p_return.v_data);
            return '';
        },
        'box',
        true);
}

/// <summary>
/// Retrieving SELECT FUNCTION SQL template.
/// </summary>
function TemplateSelectFunctionPostgresql(p_schema, p_function, p_functionid) {

    execAjax('/template_select_function_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_function": p_function,
            "p_functionid": p_functionid,
            "p_schema": p_schema
        }),
        function(p_return) {
          tabSQLTemplate(
              'Select ' + p_schema + '.' + p_function,
              p_return.v_data.v_template);
        },
        function(p_return) {
            showError(p_return.v_data);
            return '';
        },
        'box',
        true);
}

/// <summary>
/// Retrieving CALL PROCEDURE SQL template.
/// </summary>
function TemplateCallProcedurePostgresql(p_schema, p_procedure, p_procedureid) {

    execAjax('/template_call_procedure_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_procedure": p_procedure,
            "p_procedureid": p_procedureid,
            "p_schema": p_schema
        }),
        function(p_return) {
          tabSQLTemplate(
              'Call ' + p_schema + '.' + p_procedure,
              p_return.v_data.v_template);
        },
        function(p_return) {
            showError(p_return.v_data);
            return '';
        },
        'box',
        true);
}

function nodeOpenError(p_return, p_node) {

    if (p_return.v_data.password_timeout) {
        p_node.collapseNode();
        showPasswordPrompt(
            v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            function() {
                p_node.expandNode();
            },
            null,
            p_return.v_data.message
        );
    } else {

        if (p_node.childNodes.length > 0)
            p_node.removeChildNodes();

        v_node = p_node.createChildNode(
            "Error - <a class='a_link' onclick='showError(&quot;" +
            p_return.v_data.replace(/\n/g, "<br/>").replace(/"/g, '') +
            "&quot;)'>View Detail</a>", false,
            'fas fa-times node-error', {
                type: 'error',
                message: p_return.v_data
            }, null);
    }

}

function getMajorVersionPostgresql(p_version) {
    var v_version = p_version.split(' (')[0]
    var tmp = v_version.replace('PostgreSQL ', '').replace('beta', '.')
                .replace('rc', '.').split('.')
    tmp.pop()
    return tmp.join('.')
}

function postgresqlTerminateBackendConfirm(p_pid) {
    execAjax('/kill_backend_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_tab_id": v_connTabControl.selectedTab.id,
            "p_pid": p_pid
        }),
        function(p_return) {

            refreshMonitoring();

        },
        function(p_return) {
            if (p_return.v_data.password_timeout) {
                showPasswordPrompt(
                    v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                    function() {
                        postgresqlTerminateBackendConfirm(p_pid);
                    },
                    null,
                    p_return.v_data.message
                );
            } else {
                showError(p_return.v_data);
            }
        },
        'box',
        true);

}

function postgresqlTerminateBackend(p_row) {

    var v_pid = p_row[2];

    showConfirm('Are you sure you want to terminate backend ' + v_pid + '?',
        function() {

            postgresqlTerminateBackendConfirm(v_pid);

        });

}

function getExplain(p_mode) {

    var v_query;
    var v_selected_text = v_connTabControl.selectedTab.tag.tabControl.selectedTab
        .tag.editor.getSelectedText();

    if (v_selected_text != '')
        v_query = v_selected_text;
    else
        v_query = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
        .getValue();

    if (v_query.trim() == '') {
        showAlert('Please provide a string.');
    } else {
        if (p_mode == 0)
            v_query = 'explain ' + v_query;
        else if (p_mode == 1)
            v_query = 'explain analyze ' + v_query;

        querySQL(0, true, v_query, getExplainReturn, true);
    }
}

function getExplainReturn(p_data) {

    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.selectExplainTabFunc();

    if (p_data.v_error) {
        v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_explain
            .innerHTML = '<div class="error_text">' + p_data.v_data.message +
            '</div>';
    } else {
        var v_explain_text = '';
        for (var i = 0; i < p_data.v_data.v_data.length; i++)
            v_explain_text += p_data.v_data.v_data[i] + '\n';

        var resultset = [];
        v_explain_text.split(/\n/).forEach(function(item) {
            item = item.replace(/^"(.*)"$/, '$1'); // remove quotes
            item = item.replace(/^'(.*)'$/, '$1'); // remove single quotes
            if (item.match(/^-*$/)) {
                return;
            } // skip line with dashes (supposedly header separator)
            if (item.match(/^\s*QUERY PLAN\s*$/)) {
                return;
            } // skip header
            resultset.push([item]);
        });

        if (resultset.length > 0) {
            var planNodes = PGPlanNodes(resultset.slice());
            var mountNode = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_explain;
            var pgplan = React.createElement(PGPlan, {
                nodes: planNodes
            }, null);
            ReactDOM.render(pgplan, mountNode);
        }
    }

    refreshHeights();
}
