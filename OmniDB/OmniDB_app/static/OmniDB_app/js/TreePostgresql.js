/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function tabSQLTemplate(p_tab_name, p_template) {
    v_connTabControl.tag.createQueryTab(p_tab_name);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(
        p_template);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(
        0, 0, true);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
        .value = 1;

    var qtip = $(v_connTabControl.selectedTab.tag.tabControl.selectedLi).qtip({
        content: {
            text: 'Adjust command and run!'
        },
        position: {
            my: 'bottom center',
            at: 'top center'
        },
        style: {
            classes: 'qtip-bootstrap'
        },
        show: {
            ready: true
        }
    })
    window.setTimeout(function() {
        qtip.qtip('api').destroy();
    }, 4000);
}

function tabDataMining() {
    var v_name = 'Data Mining';

    v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length - 1);

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
        '<span id="tab_title">' + v_name + '</span><span id="tab_stub"><img style="width: 16px;"/></span><span id="tab_loading" style="display:none;"><img src="/static/OmniDB_app/images/spin.svg"/></span><span id="tab_check" style="display:none;"><img src="/static/OmniDB_app/images/check.png"/></span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
        false,
        null,
        renameTab,
        null,
        null,
        true,
        function() {
            if(this.tag != null) {
                refreshHeights();
            }

            if(this.tag != null && this.tag.editor != null) {
                this.tag.editor.focus();
                checkQueryStatus(this);
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

    v_tab_close_span.onclick = function() {
        removeTab(v_tab);
    };

    var v_tab_check_span = document.getElementById('tab_check');
    v_tab_check_span.id = 'tab_check_' + v_tab.id;

    var v_tab_stub_span = document.getElementById('tab_stub');
    v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

    var v_html =
        "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 400px; border: 1px solid #c3c3c3;'></div>" +
        "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
        "<button id='bt_start_" + v_tab.id + "' class='bt_execute' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block; vertical-align: middle;'><img src='/static/OmniDB_app/images/play.png' style='vertical-align: middle;'/></button>" +
        "<select id='sel_filtered_data_" + v_tab.id + "' style='display: none;'><option value='0' >Script</option><option selected='selected' value='1' >Query</option></select>" +
        "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='margin-bottom: 5px; margin-left: 5px; display: none; vertical-align: middle;' onclick='cancelSQL();'>Cancel</button>" +
        "<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
        "<button class='bt_export' title='Export Data' style='display: none; margin-bottom: 5px; margin-left: 5px; float: right;' onclick='exportData();'><img src='/static/OmniDB_app/images/table_export.png' style='vertical-align: middle;'/></button>" +
        "<select id='sel_export_type_" + v_tab.id + "' style='display: none; float: right;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option><option value='DBF' >DBF</option></select>" +
        "        <div id='query_result_tabs_" + v_tab.id + "'>" +
        "            <ul>" +
        "            <li id='query_result_tabs_" + v_tab.id + "_tab1'>Data</li>" +
        "			</ul>" +
        "			<div id='div_query_result_tabs_" + v_tab.id + "_tab1'>" +
        "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
        "			</div>";

    var v_div = document.getElementById('div_' + v_tab.id);
    v_div.innerHTML = v_html;

    var v_containerDiv = document.getElementById('txt_query_' + v_tab.id);
    v_containerDiv.style.display = 'flex';
    v_containerDiv.style.flexDirection = 'column';
    v_containerDiv.style.overflow = 'auto';

    var v_filterHeader = document.createElement('h3');
    v_filterHeader.innerHTML = 'Text Filter';
    v_filterHeader.style.marginLeft = '10px';
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

    v_inputRegex.addEventListener(
        'click',
        function(p_inputCase, p_spanCase, p_event) {
            p_inputCase.disabled = this.checked;

            if(this.checked) {
                p_spanCase.style.opacity = '0.5';
            }
            else {
                p_spanCase.style.opacity = '';
            }
        }.bind(v_inputRegex, v_inputCase, v_spanCase)
    );

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

    var v_optionList = [
        {'text': 'Data', 'value': 1},
        {'text': 'FK Name', 'value': 2},
        {'text': 'Function Definition', 'value': 3},
        {'text': 'Function Name', 'value': 4},
        {'text': 'Index Name', 'value': 5},
        {'text': 'Materialized View Column Name', 'value': 6},
        {'text': 'Materialized View Name', 'value': 7},
        {'text': 'PK Name', 'value': 8},
        {'text': 'Schema Name', 'value': 9},
        {'text': 'Sequence Name', 'value': 10},
        {'text': 'Table Column Name', 'value': 11},
        {'text': 'Table Name', 'value': 12},
        {'text': 'Trigger Name', 'value': 13},
        {'text': 'Trigger Source', 'value': 14},
        {'text': 'Unique Name', 'value': 15},
        {'text': 'View Column Name', 'value': 16},
        {'text': 'View Name', 'value': 17},
        {'text': 'Check Name', 'value': 18},
        {'text': 'Rule Name', 'value': 19},
        {'text': 'Rule Definition', 'value': 20},
        {'text': 'Partition Name', 'value': 21},
    ];

    var v_compare = function(a, b) {
        if(a.text < b.text) {
            return -1;
        }
        else if(a.text > b.text) {
            return 1;
        }
        else {
            return 0;
        }
    }

    v_optionList.sort(v_compare);

    for(var i = 0; i < v_optionList.length; i++) {
        var v_divOption = document.createElement('div');
        v_optionsContainerDiv.appendChild(v_divOption);

        var v_inputOption = document.createElement('input');
        v_inputOption.type = 'checkbox';
        v_inputOption.value = v_optionList[i].text;
        v_inputOption.classList.add('data-mining-input-option');
        v_divOption.appendChild(v_inputOption);

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

            var v_categoryList = v_grandParent.querySelectorAll('.data-mining-input-option');

            for(var i = 0; i < v_categoryList.length; i++) {
                v_categoryList[i].checked = true;
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

            var v_categoryList = v_grandParent.querySelectorAll('.data-mining-input-option');

            for(var i = 0; i < v_categoryList.length; i++) {
                v_categoryList[i].checked = false;
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
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_schemasContainerDiv, p_return) {
            var v_schemaList = p_return.v_data;

            var v_compare = function(a, b) {
                if(a.v_name < b.v_name) {
                    return -1;
                }
                else if(a.v_name > b.v_name) {
                    return 1;
                }
                else {
                    return 0;
                }
            }

            v_schemaList.sort(v_compare);

            v_disconsiderSchemas = {'information_schema': 1, 'omnidb': 1, 'pg_catalog': 1, 'pg_toast': 1}

            for(var i = 0; i < v_schemaList.length; i++) {
                if(!(v_schemaList[i].v_name in v_disconsiderSchemas) && (v_schemaList[i].v_name.search(/pg.*temp.*/) == -1)) {
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

            var v_schemaList = v_grandParent.querySelectorAll('.data-mining-input-schema');

            for(var i = 0; i < v_schemaList.length; i++) {
                v_schemaList[i].checked = true;
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

            var v_schemaList = v_grandParent.querySelectorAll('.data-mining-input-schema');

            for(var i = 0; i < v_schemaList.length; i++) {
                v_schemaList[i].checked = false;
            }
        }
    );

    v_schemasButtonsContainer.appendChild(v_buttonUnselectAllSchemas);

    var v_summarizeHeader = document.createElement('h3');
    v_summarizeHeader.innerHTML = 'Summarize Results';
    v_summarizeHeader.style.marginLeft = '10px';
    v_summarizeHeader.style.marginBottom = '0px';
    v_summarizeHeader.style.flex = '0 0 auto';
    v_containerDiv.appendChild(v_summarizeHeader);

    var v_summarizeContainerDiv = document.createElement('div');
    v_summarizeContainerDiv.style.display = 'grid';
    v_summarizeContainerDiv.style.gridTemplateColumns = '1fr';
    v_summarizeContainerDiv.style.gridRowGap = '10px';
    v_summarizeContainerDiv.style.gridColumnGap = '10px';
    v_summarizeContainerDiv.style.justifyItems = 'start';
    v_summarizeContainerDiv.style.boxSizing = 'border-box';
    v_summarizeContainerDiv.style.padding = '10px';
    v_containerDiv.appendChild(v_summarizeContainerDiv);

    var v_divSummarize = document.createElement('div');
    v_summarizeContainerDiv.appendChild(v_divSummarize);

    var v_inputSummarize = document.createElement('input');
    v_inputSummarize.type = 'checkbox';
    v_inputSummarize.classList.add('data-mining-input-summarize');
    v_divSummarize.appendChild(v_inputSummarize);

    var v_spanSummarize = document.createElement('span');
    v_spanSummarize.innerHTML = 'Summarize';
    v_divSummarize.appendChild(v_spanSummarize);

    var v_buttonStart = document.getElementById('bt_start_' + v_tab.id);

    v_buttonStart.addEventListener(
        'click',
        function(p_event) {
            var v_parent = this.parentElement;

            var v_data = {
                text: '',
                regex: false,
                caseSensitive: false,
                categoryList: [],
                schemaList: [],
                summarizeResults: false
            };

            var v_inputFilter = v_parent.querySelector('.data-mining-input-text');

            if(v_inputFilter != null) {
                v_data.text = v_inputFilter.value;
            }

            if(v_data.text.trim() == '') {
                showAlert('Please, provide a string in order to search.');
                return;
            }

            var v_inputCase = v_parent.querySelector('.data-mining-input-case');

            if(v_inputCase != null) {
                v_data.caseSensitive = v_inputCase.checked;
            }

            var v_inputRegex = v_parent.querySelector('.data-mining-input-regex');

            if(v_inputRegex != null) {
                v_data.regex = v_inputRegex.checked;
            }

            var v_categoryList = v_parent.querySelectorAll('.data-mining-input-option');

            for(var i = 0; i < v_categoryList.length; i++) {
                if(v_categoryList[i].checked) {
                    v_data.categoryList.push(v_categoryList[i].value);
                }
            }

            if(v_data.categoryList.length == 0) {
                showAlert('Please, select at least one category to search.');
                return;
            }

            var v_schemaList = v_parent.querySelectorAll('.data-mining-input-schema');

            for(var i = 0; i < v_schemaList.length; i++) {
                if(v_schemaList[i].checked) {
                    v_data.schemaList.push(v_schemaList[i].value);
                }
            }

            if(v_data.schemaList.length == 0) {
                showAlert('Please, select at least one schema to search.');
                return;
            }

            var v_inputSummarize = v_parent.querySelector('.data-mining-input-summarize');

            if(v_inputSummarize != null) {
                v_data.summarizeResults = v_inputSummarize.checked;
            }

            if(v_data.categoryList.indexOf('Data') != -1) {
                showConfirm(
                    'You have selected the category "Data". Please, be aware that it can consume a considerable amount of time and resources, depending on selected schemas size. Do you want to proceed?',
                    function(p_data) {
                        queryDataMining(p_data);
                    }.bind(null, v_data)
                );
            }
            else {
                queryDataMining(v_data);
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
        div_count_notices: document.getElementById('query_result_tabs_count_notices_' + v_tab.id),
        sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
        sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
        tab_title_span : v_tab_title_span,
        tab_loading_span : v_tab_loading_span,
        tab_close_span : v_tab_close_span,
        tab_check_span : v_tab_check_span,
        tab_stub_span : v_tab_stub_span,
        bt_start: document.getElementById('bt_start_' + v_tab.id),
        bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
        state : 0,
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

    v_tag.selectDataTabFunc    = v_selectDataTabFunc;
    v_curr_tabs.tabList[0].elementLi.onclick = v_selectDataTabFunc;

    v_selectDataTabFunc();

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+', false, v_connTabControl.tag.createQueryTab);

    v_add_tab.tag = {
        mode: 'add'
    }

    setTimeout(
        function() {
            refreshHeights();
        },
        10
    );

    var qtip = $(v_connTabControl.selectedTab.tag.tabControl.selectedLi).qtip({
        content: {
            text: 'Adjust parameters and run!'
        },
        position: {
            my: 'bottom center',
            at: 'top center'
        },
        style: {
            classes: 'qtip-bootstrap'
        },
        show: {
            ready: true
        }
    })
    window.setTimeout(function() {
        qtip.qtip('api').destroy();
    }, 4000);
}

/// <summary>
/// Retrieving tree.
/// </summary>
function getTreePostgresql(p_div) {

    var context_menu = {
        'cm_server': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
        'cm_connection': {
            elements: [{
                text: 'Vacuum Database',
                icon: '/static/OmniDB_app/images/vacuum.png',
                action: function(node) {
                    tabSQLTemplate('Vacuum Database', node.tree
                        .tag.vacuum);
                }
            }, {
                text: 'Data Mining',
                icon: '/static/OmniDB_app/images/data_mining.png',
                action: function(node) {
                    tabDataMining();
                }
            }]
        },
        'cm_databases': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Database', node.tree
                        .tag.create_database);
                }
            }, {
                text: 'Doc: Databases',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Databases',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/managing-databases.html');
                }
            }]
        },
        'cm_database': {
            elements: [{
                text: 'Alter Database',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Database', node.tree.tag
                        .alter_database.replace(
                            '#database_name#', node.text));
                }
            }, {
                text: 'Drop Database',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Database', node.tree.tag
                        .drop_database.replace(
                            '#database_name#', node.text));
                }
            }]
        },
        'cm_tablespaces': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Tablespace', node.tree
                        .tag.create_tablespace);
                }
            }, {
                text: 'Doc: Tablespaces',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Tablespaces',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/manage-ag-tablespaces.html'
                    );
                }
            }]
        },
        'cm_tablespace': {
            elements: [{
                text: 'Alter Tablespace',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Tablespace', node.tree
                        .tag.alter_tablespace.replace(
                            '#tablespace_name#', node.text)
                    );
                }
            }, {
                text: 'Drop Tablespace',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Role', node.tree.tag
                        .create_role);
                }
            }, {
                text: 'Doc: Roles',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Roles',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/user-manag.html');
                }
            }]
        },
        'cm_role': {
            elements: [{
                text: 'Alter Role',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Role', node.tree.tag.alter_role
                        .replace('#role_name#', node.text));
                }
            }, {
                text: 'Drop Role',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Role', node.tree.tag.drop_role
                        .replace('#role_name#', node.text));
                }
            }]
        },
        'cm_extensions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Extension', node.tree
                        .tag.create_extension);
                }
            }, {
                text: 'Doc: Extensions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Extensions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/extend-extensions.html');
                }
            }]
        },
        'cm_extension': {
            elements: [{
                text: 'Alter Extension',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Extension', node.tree
                        .tag.alter_extension.replace(
                            '#extension_name#', node.text));
                }
            }, {
                text: 'Drop Extension',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Schema', node.tree.tag
                        .create_schema);
                }
            }, {
                text: 'Doc: Schemas',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Schemas',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-schemas.html');
                }
            }]
        },
        'cm_schema': {
            elements: [{
                text: 'Render Graph',
                icon: '/static/OmniDB_app/images/graph.png',
                action: function(node) {

                },
                submenu: {
                    elements: [{
                        text: 'Simple Graph',
                        icon: '/static/OmniDB_app/images/graph.png',
                        action: function(node) {
                            v_connTabControl.tag.createGraphTab(
                                node.text)
                            drawGraph(false, node.text);
                        }
                    }, {
                        text: 'Complete Graph',
                        icon: '/static/OmniDB_app/images/graph.png',
                        action: function(node) {
                            v_connTabControl.tag.createGraphTab(
                                node.text)
                            drawGraph(true, node.text);
                        }
                    }]
                }
            }, {
                text: 'Alter Schema',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Schema', node.tree.tag
                        .alter_schema.replace(
                            '#schema_name#', node.text));
                }
            }, {
                text: 'Drop Schema',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Table',
                icon: '/static/OmniDB_app/images/new_table.png',
                action: function(node) {
                    startAlterTable(true, 'new', null, node.parent
                        .text);
                }
            }, {
                text: 'Doc: Basics',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Table Basics',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-basics.html');
                }
            }, {
                text: 'Doc: Constraints',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Table Constraints',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-constraints.html');
                }
            }, {
                text: 'Doc: Modifying',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Modifying Tables',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-alter.html');
                }
            }]
        },
        'cm_table': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/list.png',
                submenu: {
                    elements: [{
                        text: 'Query Data',
                        icon: '/static/OmniDB_app/images/query.png',
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
                                .tag.sel_filtered_data.value =
                                1;

                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    '-- Querying Data\nselect t.*\nfrom ' +
                                    v_table_name + ' t'
                                );
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            renameTabConfirm(
                                v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab,
                                node.text);

                            //minimizeEditor();

                            querySQL(0);
                        }
                    }, {
                        text: 'Edit Data',
                        icon: '/static/OmniDB_app/images/edit_data.png',
                        action: function(node) {
                            startEditData(node.text,
                                node.parent.parent.text
                            );
                        }
                    }, {
                        text: 'Count Records',
                        icon: '/static/OmniDB_app/images/counter.png',
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
                                    "-- Counting Records\nselect count(*) as count\nfrom " +
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
                        icon: '/static/OmniDB_app/images/tab_close.png',
                        action: function(node) {
                            v_connTabControl.tag.createQueryTab(
                                'Delete Records');
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    'DELETE FROM ' +
                                    node.parent.parent.text +
                                    '.' + node.text);
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.gotoLine(0,
                                    0, true);
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.sel_filtered_data.value =
                                1;
                        }
                    }]
                }
            }, {
                text: 'Table Actions',
                icon: '/static/OmniDB_app/images/list.png',
                submenu: {
                    elements: [{
                        text: 'Vacuum Table',
                        icon: '/static/OmniDB_app/images/vacuum.png',
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
                        text: 'Alter Table',
                        icon: '/static/OmniDB_app/images/table_edit.png',
                        action: function(node) {
                            startAlterTable(true,
                                'alter', node.text,
                                node.parent.parent.text
                            );
                        }
                    }, {
                        text: 'Drop Table',
                        icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Field', node.tree.tag
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                text: 'Drop Primary Key',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                text: 'Drop Foreign Key',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                text: 'Drop Unique',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Index', node.tree.tag
                        .create_index.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Indexes',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Indexes',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/indexes.html');
                }
            }]
        },
        'cm_index': {
            elements: [{
                text: 'Alter Index',
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Rule', node.tree.tag
                        .create_rule.replace('#table_name#',
                            node.parent.parent.parent.text +
                            '.' + node.parent.text));
                }
            }, {
                text: 'Doc: Rules',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Rules',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/rules.html');
                }
            }]
        },
        'cm_rule': {
            elements: [{
                text: 'Alter Rule',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Rule', node.tree.tag.alter_rule
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text).replace(
                            '#rule_name#', node.text));
                }
            }, {
                text: 'Drop Rule',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Trigger', node.tree.tag
                        .create_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Triggers',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Triggers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/trigger-definition.html');
                }
            }]
        },
        'cm_view_triggers': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Trigger', node.tree.tag
                        .create_view_trigger.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Triggers',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Triggers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/trigger-definition.html');
                }
            }]
        },
        'cm_trigger': {
            elements: [{
                text: 'Alter Trigger',
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/tab_close.png',
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
        'cm_partitions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Partition', node.tree
                        .tag.create_partition.replace(
                            '#table_name#', node.parent.parent
                            .parent.text + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Partitions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Partitions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-partitioning.html');
                }
            }]
        },
        'cm_partition': {
            elements: [{
                text: 'No Inherit Partition',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('No Inherit Partition', node
                        .tree.tag.noinherit_partition.replace(
                            '#table_name#', node.parent.parent
                            .parent.parent.text + '.' +
                            node.parent.parent.text).replace(
                            '#partition_name#', node.text));
                }
            }, {
                text: 'Drop Partition',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Function', node.tree
                        .tag.create_function.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Functions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createfunction.html');
                }
            }]
        },
        'cm_function': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Edit Function',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getFunctionDefinitionPostgresql(node);
                }
            }, {
                text: 'Debug Function',
                icon: '/static/OmniDB_app/images/debug.png',
                action: function(node) {
                    v_connTabControl.tag.createDebuggerTab(
                        node.text);
                    getDebugFunctionDefinitionPostgresql(node);
                    setupDebug(node);
                }
            }, {
                text: 'Drop Function',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Function', node.tree.tag
                        .drop_function.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_triggerfunctions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Trigger Function',
                        node.tree.tag.create_triggerfunction
                        .replace('#schema_name#', node.parent
                            .text));
                }
            }, {
                text: 'Doc: Trigger Functions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Trigger Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/plpgsql-trigger.html');
                }
            }]
        },
        'cm_triggerfunction': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getTriggerFunctionDefinitionPostgresql(node);
                }
            }, {
                text: 'Drop Trigger Function',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Sequence', node.tree
                        .tag.create_sequence.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Sequences',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Sequences',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createsequence.html');
                }
            }]
        },
        'cm_sequence': {
            elements: [{
                text: 'Alter Sequence',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Sequence', node.tree.tag
                        .alter_sequence.replace(
                            '#sequence_name#', node.parent.parent
                            .text + '.' + node.text));
                }
            }, {
                text: 'Drop Sequence',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create View', node.tree.tag
                        .create_view.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Views',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Views',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createview.html');
                }
            }]
        },
        'cm_view': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/query.png',
                action: function(node) {

                    var v_table_name = '';
                    if (node.parent.parent.parent.parent !=
                        null)
                        v_table_name = node.parent.parent.text +
                        '.' + node.text;
                    else
                        v_table_name = node.text;

                    v_connTabControl.tag.createQueryTab(
                        node.text);

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.sel_filtered_data.value =
                        1;

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.setValue(
                            '-- Querying Data\nselect t.*\nfrom ' +
                            v_table_name + ' t');
                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.clearSelection();
                    renameTabConfirm(v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab, node.text
                    );

                    //minimizeEditor();

                    querySQL(0);
                }
            }, {
                text: 'Edit View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getViewDefinitionPostgresql(node);
                }
            }, {
                text: 'Drop View',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Materialized View',
                        node.tree.tag
                        .create_mview.replace(
                            '#schema_name#', node.parent.text
                        ));
                }
            }, {
                text: 'Doc: Mat. Views',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Materialized Views',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-creatematerializedview.html'
                    );
                }
            }]
        },
        'cm_mview': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/query.png',
                action: function(node) {

                    var v_table_name = '';
                    if (node.parent.parent.parent.parent !=
                        null)
                        v_table_name = node.parent.parent.text +
                        '.' + node.text;
                    else
                        v_table_name = node.text;

                    v_connTabControl.tag.createQueryTab(
                        node.text);

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.sel_filtered_data.value =
                        1;

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.setValue(
                            '-- Querying Data\nselect t.*\nfrom ' +
                            v_table_name + ' t');
                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.clearSelection();
                    renameTabConfirm(v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab, node.text
                    );

                    //minimizeEditor();

                    querySQL(0);
                }
            }, {
                text: 'Edit Mat. View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getMaterializedViewDefinitionPostgresql(
                        node);
                }
            }, {
                text: 'Refresh Mat. View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Refresh Materialized View',
                        node.tree.tag.refresh_mview
                        .replace('#view_name#', node.parent
                            .parent.text + '.' + node.text)
                    );
                }
            }, {
                text: 'Drop Mat. View',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate(
                        'Create Physical Replication Slot',
                        node.tree.tag
                        .create_physicalreplicationslot);
                }
            }, {
                text: 'Doc: Replication Slots',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Physical Replication Slots',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/warm-standby.html#streaming-replication-slots'
                    );
                }
            }]
        },
        'cm_physicalreplicationslot': {
            elements: [{
                text: 'Drop Slot',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate(
                        'Create Logical Replication Slot',
                        node.tree.tag
                        .create_logicalreplicationslot);
                }
            }, {
                text: 'Doc: Replication Slots',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Logical Replication Slots',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/logicaldecoding-explanation.html#logicaldecoding-replication-slots'
                    );
                }
            }]
        },
        'cm_logicalreplicationslot': {
            elements: [{
                text: 'Drop Slot',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Publication', node.tree
                        .tag.create_publication);
                }
            }, {
                text: 'Doc: Publications',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Publications',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/logical-replication-publication.html'
                    );
                }
            }]
        },
        'cm_publication': {
            elements: [{
                text: 'Alter Publication',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Publication', node.tree
                        .tag.alter_publication
                        .replace('#pub_name#', node.text));
                }
            }, {
                text: 'Drop Publication',
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
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
                icon: '/static/OmniDB_app/images/tab_close.png',
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
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Subscription', node.tree
                        .tag.create_subscription);
                }
            }, {
                text: 'Doc: Subscriptions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Subscriptions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/logical-replication-subscription.html'
                    );
                }
            }]
        },
        'cm_subscription': {
            elements: [{
                text: 'Alter Subscription',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Subscription', node.tree
                        .tag.alter_subscription
                        .replace('#sub_name#', node.text));
                }
            }, {
                text: 'Drop Subscription',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Subscription', node.tree
                        .tag.drop_subscription
                        .replace('#sub_name#', node.text));
                }
            }]
        },
        'cm_pglogical': {
            elements: [{
                text: 'Doc: pglogical',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: pglogical',
                        'https://www.2ndquadrant.com/en/resources/pglogical/pglogical-docs/'
                    );
                }
            }]
        },
        'cm_pglogical_nodes': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Node',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Node',
                        node.tree.tag.pglogical_create_node
                    );
                }
            }]
        },
        'cm_pglogical_node': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Add Interface',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Add Node Interface',
                        node.tree.tag.pglogical_add_interface
                        .replace('#node_name#', node.text.replace(
                            ' (local)', '')));
                }
            }, {
                text: 'Drop Node',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Node',
                        node.tree.tag.pglogical_drop_node
                        .replace('#node_name#', node.text.replace(
                            ' (local)', '')));
                }
            }]
        },
        'cm_pglogical_interface': {
            elements: [{
                text: 'Drop Interface',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Node Interface',
                        node.tree.tag.pglogical_drop_interface
                        .replace('#node_name#', node.parent
                            .text.replace(' (local)', ''))
                        .replace('#interface_name#', node.text)
                    );
                }
            }]
        },
        'cm_pglogical_repsets': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Replication Set',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Replication Set',
                        node.tree.tag.pglogical_create_repset
                    );
                }
            }]
        },
        'cm_pglogical_repset': {
            elements: [{
                text: 'Alter Replication Set',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Replication Set',
                        node.tree.tag.pglogical_alter_repset
                        .replace('#repset_name#', node.text)
                    );
                }
            }, {
                text: 'Drop Replication Set',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Replication Set',
                        node.tree.tag.pglogical_drop_repset
                        .replace('#repset_name#', node.text)
                    );
                }
            }]
        },
        'cm_pglogical_repset_tables': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Add Table',
                        node.tree.tag.pglogical_repset_add_table
                        .replace('#repset_name#', node.parent
                            .text)
                    );
                }
            }, {
                text: 'Add All Tables',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Add All Tables',
                        node.tree.tag.pglogical_repset_add_all_tables
                        .replace('#repset_name#', node.parent
                            .text)
                    );
                }
            }]
        },
        'cm_pglogical_repset_table': {
            elements: [{
                text: 'Remove Table',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Remove Table',
                        node.tree.tag.pglogical_repset_remove_table
                        .replace('#repset_name#', node.parent
                            .parent.text)
                        .replace('#table_name#', node.text)
                    );
                }
            }]
        },
        'cm_pglogical_repset_seqs': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Add Sequence',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Add Sequence',
                        node.tree.tag.pglogical_repset_add_seq
                        .replace('#repset_name#', node.parent
                            .text)
                    );
                }
            }, {
                text: 'Add All Sequences',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Add All Sequences',
                        node.tree.tag.pglogical_repset_add_all_seqs
                        .replace('#repset_name#', node.parent
                            .text)
                    );
                }
            }]
        },
        'cm_pglogical_repset_seq': {
            elements: [{
                text: 'Remove Sequence',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Remove Sequence',
                        node.tree.tag.pglogical_repset_remove_seq
                        .replace('#repset_name#', node.parent
                            .parent.text)
                        .replace('#sequence_name#', node.text)
                    );
                }
            }]
        },
        'cm_pglogical_subscriptions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Subscription',
                        node.tree.tag.pglogical_create_sub
                    );
                }
            }]
        },
        'cm_pglogical_subscription': {
            elements: [{
                text: 'Enable Subscription',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Enable Subscription',
                        node.tree.tag.pglogical_enable_sub
                        .replace('#sub_name#', node.text));
                }
            }, {
                text: 'Disable Subscription',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Disable Subscription',
                        node.tree.tag.pglogical_disable_sub
                        .replace('#sub_name#', node.text));
                }
            }, {
                text: 'Sync Subscription',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Synchronize Subscription',
                        node.tree.tag.pglogical_sync_sub
                        .replace('#sub_name#', node.text));
                }
            }, {
                text: 'Drop Subscription',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Subscription',
                        node.tree.tag.pglogical_drop_sub
                        .replace('#sub_name#', node.text));
                }
            }]
        },
        'cm_pglogical_subscription_repsets': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Add Replication Set',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Add Replication Set', node.tree
                        .tag.pglogical_sub_add_repset
                        .replace('#sub_name#', node.parent.text)
                    );
                }
            }]
        },
        'cm_pglogical_subscription_repset': {
            elements: [{
                text: 'Remove Replication Set',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Remove Replication Set',
                        node.tree.tag.pglogical_sub_remove_repset
                        .replace('#sub_name#', node.parent.parent
                            .text)
                        .replace('#set_name#', node.text)
                    );
                }
            }]
        },
        'cm_bdr': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
        'cm_bdrnodes': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
        'cm_bdrnode': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
        'cm_bdrrepsets': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Insert Replication Set',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Insert Replication Set',
                        node.tree.tag.bdr_insert_repset);
                }
            }]
        },
        'cm_bdrrepset': {
            elements: [{
                text: 'Update Rep. Set',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Update Replication Set',
                        node.tree.tag.bdr_update_repset
                        .replace('#set_name#', node.text));
                }
            }, {
                text: 'Delete Replication Set',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Delete Replication Set',
                        node.tree.tag.bdr_delete_repset
                        .replace('#set_name#', node.text));
                }
            }]
        },
        'cm_bdr_table_repsets': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Set Replication Sets',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Set Replication Sets', node
                        .tree.tag.bdr_set_repsets
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text));
                }
            }]
        },
        'cm_bdr_table_confhands': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Conf. Handler',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Conflict Handler',
                        node.tree.tag.bdr_create_confhand
                        .replace(/#table_name#/g, node.parent
                            .parent.parent.parent.text +
                            '.' + node.parent.parent.text));
                }
            }]
        },
        'cm_bdr_table_confhand': {
            elements: [{
                text: 'Drop Conf. Handler',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Conflict Handler',
                        node.tree.tag.bdr_drop_confhand
                        .replace('#table_name#', node.parent
                            .parent.parent.parent.parent.text +
                            '.' + node.parent.parent.parent
                            .text)
                        .replace('#ch_name#', node.text));
                }
            }]
        },
        'cm_xl': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Pause Cluster',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Pause Cluster',
                        node.tree.tag.xl_pause_cluster);
                }
            }, {
                text: 'Unpause Cluster',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Unpause Cluster',
                        node.tree.tag.xl_unpause_cluster);
                }
            }, {
                text: 'Clean Connection',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Clean Connection',
                        node.tree.tag.xl_clean_connection);
                }
            }, {
                text: 'Doc: Postgres-XL',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Postgres-XL',
                        'https://www.postgres-xl.org/documentation/'
                    );
                }
            }]
        },
        'cm_xlnodes': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Node',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Node',
                        node.tree.tag.xl_create_node);
                }
            }]
        },
        'cm_xlnode': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Execute Direct',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Execute Direct',
                        node.tree.tag.xl_execute_direct
                        .replace('#node_name#', node.text));
                }
            }, {
                text: 'Pool Reload',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Pool Reload',
                        node.tree.tag.xl_pool_reload
                        .replace('#node_name#', node.text));
                }
            }, {
                text: 'Alter Node',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Node',
                        node.tree.tag.xl_alter_node
                        .replace('#node_name#', node.text));
                }
            }, {
                text: 'Drop Node',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Node',
                        node.tree.tag.xl_drop_node
                        .replace('#node_name#', node.text));
                }
            }]
        },
        'cm_xlgroups': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Group',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Group',
                        node.tree.tag.xl_create_group);
                }
            }]
        },
        'cm_xlgroup': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Drop Group',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Group',
                        node.tree.tag.xl_drop_group
                        .replace('#group_name#', node.text)
                    );
                }
            }]
        },
        'cm_xl_table': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Alter Distribution',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Table Distribution',
                        node.tree.tag.xl_altertable_distribution
                        .replace('#table_name#',
                            node.parent.parent.parent.text +
                            '.' + node.parent.text));
                }
            }, {
                text: 'Alter Location',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Table Distribution',
                        node.tree.tag.xl_altertable_location
                        .replace('#table_name#',
                            node.parent.parent.parent.text +
                            '.' + node.parent.text));
                }
            }]
        },
        'cm_xl_table_nodes': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Add Node',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Table Add Node',
                        node.tree.tag.xl_altertable_addnode
                        .replace('#table_name#',
                            node.parent.parent.parent.parent
                            .text + '.' +
                            node.parent.parent.text));
                }
            }]
        },
        'cm_xl_table_node': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Delete Node',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Alter Table Delete Node',
                        node.tree.tag.xl_altertable_deletenode
                        .replace('#table_name#',
                            node.parent.parent.parent.parent
                            .parent.text + '.' +
                            node.parent.parent.parent.text)
                        .replace('#node_name#', node.text));
                }
            }]
        },
        'cm_refresh': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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

    tree.nodeAfterOpenEvent = function(node) {
      refreshTreePostgresql(node);
    }

    tree.clickNodeEvent = function(node) {
      getPropertiesPostgresql(node);
    }

    var node_server = tree.createNode('PostgreSQL', false,
        '/static/OmniDB_app/images/postgresql_medium.png', null, {
            type: 'server'
        }, 'cm_server');
    node_server.createChildNode('', true, '/static/OmniDB_app/images/spin.svg',
        null, null);
    tree.drawTree();


}

