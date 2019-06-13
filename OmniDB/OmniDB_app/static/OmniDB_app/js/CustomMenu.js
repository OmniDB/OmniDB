/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function customMenu(p_position,p_menu,p_object) {

      var v_div = createSimpleElement('ul','ul_cm','aimara_menu');
      document.body.appendChild(v_div);

      var v_closediv = createSimpleElement('div',null,'div_close_cm');
      v_closediv.onmousedown = function() {
        v_div.parentNode.removeChild(v_div);
        this.parentNode.removeChild(this);
      };
      v_closediv.oncontextmenu = function(e) {
        e.preventDefault();
        e.stopPropagation();
        v_div.parentNode.removeChild(v_div);
        this.parentNode.removeChild(this);
      };
      document.body.appendChild(v_closediv);

      v_div.innerHTML = '';

      var v_left = p_position.x-5;
      var v_right = p_position.y-5;

      v_div.style.display = 'block';
      v_div.style.position = 'absolute';
      v_div.style.left = v_left + 'px';
      v_div.style.top = v_right + 'px';

      for (var i=0; i<p_menu.length; i++) (function(i){

        var v_li = createSimpleElement('li',null,null);
        v_li.aimara_level = 0;

        var v_span = createSimpleElement('span',null,null);
        v_span.onmousedown = function () {
          v_div.parentNode.removeChild(v_div);
          v_closediv.parentNode.removeChild(v_closediv);

          if (p_menu[i].action!=null)
            p_menu[i].action(p_object);
        };

        var v_a = createSimpleElement('a',null,null);
        var v_ul = createSimpleElement('ul',null,'aimara_sub-menu');
        v_ul.aimara_level = 0;

        //v_a.appendChild(document.createTextNode(p_menu[i].text));
        v_a.innerHTML = p_menu[i].text;

        v_li.appendChild(v_span);

        if (p_menu[i].icon!=undefined) {
          var v_img = createSimpleElement('i',null,p_menu[i].icon);
          v_img.innerHTML = '&nbsp;';
          v_li.appendChild(v_img);
        }

        v_li.appendChild(v_a);

        v_div.appendChild(v_li);

        if (p_menu[i].submenu!=undefined) {

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
          v_span_more.appendChild(createImgElement(null,'menu_img',v_url_folder + '/static/OmniDB_app/images/right.png'));
          v_li.appendChild(v_span_more);
          customMenuRecursive(p_menu[i].submenu.elements,v_ul,p_object,v_closediv,v_div, 1);
        }

      })(i);
}

function customMenuRecursive(p_submenu,p_ul,p_object,p_closediv, p_cm_div, p_level) {

  for (var i=0; i<p_submenu.length; i++) (function(i){

    var v_li = createSimpleElement('li',null,null);
    v_li.aimara_level = p_level;

    var v_span = createSimpleElement('span',null,null);
    v_span.onmousedown = function () {
      p_cm_div.parentNode.removeChild(p_cm_div);
      p_closediv.parentNode.removeChild(p_closediv);

      if (p_submenu[i].action!=null)
        p_submenu[i].action(p_object)
    };

    var v_a = createSimpleElement('a',null,null);
    var v_ul = createSimpleElement('ul',null,'aimara_sub-menu');
    v_ul.aimara_level = p_level;

    //v_a.appendChild(document.createTextNode(p_submenu[i].text));
    v_a.innerHTML = p_submenu[i].text;

    v_li.appendChild(v_span);

    if (p_submenu[i].icon!=undefined) {
      var v_img = createSimpleElement('i',null,p_submenu[i].icon);
      v_img.innerHTML = '&nbsp;';
      v_li.appendChild(v_img);
    }

    v_li.appendChild(v_a);

    p_ul.appendChild(v_li);


    if (p_submenu[i].submenu!=undefined) {

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
      v_span_more.appendChild(createImgElement(null,'menu_img',v_url_folder + '/static/OmniDB_app/images/right.png'));
      v_li.appendChild(v_span_more);
      customMenuRecursive(p_submenu[i].submenu.elements,v_ul,p_object,p_closediv,p_cm_div, p_level+1);
    }

  })(i);
}
