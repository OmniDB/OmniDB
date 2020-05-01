var v_createConnTabFunction = function(p_index,p_create_query_tab = true) {

  if (v_connTabControl.tag.connections.length==0) {
    v_connTabControl.selectTabIndex(v_connTabControl.tabList.length-2);
    showAlert('Create connections first.');
  }
  else {

    v_connTabControl.removeLastTab();

    if (v_connTabControl.tabList.length === 0) {
      // Create the branding item for omnidb
      var v_tab = v_connTabControl.createTab({
        p_icon: `<svg class="omnidb-icon__theme--branding" height="27" viewBox="0 0 58 58" xmlns="http://www.w3.org/2000/svg">
                  <path d="M40.8635 21.9291C39.8124 20.2722 38.403 18.8703 36.7378 17.827C37.1953 18.7168 37.5976 19.6889 37.9355 20.7357C38.9901 21.0739 39.9683 21.4761 40.8635 21.9291Z" fill="#878FC6"/>
                  <path d="M30.6628 15.8552V19.5423C32.3082 19.5931 33.8876 19.7769 35.3722 20.0791C34.6859 18.4279 33.8104 17.0944 32.8125 16.1828C32.1155 16.0165 31.3987 15.9066 30.6628 15.8552Z" fill="#878FC6"/>
                  <path d="M40.8621 35.8357C39.9661 36.2894 38.9901 36.6916 37.9355 37.0269C37.5976 38.0759 37.1946 39.0466 36.7378 39.9377C38.4037 38.8937 39.8124 37.4919 40.8621 35.8357Z" fill="#878FC6"/>
                  <path d="M42.6299 31.4759C42.3757 30.9532 42.1965 30.3931 42.103 29.7986H39.1338C39.0829 31.4343 38.8987 33.0046 38.5984 34.4797C40.2586 33.7971 41.6001 32.925 42.5166 31.931C42.5534 31.7781 42.5995 31.6302 42.6299 31.4759Z" fill="#878FC6"/>
                  <path d="M42.5173 25.8359C41.6015 24.8398 40.26 23.9677 38.5977 23.283C38.898 24.7602 39.0821 26.3297 39.1331 27.9655H42.1022C42.1957 27.3709 42.3749 26.8109 42.6313 26.2903C42.5994 26.136 42.5534 25.9867 42.5173 25.8359Z" fill="#878FC6"/>
                  <path d="M36.9496 29.7986H30.6636V36.0492C32.6397 35.9844 34.5032 35.7146 36.1754 35.2785C36.6131 33.6153 36.8844 31.764 36.9496 29.7986Z" fill="#878FC6"/>
                  <path d="M30.6628 27.9663H36.9488C36.8837 26.0008 36.6124 24.1474 36.174 22.4842C34.5017 22.0481 32.6382 21.7783 30.6621 21.7135V27.9663H30.6628Z" fill="#878FC6"/>
                  <path d="M30.6628 41.9103C31.3987 41.8596 32.1148 41.749 32.8132 41.582C33.8112 40.669 34.6866 39.3369 35.3729 37.6857C33.8884 37.9865 32.3082 38.1696 30.6635 38.2204V41.9103H30.6628Z" fill="#878FC6"/>
                  <path d="M20.8935 34.4797C20.5911 33.0046 20.4069 31.435 20.3559 29.7986H16.6445C16.6948 30.5284 16.806 31.2399 16.9718 31.9303C17.889 32.9271 19.2312 33.7971 20.8935 34.4797Z" fill="#878FC6"/>
                  <path d="M28.8234 15.8552C28.0883 15.9059 27.3715 16.0165 26.6745 16.1828C25.6766 17.0944 24.8011 18.4286 24.1162 20.077C25.6008 19.7769 27.1788 19.5931 28.8234 19.5423V15.8552Z" fill="#878FC6"/>
                  <path d="M28.8234 21.7135C26.848 21.7783 24.9852 22.0481 23.3137 22.4842C22.8738 24.1474 22.604 26.0008 22.5388 27.9663H28.8234V21.7135Z" fill="#878FC6"/>
                  <path d="M22.7519 17.8256C21.0853 18.8689 19.6751 20.2714 18.6248 21.9269C19.5207 21.4739 20.4982 21.0717 21.5535 20.7357C21.8928 19.6874 22.2958 18.7146 22.7519 17.8256Z" fill="#878FC6"/>
                  <path d="M28.8234 41.9103V38.2204C27.1788 38.1696 25.5994 37.9865 24.1162 37.6857C24.8011 39.3376 25.6758 40.6712 26.6745 41.582C27.3722 41.7483 28.0883 41.8589 28.8234 41.9103Z" fill="#878FC6"/>
                  <path d="M16.6438 27.9662H20.3559C20.4062 26.3305 20.591 24.7602 20.8935 23.2837C19.2304 23.9663 17.8882 24.8405 16.971 25.8366C16.8053 26.527 16.6948 27.2378 16.6438 27.9662Z" fill="#878FC6"/>
                  <path d="M22.752 39.9392C22.2958 39.0481 21.8928 38.0774 21.5543 37.0291C20.4996 36.6924 19.5229 36.2902 18.627 35.8379C19.6766 37.4934 21.0861 38.8952 22.752 39.9392Z" fill="#878FC6"/>
                  <path d="M28.8234 29.7986H22.5388C22.604 31.764 22.8753 33.6153 23.3137 35.2785C24.9845 35.7146 26.848 35.9844 28.8234 36.0492V29.7986Z" fill="#878FC6"/>
                  <path d="M25.8068 10.1681C26.2615 10.95 26.5002 11.7926 26.5732 12.6372C27.6009 12.4392 28.6584 12.3286 29.7441 12.3286C37.0387 12.3286 43.2227 17.0027 45.4701 23.4971C46.245 23.1357 47.0999 22.9173 48.0128 22.9173C48.3181 22.9173 48.612 22.9624 48.9053 23.0068C46.3831 14.8619 38.7591 8.94092 29.7449 8.94092C28.2114 8.94092 26.7247 9.1283 25.2891 9.45235C25.4704 9.6813 25.656 9.90814 25.8068 10.1681Z" fill="#878FC6"/>
                  <path d="M15.4199 41.6361C15.8774 40.8507 16.4958 40.2223 17.1998 39.7376C14.6641 36.8444 13.1166 33.0713 13.1038 28.932C13.1038 28.9165 13.0996 28.901 13.0996 28.8841C13.0996 28.8707 13.1031 28.8587 13.1031 28.8453C13.1123 24.7073 14.6564 20.9364 17.187 18.0397C16.4858 17.5543 15.8739 16.9175 15.4185 16.1334C15.269 15.8756 15.1663 15.6072 15.0587 15.3395C11.7404 18.8984 9.69556 23.6485 9.69556 28.8841C9.69556 34.1224 11.7418 38.8725 15.0615 42.4293C15.1677 42.1624 15.2711 41.8925 15.4199 41.6361Z" fill="#878FC6"/>
                  <path d="M48.0121 34.8495C47.0991 34.8495 46.2421 34.6304 45.4679 34.2676C43.2191 40.7641 37.0387 45.4353 29.7441 45.4353C28.6569 45.4353 27.5973 45.3233 26.5689 45.1268C26.4959 45.9735 26.2629 46.8182 25.8096 47.6029C25.6594 47.8622 25.4753 48.0869 25.2939 48.3144C26.7268 48.6385 28.2128 48.8252 29.7441 48.8252C38.7591 48.8252 46.383 42.9056 48.9066 34.7607C48.6105 34.8037 48.3173 34.8495 48.0121 34.8495Z" fill="#878FC6"/>
                  <path d="M52.0317 28.8833C52.0317 26.6734 50.2334 24.8834 48.0115 24.8834C45.7896 24.8834 43.9863 26.6734 43.9863 28.8833C43.9863 31.0932 45.7896 32.8804 48.0115 32.8804C50.2334 32.8804 52.0317 31.0932 52.0317 28.8833Z" fill="#525678"/>
                  <path d="M18.6008 9.68901C16.6757 10.7922 16.0177 13.2345 17.1283 15.1507C18.2375 17.0633 20.6995 17.7184 22.6225 16.6152C24.5476 15.5106 25.2041 13.0612 24.095 11.1522C22.9809 9.23957 20.5252 8.5809 18.6008 9.68901Z" fill="#525678"/>
                  <path d="M18.6043 48.0832C20.5308 49.1878 22.9864 48.5334 24.097 46.6208C25.2062 44.7082 24.5475 42.2609 22.6259 41.1577C20.6994 40.051 18.2409 40.7076 17.1353 42.6188C16.0226 44.5349 16.6792 46.9808 18.6043 48.0832Z" fill="#525678"/>
                </svg>`,
        p_name: `<svg class="omnidb-icon__theme--branding" height="27" viewBox="0 0 133 58" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.8526 21.4207H15.0254C11.1455 21.4207 8 24.8352 8 29.0471C8 33.2612 11.1455 36.6757 15.0254 36.6757H22.8526C26.734 36.6757 29.8795 33.2612 29.8795 29.0471C29.8795 24.8345 26.734 21.4207 22.8526 21.4207ZM21.271 33.2118H16.607C14.2952 33.2118 12.4204 31.3486 12.4204 29.0471C12.4204 26.7478 14.2945 24.8845 16.607 24.8845H21.271C23.5843 24.8845 25.4577 26.7485 25.4577 29.0471C25.4584 31.3486 23.5843 33.2118 21.271 33.2118Z" fill="#878FC6"/>
                  <path d="M52.2109 23.7824C51.7439 22.2256 50.9429 21.4169 49.5109 21.4169C48.5809 21.4169 47.4339 21.712 46.8079 22.9406C45.6479 25.216 43.1874 30.1549 43.1874 30.1549C43.1874 30.1549 40.7339 25.2435 39.573 22.9681C38.9469 21.7388 37.7931 21.4169 36.8638 21.4169C35.4324 21.4169 34.6321 22.2256 34.1639 23.7824C33.7 25.328 30.4199 36.4366 30.4199 36.4366H34.9281L37.2768 27.4738C37.2768 27.4738 38.4355 30.5748 39.4916 33.0693C40.2183 34.7867 41.7559 35.4046 43.0238 35.4046C44.2916 35.4046 45.5389 34.8375 46.4529 33.2116C47.5729 31.2229 49.0979 27.4005 49.0979 27.4005L51.4459 36.4366H55.9539C55.9539 36.4366 52.6749 25.3287 52.2109 23.7824Z" fill="#878FC6"/>
                  <path d="M57.6339 36.4366C57.6339 36.4366 57.6339 25.3689 57.6339 24.1783C57.6339 22.9871 58.4759 21.4169 59.9319 21.4169C61.3879 21.4169 62.5749 22.7335 63.2519 23.3393C63.9299 23.9452 71.3249 30.5163 71.3249 30.5163V21.6599H75.2899C75.2899 21.6599 75.2899 32.6706 75.2899 34.0302C75.2899 35.3898 74.4459 36.6796 72.7579 36.6796C71.0699 36.6796 70.2499 35.6391 69.1759 34.5719C68.1029 33.5046 61.7879 27.0067 61.7879 27.0067V36.438H57.6339V36.4366Z" fill="#878FC6"/>
                  <path d="M82.0319 21.6599H78.0659V36.4373H82.0319V21.6599Z" fill="#878FC6"/>
                  <path d="M84.8739 27.2261C84.8739 27.2261 84.8739 33.5598 84.8739 34.4644C84.8739 35.3689 85.2319 36.4368 86.7609 36.4368C88.2899 36.4368 91.1979 36.4368 94.8219 36.4368C98.4459 36.4368 103.774 33.5901 103.774 28.9048C103.774 24.2194 99.5759 21.6602 94.6979 21.6602C89.8199 21.6602 87.8059 21.6602 87.8059 21.6602L84.8749 25.5037C84.8749 25.5037 90.8709 25.5037 94.8229 25.5037C98.7749 25.5037 99.2219 28.2412 99.2219 29.1034C99.2219 29.9657 98.5889 32.637 94.8229 32.637C91.0569 32.637 89.4929 32.637 89.4929 32.637V27.2261H84.8739Z" fill="#515579"/>
                  <path d="M122.871 28.8383C122.871 28.8383 124.892 27.8542 124.892 25.7457C124.892 23.6373 123.387 21.6592 119.053 21.6592C114.718 21.6592 109.213 21.6592 109.213 21.6592L106.104 25.5027C106.104 25.5027 117.651 25.5027 118.794 25.5027C119.938 25.5027 120.54 25.7521 120.54 26.4516C120.54 27.1511 119.997 27.4463 118.724 27.4463C117.449 27.4463 106.105 27.4463 106.105 27.4463C106.105 27.4463 106.105 33.1249 106.105 34.102C106.105 35.0791 106.564 36.4359 109.294 36.4359C112.025 36.4359 116.689 36.4359 119.163 36.4359C121.635 36.4359 125.198 35.0812 125.198 32.3282C125.196 29.5766 122.871 28.8383 122.871 28.8383ZM118.685 32.6367C117.449 32.6367 110.722 32.6367 110.722 32.6367V30.6051C110.722 30.6051 117.75 30.6051 118.794 30.6051C119.838 30.6051 120.605 30.6544 120.605 31.5998C120.605 32.5451 119.923 32.6367 118.685 32.6367Z" fill="#515579"/>
                </svg>`,
        p_close: false,
        p_selectable: false,
        p_clickFunction: function(e) {
          return startConnectionManagement();
        }
      });
    }

    var v_tab = v_connTabControl.createTab({
      p_icon: '<img src="' + v_url_folder + '/static/OmniDB_app/images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/>',
      p_name: '<span id="tab_title">' + v_connTabControl.tag.connections[0].v_alias + '</span>',
      p_selectFunction: function() {
        document.title = 'OmniDB'
        if(this.tag != null) {
          checkTabStatus(this);
          refreshHeights(true);
        }
        if(this.tag != null && this.tag.tabControl != null && this.tag.tabControl.selectedTab.tag.editor != null) {
            this.tag.tabControl.selectedTab.tag.editor.focus();
        }
      },
      p_closeFunction: function(e,p_tab) {
        var v_this_tab = p_tab;
        beforeCloseTab(e,
          function() {
            var v_tabs_to_remove = [];
            for (var i=0; i < v_connTabControl.selectedTab.tag.tabControl.tabList.length; i++) {

              var v_tab = v_connTabControl.selectedTab.tag.tabControl.tabList[i];
              if (v_tab.tag!=null) {
                if (v_tab.tag.mode=='query' || v_tab.tag.mode=='edit' || v_tab.tag.mode=='debug' || v_tab.tag.mode=='console') {
                  var v_message_data = { tab_id: v_tab.tag.tab_id, tab_db_id: null };
                  if (v_tab.tag.mode=='query')
                    v_message_data.tab_db_id = v_tab.tag.tab_db_id;
                  v_tabs_to_remove.push(v_message_data);
                }
                else if (v_tab.tag.mode=='monitor_dashboard') {
                  v_tab.tag.tab_active = false;
                  cancelMonitorUnits(v_tab.tag);
                }
              }

              if (v_tab.tag.tabCloseFunction)
                v_tab.tag.tabCloseFunction(v_tab.tag);
            }
            if (v_tabs_to_remove.length>0)
              sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CloseTab, v_tabs_to_remove, false, null);
            v_this_tab.removeTab();
          });
      }
    });

    v_connTabControl.selectTab(v_tab);

    var v_width = Math.ceil((300/window.innerWidth)*100);
    var v_complement_width = 100 - v_width;

    var v_html =
    "<div class='container-fluid' style='position: relative;'>" +
      "<div class='row'>" +
        "<div id='" + v_tab.id + "_div_left' class='omnidb__workspace__div-left col-md-2'>" +
          "<div class='row'>" +

            // "<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +


            "<div class='omnidb__workspace__content-left'>" +
              "<div id='" + v_tab.id + "_details' class='connection_details' ></div>" +
              "<div id='" + v_tab.id + "_tree' style='margin-top: 5px; overflow: auto; flex-grow: 1;'></div>" +
              "<div id='" + v_tab.id + "_left_resize_line_horizontal' onmousedown='resizeTreeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
              "<div id='tree_tabs_parent_" + v_tab.id + "' class='omnidb__tree-tabs' style='position: relative;flex-shrink: 0;flex-basis: 40vh;'>" +
                "<div id='" + v_tab.id + "_loading' class='div_loading' style='z-index: 1000;'>" +

                '<div class="div_loading_cover"></div>' +
                '<div class="div_loading_content">' +
                '  <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">' +
                '    <span class="sr-only ">Loading...</span>' +
                '  </div>' +
                '</div>' +
                "</div>" +
                "<button type='button' onclick='toggleTreeTabsContainer(" + '"tree_tabs_parent_' + v_tab.id + '","' + v_tab.id + '_left_resize_line_horizontal"' + ")' class='btn btn-secondary omnidb__tree-tabs__toggler'><i class='fas fa-arrows-alt-v'></i></button>" +
                "<div id='tree_tabs_" + v_tab.id + "' class='omnidb__tree-tabs__container' style='position: relative;'></div>" +
              "</div>" +
            "</div>" +
          "</div>" +
        "</div>" +//.div_left
        "<div id='" + v_tab.id + "_div_right' class='omnidb__workspace__div-right col-md-10'>" +
          // "<div class='row'>" +
            "<div id='" + v_tab.id + "_tabs' class='w-100'></div>" +
          // "</div>" +
        "</div>" +//.div_right
      "</div>" +//.row

      "<div id='" + v_tab.id + "_workspace_resize_grid' class='omnidb__workspace-resize-grid'>" +
        "<div class='container-fluid h-100'>" +
          "<div class='row h-100'>" +

            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +

            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'>" +
              "<div id='"+ v_tab.id + "_workspace_resize_draggable' ondragstart='dragStart(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragend='dragEnd(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' draggable='true' class='omnidb__workspace-resize-grid__draggable' style='width: 30px; height: 100%; cursor: ew-resize;'>" +
                "<div class='resize_line_vertical'><span>&#8633;</span></div>" +
              "</div>" +
            "</div></div>" +

            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
            "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +

          "</div>" +
        "</div>" +
      "</div>" +

    "</div>";

    var v_tab_title_span = document.getElementById('tab_title');
    v_tab_title_span.id = 'tab_title_' + v_tab.id;

    v_tab.elementDiv.innerHTML = v_html;

    // Tab control under the tree
    var v_treeTabs = createTabControl({ p_div: 'tree_tabs_' + v_tab.id });

    // Functions called when Properties and DDL tabs are clicked on
    var v_selectPropertiesTabFunc = function() {
      v_treeTabs.selectTabIndex(0);
      v_connTabControl.selectedTab.tag.currTreeTab = 'properties';
      refreshTreeHeight();
    }

    var v_selectDDLTabFunc = function() {
      v_treeTabs.selectTabIndex(1);
      v_connTabControl.selectedTab.tag.currTreeTab = 'ddl';
      refreshTreeHeight();
    }

    var v_properties_tab = v_treeTabs.createTab(
      {
        p_name: 'Properties',
        p_close: false,
        p_clickFunction: function(e) {
          v_selectPropertiesTabFunc();
        }
      });
    var v_ddl_tab = v_treeTabs.createTab(
      {
        p_name: 'DDL',
        p_close: false,
        p_clickFunction: function(e) {
          v_selectDDLTabFunc();
        }
      });
    v_treeTabs.selectTabIndex(0);

    // Tab control on the right (for queries, consoles, etc)
    // var v_currTabControl = createTabControl({ p_div: v_tab.id + '_tabs' });
    var v_currTabControl = createTabControl({
      p_div: v_tab.id + '_tabs',
      p_hierarchy: 'secondary'
    });
    v_currTabControl.createTab(
      {
        p_name: '+',
        p_close: false,
        p_selectable: false,
        p_clickFunction: function(e) {
          showMenuNewTab(e);
        }
      });

    //DDL editor
    var v_ddl_div = v_ddl_tab.elementDiv;

    var langTools = ace.require("ace/ext/language_tools");
    var v_editor = ace.edit(v_ddl_tab.elementDiv);
    v_editor.$blockScrolling = Infinity;
    v_editor.setTheme("ace/theme/" + v_editor_theme);
    v_editor.session.setMode("ace/mode/sql");

    v_editor.setFontSize(Number(v_editor_font_size));

    v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.commands.bindKey("Ctrl-Up", null)
    v_editor.commands.bindKey("Ctrl-Down", null)
    v_editor.setReadOnly(true);

    v_ddl_div.onclick = function() {
      v_editor.focus();
    };

    //Properties Grid
    var v_divProperties = v_properties_tab.elementDiv;
    v_divProperties.classList.add('ht_invisible')
    v_divProperties.style.overflow = 'hidden';
    var v_ddlProperties = v_ddl_tab.elementDiv;

    var columnProperties = [];

    var col = new Object();
    col.title =  'Property';
    col.readOnly = true;
    columnProperties.push(col);

    var col = new Object();
    col.title =  'Value';
    col.readOnly = true;
    columnProperties.push(col);

    var ht = new Handsontable(v_divProperties,
                        {
                          licenseKey: 'non-commercial-and-evaluation',
                          data: [],
                          columns : columnProperties,
                          colHeaders : true,
                          stretchH: 'all',
                          autoColumnSize : true,
                          manualColumnResize: false,
                          minSpareCols :0,
                          minSpareRows :0,
                          fillHandle:false,
                          disableVisualSelection: true,
                          contextMenu: {
                            callback: function (key, options) {
                              if (key === 'view_data') {
                                  editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),false);
                              }
                              else if (key === 'copy') {
                                this.selectCell(options[0].start.row,options[0].start.col,options[0].end.row,options[0].end.col);
                                document.execCommand('copy');
                              }
                            },
                            items: {
                              "copy": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-copy cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Copy</div>'},
                              "view_data": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
                            }
                          },
                          cells: function (row, col, prop) {

                            var cellProperties = {};
                            cellProperties.renderer = whiteHtmlRenderer;
                            return cellProperties;

                          }
                        });

    var v_tag = {
      tab_id: v_tab.id,
      tabControl: v_currTabControl,
      tabTitle: v_tab_title_span,
      divDetails: document.getElementById(v_tab.id + '_details'),
      divTree: document.getElementById(v_tab.id + '_tree'),
      divTreeTabs: document.getElementById('tree_tabs_parent_' + v_tab.id),
      divProperties: v_divProperties,
      gridProperties: ht,
      gridPropertiesCleared: true,
      divDDL: v_ddlProperties,
      divLoading: document.getElementById(v_tab.id + '_loading'),
      divLeft: document.getElementById(v_tab.id + '_div_left'),
      divRight: document.getElementById(v_tab.id + '_div_right'),
      selectedDatabaseIndex: 0,
      connTabControl: v_connTabControl,
      mode: 'connection',
      firstTimeOpen: true,
      TreeTabControl: v_treeTabs,
      currTreeTab: null,
      ddlEditor: v_editor,
      consoleHistoryFecthed: false,
      consoleHistoryList: null
    };

    v_tab.tag = v_tag;

    v_tag.selectPropertiesTabFunc = v_selectPropertiesTabFunc;
    v_tag.selectDDLTabFunc = v_selectDDLTabFunc;

    var v_index = v_connTabControl.tag.connections[0].v_conn_id;
    if (p_index)
      v_index = p_index;

    changeDatabase(v_index);

    if (p_create_query_tab) {
       v_connTabControl.tag.createConsoleTab();
       v_connTabControl.tag.createQueryTab();
    }

    // Creating + tab in the outer tab list
    v_connTabControl.createTab(
      {
        p_icon: "<i class='fas fa-plus'></i>",
        p_name: 'Add connection',
        p_close: false,
        p_selectable: false,
        p_clickFunction: function(e) {
          showMenuNewTabOuter(e);
        }
      });


    setTimeout(function() {
      v_selectPropertiesTabFunc();
    },10);

  }

  endLoading();

}