/// <summary>
/// Retrieving properties.
/// </summary>
/// <param name="node">Node object.</param>
function getPropertiesPostgresql(node) {
    if (node.tag != undefined)
      if (node.tag.type == 'table') {
        getProperties('/get_properties_postgresql/',
          {
            p_schema: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
          });
      }
      else if (node.tag.type == 'sequence') {
        getProperties('/get_properties_postgresql/',
          {
            p_schema: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
          });
      }
      else {
        clearProperties();
      }
}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreePostgresql(node) {
    if (node.tag != undefined)
        if (node.tag.type == 'schema_list') {
            getSchemasPostgresql(node);
        } else if (node.tag.type == 'table_list') {
        getTablesPostgresql(node);
    } else if (node.tag.type == 'table') {
        getColumnsPostgresql(node);
    } else if (node.tag.type == 'primary_key') {
        getPKPostgresql(node);
    } else if (node.tag.type == 'uniques') {
        getUniquesPostgresql(node);
    } else if (node.tag.type == 'foreign_keys') {
        getFKsPostgresql(node);
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
    } else if (node.tag.type == 'function_list') {
        getFunctionsPostgresql(node);
    } else if (node.tag.type == 'function') {
        getFunctionFieldsPostgresql(node);
    } else if (node.tag.type == 'sequence_list') {
        getSequencesPostgresql(node);
    } else if (node.tag.type == 'database_list') {
        getDatabasesPostgresql(node);
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
    } else if (node.tag.type == 'pglogical_node_list') {
        getPglogicalNodesPostgresql(node);
    } else if (node.tag.type == 'pglogical_node') {
        getPglogicalInterfacesPostgresql(node);
    } else if (node.tag.type == 'pglogical_repset_list') {
        getPglogicalReplicationSetsPostgresql(node);
    } else if (node.tag.type == 'pglogical_repset_table_list') {
        getPglogicalReplicationSetTablesPostgresql(node);
    } else if (node.tag.type == 'pglogical_repset_seq_list') {
        getPglogicalReplicationSetSequencesPostgresql(node);
    } else if (node.tag.type == 'pglogical_subscription_list') {
        getPglogicalSubscriptionsPostgresql(node);
    } else if (node.tag.type == 'pglogical_subscription_repset_list') {
        getPglogicalSubscriptionReplicationSetsPostgresql(node);
    } else if (node.tag.type == 'bdr') {
        getBDRPropertiesPostgresql(node);
    } else if (node.tag.type == 'bdr_node_list') {
        getBDRNodesPostgresql(node);
    } else if (node.tag.type == 'bdr_repset_list') {
        getBDRReplicationSetsPostgresql(node);
    } else if (node.tag.type == 'bdr_table_repset_list') {
        getBDRTableReplicationSetsPostgresql(node);
    } else if (node.tag.type == 'bdr_table_confhand_list') {
        getBDRTableConflictHandlersPostgresql(node);
    } else if (node.tag.type == 'xl_node_list') {
        getXLNodesPostgresql(node);
    } else if (node.tag.type == 'xl_group_list') {
        getXLGroupsPostgresql(node);
    } else if (node.tag.type == 'xl_group') {
        getXLGroupNodesPostgresql(node);
    } else if (node.tag.type == 'xl_table') {
        getXLTablePropertiesPostgresql(node);
    } else if (node.tag.type == 'xl_table_node_list') {
        getXLTableNodesPostgresql(node);
    }
}

