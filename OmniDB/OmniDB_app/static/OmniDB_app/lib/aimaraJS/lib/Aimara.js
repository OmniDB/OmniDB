/*
Copyright 2015-2017 The OmniDB Team
This file is part of OmniDB.
OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

///// Creating the tree component
// p_div: ID of the div where the tree will be rendered;
// p_backColor: Background color of the region where the tree is being rendered;
// p_contextMenu: Object containing all the context menus. Set null for no context menu;
function createTree(p_div,p_backColor,p_contextMenu) {
	var v_tree_object = {
		name: 'tree_' + p_div,
		div: p_div,
		ulElement: null,
		childNodes: [],
		backcolor: p_backColor,
		contextMenu: p_contextMenu,
		selectedNode: null,
		nodeCounter: 0,
		contextMenuDiv: null,
		rendered: false,
		tag: null,
		///// Creating a new node
		// p_text: Text displayed on the node;
		// p_expanded: True or false, indicating wether the node starts expanded or not;
		// p_icon: Relative path to the icon displayed with the node. Set null if the node has no icon;
		// p_parentNode: Reference to the parent node. Set null to create the node on the root;
		// p_tag: Tag is used to store additional information on the node. All node attributes are visible when programming events and context menu actions;
		// p_contextmenu: Name of the context menu, which is one of the attributes of the p_contextMenu object created with the tree;
		createNode: function(p_text,p_expanded, p_icon, p_parentNode,p_tag,p_contextmenu,p_color) {
			var v_tree = this;
			var node = {
				tree: v_tree,
				id: 'node_' + this.nodeCounter,
				text: p_text,
				icon: p_icon,
				parent: p_parentNode,
				expanded : p_expanded,
				childNodes : [],
				tag : p_tag,
				contextMenu: p_contextmenu,
				color: p_color,
				elementLi: null,
				doubleClickNodeEvent: null,
				clickNodeEvent: null,
				///// Removing the node and all its children
				removeNode: function() { v_tree.removeNode(this); },
				///// Expanding or collapsing the node, depending on the expanded value
				toggleNode: function(p_event) { v_tree.toggleNode(this); },
				///// Expanding the node
				expandNode: function(p_event) { v_tree.expandNode(this); },
				///// Expanding the node and its children recursively
				expandSubtree: function() { v_tree.expandSubtree(this); },
				///// Changing the node text
				// p_text: New text;
				setText: function(p_text) { v_tree.setText(this,p_text); },
				///// Collapsing the node
				collapseNode: function() { v_tree.collapseNode(this); },
				///// Collapsing the node and its children recursively
				collapseSubtree: function() { v_tree.collapseSubtree(this); },
				///// Deleting all child nodes
				removeChildNodes: function() { v_tree.removeChildNodes(this); },
				///// Creating a new child node;
				// p_text: Text displayed;
				// p_expanded: True or false, indicating wether the node starts expanded or not;
				// p_icon: Icon;
				// p_tag: Tag;
				// p_contextmenu: Context Menu;
				createChildNode: function(p_text,p_expanded,p_icon,p_tag,p_contextmenu) { return v_tree.createNode(p_text,p_expanded,p_icon,this,p_tag,p_contextmenu); }
			}

			this.nodeCounter++;

			if (this.rendered) {
				if (p_parentNode==undefined) {
					this.drawNode(this.ulElement,node);
					this.adjustLines(this.ulElement,false);
				}
				else {
					var v_ul = p_parentNode.elementLi.getElementsByTagName("ul")[0];
					if (p_parentNode.childNodes.length==0) {
						if (p_parentNode.expanded) {
						p_parentNode.elementLi.getElementsByTagName("ul")[0].style.display = 'block';
						var v_img = p_parentNode.elementLi.getElementsByTagName("img")[0];
						v_img.style.visibility = "visible";
						v_img.src = '/static/OmniDB_app/images/collapse.png';
						v_img.id = 'toggle_off';
						}
						else {
							p_parentNode.elementLi.getElementsByTagName("ul")[0].style.display = 'none';
							var v_img = p_parentNode.elementLi.getElementsByTagName("img")[0];
							v_img.style.visibility = "visible";
							v_img.src = '/static/OmniDB_app/images/expand.png';
							v_img.id = 'toggle_on';
						}
					}
					this.drawNode(v_ul,node);
					this.adjustLines(v_ul,false);
				}
			}

			if (p_parentNode==undefined) {
				this.childNodes.push(node);
				node.parent=this;
			}
			else
				p_parentNode.childNodes.push(node);

			return node;
		},
		///// Render the tree;
		drawTree: function() {

			this.rendered = true;

			var div_tree = document.getElementById(this.div);

			div_tree.innerHTML = '';

			ulElement = createSimpleElement('ul',this.name,'tree');
			this.ulElement = ulElement;

			for (var i=0; i<this.childNodes.length; i++) {
				this.drawNode(ulElement,this.childNodes[i]);
			}

			div_tree.appendChild(ulElement);

      		this.adjustLines(document.getElementById(this.name),true);

		},
		///// Drawing the node. This function is used when drawing the Tree and should not be called directly;
		// p_ulElement: Reference to the UL tag element where the node should be created;
		// p_node: Reference to the node object;
		drawNode: function(p_ulElement,p_node) {

			var v_tree = this;

			var v_icon = null;

			if (p_node.icon!=null)
				v_icon = createSimpleElement('span',null,'icon_tree');
				v_icon.style.backgroundImage = 'url(' + p_node.icon + ')';

			var v_li = document.createElement('li');
			p_node.elementLi = v_li;

			var v_span = createSimpleElement('span',null,'node');

			var v_exp_col = null;

			if (p_node.childNodes.length == 0) {
				v_exp_col = createImgElement('toggle_off','exp_col','/static/OmniDB_app/images/collapse.png');
				v_exp_col.style.visibility = "hidden";
			}
			else {
				if (p_node.expanded) {
					v_exp_col = createImgElement('toggle_off','exp_col','/static/OmniDB_app/images/collapse.png');
				}
				else {
					v_exp_col = createImgElement('toggle_on','exp_col','/static/OmniDB_app/images/expand.png');
				}
			}

			v_span.ondblclick = function() {
				v_tree.doubleClickNode(p_node);
			};

			v_exp_col.onclick = function() {
				v_tree.toggleNode(p_node);
			};

			v_span.onclick = function(e) {
				v_tree.clickNode(p_node);
				v_tree.selectNode(p_node);

				if (e.ctrlKey) {
					if (p_node.contextMenu!=null) {
						v_tree.nodeContextMenu(e,p_node);
					}
				}
			};

			v_span.oncontextmenu = function(e) {
				if (e.button==2) {
					e.preventDefault();
					e.stopPropagation();
				}

				if (p_node.contextMenu!=null) {
						v_tree.selectNode(p_node);
						v_tree.nodeContextMenu(e,p_node);
				}
			};

			if (v_icon!=undefined)
				v_span.appendChild(v_icon);

				v_a = createSimpleElement('a',null,null);

				if (p_node.color!=null)
					v_a.style.color = p_node.color;

				v_a.innerHTML=p_node.text.replace(/"/g, '');
				v_span.appendChild(v_a);
				v_li.appendChild(v_exp_col);
				v_li.appendChild(v_span);

			p_ulElement.appendChild(v_li);

			var v_ul = createSimpleElement('ul','ul_' + p_node.id,null);
			v_li.appendChild(v_ul);

			if (p_node.childNodes.length > 0) {

				if (!p_node.expanded)
					v_ul.style.display = 'none';

				for (var i=0; i<p_node.childNodes.length; i++) {
					this.drawNode(v_ul,p_node.childNodes[i]);
				}
			}
		},
		///// Changing node text
		// p_node: Reference to the node that will have its text updated;
		// p_text: New text;
		setText: function(p_node,p_text) {
			p_node.elementLi.getElementsByTagName('span')[0].lastChild.innerHTML = p_text;
			p_node.text = p_text;
		},
		///// Expanding all tree nodes
		expandTree: function() {
			for (var i=0; i<this.childNodes.length; i++) {
				if (this.childNodes[i].childNodes.length>0) {
					this.expandSubtree(this.childNodes[i]);
				}
			}
		},
		///// Expanding all nodes inside the subtree that have parameter 'p_node' as root
		// p_node: Subtree root;
		expandSubtree: function(p_node) {
			this.expandNode(p_node);
			for (var i=0; i<p_node.childNodes.length; i++) {
				if (p_node.childNodes[i].childNodes.length>0) {
					this.expandSubtree(p_node.childNodes[i]);
				}
			}
		},
		///// Collapsing all tree nodes
		collapseTree: function() {
			for (var i=0; i<this.childNodes.length; i++) {
				if (this.childNodes[i].childNodes.length>0) {
					this.collapseSubtree(this.childNodes[i]);
				}
			}
		},
		///// Collapsing all nodes inside the subtree that have parameter 'p_node' as root
		// p_node: Subtree root;
		collapseSubtree: function(p_node) {
			this.collapseNode(p_node);
			for (var i=0; i<p_node.childNodes.length; i++) {
				if (p_node.childNodes[i].childNodes.length>0) {
					this.collapseSubtree(p_node.childNodes[i]);
				}
			}
		},
		///// Expanding node
		// p_node: Reference to the node;
		expandNode: function(p_node) {
			if (p_node.childNodes.length>0 && p_node.expanded==false) {
				if (this.nodeBeforeOpenEvent!=undefined)
					this.nodeBeforeOpenEvent(p_node);

				var img=p_node.elementLi.getElementsByTagName("img")[0];

				p_node.expanded = true;

				img.id="toggle_off";
				img.src = '/static/OmniDB_app/images/collapse.png';
				elem_ul = img.parentElement.getElementsByTagName("ul")[0];
				elem_ul.style.display = 'block';

				if (this.nodeAfterOpenEvent!=undefined)
					this.nodeAfterOpenEvent(p_node);
			}
		},
		///// Collapsing node
		// p_node: Reference to the node;
		collapseNode: function(p_node) {
			if (p_node.childNodes.length>0 && p_node.expanded==true) {
				var img=p_node.elementLi.getElementsByTagName("img")[0];

				p_node.expanded = false;
				if (this.nodeBeforeCloseEvent!=undefined)
					this.nodeBeforeCloseEvent(p_node);

				img.id="toggle_on";
				img.src = '/static/OmniDB_app/images/expand.png';
				elem_ul = img.parentElement.getElementsByTagName("ul")[0];
				elem_ul.style.display = 'none';

			}
		},
		///// Toggling node
		// p_node: Reference to the node;
		toggleNode: function(p_node) {
			if (p_node.childNodes.length>0) {
				if (p_node.expanded)
					p_node.collapseNode();
				else
					p_node.expandNode();
			}
		},
		///// Clicking node
		// p_node: Reference to the node;
		clickNode: function(p_node) {
			//global event
			if (this.clickNodeEvent)
				this.clickNodeEvent(p_node);

			//node event
			if (p_node.clickNodeEvent)
				p_node.clickNodeEvent(p_node);
		},
		///// Double clicking node
		// p_node: Reference to the node;
		doubleClickNode: function(p_node) {
			this.toggleNode(p_node);
			if (p_node.doubleClickNodeEvent)
				p_node.doubleClickNodeEvent(p_node);
		},
		///// Selecting node
		// p_node: Reference to the node;
		selectNode: function(p_node) {
			var span = p_node.elementLi.getElementsByTagName("span")[0];
			span.className = 'node_selected';
			if (this.selectedNode!=null && this.selectedNode!=p_node)
				this.selectedNode.elementLi.getElementsByTagName("span")[0].className = 'node';
			this.selectedNode = p_node;
		},
		///// Deleting node
		// p_node: Reference to the node;
		removeNode: function(p_node) {
			var index = p_node.parent.childNodes.indexOf(p_node);

			if (p_node.elementLi.className=="last" && index!=0) {
				p_node.parent.childNodes[index-1].elementLi.className += "last";
				p_node.parent.childNodes[index-1].elementLi.style.backgroundColor = this.backcolor;
			}

			p_node.elementLi.parentNode.removeChild(p_node.elementLi);
			p_node.parent.childNodes.splice(index, 1);

			if (p_node.parent.childNodes.length==0) {
				var v_img = p_node.parent.elementLi.getElementsByTagName("img")[0];
				v_img.style.visibility = "hidden";
			}

		},
		///// Deleting all node children
		// p_node: Reference to the node;
		removeChildNodes: function(p_node) {

			if (p_node.childNodes.length>0) {
				var v_ul = p_node.elementLi.getElementsByTagName("ul")[0];

				var v_img = p_node.elementLi.getElementsByTagName("img")[0];
				v_img.style.visibility = "hidden";

				p_node.childNodes = [];
				v_ul.innerHTML = "";
			}
		},
		///// Rendering context menu when mouse right button is pressed over a node. This function should no be called directly
		// p_event: Event triggered when right clicking;
		// p_node: Reference to the node;
		nodeContextMenu: function(p_event,p_node) {
				if (p_node.contextMenu!=undefined) {

					var v_tree = this;

					var v_menu = this.contextMenu[p_node.contextMenu];

					var v_div;
					if (this.contextMenuDiv==null) {
						v_div = createSimpleElement('ul','ul_cm','aimara_menu');
						document.body.appendChild(v_div);
					}
					else
						v_div = this.contextMenuDiv;

					var v_closediv = createSimpleElement('div',null,'div_close_cm');
					v_closediv.onmousedown = function() {
						if (v_tree.contextMenuDiv!=null) {
							//v_tree.contextMenuDiv.style.display = 'none';
							v_tree.contextMenuDiv.parentNode.removeChild(v_tree.contextMenuDiv);
							v_tree.contextMenuDiv = null;
						}
						this.parentNode.removeChild(this);
					};
					v_closediv.oncontextmenu = function(e) {
						e.preventDefault();
						e.stopPropagation();
						if (v_tree.contextMenuDiv!=null) {
							//v_tree.contextMenuDiv.style.display = 'none';
							v_tree.contextMenuDiv.parentNode.removeChild(v_tree.contextMenuDiv);
							v_tree.contextMenuDiv = null;
						}
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
						v_li.aimara_level = 0;

						var v_span = createSimpleElement('span',null,null);
						v_span.onmousedown = function () {
							if (v_tree.contextMenuDiv!=null) {
								//v_tree.contextMenuDiv.style.display = 'none';
								v_tree.contextMenuDiv.parentNode.removeChild(v_tree.contextMenuDiv);
								v_tree.contextMenuDiv = null;
							}
							v_closediv.parentNode.removeChild(v_closediv);

							if (v_menu.elements[i].action!=null)
								v_menu.elements[i].action(p_node);
						};

						var v_a = createSimpleElement('a',null,null);
						var v_ul = createSimpleElement('ul',null,'aimara_sub-menu');
						v_ul.aimara_level = 0;

						v_a.appendChild(document.createTextNode(v_menu.elements[i].text));

						v_li.appendChild(v_span);

						if (v_menu.elements[i].icon!=undefined) {
							var v_img = createImgElement('null','null',v_menu.elements[i].icon);
							v_li.appendChild(v_img);
						}

						v_li.appendChild(v_a);

						v_div.appendChild(v_li);

						if (v_menu.elements[i].submenu!=undefined) {

							v_li.onmouseenter = function() {
								var v_submenus = document.getElementsByClassName("aimara_sub-menu");
								for (var k=0; k<v_submenus.length;k++) {
									if (v_submenus[k].aimara_level>=this.aimara_level)
										v_submenus[k].style.display = 'none';
								}
								v_ul.style.display = 'block';
							}

							v_li.appendChild(v_ul);
							var v_span_more = createSimpleElement('div',null,null);
							v_span_more.appendChild(createImgElement(null,'menu_img','/static/OmniDB_app/images/right.png'));
							v_li.appendChild(v_span_more);
							v_tree.contextMenuLi(v_menu.elements[i].submenu,v_ul,p_node,v_closediv, 1);
						}

					})(i);

					this.contextMenuDiv = v_div;

			}
		},
		///// Recursive function called when rendering context menu submenus. This function should no be called directly
		// p_submenu: Reference to the submenu object;
		// p_ul: Reference to the UL tag;
		// p_node: Reference to the node;
		contextMenuLi : function(p_submenu,p_ul,p_node,p_closediv, p_level) {

			var v_tree = this;

			for (var i=0; i<p_submenu.elements.length; i++) (function(i){

				var v_li = createSimpleElement('li',null,null);
				v_li.aimara_level = p_level;

				var v_span = createSimpleElement('span',null,null);
				v_span.onmousedown = function () {
					if (v_tree.contextMenuDiv!=null) {
						//v_tree.contextMenuDiv.style.display = 'none';
						v_tree.contextMenuDiv.parentNode.removeChild(v_tree.contextMenuDiv);
						v_tree.contextMenuDiv = null;
					}
					p_closediv.parentNode.removeChild(p_closediv);

					if (p_submenu.elements[i].action!=null)
						p_submenu.elements[i].action(p_node)
				};

				var v_a = createSimpleElement('a',null,null);
				var v_ul = createSimpleElement('ul',null,'aimara_sub-menu');
				v_ul.aimara_level = p_level;

				v_a.appendChild(document.createTextNode(p_submenu.elements[i].text));

				v_li.appendChild(v_span);

				if (p_submenu.elements[i].icon!=undefined) {
					var v_img = createImgElement('null','null',p_submenu.elements[i].icon);
					v_li.appendChild(v_img);
				}

				v_li.appendChild(v_a);

				p_ul.appendChild(v_li);

				if (p_submenu.elements[i].submenu!=undefined) {

					v_li.onmouseenter = function() {
						var v_submenus = document.getElementsByClassName("aimara_sub-menu");
						for (var k=0; k<v_submenus.length;k++) {
							if (v_submenus[k].aimara_level>=this.aimara_level)
								v_submenus[k].style.display = 'none';
						}
						v_ul.style.display = 'block';
					}

					v_li.appendChild(v_ul);
					var v_span_more = createSimpleElement('div',null,null);
					v_span_more.appendChild(createImgElement(null,'menu_img','/static/OmniDB_app/images/right.png'));
					v_li.appendChild(v_span_more);
					v_tree.contextMenuLi(p_submenu.elements[i].submenu,v_ul,p_node,p_closediv, p_level+1);
				}

			})(i);
		},
		///// Adjusting tree dotted lines. This function should not be called directly
		// p_node: Reference to the node;
		adjustLines: function(p_ul,p_recursive) {
			var tree = p_ul;

      var lists = [];

			if (tree.childNodes.length>0) {
				lists = [ tree ];

				if (p_recursive) {
		      for (var i = 0; i < tree.getElementsByTagName("ul").length; i++) {
						var check_ul = tree.getElementsByTagName("ul")[i];
						if (check_ul.childNodes.length!=0)
		        	lists[lists.length] = check_ul;
					}
				}

			}

      for (var i = 0; i < lists.length; i++) {
        var item = lists[i].lastChild;

        while (!item.tagName || item.tagName.toLowerCase() != "li") {
     	  item = item.previousSibling;
				}

        item.className += "last";
				item.style.backgroundColor = this.backcolor;

				item = item.previousSibling;

				if (item!=null)
					if (item.tagName.toLowerCase() == "li") {
						item.className = "";
						item.style.backgroundColor = 'transparent';
					}
      }
		}
	}

	//Disabling context menu in tree div
	document.getElementById(p_div).setAttribute("oncontextmenu", "return false;");

	return v_tree_object;
}

// Helper Functions

//Create a HTML element specified by parameter 'p_type'
function createSimpleElement(p_type,p_id,p_class) {
	var element = document.createElement(p_type);
	if (p_id!=undefined)
		element.id = p_id;
	if (p_class!=undefined)
		element.className = p_class;
	return element;
}

//Create img element
function createImgElement(p_id,p_class,p_src) {
	var element = document.createElement('img');
	if (p_id!=undefined)
		element.id = p_id;
	if (p_class!=undefined)
		element.className = p_class;
	if (p_src!=undefined)
		element.src = p_src;
	return element;
}
