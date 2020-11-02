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

function composedPath(el) {
    var path = [];
    while (el) {
        path.push(el);
        if (el.tagName === 'HTML') {
            path.push(document);
            path.push(window);
            return path;
       }
       el = el.parentElement;
    }
}


/**
 * ## createTabControl
 * @desc Creates the `tabControl` with methods to manipulate the tab-system.
 *
 * @param  {string} { p_div   String for the ID of the target DOM element where the tabControl will create/remove tabs.
 * @param  {type} p_hierarchy Optional string defining the tab-system classes with OmniDB pre-defined styles ['primary', 'secondary',...].
 * The classes system refers to BEM practices implemented inside OmniDB: 'omnidb__tab-menu' (default base class), 'omnidb__tab-menu--primary', 'omnidb__tab-menu--secondary'.
 * - 'primary': OmniDB Outer Tabs. Results in the tab classlists containing 'omnidb__tab-menu omnidb__tab-menu--primary', 'omnidb__tab-content omnidb__tab-content--primary'
 * - 'secondary': OmniDB Inner Tabs. Results in the tab classlists containing 'omnidb__tab-menu omnidb__tab-menu--secondary', 'omnidb__tab-content omnidb__tab-content--secondary'
 * @param  {type} p_layout}   String defining some additional ready-to-use styles for the tab system.
 * - 'card': Adds a bootstrap based card style to the tab system, with the tab-menu inside the card-header and the tab-content inside the card-body.
 * @return {type} Returns the `tabControl` object.
 */