/// <summary>
/// Retrieving tree details.
/// </summary>
/// <param name="node">Node object.</param>
function getTreeDetailsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_tree_info_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            node.tree.contextMenu.cm_server.elements = []
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
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
                icon: '/static/OmniDB_app/images/monitoring.png',
                action: function(node) {},
                submenu: {
                    elements: [{
                        text: 'Dashboard',
                        icon: '/static/OmniDB_app/images/monitoring.png',
                        action: function(node) {
                            v_connTabControl.tag.createMonitorDashboardTab();
                            startMonitorDashboard();
                        }
                    }, {
                        text: 'Backends',
                        icon: '/static/OmniDB_app/images/monitoring.png',
                        action: function(node) {
                            v_connTabControl.tag.createMonitoringTab(
                                'Backends',
                                'select * from pg_stat_activity', [{
                                    icon: '/static/OmniDB_app/images/tab_close.png',
                                    title: 'Terminate',
                                    action: 'postgresqlTerminateBackend'
                                }]);
                        }
                    }, {
                        text: 'Replication',
                        icon: '/static/OmniDB_app/images/monitoring.png',
                        action: function(node) {
                            v_connTabControl.tag.createMonitoringTab(
                                'Replication',
                                'select * from pg_stat_replication',
                                null);
                        }
                    }]
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: PostgreSQL',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: PostgreSQL',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/');
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: SQL Language',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: SQL Language',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql.html');
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: SQL Commands',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: SQL Commands',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-commands.html');
                }
            });

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tree.tag = {
                version: p_return.v_data.v_database_return.version,
                superuser: p_return.v_data.v_database_return.superuser,
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
                create_triggerfunction: p_return.v_data.v_database_return
                    .create_triggerfunction,
                drop_triggerfunction: p_return.v_data.v_database_return
                    .drop_triggerfunction,
                create_view: p_return.v_data.v_database_return.create_view,
                drop_view: p_return.v_data.v_database_return.drop_view,
                create_mview: p_return.v_data.v_database_return.create_mview,
                refresh_mview: p_return.v_data.v_database_return.refresh_mview,
                drop_mview: p_return.v_data.v_database_return.drop_mview,
                //create_table
                //alter_table
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
                create_partition: p_return.v_data.v_database_return.create_partition,
                noinherit_partition: p_return.v_data.v_database_return.noinherit_partition,
                drop_partition: p_return.v_data.v_database_return.drop_partition,
                vacuum: p_return.v_data.v_database_return.vacuum,
                vacuum_table: p_return.v_data.v_database_return.vacuum_table,
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
                pglogical_version: p_return.v_data.v_database_return.pglogical_version,
                pglogical_create_node: p_return.v_data.v_database_return
                    .pglogical_create_node,
                pglogical_drop_node: p_return.v_data.v_database_return.pglogical_drop_node,
                pglogical_add_interface: p_return.v_data.v_database_return
                    .pglogical_add_interface,
                pglogical_drop_interface: p_return.v_data.v_database_return
                    .pglogical_drop_interface,
                pglogical_create_repset: p_return.v_data.v_database_return
                    .pglogical_create_repset,
                pglogical_alter_repset: p_return.v_data.v_database_return
                    .pglogical_alter_repset,
                pglogical_drop_repset: p_return.v_data.v_database_return
                    .pglogical_drop_repset,
                pglogical_repset_add_table: p_return.v_data.v_database_return
                    .pglogical_repset_add_table,
                pglogical_repset_add_all_tables: p_return.v_data.v_database_return
                    .pglogical_repset_add_all_tables,
                pglogical_repset_remove_table: p_return.v_data.v_database_return
                    .pglogical_repset_remove_table,
                pglogical_repset_add_seq: p_return.v_data.v_database_return
                    .pglogical_repset_add_seq,
                pglogical_repset_add_all_seqs: p_return.v_data.v_database_return
                    .pglogical_repset_add_all_seqs,
                pglogical_repset_remove_seq: p_return.v_data.v_database_return
                    .pglogical_repset_remove_seq,
                pglogical_create_sub: p_return.v_data.v_database_return
                    .pglogical_create_sub,
                pglogical_enable_sub: p_return.v_data.v_database_return
                    .pglogical_enable_sub,
                pglogical_disable_sub: p_return.v_data.v_database_return
                    .pglogical_disable_sub,
                pglogical_sync_sub: p_return.v_data.v_database_return
                    .pglogical_sync_sub,
                pglogical_drop_sub: p_return.v_data.v_database_return
                    .pglogical_drop_sub,
                pglogical_sub_add_repset: p_return.v_data.v_database_return
                    .pglogical_sub_add_repset,
                pglogical_sub_remove_repset: p_return.v_data.v_database_return
                    .pglogical_sub_remove_repset,
                bdr_version: p_return.v_data.v_database_return.bdr_version,
                bdr_create_group: p_return.v_data.v_database_return.bdr_create_group,
                bdr_join_group: p_return.v_data.v_database_return.bdr_join_group,
                bdr_join_wait: p_return.v_data.v_database_return.bdr_join_wait,
                bdr_pause: p_return.v_data.v_database_return.bdr_pause,
                bdr_resume: p_return.v_data.v_database_return.bdr_resume,
                bdr_replicate_ddl_command: p_return.v_data.v_database_return
                    .bdr_replicate_ddl_command,
                bdr_part_node: p_return.v_data.v_database_return.bdr_part_node,
                bdr_insert_repset: p_return.v_data.v_database_return.bdr_insert_repset,
                bdr_update_repset: p_return.v_data.v_database_return.bdr_update_repset,
                bdr_delete_repset: p_return.v_data.v_database_return.bdr_delete_repset,
                bdr_set_repsets: p_return.v_data.v_database_return.bdr_set_repsets,
                bdr_create_confhand: p_return.v_data.v_database_return.bdr_create_confhand,
                bdr_drop_confhand: p_return.v_data.v_database_return.bdr_drop_confhand,
                bdr_terminate_apply: p_return.v_data.v_database_return.bdr_terminate_apply,
                bdr_terminate_walsender: p_return.v_data.v_database_return
                    .bdr_terminate_walsender,
                bdr_remove: p_return.v_data.v_database_return.bdr_remove,
                xl_pause_cluster: p_return.v_data.v_database_return.xl_pause_cluster,
                xl_unpause_cluster: p_return.v_data.v_database_return.xl_unpause_cluster,
                xl_clean_connection: p_return.v_data.v_database_return.xl_clean_connection,
                xl_create_group: p_return.v_data.v_database_return.xl_create_group,
                xl_drop_group: p_return.v_data.v_database_return.xl_drop_group,
                xl_create_node: p_return.v_data.v_database_return.xl_create_node,
                xl_alter_node: p_return.v_data.v_database_return.xl_alter_node,
                xl_drop_node: p_return.v_data.v_database_return.xl_drop_node,
                xl_execute_direct: p_return.v_data.v_database_return.xl_execute_direct,
                xl_pool_reload: p_return.v_data.v_database_return.xl_pool_reload,
                xl_altertable_distribution: p_return.v_data.v_database_return
                    .xl_altertable_distribution,
                xl_altertable_location: p_return.v_data.v_database_return
                    .xl_altertable_location,
                xl_altertable_addnode: p_return.v_data.v_database_return
                    .xl_altertable_addnode,
                xl_altertable_deletenode: p_return.v_data.v_database_return
                    .xl_altertable_deletenode
            }

            node.setText(p_return.v_data.v_database_return.version);

            var node_connection = node.createChildNode(p_return.v_data.v_database_return
                .v_database, true, '/static/OmniDB_app/images/db.png', {
                    type: 'connection'
                }, 'cm_connection');
            var node_databases = node.createChildNode('Databases', false,
                '/static/OmniDB_app/images/db.png', {
                    type: 'database_list',
                    num_databases: 0
                }, 'cm_databases');
            node_databases.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            var node_tablespaces = node.createChildNode('Tablespaces',
                false, '/static/OmniDB_app/images/folder.png', {
                    type: 'tablespace_list',
                    num_tablespaces: 0
                }, 'cm_tablespaces');
            node_tablespaces.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            var node_roles = node.createChildNode('Roles', false,
                '/static/OmniDB_app/images/role.png', {
                    type: 'role_list',
                    num_roles: 0
                }, 'cm_roles');
            node_roles.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            var node_schemas = node_connection.createChildNode('Schemas',
                false, '/static/OmniDB_app/images/schemas.png', {
                    type: 'schema_list',
                    num_schemas: 0
                }, 'cm_schemas');
            node_schemas.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            var node_extensions = node_connection.createChildNode(
                'Extensions', false,
                '/static/OmniDB_app/images/extension.png', {
                    type: 'extension_list',
                    num_extensions: 0
                }, 'cm_extensions');
            node_extensions.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            var node_replication = node.createChildNode(
                'Replication Slots', false,
                '/static/OmniDB_app/images/replication.png', {
                    type: 'replication',
                }, null);
            var node_phyrepslots = node_replication.createChildNode(
                'Physical Replication Slots', false,
                '/static/OmniDB_app/images/repslot.png', {
                    type: 'physicalreplicationslot_list',
                    num_repslots: 0
                }, 'cm_physicalreplicationslots');
            node_phyrepslots.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            var node_logrepslots = node_replication.createChildNode(
                'Logical Replication Slots', false,
                '/static/OmniDB_app/images/repslot.png', {
                    type: 'logicalreplicationslot_list',
                    num_repslots: 0
                }, 'cm_logicalreplicationslots');
            node_logrepslots.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            if (parseInt(getMajorVersion(node.tree.tag.version)) >= 10) {
                var node_replication = node_connection.createChildNode(
                    'Logical Replication', false,
                    '/static/OmniDB_app/images/replication.png', {
                        type: 'replication',
                    }, null);
                var node_publications = node_replication.createChildNode(
                    'Publications', false,
                    '/static/OmniDB_app/images/publication.png', {
                        type: 'publication_list',
                        num_pubs: 0
                    }, 'cm_publications');
                node_publications.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                var node_subscriptions = node_replication.createChildNode(
                    'Subscriptions', false,
                    '/static/OmniDB_app/images/subscription.png', {
                        type: 'subscription_list',
                        num_subs: 0
                    }, 'cm_subscriptions');
                node_subscriptions.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }
            if (node.tree.tag.pglogical_version != null) {
                var node_pglogical = node_connection.createChildNode(
                    'pglogical', false,
                    '/static/OmniDB_app/images/replication.png', {
                        type: 'pglogical',
                    }, 'cm_pglogical');
                var node_nodes = node_pglogical.createChildNode(
                    'Nodes', false,
                    '/static/OmniDB_app/images/node.png', {
                        type: 'pglogical_node_list'
                    }, 'cm_pglogical_nodes');
                node_nodes.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                var node_repsets = node_pglogical.createChildNode(
                    'Replication Sets', false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'pglogical_repset_list'
                    }, 'cm_pglogical_repsets');
                node_repsets.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                var node_subscriptions = node_pglogical.createChildNode(
                    'Subscriptions', false,
                    '/static/OmniDB_app/images/subscription.png', {
                        type: 'pglogical_subscription_list'
                    }, 'cm_pglogical_subscriptions');
                node_subscriptions.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }
            if (node.tree.tag.bdr_version != null) {
                var node_bdr = node_connection.createChildNode(
                    'BDR', false,
                    '/static/OmniDB_app/images/bdr.png', {
                        type: 'bdr',
                    }, 'cm_bdr');
                node_bdr.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }
            if (node.tree.tag.version.indexOf('XL') !== -1) {
                var node_xl = node.createChildNode('Postgres-XL', false,
                    '/static/OmniDB_app/images/xl.png', {
                        type: 'xl',
                    }, 'cm_xl');
                var node_xl_nodes = node_xl.createChildNode('Nodes', false,
                    '/static/OmniDB_app/images/xlnode.png', {
                        type: 'xl_node_list',
                    }, 'cm_xlnodes');
                node_xl_nodes.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                var node_xl_groups = node_xl.createChildNode('Groups',
                    false,
                    '/static/OmniDB_app/images/xlgroup.png', {
                        type: 'xl_group_list',
                    }, 'cm_xlgroups');
                node_xl_groups.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (v_connTabControl.selectedTab.tag.firstTimeOpen) {
              v_connTabControl.selectedTab.tag.firstTimeOpen = false;
              v_connTabControl.tag.createMonitorDashboardTab();
              startMonitorDashboard();
            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_databases_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Databases (' + p_return.v_data.length + ')');

            node.tag.num_databases = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/db.png', {
                        type: 'database'
                    }, 'cm_database');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_tablespaces_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tablespaces (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/folder.png', {
                        type: 'tablespace'
                    }, 'cm_tablespace');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_roles_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Roles (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/role.png', {
                        type: 'role'
                    }, 'cm_role');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_extensions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Extensions (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/extension.png', {
                        type: 'extension'
                    }, 'cm_extension');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/table.png', {
                        type: 'table',
                        has_primary_keys: p_return.v_data[i].v_has_primary_keys,
                        has_foreign_keys: p_return.v_data[i].v_has_foreign_keys,
                        has_uniques: p_return.v_data[i].v_has_uniques,
                        has_indexes: p_return.v_data[i].v_has_indexes,
                        has_checks: p_return.v_data[i].v_has_checks,
                        has_excludes: p_return.v_data[i].v_has_excludes,
                        has_rules: p_return.v_data[i].v_has_rules,
                        has_triggers: p_return.v_data[i].v_has_triggers,
                        has_partitions: p_return.v_data[i].v_has_partitions
                    }, 'cm_table');

                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'table_field'
                    }, null);

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_schemas_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Schemas (' + p_return.v_data.length + ')');

            node.tag.num_schemas = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/schemas.png', {
                        type: 'schema',
                        num_tables: 0
                    }, 'cm_schema');

                var node_tables = v_node.createChildNode('Tables', false,
                    '/static/OmniDB_app/images/table_multiple.png', {
                        type: 'table_list',
                        schema: p_return.v_data[i].v_name,
                        num_tables: 0
                    }, 'cm_tables');
                node_tables.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

                var node_sequences = v_node.createChildNode('Sequences',
                    false,
                    '/static/OmniDB_app/images/sequence_list.png', {
                        type: 'sequence_list',
                        schema: p_return.v_data[i].v_name,
                        num_sequences: 0
                    }, 'cm_sequences');
                node_sequences.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

                var node_views = v_node.createChildNode('Views', false,
                    '/static/OmniDB_app/images/view_multiple.png', {
                        type: 'view_list',
                        schema: p_return.v_data[i].v_name,
                        num_views: 0
                    }, 'cm_views');
                node_views.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

                var node_views = v_node.createChildNode(
                    'Materialized Views', false,
                    '/static/OmniDB_app/images/view_multiple.png', {
                        type: 'mview_list',
                        schema: p_return.v_data[i].v_name,
                        num_views: 0
                    }, 'cm_mviews');
                node_views.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

                var node_functions = v_node.createChildNode('Functions',
                    false, '/static/OmniDB_app/images/gear2.png', {
                        type: 'function_list',
                        schema: p_return.v_data[i].v_name,
                        num_functions: 0
                    }, 'cm_functions');
                node_functions.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

                var node_triggerfunctions = v_node.createChildNode(
                    'Trigger Functions', false,
                    '/static/OmniDB_app/images/gear2.png', {
                        type: 'triggerfunction_list',
                        schema: p_return.v_data[i].v_name,
                        num_triggerfunctions: 0
                    }, 'cm_triggerfunctions');
                node_triggerfunctions.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_sequences_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                    '/static/OmniDB_app/images/sequence_list.png', {
                        type: 'sequence'
                    }, 'cm_sequence');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_views_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Views (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/view.png', {
                        type: 'view',
                        has_triggers: p_return.v_data[i].v_has_triggers
                    }, 'cm_view');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'view_field'
                    }, null);
            }
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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_views_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, '/static/OmniDB_app/images/add.png', null,
                null);

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, '/static/OmniDB_app/images/add.png', {
                        type: 'table_field'
                    }, null);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }

            if (node.tag.has_rules) {
                v_node = node.createChildNode('Rules', false,
                    '/static/OmniDB_app/images/rule.png', {
                        type: 'rule_list'
                    }, 'cm_rules');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_triggers) {
                v_node = node.createChildNode('Triggers', false,
                    '/static/OmniDB_app/images/trigger.png', {
                        type: 'trigger_list'
                    }, 'cm_view_triggers');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

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
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_mviews_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                    false, '/static/OmniDB_app/images/view.png', {
                        type: 'mview'
                    }, 'cm_mview');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'mview_field'
                    }, null);
            }
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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_mviews_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_column_name,
                    false, '/static/OmniDB_app/images/add.png', {
                        type: 'table_field'
                    }, null);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }

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
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_columns_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.text,
            "p_schema": node.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, '/static/OmniDB_app/images/add.png', {
                    type: 'column_list'
                }, 'cm_columns');

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, '/static/OmniDB_app/images/add.png', {
                        type: 'table_field'
                    }, 'cm_column');
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Nullable: ' + p_return.v_data[i].v_nullable,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }

            if (node.tag.has_primary_keys) {
                v_node = node.createChildNode('Primary Key', false,
                    '/static/OmniDB_app/images/key.png', {
                        type: 'primary_key'
                    }, 'cm_pks');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_foreign_keys) {
                v_node = node.createChildNode('Foreign Keys', false,
                    '/static/OmniDB_app/images/silver_key.png', {
                        type: 'foreign_keys'
                    }, 'cm_fks');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_uniques) {
                v_node = node.createChildNode('Uniques', false,
                    '/static/OmniDB_app/images/blue_key.png', {
                        type: 'uniques'
                    }, 'cm_uniques');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_checks) {
                v_node = node.createChildNode('Checks', false,
                    '/static/OmniDB_app/images/check.png', {
                        type: 'check_list'
                    }, 'cm_checks');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_excludes) {
                v_node = node.createChildNode('Excludes', false,
                    '/static/OmniDB_app/images/exclude.png', {
                        type: 'exclude_list'
                    }, 'cm_excludes');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_indexes) {
                v_node = node.createChildNode('Indexes', false,
                    '/static/OmniDB_app/images/index.png', {
                        type: 'indexes'
                    }, 'cm_indexes');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_rules) {
                v_node = node.createChildNode('Rules', false,
                    '/static/OmniDB_app/images/rule.png', {
                        type: 'rule_list'
                    }, 'cm_rules');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_triggers) {
                v_node = node.createChildNode('Triggers', false,
                    '/static/OmniDB_app/images/trigger.png', {
                        type: 'trigger_list'
                    }, 'cm_triggers');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_partitions) {
                v_node = node.createChildNode('Partitions', false,
                    '/static/OmniDB_app/images/partition.png', {
                        type: 'partition_list'
                    }, 'cm_partitions');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tree.tag.bdr_version != null) {
                var node_bdr = node.createChildNode(
                    'BDR', false,
                    '/static/OmniDB_app/images/bdr.png', null, null);
                var node_bdr_repsets = node_bdr.createChildNode(
                    'Replication Sets', false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'bdr_table_repset_list',
                    }, 'cm_bdr_table_repsets');
                node_bdr_repsets.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                var node_bdr_confhands = node_bdr.createChildNode(
                    'Conflict Handlers', false,
                    '/static/OmniDB_app/images/conflict_handler.png', {
                        type: 'bdr_table_confhand_list',
                    }, 'cm_bdr_table_confhands');
                node_bdr_confhands.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tree.tag.version.indexOf('XL') !== -1) {
                var node_xl = node.createChildNode('Postgres-XL', false,
                    '/static/OmniDB_app/images/xl.png', {
                        type: 'xl_table',
                    }, 'cm_xl_table');
                node_xl.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pk_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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

            if (p_return.v_data.length > 0)
                v_node = node.createChildNode(p_return.v_data[0][0], false,
                    '/static/OmniDB_app/images/key.png', {
                        type: 'pk'
                    }, 'cm_pk');

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node.createChildNode(p_return.v_data[i][1], false,
                    '/static/OmniDB_app/images/add.png', null, null);

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_uniques_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Uniques (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_curr_fk = '';

            new_node = '';
            new_name = '';

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    if (v_curr_fk == '' || (p_return.v_data[i][0] !=
                            v_curr_fk && v_curr_fk != '')) {

                        v_curr_fk = p_return.v_data[i][0];

                        v_node = node.createChildNode(p_return.v_data[i][0],
                            false,
                            '/static/OmniDB_app/images/blue_key.png', {
                                type: 'unique'
                            }, 'cm_unique');

                    }

                    v_node.createChildNode(p_return.v_data[i][1], false,
                        '/static/OmniDB_app/images/add.png', null, null
                    );

                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_indexes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Indexes (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_curr_fk = '';

            new_node = '';
            new_name = '';

            var v_node;


            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    if (v_curr_fk == '' || (p_return.v_data[i][0] !=
                            v_curr_fk && v_curr_fk != '')) {

                        v_curr_fk = p_return.v_data[i][0];

                        v_node = node.createChildNode(p_return.v_data[i][0] +
                            ' (' + p_return.v_data[i][1] + ')', false,
                            '/static/OmniDB_app/images/index.png', {
                                type: 'index'
                            }, 'cm_index');

                    }

                    v_node.createChildNode(p_return.v_data[i][2], false,
                        '/static/OmniDB_app/images/add.png', null, null
                    );

                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_fks_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Foreign Keys (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_curr_fk = '';

            new_node = '';
            new_name = '';

            var v_node;

            for (i = 0; i < p_return.v_data.length; i++) {

                if (v_curr_fk == '' || (p_return.v_data[i][0] != v_curr_fk &&
                        v_curr_fk != '')) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false,
                        '/static/OmniDB_app/images/silver_key.png', {
                            type: 'foreign_key'
                        }, 'cm_fk');
                    v_node.createChildNode('Referenced Table: ' + p_return.v_data[
                            i][2], false,
                        '/static/OmniDB_app/images/table.png', null,
                        null);
                    v_node.createChildNode('Delete Rule: ' + p_return.v_data[
                            i][4], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);
                    v_node.createChildNode('Update Rule: ' + p_return.v_data[
                            i][5], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);

                    v_curr_fk = p_return.v_data[i][0];

                }

                v_node.createChildNode(p_return.v_data[i][1] +
                    ' <img style="vertical-align: middle;" src="/static/OmniDB_app/images/arrow_right.png"/> ' +
                    p_return.v_data[i][3], false,
                    '/static/OmniDB_app/images/add.png', null, null);

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_checks_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                        false, '/static/OmniDB_app/images/check.png', {
                            type: 'check'
                        }, 'cm_check');
                    v_node.createChildNode(p_return.v_data[i][1], false,
                        '/static/OmniDB_app/images/text_edit.png', null,
                        null);

                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_excludes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                        false, '/static/OmniDB_app/images/exclude.png', {
                            type: 'exclude'
                        }, 'cm_exclude');
                    v_node.createChildNode('Attributes: ' + p_return.v_data[
                            i][1],
                        false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);
                    v_node.createChildNode('Operators: ' + p_return.v_data[
                            i][2],
                        false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);

                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_rules_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                        false, '/static/OmniDB_app/images/rule.png', {
                            type: 'rule'
                        }, 'cm_rule');

                }

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Triggers.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggersPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_triggers_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            node.setText('Triggers (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false, '/static/OmniDB_app/images/trigger.png', {
                            type: 'trigger'
                        }, 'cm_trigger');
                    v_node.createChildNode('Enabled: ' + p_return.v_data[i]
                        [1], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);
                    v_node.createChildNode('Function: ' + p_return.v_data[i]
                        [2], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);

                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_partitions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                        '/static/OmniDB_app/images/partition.png', {
                            type: 'partition'
                        }, 'cm_partition');

                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_functions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Functions (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/gear2.png', {
                        type: 'function',
                        id: p_return.v_data[i].v_id
                    }, 'cm_function');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'function_field'
                    }, null);

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_function_fields_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                        false, '/static/OmniDB_app/images/output.png', null,
                        null);
                else {
                    if (p_return.v_data[i].v_type == 'I')
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false, '/static/OmniDB_app/images/input.png',
                            null, null);
                    else
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false,
                            '/static/OmniDB_app/images/input_output.png',
                            null, null);
                }

            }

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
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_triggerfunctions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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
                    '/static/OmniDB_app/images/gear2.png', {
                        type: 'triggerfunction',
                        id: p_return.v_data[i].v_id
                    }, 'cm_triggerfunction');

            }

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
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_physicalreplicationslots_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Physical Replication Slots (' + p_return.v_data.length +
                ')');

            node.tag.num_repslots = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/repslot.png', {
                        type: 'physicalreplicationslot'
                    }, 'cm_physicalreplicationslot');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_logicalreplicationslots_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Logical Replication Slots (' + p_return.v_data.length +
                ')');

            node.tag.num_repslots = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/repslot.png', {
                        type: 'logicalreplicationslot'
                    }, 'cm_logicalreplicationslot');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_publications_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Publications (' + p_return.v_data.length + ')');

            node.tag.num_pubs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/publication.png', {
                        type: 'publication'
                    }, 'cm_publication');
                v_node.createChildNode('All Tables: ' + p_return.v_data[i].v_alltables,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Insert: ' + p_return.v_data[i].v_insert,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Update: ' + p_return.v_data[i].v_update,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Delete: ' + p_return.v_data[i].v_delete,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                if (p_return.v_data[i].v_alltables == 'False') {
                    v_tables = v_node.createChildNode('Tables',
                        false,
                        '/static/OmniDB_app/images/table_multiple.png', {
                            type: 'publication_table_list'
                        }, 'cm_pubtables');
                    v_tables.createChildNode('', true,
                        '/static/OmniDB_app/images/spin.svg', null,
                        null);
                }

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_publication_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_pub": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/table.png', {
                        type: 'pubtable'
                    }, 'cm_pubtable');

            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_subscriptions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Subscriptions (' + p_return.v_data.length + ')');

            node.tag.num_subs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/subscription.png', {
                        type: 'subscription'
                    }, 'cm_subscription');
                v_node.createChildNode('Enabled: ' + p_return.v_data[i].v_enabled,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('ConnInfo: ' + p_return.v_data[i].v_conninfo,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_publications = v_node.createChildNode(
                    'Referenced Publications',
                    false, '/static/OmniDB_app/images/publication.png', {
                        type: 'subpubs'
                    }, null);
                tmp = p_return.v_data[i].v_publications.split(',')
                for (j = 0; j < tmp.length; j++) {
                    v_publications.createChildNode(tmp[j],
                        false,
                        '/static/OmniDB_app/images/publication.png', {
                            type: 'subpub'
                        }, null);
                }
                v_tables = v_node.createChildNode('Tables',
                    false,
                    '/static/OmniDB_app/images/table_multiple.png', {
                        type: 'subscription_table_list'
                    }, null);
                v_tables.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

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
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_subscription_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_sub": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/table.png', {
                        type: 'subtable'
                    }, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalNodesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_nodes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Nodes (' + p_return.v_data.length + ')');

            node.tag.num_nodes = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/node.png', {
                        type: 'pglogical_node'
                    }, 'cm_pglogical_node');
                v_node.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Interfaces.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalInterfacesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_interfaces_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_node": node.text.replace(' (local)', '')
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/plug.png', {
                        type: 'pglogical_interface'
                    }, 'cm_pglogical_interface');
                v_node.createChildNode(p_return.v_data[i].v_dsn, true,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Replication Sets.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalReplicationSetsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_replicationsets_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Replication Sets (' + p_return.v_data.length +
                ')');

            node.tag.num_repsets = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'pglogical_repset'
                    }, 'cm_pglogical_repset');
                v_node.createChildNode('Insert: ' + p_return.v_data[i].v_insert,
                    true, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Update: ' + p_return.v_data[i].v_update,
                    true, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Delete: ' + p_return.v_data[i].v_delete,
                    true, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Truncate: ' + p_return.v_data[i].v_truncate,
                    true, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_tables = v_node.createChildNode('Tables',
                    false,
                    '/static/OmniDB_app/images/table_multiple.png', {
                        type: 'pglogical_repset_table_list'
                    }, 'cm_pglogical_repset_tables');
                v_tables.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                v_seqs = v_node.createChildNode('Sequences',
                    false,
                    '/static/OmniDB_app/images/sequence_list.png', {
                        type: 'pglogical_repset_seq_list'
                    }, 'cm_pglogical_repset_seqs');
                v_seqs.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Replication Set Tables.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalReplicationSetTablesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_repset_tables_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_repset": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/table.png', {
                        type: 'pglogical_repset_table'
                    }, 'cm_pglogical_repset_table');

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Replication Set Sequences.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalReplicationSetSequencesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_repset_seqs_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_repset": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Sequences (' + p_return.v_data.length + ')');

            node.tag.num_seqs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false,
                    '/static/OmniDB_app/images/sequence_list.png', {
                        type: 'pglogical_repset_seq'
                    }, 'cm_pglogical_repset_seq');

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Subscriptions.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalSubscriptionsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_subscriptions_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Subscriptions (' + p_return.v_data.length + ')');

            node.tag.num_subs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/subscription.png', {
                        type: 'pglogical_subscription'
                    }, 'cm_pglogical_subscription');
                v_node.createChildNode('Status: ' + p_return.v_data[i].v_status,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Provider: ' + p_return.v_data[i].v_origin,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Enabled: ' + p_return.v_data[i].v_enabled,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Apply Delay: ' + p_return.v_data[i]
                    .v_delay,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_repsets = v_node.createChildNode('Replication Sets',
                    false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'pglogical_subscription_repset_list'
                    }, 'cm_pglogical_subscription_repsets');
                v_repsets.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving pglogical Subscription Replication Sets.
