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

function customMenu(p_position,p_menu,p_object) {

      var v_outer_div = createSimpleElement('div','ul_cm_overlay','aimara_menu__overlay');

      var v_div = createSimpleElement('ul','ul_cm','aimara_menu');

      var v_closediv = createSimpleElement('div','close_cm','div_close_cm');
      v_closediv.onmousedown = function() {
        v_div.parentNode.removeChild(v_div);
        this.parentNode.removeChild(this);
        v_outer_div.parentNode.removeChild(v_outer_div);
      };
      v_closediv.oncontextmenu = function(e) {
        e.preventDefault();
        e.stopPropagation();
        v_div.parentNode.removeChild(v_div);
        this.parentNode.removeChild(this);
        v_outer_div.parentNode.removeChild(v_outer_div);
      };
      v_outer_div.appendChild(v_div);
      v_outer_div.appendChild(v_closediv);
      document.body.appendChild(v_outer_div);

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
          v_outer_div.parentNode.removeChild(v_outer_div);

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
            v_ul.style['z-index'] = this.aimara_level + 1;
            custoMenuRepositionSubmenu(v_ul);
          }

          v_li.appendChild(v_ul);
          var v_span_more = createSimpleElement('div',null,null);
          v_span_more.appendChild(createImgElement(null,'menu_img',v_url_folder + '/static/OmniDB_app/images/right.png'));
          v_li.appendChild(v_span_more);

          customMenuRecursive(p_menu[i].submenu.elements,v_ul,p_object,v_closediv,v_div,1,v_outer_div);
        }

      })(i);

      customMenuReposition(v_div);
}

function customMenuRecursive(p_submenu,p_ul,p_object,p_closediv, p_cm_div, p_level, p_outer_div) {

  for (var i=0; i<p_submenu.length; i++) (function(i){

    var v_li = createSimpleElement('li',null,null);
    v_li.aimara_level = p_level;

    var v_span = createSimpleElement('span',null,null);
    v_span.onmousedown = function () {
      p_cm_div.parentNode.removeChild(p_cm_div);
      p_closediv.parentNode.removeChild(p_closediv);
      p_outer_div.parentNode.removeChild(p_outer_div);

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
        v_ul.style['z-index'] = this.aimara_level + 1;
        custoMenuRepositionSubmenu(v_ul);
      }

      v_li.appendChild(v_ul);
      var v_span_more = createSimpleElement('div',null,null);
      v_span_more.appendChild(createImgElement(null,'menu_img',v_url_folder + '/static/OmniDB_app/images/right.png'));
      v_li.appendChild(v_span_more);
      customMenuRecursive(p_submenu[i].submenu.elements,v_ul,p_object,p_closediv,p_cm_div,p_level+1,p_outer_div);
    }
  })(i);


}

function customMenuReposition(p_div) {
  var v_div = p_div;

  // Repositioning the sub-menu if its out of the frame.
  let v_div_rect = v_div.getBoundingClientRect();
  let v_div_h_diff = v_div_rect.x + v_div_rect.width - window.innerWidth;
  if (v_div_h_diff > 0) {
    v_div.style.left = v_div_rect.x - v_div_h_diff - 5 + 'px';
    v_div.classList.add('aimara_menu_left');
  }

  // Getting vertical position.
  let v_div_y = v_div_rect.y;
  let v_div_v_diff = v_div_y + v_div_rect.height - window.innerHeight;

  // Case where element is out of frame.
  if (v_div_v_diff > 0) {
    // Checking if the menu fits on the screen
    let v_div_v_fits = ((v_div_rect.height - window.innerHeight) <= 5);
    // Case where it doesnt fit.
    if (!v_div_v_fits) {
      v_div.style.top = '5px';
    }
    // Case where it fits but should be pulled up.
    else {
      v_div.style.top = v_div_y - v_div_v_diff - 5 + 'px';
    }
  }
  document.getElementById('close_cm').style.height = document.getElementById('ul_cm_overlay').scrollHeight + 'px';
}

function custoMenuRepositionSubmenu(p_ul) {
  var v_ul = p_ul;

  // Repositioning the sub-menu if its out of the frame.
  let v_ul_rect = v_ul.getBoundingClientRect();
  let v_ul_h_diff = v_ul_rect.x + v_ul_rect.width - window.innerWidth;
  if (v_ul_h_diff > 0) {
    v_ul.classList.add('aimara_menu_left');
  }

  // Getting vertical position.
  let v_ul_y = v_ul_rect.y;
  let v_ul_v_diff = v_ul_y + v_ul_rect.height - window.innerHeight;

  // Case where element is out of frame.
  if (v_ul_v_diff > 0) {
    // Checking if the menu fits on the screen
    let v_ul_v_fits = ((v_ul_rect.height - window.innerHeight) <= 5);
    // Case where it doesnt fit.
    if (!v_ul_v_fits) {
      v_ul.style.top = (-1)*v_ul_y + 5 + 'px';
    }
    // Case where it fits but should be pulled up.
    else {
      v_ul.style.top = (-1)*v_ul_v_diff - 5 + 'px';
    }
  }
  document.getElementById('close_cm').style.height = document.getElementById('ul_cm_overlay').scrollHeight + 'px';
}
