function createTabControl(p_div, p_selected_index, p_contextMenu, p_tabColor) {

	var v_tabControl = {
		id: p_div,
		tabColor: p_tabColor,
		selectedTab: null,
		selectedDiv: null,
		selectedLi: null,
		elementDiv : null,
		tabList : [],
		elementUl : null,
		contextMenu: p_contextMenu,
		contextMenuDiv: null,
		tabCounter : 0,
		tag: new Object(),
		selectTabIndex : function(p_index) {


			if (this.selectedTab!=null)
				this.selectedTab.selected = false;

			this.tabList[p_index].selected = true;

			this.selectedTab = this.tabList[p_index];

			if (this.selectedDiv!=null) {
				this.selectedDiv.className = 'tab';
				this.selectedLi.className = '';
			}

			this.tabList[p_index].elementLi.className = 'selected';

			this.tabList[p_index].elementDiv.className = 'tab selected_div';

			this.selectedLi = this.tabList[p_index].elementLi;
			this.selectedDiv = this.tabList[p_index].elementDiv;

		},
		selectTab : function(p_tab) {

			if (this.selectedTab!=p_tab) {


				if (this.selectedTab!=null)
					this.selectedTab.selected = false;

				p_tab.selected = true;

				this.selectedTab = p_tab;

				if (this.selectedDiv!=null) {
					this.selectedDiv.className = 'tab';
					this.selectedLi.className = '';
				}

				p_tab.elementLi.className = 'selected';

				p_tab.elementDiv.className = 'tab selected_div';

				this.selectedLi = p_tab.elementLi;
				this.selectedDiv = p_tab.elementDiv;
			}

		},
		removeTabIndex : function(p_index) {
			var v_tab = this.tabList[p_index];

			v_tab.elementDiv.parentNode.removeChild(v_tab.elementDiv);
			v_tab.elementLi.parentNode.removeChild(v_tab.elementLi);

			this.tabList.splice(p_index, 1);
		},
		removeTab : function(p_tab) {

			var v_tab = p_tab;

			v_tab.elementDiv.parentNode.removeChild(v_tab.elementDiv);
			v_tab.elementLi.parentNode.removeChild(v_tab.elementLi);

			var v_index = this.tabList.indexOf(p_tab);

			if (v_index > 0)
				this.selectTabIndex(v_index-1);
			else if (this.tabList[v_index+1]!=null)
				this.selectTabIndex(v_index+1);

			this.tabList.splice(this.tabList.indexOf(p_tab), 1);


		},
		renameTab : function(p_tab,p_name) {

			var v_span = p_tab.elementLi.childNodes[0];
			v_span.innerHTML = p_name;

			p_tab.text = p_name;

		},
		createTab : function(p_name,p_close,p_clickFunction,p_dblClickFunction,p_contextMenu, p_deleteFunction) {

			var v_control = this;
			var v_index = this.tabCounter;

			this.tabCounter++;

			var v_tab = {
				id : p_div + '_tab' + v_index,
				text: p_name,
				selected : false,
				elementLi : null,
				elementDiv : null,
				tag: null,
				clickFunction: p_clickFunction,
				dblClickFunction : p_dblClickFunction,
				deleteFunction: p_deleteFunction,
				contextMenu : p_contextMenu,
				removeTab: function() { v_control.removeTab(this); },
				renameTab: function(p_name) { v_control.renameTab(this,p_name); }
			};

			if (p_close) {
				var v_li = createSimpleElement('li',p_div + '_tab' + v_index,null);

				var v_img = createImgElement(null,null,'images/tab_close.png');
				v_img.onclick = function() {
					showConfirm('Are you sure you want to remove this tab?',
	                    function() {

	                      if (v_tab.deleteFunction!=null)
						    v_tab.deleteFunction(v_tab);

	                      v_tab.removeTab();
	                    });
				};

				v_li.innerHTML = '<span>' + p_name + '</span>';
				v_li.appendChild(v_img);
			}
			else {
				var v_li = createSimpleElement('li',p_div + '_tab' + v_index,null);
				v_li.innerHTML = '<span>' + p_name + '</span>';
			}

			if (this.tabColor!=null)
				v_li.style['background-color'] = this.tabColor;

			v_li.oncontextmenu = function(e) {
				v_control.selectTab(v_tab);
				v_control.tabContextMenu(e,v_tab);
			};

			v_li.ondblclick = function(e) {

				if (v_tab.dblClickFunction!=null)
					v_tab.dblClickFunction(v_tab);
			};

			var v_div = createSimpleElement('div','div_' + p_div + '_tab' + v_index,'tab');

			if (this.tabColor!=null)
				v_div.style['background-color'] = this.tabColor;

			v_tab.elementLi = v_li;
			v_tab.elementDiv = v_div;

			v_li.onclick = function() {

				v_control.selectTab(v_tab);

				if (v_tab.clickFunction!=null)
					v_tab.clickFunction();
			};

			this.elementUl.appendChild(v_li);
			this.elementDiv.appendChild(v_div);

			this.tabList.push(v_tab);

			return v_tab;
		},
		tabContextMenu: function(p_event,p_tag) {
			if (p_event.button==2) {
				p_event.preventDefault();
				p_event.stopPropagation();
				if (p_tag.contextMenu!=undefined) {

					var v_tree = this;

					var v_menu = this.contextMenu[p_tag.contextMenu];

					var v_div;
					if (this.contextMenuDiv==null) {
						v_div = createSimpleElement('ul','ul_cm','menu');
						document.body.appendChild(v_div);
					}
					else
						v_div = this.contextMenuDiv;

					var v_closediv = createSimpleElement('div',null,'div_close_cm');
					v_closediv.onclick = function() {
						if (v_tree.contextMenuDiv!=null)
							v_tree.contextMenuDiv.style.display = 'none';
							this.parentNode.removeChild(this);
					};
					v_closediv.oncontextmenu = function(e) {
						e.preventDefault();
						e.stopPropagation();
						if (v_tree.contextMenuDiv!=null)
							v_tree.contextMenuDiv.style.display = 'none';
							this.parentNode.removeChild(this);
					};
					document.body.appendChild(v_closediv);

					v_div.innerHTML = '';

					var v_left = p_event.pageX-5;
					var v_right = p_event.pageY-5;

					v_div.style.display = 'block';
					v_div.style.position = 'absolute';
					v_div.style.left = v_left + 'px';
					v_div.style.top = v_right + 'px';

					for (var i=0; i<v_menu.elements.length; i++) (function(i){

						var v_li = createSimpleElement('li',null,null);

						var v_span = createSimpleElement('span',null,null);
						v_span.onclick = function () {
							if (v_tree.contextMenuDiv!=null)
							v_tree.contextMenuDiv.style.display = 'none';
							v_closediv.parentNode.removeChild(v_closediv);

							v_menu.elements[i].action(p_tag);
						};

						var v_a = createSimpleElement('a',null,null);
						var v_ul = createSimpleElement('ul',null,'sub-menu');

						v_a.appendChild(document.createTextNode(v_menu.elements[i].text));

						v_li.appendChild(v_span);

						if (v_menu.elements[i].icon!=undefined) {
							var v_img = createImgElement('null','null',v_menu.elements[i].icon);
							v_li.appendChild(v_img);
						}

						v_li.appendChild(v_a);

						v_div.appendChild(v_li);

						if (v_menu.elements[i].submenu!=undefined) {
							v_li.appendChild(v_ul);
							var v_span_more = createSimpleElement('div',null,null);
							v_span_more.appendChild(createImgElement(null,'menu_img','images/right.png'));
							v_li.appendChild(v_span_more);
							v_tree.contextMenuLi(v_menu.elements[i].submenu,v_ul,p_tag,v_closediv);
						}

					})(i);

					this.contextMenuDiv = v_div;

				}
			}
		},
		contextMenuLi : function(p_submenu,p_ul,p_tag,p_closediv) {

			var v_tree = this;

			for (var i=0; i<p_submenu.elements.length; i++) (function(i){

				var v_li = createSimpleElement('li',null,null);

				var v_span = createSimpleElement('span',null,null);
				v_span.onclick = function () {
					if (v_tree.contextMenuDiv!=null)
						v_tree.contextMenuDiv.style.display = 'none';
					p_closediv.parentNode.removeChild(p_closediv);

					p_submenu.elements[i].action(p_tag)
				};

				var v_a = createSimpleElement('a',null,null);
				var v_ul = createSimpleElement('ul',null,'sub-menu');

				v_a.appendChild(document.createTextNode(p_submenu.elements[i].text));

				v_li.appendChild(v_span);

				if (p_submenu.elements[i].icon!=undefined) {
					var v_img = createImgElement('null','null',p_submenu.elements[i].icon);
					v_li.appendChild(v_img);
				}

				v_li.appendChild(v_a);

				p_ul.appendChild(v_li);

				if (p_submenu.elements[i].p_submenu!=undefined) {
					v_li.appendChild(v_ul);
					var v_span_more = createSimpleElement('div',null,null);
					v_span_more.appendChild(createImgElement(null,'menu_img','images/right.png'));
					v_li.appendChild(v_span_more);
					v_tree.contextMenuLi(p_submenu.elements[i].p_submenu,v_ul,p_tag,p_closediv);
				}

			})(i);
		},
	};


	// Initializing existing Tabs
	var v_div = document.getElementById(p_div);
	v_div.className = 'div_tabs';

	v_tabControl.elementDiv = v_div;

	v_selected_counter = 0;

	// Initializing UL and LI elements
	for (var i=0; i<v_div.childNodes.length; i++) {
		if (v_div.childNodes[i].nodeName=='UL') {

			var v_ul = v_div.childNodes[i];
			v_ul.className = 'tabs';
			v_tabControl.elementUl = v_ul;

			var v_lis = v_ul.getElementsByTagName('li');

			for (var j=0; j<v_lis.length; j++) {


				var v_index = v_tabControl.tabCounter;
				v_tabControl.tabCounter++;


				var v_new_tab = {
					id : v_lis[j].id,
					text: null,
					selected : false,
					elementLi : null,
					elementDiv : null,
					tag : null,
					contextMenu: null
				};

				v_new_tab.elementLi = v_lis[j];

				if (p_tabColor!=null)
				v_lis[j].style['background-color'] = p_tabColor;

				var v_div = document.getElementById('div_' + v_lis[j].id);

				v_new_tab.elementDiv = v_div;
				v_new_tab.elementLi = v_lis[j];
				v_div.className = 'tab';

				if (p_tabColor!=null)
					v_div.style['background-color'] = p_tabColor;


				v_lis[j].oncontextmenu = function(x) {
			        v_tabControl.selectTab(x);
					v_tabControl.tabContextMenu(x);
			    }.bind(this, v_new_tab);;


				v_lis[j].onclick = function(x) {
			        v_tabControl.selectTab(x);
			    }.bind(this, v_new_tab);;


				v_selected_counter++;

				v_tabControl.tabList.push(v_new_tab);
			}


			break;
		}
	}

	v_tabControl.selectedTab = v_tabControl.tabList[p_selected_index];

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