/// </summary>
/// <param name="node">Node object.</param>
function getPglogicalSubscriptionReplicationSetsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pglogical_subscription_repsets_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_sub": node.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Replication Sets (' + p_return.v_data.length +
                ')');

            node.tag.num_repsets = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'pglogical_subscription_repset'
                    }, 'cm_pglogical_subscription_repset');

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving BDR Properties.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRPropertiesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_bdr_properties_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tree.contextMenu.cm_bdr.elements = []
            node.tree.contextMenu.cm_bdr.elements.push({
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreePostgresql(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            });

            if (p_return.v_data[0].v_node_name == 'Not set') {

                node.tree.contextMenu.cm_bdr.elements.push({
                    text: 'Create Group',
                    icon: '/static/OmniDB_app/images/text_edit.png',
                    action: function(node) {
                        tabSQLTemplate('Create Group', node.tree
                            .tag
                            .bdr_create_group);
                    }
                });
                node.tree.contextMenu.cm_bdr.elements.push({
                    text: 'Join Group',
                    icon: '/static/OmniDB_app/images/text_edit.png',
                    action: function(node) {
                        tabSQLTemplate('Join Group', node.tree.tag
                            .bdr_join_group);
                    }
                });
                node.tree.contextMenu.cm_bdr.elements.push({
                    text: 'Join Group Wait',
                    icon: '/static/OmniDB_app/images/text_edit.png',
                    action: function(node) {
                        tabSQLTemplate('Join Group Wait', node.tree
                            .tag
                            .bdr_join_wait);
                    }
                });
                node.tree.contextMenu.cm_bdr.elements.push({
                    text: 'Doc: BDR',
                    icon: '/static/OmniDB_app/images/globe.png',
                    action: function(node) {
                        v_connTabControl.tag.createWebsiteTab(
                            'Documentation: BDR',
                            'http://bdr-project.org/docs/1.0/index.html'
                        );
                    }
                });

            } else {

                if (!p_return.v_data[0].v_paused) {
                    node.tree.contextMenu.cm_bdr.elements.push({
                        text: 'Pause Apply',
                        icon: '/static/OmniDB_app/images/text_edit.png',
                        action: function(node) {
                            tabSQLTemplate('Pause Apply', node.tree
                                .tag.bdr_pause);
                        }
                    });
                } else {
                    node.tree.contextMenu.cm_bdr.elements.push({
                        text: 'Resume Apply',
                        icon: '/static/OmniDB_app/images/text_edit.png',
                        action: function(node) {
                            tabSQLTemplate('Resume Apply', node
                                .tree.tag.bdr_resume);
                        }
                    });
                }
                node.tree.contextMenu.cm_bdr.elements.push({
                    text: 'Replicate DDL',
                    icon: '/static/OmniDB_app/images/text_edit.png',
                    action: function(node) {
                        tabSQLTemplate('Replicate DDL Command',
                            node.tree.tag
                            .bdr_replicate_ddl_command);
                    }
                });

                if (getBDRMajorVersion(node.tree.tag.bdr_version) != '0') {

                    node.tree.contextMenu.cm_bdr.elements.push({
                        text: 'Remove BDR',
                        icon: '/static/OmniDB_app/images/text_edit.png',
                        action: function(node) {
                            tabSQLTemplate('Remove BDR', node.tree
                                .tag
                                .bdr_remove);
                        }
                    });
                }

                node.tree.contextMenu.cm_bdr.elements.push({
                    text: 'Doc: BDR',
                    icon: '/static/OmniDB_app/images/globe.png',
                    action: function(node) {
                        v_connTabControl.tag.createWebsiteTab(
                            'Documentation: BDR',
                            'http://bdr-project.org/docs/1.0/index.html'
                        );
                    }
                });

            }

            node.createChildNode('Version: ' + p_return.v_data[0]
                .v_version, false,
                '/static/OmniDB_app/images/bullet_red.png', null,
                null);
            node.createChildNode('Active: ' + p_return.v_data[0]
                .v_active, false,
                '/static/OmniDB_app/images/bullet_red.png', null,
                null);
            node.createChildNode('Node name: ' + p_return.v_data[0]
                .v_node_name, false,
                '/static/OmniDB_app/images/bullet_red.png', null,
                null);
            node.createChildNode('Paused: ' + p_return.v_data[0]
                .v_paused, false,
                '/static/OmniDB_app/images/bullet_red.png', null,
                null);
            v_nodes = node.createChildNode('Nodes',
                false, '/static/OmniDB_app/images/node.png', {
                    type: 'bdr_node_list'
                }, 'cm_bdrnodes');
            v_nodes.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);
            v_repsets = node.createChildNode('Replication Sets',
                false, '/static/OmniDB_app/images/replication_set.png', {
                    type: 'bdr_repset_list'
                }, 'cm_bdrrepsets');
            v_repsets.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving BDR Nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRNodesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_bdr_nodes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Nodes (' + p_return.v_data.length + ')');

            node.tag.num_nodes = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/node.png', {
                        type: 'bdr_node'
                    }, 'cm_bdrnode');

                v_node.tree.contextMenu.cm_bdrnode.elements = []
                v_node.tree.contextMenu.cm_bdrnode.elements.push({
                    text: 'Refresh',
                    icon: '/static/OmniDB_app/images/refresh.png',
                    action: function(node) {
                        if (node.childNodes == 0)
                            refreshTreePostgresql(node);
                        else {
                            node.collapseNode();
                            node.expandNode();
                        }
                    }
                });
                v_node.tree.contextMenu.cm_bdrnode.elements.push({
                    text: 'Part Node',
                    icon: '/static/OmniDB_app/images/tab_close.png',
                    action: function(node) {
                        tabSQLTemplate('Part Node', node.tree.tag
                            .bdr_part_node
                            .replace('#node_name#', v_node.text)
                        );
                    }
                });
                if (getBDRMajorVersion(node.tree.tag.bdr_version) != '0') {

                    v_node.tree.contextMenu.cm_bdrnode.elements.push({
                        text: 'Terminate Apply',
                        icon: '/static/OmniDB_app/images/text_edit.png',
                        action: function(node) {
                            tabSQLTemplate('Terminate Apply',
                                node.tree.tag
                                .bdr_terminate_apply
                                .replace('#node_name#',
                                    v_node.text));
                        }
                    });
                    v_node.tree.contextMenu.cm_bdrnode.elements.push({
                        text: 'Terminate WAL Sender',
                        icon: '/static/OmniDB_app/images/text_edit.png',
                        action: function(node) {
                            tabSQLTemplate(
                                'Terminate WAL Sender',
                                node.tree.tag
                                .bdr_terminate_walsender
                                .replace('#node_name#',
                                    v_node.text));
                        }
                    });
                }

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving BDR Replication Sets.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRReplicationSetsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_bdr_replicationsets_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Replication Sets (' + p_return.v_data.length +
                ')');

            node.tag.num_repsets = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'bdr_repset'
                    }, 'cm_bdrrepset');
                v_node.createChildNode('Inserts: ' + p_return.v_data[0]
                    .v_inserts, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Updates: ' + p_return.v_data[0]
                    .v_updates, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Deletes: ' + p_return.v_data[0]
                    .v_deletes, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving BDR Table Replication Sets.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRTableReplicationSetsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_bdr_table_replicationsets_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Replication Sets (' + p_return.v_data.length +
                ')');

            node.tag.num_repsets = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                node.createChildNode(p_return.v_data[i].v_name, false,
                    '/static/OmniDB_app/images/replication_set.png', {
                        type: 'bdr_table_repset'
                    }, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving BDR Table Conflict Handlers.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRTableConflictHandlersPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_bdr_table_conflicthandlers_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Conflict Handlers (' + p_return.v_data.length +
                ')');

            node.tag.num_chs = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false,
                    '/static/OmniDB_app/images/conflict_handler.png', {
                        type: 'bdr_table_confhand'
                    }, 'cm_bdr_table_confhand');
                v_node.createChildNode('Type: ' + p_return.v_data[i]
                    .v_type, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Function: ' + p_return.v_data[i]
                    .v_function, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving XL Nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getXLNodesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_xl_nodes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Nodes (' + p_return.v_data.length + ')');

            node.tag.num_nodes = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/xlnode.png', {
                        type: 'xlnode'
                    }, 'cm_xlnode');
                v_node.createChildNode('Type: ' + p_return.v_data[i]
                    .v_type, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Host: ' + p_return.v_data[i]
                    .v_host, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Port: ' + p_return.v_data[i]
                    .v_port, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Primary: ' + p_return.v_data[i]
                    .v_primary, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node.createChildNode('Preferred: ' + p_return.v_data[i]
                    .v_preferred, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving XL Groups.
/// </summary>
/// <param name="node">Node object.</param>
function getXLGroupsPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_xl_groups_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Groups (' + p_return.v_data.length + ')');

            node.tag.num_groups = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/xlgroup.png', {
                        type: 'xl_group'
                    }, 'cm_xlgroup');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null,
                    null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving XL Group Nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getXLGroupNodesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_xl_group_nodes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_group": node.text,
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText(node.text + ' (' + p_return.v_data.length +
                ' nodes)');

            node.tag.num_nodes = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/xlnode.png', null,
                    null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving XL Table Properties.