function createTabControl({ p_div, p_hierarchy, p_layout}) {

	// Get an element's exact position
	function getPosition(el) {
		var xPos = 0;
		var yPos = 0;

		while (el) {
			if (el.tagName == "BODY") {
				var xScroll = el.scrollLeft || document.documentElement.scrollLeft;
				var yScroll = el.scrollTop || document.documentElement.scrollTop;

				xPos += (el.offsetLeft - xScroll + el.clientLeft);
				yPos += (el.offsetTop - yScroll + el.clientTop);
			}
			else {
				xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
				yPos += (el.offsetTop - el.scrollTop + el.clientTop);
			}

			el = el.offsetParent;
		}

		return {
			x: xPos,
			y: yPos
		};
	}

  // Initializing HTML elements
	var v_div = document.getElementById(p_div);
  v_div.innerHTML = '';

  var v_nav = document.createElement('nav');
  var v_div_tab_list = document.createElement('div');
  v_div_tab_list.className = 'nav nav-tabs';
  v_nav.appendChild(v_div_tab_list);
  var v_div_tab_content_list = document.createElement('div');
  v_div_tab_content_list.className = 'tab-content omnidb__tab-content';

  var v_tab_menu = document.createElement('div');
  v_tab_menu.className = 'omnidb__tab-menu';

  var css_tab_menu_variations = [
    'omnidb__tab-menu--',
    'omnidb__theme-bg--menu-'
  ];
  // Adding classes based on variations and hierarchy.
  v_div.classList.add(css_tab_menu_variations[0] + 'container');
  if (p_hierarchy !== undefined) {
    v_div.classList.add(css_tab_menu_variations[0] + 'container--' + p_hierarchy);
    for (let i = 0; i < css_tab_menu_variations.length; i++) {
      v_tab_menu.classList.add(css_tab_menu_variations[i] + p_hierarchy);
    }
    v_div_tab_content_list.classList.add('omnidb__tab-content--' + p_hierarchy);
  }

  v_tab_menu.appendChild(v_nav);
  v_div.appendChild(v_tab_menu);
  v_div.appendChild(v_div_tab_content_list);

  if (p_layout === 'card') {
    v_div.classList.add('card');
    v_tab_menu.classList.add('card-header');
    v_tab_menu.classList.add('pb-0');
    v_div_tab_content_list.classList.add('card-body');
  }

	var v_tabControl = {
    // Params
		id: p_div,
		selectedTab: null,
		selectedDiv: null,
		selectedA: null,
    tabColor: null,
    tabCounter : 0,
		tabListContentDiv: v_div_tab_content_list,
		tabList: [],
		tabListDiv: v_div_tab_list,
    tabMenu: v_tab_menu,
    tabCssVariation: css_tab_menu_variations[0],
		tag: new Object(),
    isToggleable: (p_hierarchy === 'primary'),
    // Actions
    disableTabIndex : function(p_index) {
      this.tabList[p_index].elementA.classList.add('disabled');
		},
    enableTabIndex : function(p_index) {
      this.tabList[p_index].elementA.classList.remove('disabled');
		},
    disableSelectableTabIndex : function(p_index) {
      this.tabList[p_index].selectable = false;
		},
    enableSelectableTabIndex : function(p_index) {
      this.tabList[p_index].selectable = true;
		},
		selectTab : function(p_tab) {

			if (this.selectedTab!=p_tab) {
				if (p_tab.selectable) {

					if (this.selectedTab!=null)
						this.selectedTab.selected = false;

					p_tab.selected = true;

					this.selectedTab = p_tab;

					if (this.selectedDiv!=null) {
						this.selectedDiv.classList.remove('active');
						this.selectedA.classList.remove('active');
					}

					p_tab.elementA.classList.add('active');
					p_tab.elementDiv.classList.add('active');

					this.selectedA = p_tab.elementA;
					this.selectedDiv = p_tab.elementDiv;

					if(p_tab.selectFunction != null) {
						p_tab.selectFunction();
					}
				}
			}
		},
    selectTabIndex : function(p_index) {

			if (this.tabList[p_index].selectable) {

				if (this.selectedTab!=null)
					this.selectedTab.selected = false;

				this.tabList[p_index].selected = true;

				this.selectedTab = this.tabList[p_index];

        //$(this.tabList[p_index].elementA).tab('show');

				if (this.selectedDiv!=null) {
          this.selectedDiv.classList.remove('active');
          this.selectedA.classList.remove('active');
				}

				this.tabList[p_index].elementA.classList.add('active');
				this.tabList[p_index].elementDiv.classList.add('active');

				this.selectedA = this.tabList[p_index].elementA;
				this.selectedDiv = this.tabList[p_index].elementDiv;

				if(this.tabList[p_index].selectFunction != null) {
					this.tabList[p_index].selectFunction();
				}
			}

		},
    disableTab : function(p_tab) {
      p_tab.elementA.classList.add('disabled');
		},
    enableTab : function(p_tab) {
      p_tab.elementA.classList.remove('disabled');
		},
    disableSelectableTab : function(p_tab) {
      p_tab.selectable = false;
		},
    enableSelectableTab : function(p_tab) {
      p_tab.selectable = true;
		},
		disableClose : function(p_tab) {
			if (p_tab.elementClose!=null) {
				p_tab.elementClose.style.display = 'none';
			}
		},
		enableClose : function(p_tab) {
			if (p_tab.elementClose!=null) {
				p_tab.elementClose.style.display = '';
			}
		},
		removeTabIndex : function(p_index) {
			var v_tab = this.tabList[p_index];

      if (v_tab.closeFunction!=null) {
        v_tab.closeFunction(null,v_tab);
      }
      else if (v_tab) {
        this.removeTab(v_tab);
      }
		},
    removeLastTab : function() {
      var v_this = this
      var v_tab_index = v_this.tabList.length-1;

      this.removeTabIndex(v_tab_index);
		},
		removeTab : function(p_tab) {

			var v_tab = p_tab;

			v_tab.elementDiv.parentNode.removeChild(v_tab.elementDiv);
			v_tab.elementA.parentNode.removeChild(v_tab.elementA);

			var v_index = this.tabList.indexOf(p_tab);

      var v_current_index = this.tabList.indexOf(this.selectedTab);

      if (v_index == v_current_index) {
  			if (v_index > 0)
  				this.selectTabIndex(v_index-1);
  			else if (this.tabList[v_index+1]!=null)
  				this.selectTabIndex(v_index+1);
      }

			this.tabList.splice(this.tabList.indexOf(p_tab), 1);

      // When there are not outer tabs left to select, need to search and select or create a welcome tab.
      if (  (this === v_connTabControl) &&// Checking if the removed tab belongs to the outer menu.
            (v_connTabControl.tabList.indexOf(v_connTabControl.selectedTab) === -1)// Checking if there are no other tabs to select.
      ) {
        // Looking for a welcome tab
        var v_welcome_tab_index = false;
        for (let i = 0; i < v_connTabControl.tabList.length; i++) {
          if (v_connTabControl.tabList[i].tag) {
            if (v_connTabControl.tabList[i].tag.mode === 'welcome') {
              v_welcome_tab_index = i;
            }
          }
        }

        if (v_welcome_tab_index) {
          this.selectTabIndex(v_welcome_tab_index);
        }
        // Not forcing user to have a welcome tab.
        // else {
        //   v_connTabControl.tag.createWelcomeTab();
        // }
      }

		},
		renameTab : function(p_tab,p_name) {

      var v_tab_title_span = $(p_tab.elementA).find('.omnidb__tab-menu__link-name');
      if (v_tab_title_span) {
        v_tab_title_span.html(p_name);
      }

			p_tab.text = p_name;

		},
    dragEndFunction : function(e,p_tab) {
      let el = e.target;
      let el_pos = el.getBoundingClientRect();
      let el_index = $(el).index();

      let drop_pos_x = e.x;
      let drop_pos_y = e.y;

      let old_index = el_index;
      let new_index;

      let siblings = $(el).siblings();
      let total = siblings.length;
      for (let i = 0; i < total; i++) {
        let sibling = siblings[i];
        let sibling_pos = sibling.getBoundingClientRect();
        let sibling_pos_x = sibling_pos.x;
        let sibling_pos_x_center = sibling_pos_x + (sibling_pos.width / 2);
        let sibling_pos_x_end = sibling_pos_x + sibling_pos.width;
        let sibling_pos_y = sibling_pos.y;
        let sibling_pos_y_end = sibling_pos.y + sibling_pos.height;
        if (sibling_pos_y < drop_pos_y && drop_pos_y < sibling_pos_y_end && sibling_pos_x < drop_pos_x && drop_pos_x < sibling_pos_x_end) {
          var removedEl = p_tab.tabList.splice(old_index, 1)[0];
          if (drop_pos_x < sibling_pos_x_center) {
            new_index = i;
            p_tab.tabList.splice(new_index, 0, removedEl);
            sibling.before(el);
          }
          else {
            new_index = i + 1;
            p_tab.tabList.splice(new_index, 0, removedEl);
            sibling.after(el);
          }
        }
      }
    },
    hideTabMenu : function() {
      document.getElementById(p_div).classList.remove(this.tabCssVariation + 'container--menu-shown');
      this.tabMenu.classList.remove(this.tabCssVariation + 'shown');
    },
    showTabMenu : function() {
      document.getElementById(p_div).classList.add(this.tabCssVariation + 'container--menu-shown');
      this.tabMenu.classList.add(this.tabCssVariation + 'shown');
    },
    toggleTabMenu : function(e) {
      var v_this = this;
      $('#'+p_div).toggleClass(this.tabCssVariation + 'container--menu-shown');
      $(v_this.tabMenu).toggleClass(v_this.tabCssVariation + 'shown');
      // if (this.tabMenu === e.target)
      //   this.showTabMenu();
      // else
      //   this.hideTabMenu();
    },

		/**
      * ## createTab
      * @desc Creates a generic tab object with optional parameters and callbacks.
      * Ex: p_mode === 'customer_dashboard' expects data based on columns from customer tables, and will return all data necessary to kickoff a customer dashboard.
      *
      * @param  {function} p_clickFunction Callback for onclick.
      * @param  {boolean} p_close Defines if the elementA has a closing icon.
      * @param  {function} p_dblClickFunction  Callback for ondoubleclick.
      * @param  {boolean} p_disabled  Defines if the elementA is disabled.
      * @param  {string} p_icon HTML string is accepted as an optional icon.
      * @param  {boolean} p_isDraggable Defines if the elementA is draggable inside the tab-menu.
      * @param  {string} p_name HTML string is accepted as an optional name for the elementA.
      * @param  {function} p_rightClickFunction Callback for oncontextmenu.
      * @param  {function} p_selectFunction  Callback for after the tab-content is rendered.
      * @param  {boolean} p_selectable  Defines if the the tab-content is controlled by default bootstrap tab system selection. Used together with p_clickFunction to override the selecting tab behaviour, like the snippets panel.
      * @param  {string} p_tooltip_name  HTML string is accepted as an optional tooltip. This is bootstrap's default tooltip.
      * @param  {string} p_omnidb_tooltip_name  HTML string is accepted as an optional tooltip. This is OmniDB custom tooltip, used in the outer menu to avoid overflow bugs from bootstrap.
      * @return {oject} Creates the tab object in this tabControl.
		 */
		createTab : function({
      p_clickFunction = null,
      p_close = true,
      p_closeFunction = null,
      p_dblClickFunction = null,
      p_disabled = false,
      p_icon = false,
      p_isDraggable = true,
      p_name = '',
      p_rightClickFunction = false,
      p_selectFunction = null,
      p_selectable = true,
      p_tooltip_name = false,
      p_omnidb_tooltip_name = false
    }) {
			var v_control = this;
			var v_index = this.tabCounter;

			this.tabCounter++;

			var v_tab = {
				id : p_div + '_tab' + v_index + '_' + Date.now(),
				seq: v_index,
				text: p_name,
				selected : false,
				elementA : null,
				elementDiv : null,
				elementClose: null,
				tag: null,
				clickFunction: p_clickFunction,
				dblClickFunction : p_dblClickFunction,
				closeFunction: p_closeFunction,
				selectFunction: p_selectFunction,
				selectable: p_selectable,
        disabled: p_disabled,
				removeTab: function() { v_control.removeTab(this); },
				renameTab: function(p_name) { v_control.renameTab(this,p_name); },
				disableClose: function() { v_control.disableClose(this) },
				enableClose: function() { v_control.enableClose(this) },
        dragEndFunction: function(e,p_tab,p_index) { v_control.dragEndFunction(e,p_tab) },
				isDraggable: p_isDraggable
			};

      // Sets tabMenu toggle action based on page interaction
      // if (this.isToggleable && v_index === 1) {
      //   document.body.addEventListener("click", v_control.toggleTabMenu.bind(v_control));
      // }

			var v_a = document.createElement('a');
      v_a.setAttribute('id','a_' + v_tab.id);
      v_a.setAttribute('data-toggle','tab');
      v_a.setAttribute('role','tab');
      v_a.setAttribute('aria-selected','false');
      v_a.setAttribute('aria-selected','false');
      v_a.setAttribute('href','#' + 'div_' + v_tab.id);
      v_a.setAttribute('aria-controls','div_' + v_tab.id);

      if (v_tab.isDraggable) {
        v_a.setAttribute('draggable','true');
        v_a.ondragend = function(e) {
          e.stopPropagation();
          e.preventDefault();
          v_tab.dragEndFunction(e,this);
  			}.bind(this);
      }

      if (p_disabled) {
        v_a.className = 'omnidb__tab-menu__link nav-item nav-link disabled';
      }
      else {
        v_a.className = 'omnidb__tab-menu__link nav-item nav-link';
      }

      var v_close = document.createElement('i');
      v_close.className = 'fas fa-times tab-icon icon-close omnidb__tab-menu__link-close';

			v_tab.elementClose = v_close;

			v_close.onclick = function(e) {
        e.stopPropagation();
        e.preventDefault();
        if (v_tab.closeFunction!=null) {
          v_tab.closeFunction(e,v_tab);
        }
			};

      if (p_rightClickFunction) {
        v_a.oncontextmenu = function(e) {
          e.stopPropagation();
          e.preventDefault();
          p_rightClickFunction(e);
        }
      }

      var v_icon = (p_icon !== false) ? '<span class="omnidb__menu__btn omnidb__tab-menu__link-icon">' + p_icon + '</span>' : '';
      var v_name = (p_name !== undefined && p_name !== null && p_name !== '') ? p_name : '';

      if (p_tooltip_name) {
        getAttributesTooltip(v_a, p_tooltip_name, null, 'right');
      }
      else if (p_omnidb_tooltip_name) {
        getAttributesOmniDBTooltip(v_a, p_omnidb_tooltip_name, null, 'right');
      }
			v_a.innerHTML = '<span class="omnidb__tab-menu__link-content">' +
                        v_icon +
                        '<span class="omnidb__tab-menu__link-name">' + v_name + '<span>' +
                      '<span>';
      if (p_close) {
  			v_a.appendChild(v_close);
      }

			v_a.ondblclick = function(e) {

				if (v_tab.dblClickFunction!=null)
					v_tab.dblClickFunction(v_tab);
			};

			var v_div = document.createElement('div');
      v_div.className = 'tab-pane';
      v_div.setAttribute('id','div_' + v_tab.id);
      v_div.setAttribute('role','tabpanel');
      v_div.setAttribute('aria-labelledby','a_' + v_tab.id);


			v_tab.elementA = v_a;
			v_tab.elementDiv = v_div;

			v_a.onclick = function(e) {

        e.stopPropagation();
        e.preventDefault();
        if (v_tab.selectable) {
          v_control.selectTab(v_tab);
        }
				if (v_tab.clickFunction!=null) {
          v_tab.clickFunction(e);
        }
        // Hiding the tooltip on click if the has tooltips.
        if (p_tooltip_name) {
          $(v_a).tooltip('hide');
        }
			};

			this.tabListDiv.appendChild(v_a);

			this.tabListContentDiv.appendChild(v_div);

			this.tabList.push(v_tab);

			return v_tab;
		},
	};

	return v_tabControl;

}

//Create a HTML element specified by parameter 'p_type'
function createSimpleElement(p_type,p_id,p_class) {
	element = document.createElement(p_type);
	if (p_id!=undefined)
		element.id = p_id;
	if (p_class!=undefined)
		element.className = p_class;
	return element;
}

//Create img element
function createImgElement(p_id,p_class,p_src) {
	element = document.createElement('img');
	if (p_id!=undefined)
		element.id = p_id;
	if (p_class!=undefined)
		element.className = p_class;
	if (p_src!=undefined)
		element.src = p_src;
	return element;
}
