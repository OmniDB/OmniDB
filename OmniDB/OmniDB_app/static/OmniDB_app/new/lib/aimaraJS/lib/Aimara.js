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

///// Creating the tree component
// p_div: ID of the div where the tree will be rendered;
// p_backColor: Background color of the region where the tree is being rendered;
// p_contextMenu: Object containing all the context menus. Set null for no context menu;

/**
 * ## createTree
 * @desc Creating the tree component.
 *
 * @param  {string} p_div         ID of the div where the tree will be rendered.
 * @param  {string} p_backColor   Background color of the region where the tree is being rendered.
 * @param  {object} p_contextMenu Object containing all the context menus. Set null for no context menu.
 * @return {object}               Tree component.
 */
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
		nodeAfterOpenEvent: null,
		clickNodeEvent: null,
		beforeContextMenuEvent: null,
		///// Creating a new node
		// p_text: Text displayed on the node;
		// p_expanded: True or false, indicating wether the node starts expanded or not;
		// p_icon: Relative path to the icon displayed with the node. Set null if the node has no icon;
		// p_parentNode: Reference to the parent node. Set null to create the node on the root;
		// p_tag: Tag is used to store additional information on the node. All node attributes are visible when programming events and context menu actions;
		// p_contextmenu: Name of the context menu, which is one of the attributes of the p_contextMenu object created with the tree;
		// p_level: Depth of the node inside the tree
		createNode: function(p_text,p_expanded, p_icon, p_parentNode,p_tag,p_contextmenu,p_color,p_render=true,p_level = 0) {
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
				isBold: false,
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
				// p_level: Level of the node, child would be + 1, childeNodes would be + 2
				createChildNode: function(p_text,p_expanded,p_icon,p_tag,p_contextmenu,p_color,p_render=true,v_level=p_level+1) { return v_tree.createNode(p_text,p_expanded,p_icon,this,p_tag,p_contextmenu,p_color,p_render,v_level); },
				drawChildNodes: function(p_node, v_level = p_level + 2) { return v_tree.drawChildNodes(this, v_level); },
				setNodeBold: function() { v_tree.setNodeBold(this); },
				clearNodeBold: function() { v_tree.clearNodeBold(this); }
			}

			this.nodeCounter++;
			if (this.rendered && p_render) {
				if (p_parentNode==undefined) {
					this.drawNode(this.ulElement,node,p_level + 1);
				}
				else {

					var v_ul = p_parentNode.elementUl;
					if (p_parentNode.childNodes.length==0) {
						if (p_parentNode.expanded) {
						p_parentNode.elementDiv.style.display = 'block';
						var v_img = p_parentNode.elementExpCol;
						v_img.style.visibility = "visible";
						v_img.classList.remove('fa-chevron-right');
						v_img.classList.add('fa-chevron-down');
						v_img.id = 'toggle_off';
						}
						else {
							p_parentNode.elementDiv.style.display = 'none';
							var v_img = p_parentNode.elementExpCol;
							v_img.style.visibility = "visible";
							v_img.classList.add('fa-chevron-right');
							v_img.classList.remove('fa-chevron-down');
							v_img.id = 'toggle_on';
						}
					}
					this.drawNode(v_ul,node,p_level + 1);
				}
			}

			if (p_parentNode==undefined) {
				this.childNodes.push(node);
				node.parent=this;
			}
			else {
				p_parentNode.childNodes.push(node);
			}

			return node;
		},
		///// Render the tree;
		drawTree: function() {
			this.rendered = true;

			var div_tree = document.getElementById(this.div);

			div_tree.innerHTML = '';

			ulElement = this.createSimpleElement('ul',this.name,'nav flex-column');
			this.ulElement = ulElement;

			for (var i=0; i<this.childNodes.length; i++) {
				this.drawNode(ulElement,this.childNodes[i],1);
			}

			div_tree.appendChild(ulElement);
		},
		///// Drawing child nodes. This function is used when drawing nodes of the tree
		// p_node: Reference to the node object;
		// p_level: Depth of the node inside the tree
		drawChildNodes: function(p_node,p_level = 1) {
			if (p_node.childNodes.length>0) {
				if (p_node.expanded) {
					p_node.elementDiv.style.display = 'block';
					var v_img = p_node.elementExpCol;
					v_img.style.visibility = "visible";
					v_img.classList.remove('fa-chevron-right');
					v_img.classList.add('fa-chevron-down');
					v_img.id = 'toggle_off';
				}
				else {
					p_node.elementDiv.style.display = 'none';
					var v_img = p_node.elementExpCol;
					v_img.style.visibility = "visible";
					v_img.classList.add('fa-chevron-right');
					v_img.classList.remove('fa-chevron-down');
					v_img.id = 'toggle_on';
				}

				var v_ul = this.createSimpleElement('ul','ul_' + p_node.id,'nav flex-column');

				for (var i=0; i<p_node.childNodes.length; i++) {
					this.drawNode(v_ul,p_node.childNodes[i],p_level);
				}

				p_node.elementUl.parentNode.removeChild(p_node.elementUl);
				p_node.elementDiv.appendChild(v_ul);
				p_node.elementUl = v_ul;
			}
		},
		//Set note text as bold
		setNodeBold: function(p_node) {
			p_node.isBold = true;
			if (p_node.elementA!=null) {
				p_node.elementA.innerHTML= '<b>' + p_node.text.replace(/"/g, '') + '</b>';
			}
		},
		//Set note text as not bold
		clearNodeBold: function(p_node) {
			p_node.isBold = false;
			if (p_node.elementA!=null) {
				p_node.elementA.innerHTML= p_node.text.replace(/"/g, '');
			}
		},
		///// Drawing the node. This function is used when drawing the Tree and should not be called directly;
		// p_ulElement: Reference to the UL tag element where the node should be created;
		// p_node: Reference to the node object;
		// p_level: Depth of the node inside the tree
		drawNode: function(p_ulElement,p_node,p_level = 1) {
			var v_tree = this;

			var v_icon = null;

			if (p_node.icon!=null) {
				v_icon = this.createSimpleElement('i',null,'icon_tree ' + p_node.icon);
			}
			//v_icon.innerHTML = '<i class="' + p_node.icon + '" style="display: block;"></i>';
			//v_icon.style.backgroundImage = 'url(' + p_node.icon + ')';

			var v_li = this.createSimpleElement('li',null,'nav-item');
			p_node.elementLi = v_li;

			var v_a = this.createSimpleElement('a',null,'nav-link');

			var v_span_outer = this.createSimpleElement('span',null,'node');
			v_span_outer.style['padding-left'] = (p_level - 1)*16 + 'px';

			var v_exp_col = null;

			if (p_node.childNodes.length == 0) {
				v_exp_col = this.createSimpleElement('i','toggle_off','exp_col fas fa-chevron-down');
				v_exp_col.style.visibility = "hidden";
			}
			else {
				if (p_node.expanded) {
					v_exp_col = this.createSimpleElement('i','toggle_off','exp_col fas fa-chevron-down');
				}
				else {
					v_exp_col = this.createSimpleElement('i','toggle_on','exp_col fas fa-chevron-right');
				}
			}

			v_a.ondblclick = function() {
				v_tree.doubleClickNode(p_node);
			};

			v_exp_col.onclick = function() {
				v_tree.toggleNode(p_node);
			};

			v_span_outer.onclick = function(e) {
				v_tree.clickNode(p_node);
				v_tree.selectNode(p_node);

				if (e.ctrlKey) {
					if (v_tree.beforeContextMenuEvent!=null) {
						v_tree.beforeContextMenuEvent(p_node,function(p_items) { v_tree.nodeContextMenu(e,p_node,p_items); })
					}
					else {
						v_tree.nodeContextMenu(e,p_node);
					}
				}
			};

			v_a.oncontextmenu = function(e) {
				v_tree.clickNode(p_node);
				v_tree.selectNode(p_node);

				if (e.button==2) {
					e.preventDefault();
					e.stopPropagation();
				}

				//v_tree.selectNode(p_node);
				if (v_tree.beforeContextMenuEvent!=null) {
					v_tree.beforeContextMenuEvent(p_node,function(p_items) { v_tree.nodeContextMenu(e,p_node,p_items); })
				}
				else {
					v_tree.nodeContextMenu(e,p_node);
				}
			};

			v_span_outer.appendChild(v_exp_col);

			if (v_icon!=undefined) {
				v_span_outer.appendChild(v_icon);
			}

			var v_span_inner = this.createSimpleElement('span',null,null);

			if (p_node.color!=null) {
				v_span_inner.style.color = p_node.color;
			}

		  if (p_node.isBold) {
				v_span_inner.innerHTML= '<b>' + p_node.text.replace(/"/g, '') + '</b>';
			}
			else {
				v_span_inner.innerHTML= p_node.text.replace(/"/g, '');
			}
			p_node.elementA = v_span_inner;
			v_span_outer.appendChild(v_span_inner);
			v_a.appendChild(v_span_outer);
			v_li.appendChild(v_a);
			p_ulElement.appendChild(v_li);

			var v_div = this.createSimpleElement('div',null,'collapse');

			var v_ul = this.createSimpleElement('ul','ul_' + p_node.id,'nav flex-column');
			v_div.appendChild(v_ul);
			v_li.appendChild(v_div);

			if (p_node.childNodes.length > 0) {
				if (!p_node.expanded) {
					v_div.style.display = 'none';
				}

				var v_level = p_level + 1;

				for (var i=0; i<p_node.childNodes.length; i++) {
					this.drawNode(v_ul,p_node.childNodes[i],v_level);
				}
			}
			p_node.elementUl = v_ul;
			p_node.elementDiv = v_div;
			p_node.elementExpCol = v_exp_col;
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
		//Create a HTML element specified by parameter 'p_type'
		createSimpleElement: function(p_type,p_id,p_class) {
			var v_element = document.createElement(p_type);
			if (p_id!=undefined) {
				v_element.id = p_id;
			}
			if (p_class!=undefined) {
				v_element.className = p_class;
			}
			return v_element;
		},
		///// Expanding node
		// p_node: Reference to the node;
		expandNode: function(p_node) {
			if (p_node.childNodes.length>0 && p_node.expanded==false) {
				if (this.nodeBeforeOpenEvent!=undefined) {
					this.nodeBeforeOpenEvent(p_node);
				}

				var img=p_node.elementExpCol;
				p_node.expanded = true;

				img.id="toggle_off";
				img.classList.remove('fa-chevron-right');
				img.classList.add('fa-chevron-down');
				elem_ul = p_node.elementDiv;
				elem_ul.style.display = 'block';

				if (this.nodeAfterOpenEvent!=undefined) {
					this.nodeAfterOpenEvent(p_node);
				}
			}
		},
		///// Collapsing node
		// p_node: Reference to the node;
		collapseNode: function(p_node) {
			if (p_node.childNodes.length>0 && p_node.expanded==true) {
				var img=p_node.elementExpCol;

				p_node.expanded = false;
				if (this.nodeBeforeCloseEvent!=undefined) {
					this.nodeBeforeCloseEvent(p_node);
				}

				img.classList.add('fa-chevron-right');
				img.classList.remove('fa-chevron-down');
				elem_ul = p_node.elementDiv;
				elem_ul.style.display = 'none';

			}
		},
		///// Toggling node
		// p_node: Reference to the node;
		toggleNode: function(p_node) {
			if (p_node.childNodes.length>0) {
				if (p_node.expanded) {
					p_node.collapseNode();
				}
				else {
					p_node.expandNode();
				}
			}
		},
		///// Clicking node
		// p_node: Reference to the node;
		clickNode: function(p_node) {
			//global event
			if (this.clickNodeEvent) {
				this.clickNodeEvent(p_node);
			}

			//node event
			if (p_node.clickNodeEvent) {
				p_node.clickNodeEvent(p_node);
			}
		},
		///// Double clicking node
		// p_node: Reference to the node;
		doubleClickNode: function(p_node) {
			this.toggleNode(p_node);
			if (p_node.doubleClickNodeEvent) {
				p_node.doubleClickNodeEvent(p_node);
			}
		},
		///// Selecting node
		// p_node: Reference to the node;
		selectNode: function(p_node) {
			var span = p_node.elementLi.getElementsByTagName("span")[0];
			span.className = 'node_selected';
			if (this.selectedNode!=null && this.selectedNode!=p_node) {
				this.selectedNode.elementLi.getElementsByTagName("span")[0].className = 'node';
			}
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
				var v_img = p_node.parent.elementLi.getElementsByTagName("i")[0];
				v_img.style.visibility = "hidden";
			}

		},
		///// Deleting all node children
		// p_node: Reference to the node;
		removeChildNodes: function(p_node) {
			if (p_node.childNodes.length>0) {
				var v_ul = p_node.elementUl;

				var v_img = p_node.elementExpCol;
				v_img.style.visibility = "hidden";

				p_node.childNodes = [];
				v_ul.innerHTML = "";
			}
		},
		///// Rendering context menu when mouse right button is pressed over a node. This function should no be called directly
		// p_event: Event triggered when right clicking;
		// p_node: Reference to the node;
		nodeContextMenu: function(p_event,p_node, p_items) {
			var v_items_list = [];

			if (p_node.contextMenu!=undefined) {
				try {
						var v_menu_list = null;
						if (typeof(this.contextMenu[p_node.contextMenu].elements)=='function') {
							v_menu_list = this.contextMenu[p_node.contextMenu].elements(p_node);
						}
						else {
							v_menu_list = this.contextMenu[p_node.contextMenu].elements;
						}
						v_items_list = v_items_list.concat(v_menu_list);
				}
				catch(err) {
				}
			}

			if (p_items!=null) {
				v_items_list = v_items_list.concat(p_items);
			}

			customMenu(
				{
					x:p_event.clientX+5,
					y:p_event.clientY+5
				},
				v_items_list,
				p_node);
		}
	}

	//Disabling context menu in tree div
	var v_div = document.getElementById(p_div);
	v_div.setAttribute("oncontextmenu", "return false;");
	v_div.classList.add('aimara_tree');

	return v_tree_object;
}