/// </summary>
/// <param name="node">Node object.</param>
function getXLTablePropertiesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_xl_table_properties_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": node.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            if (p_return.v_data.length > 0) {

                node.createChildNode('Distributed by: ' + p_return.v_data[0]
                    .v_distributed_by, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                node.createChildNode('Located in all nodes: ' + p_return.v_data[
                        0]
                    .v_all_nodes, false,
                    '/static/OmniDB_app/images/bullet_red.png', null,
                    null);
                v_node = node.createChildNode('Located in nodes', false,
                    '/static/OmniDB_app/images/xlnode.png', {
                        type: 'xl_table_node_list'
                    }, 'cm_xl_table_nodes');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);

            } else {

                node.createChildNode('Exists only in coordinator',
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }
        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving XL Table Nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getXLTableNodesPostgresql(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_xl_table_nodes_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.parent.text,
            "p_schema": node.parent.parent.parent.parent.text
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Located in nodes (' + p_return.v_data.length +
                ')');

            node.tag.num_nodes = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/xlnode.png', null,
                    'cm_xl_table_node');

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
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
            '/static/OmniDB_app/images/tab_close.png', {
                type: 'error',
                message: p_return.v_data
            }, null);
    }

}

function getMajorVersion(p_version) {
    var v_version = p_version.split(' (')[0]
    var tmp = v_version.replace('PostgreSQL ', '').replace('beta', '.').split(
        '.')
    tmp.pop()
    return tmp.join('.')
}

function getBDRMajorVersion(p_version) {
    return p_version.split('.')[0]
}

function postgresqlTerminateBackendConfirm(p_pid) {
    execAjax('/kill_backend_postgresql/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
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

    var v_query = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
        .getValue();

    if (v_query.trim() == '') {
        showAlert('Please provide a string.');
    } else {
        if (p_mode == 0)
            v_query = 'explain ' + v_query;
        else if (p_mode == 1)
            v_query = 'explain analyze ' + v_query;

        querySQL(0, true, v_query, getExplainReturn,false);
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
