/*
Copyright 2015-2017 The OmniDB Team
This file is part of OmniDB.
OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function createTabControl(p_div, p_selected_index, p_contextMenu, p_tabColor) {

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

			if (this.tabList[p_index].selectable) {
				if (this.selectedTab!=null)
					this.selectedTab.selected = false;

				this.tabList[p_index].selected = true;

				this.selectedTab = this.tabList[p_index];

				if (this.selectedDiv!=null) {
					this.selectedDiv.className = 'tab';
					this.selectedLi.classList.remove('selected');
				}

				this.tabList[p_index].elementLi.classList.add('selected');

				this.tabList[p_index].elementDiv.className = 'tab selected_div';

				this.selectedLi = this.tabList[p_index].elementLi;
				this.selectedDiv = this.tabList[p_index].elementDiv;

				if(this.tabList[p_index].selectFunction != null) {
					this.tabList[p_index].selectFunction();
				}
			}

		},
		selectTab : function(p_tab) {

			if (this.selectedTab!=p_tab) {
				if (p_tab.selectable) {

					if (this.selectedTab!=null)
						this.selectedTab.selected = false;

					p_tab.selected = true;

					this.selectedTab = p_tab;

					if (this.selectedDiv!=null) {
						this.selectedDiv.className = 'tab';
						this.selectedLi.classList.remove('selected');
					}

					p_tab.elementLi.classList.add('selected');

					p_tab.elementDiv.className = 'tab selected_div';

					this.selectedLi = p_tab.elementLi;
					this.selectedDiv = p_tab.elementDiv;

					if(p_tab.selectFunction != null) {
						p_tab.selectFunction();
					}
				}
			}

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
		createTab : function(p_name,p_close,p_clickFunction,p_dblClickFunction,p_contextMenu, p_deleteFunction, p_isDraggable, p_selectFunction, p_selectable = true) {

			var v_control = this;
			var v_index = this.tabCounter;

			this.tabCounter++;

			var v_tab = {
				id : p_div + '_tab' + v_index,
				seq: v_index,
				text: p_name,
				selected : false,
				elementLi : null,
				elementDiv : null,
				elementClose: null,
				tag: null,
				clickFunction: p_clickFunction,
				dblClickFunction : p_dblClickFunction,
				deleteFunction: p_deleteFunction,
				contextMenu : p_contextMenu,
				selectFunction: p_selectFunction,
				selectable: p_selectable,
				removeTab: function() { v_control.removeTab(this); },
				renameTab: function(p_name) { v_control.renameTab(this,p_name); },
				disableClose: function() { v_control.disableClose(this) },
				enableClose: function() { v_control.enableClose(this) },
				setClickFunction: function(p_function) {

					this.clickFunction = p_function;
					var v_tab = this;
					v_li.onclick = function(e) {
						v_control.selectTab(v_tab);
						v_tab.clickFunction(e);
					};

				},
				isDraggable: p_isDraggable
			};

			var v_li = createSimpleElement('li',p_div + '_tab' + v_index,'original');

			var v_img = createSimpleElement('i',null,'fas fa-times tab-icon icon-close');

			v_tab.elementClose = v_img;

			v_img.onclick = function() {
				showConfirm('Are you sure you want to remove this tab?',
										function() {

											if (v_tab.deleteFunction!=null) {
												v_tab.deleteFunction(v_tab);
											}

											v_tab.removeTab();
										});
			};

			v_li.innerHTML = '<span>' + p_name + '</span>';
			v_li.appendChild(v_img);

			if (!p_close) {
				v_img.style.display = 'none';
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

			v_li.onclick = function(e) {

				v_control.selectTab(v_tab);

				if (v_tab.clickFunction!=null)
					v_tab.clickFunction(e);
			};

						if(typeof p_isDraggable != 'undefined' && p_isDraggable != null && p_isDraggable == true) {
				v_li.draggable = true;

				function handleDragStart(e) {
					var v_srcIndex = Array.prototype.indexOf.call(document.querySelectorAll('#' + v_tabControl.id + ' > ul > li'), this);
					gv_dragSrcTab = v_tabControl.tabList.splice(v_srcIndex, 1)[0];

					gv_dragSrcElement = this;
					var v_parentElement = gv_dragSrcElement.parentElement;

					setTimeout(function() {//Used because of bug in chrome during dragstart
							gv_dragSrcElement.style.display = 'none';

							gv_dragSrcElementFake = createSimpleElement('li', null, 'fake')
							gv_dragSrcElementFake.classList.add('fake');
							gv_dragSrcElementFake.innerHTML = gv_dragSrcElement.innerHTML;
							gv_dragSrcElement.parentElement.insertBefore(gv_dragSrcElementFake, gv_dragSrcElement);

							v_parentElement.removeChild(gv_dragSrcElement);
							v_parentElement.appendChild(gv_dragSrcElement);
						},
						10
					);
				}

				function handleDragOver(e) {
					if(e.path.length == 0) {
						return false;
					}

					if(typeof gv_dragSrcElement == 'undefined' || gv_dragSrcElement == null) {
						return false;
					}

					var v_found = false;
					var v_overElement;
					for(var i = 0; i < e.path.length && !v_found; i++) {
						if(typeof e.path[i].classList != 'undefined' && e.path[i].classList != null && e.path[i].classList.length != 0) {
							for(var j = 0; j < e.path[i].classList.length && !v_found; j++) {
								if(e.path[i].classList[j] == 'original') {
									if(e.path[i].parentElement.parentElement.id == gv_dragSrcElement.parentElement.parentElement.id) {
										v_found = true;
										v_overElement = e.path[i];
									}
								}
							}
						}
					}

					if(!v_found) {
						return false;
					}

					if(typeof gv_dragSrcElementFake == 'undefined' || gv_dragSrcElementFake == null) {
						return false;
					}

					if((v_overElement.offsetWidth - gv_dragSrcElementFake.offsetWidth) > 0) {
						v_overElementPosition = getPosition(v_overElement);

						if(e.pageX < (v_overElementPosition.x + ((v_overElement.offsetWidth - gv_dragSrcElementFake.offsetWidth) / 2)) ||
						   e.pageX > v_overElementPosition.x + (v_overElement.offsetWidth - ((v_overElement.offsetWidth - gv_dragSrcElementFake.offsetWidth) / 2))) {
						  	return false;
						}
					}

					if (e.preventDefault) {
						e.preventDefault(); // Allows dropping.
					}

					e.dataTransfer.dropEffect = 'move';
					var v_overIndex = Array.prototype.indexOf.call(this.parentElement.childNodes, this);
					var v_fakeIndex = Array.prototype.indexOf.call(this.parentElement.childNodes, gv_dragSrcElementFake);

					if(v_overIndex < v_fakeIndex) {
						this.parentElement.insertBefore(gv_dragSrcElementFake, this.parentElement.childNodes[v_overIndex]);
					}
					else {
						this.parentElement.insertBefore(gv_dragSrcElementFake, this.parentElement.childNodes[v_overIndex + 1]);
					}

					return false;
				}

				function handleDragEnter(e) {

				}

				function handleDragLeave(e) {

				}

				function handleDrop(e) {


					if (e.stopPropagation) {
						e.stopPropagation(); // stops the browser from redirecting.
					}

					return false;
				}

				function handleDragEnd(e) {
					var v_dragSrcElement = this;
					var v_parentElement = this.parentElement;
					var v_fakeIndex = Array.prototype.indexOf.call(document.querySelectorAll('#' + v_tabControl.id + ' > ul > li'), gv_dragSrcElementFake);

					v_tabControl.tabList.join();
					v_tabControl.tabList.splice((v_fakeIndex), 0, gv_dragSrcTab);
					v_tabControl.tabList.join();

					this.parentElement.removeChild(this);
					v_dragSrcElement.style.display = 'inline-block';
					v_parentElement.insertBefore(v_dragSrcElement, v_parentElement.childNodes[v_fakeIndex + 1]);

					[].forEach.call(
						document.querySelectorAll('.tabs li.fake'),
						function(element) {
							element.parentElement.removeChild(element);
						}
					);

					gv_dragSrcTab = null;
					gv_dragSrcElement = null;
					gv_dragSrcElementFake = null;
				}

				v_li.addEventListener('dragstart', handleDragStart, false);
				v_li.addEventListener('dragenter', handleDragEnter, false);
				v_li.addEventListener('dragover', handleDragOver, false);
				v_li.addEventListener('dragleave', handleDragLeave, false);
				v_li.addEventListener('drop', handleDrop, false);
				v_li.addEventListener('dragend', handleDragEnd, false);
			}

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
							v_span_more.appendChild(createImgElement(null,'menu_img','/static/OmniDB_app/images/right.png'));
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
					v_span_more.appendChild(createImgElement(null,'menu_img','/static/OmniDB_app/images/right.png'));
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
					contextMenu: null,
					selectable: true
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
