/*
Copyright 2015-2019 The OmniDB Team
This file is part of OmniDB.
OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function createOmnis(p_steps = []) {

  // tmp steps
  var v_steps = (p_steps.length !== 0) ? p_steps : [
    {
      p_message: 'This contains the outer connection and global panels [ connections_list_manager, snippets_panel, [conn_1, conn_2, ...], add_connection]',
      p_target: document.getElementsByClassName('omnidb__tab-menu omnidb__tab-menu--primary')[0],
      p_title: 'Primary menu'
    },
    {
      p_message: 'This contains general settings and options, such as [ versioning, connections_list_manager, user_setting, plugins...]',
      p_target: document.getElementsByClassName('omnidb__utilities-menu')[0],
      p_title: 'Utilities menu'
    }
  ];

  // tmp state control
  var v_state_active = true;

  var v_omnisControl = {
    // Params
		id: 'omnis_control_' + Date.now(),
		stateActive: v_state_active,
    stepCounter: 0,
    stepList: [],
    stepSelected: null,
    // Actions
    getPosition : function(p_el) {
  		var xPos = 0;
  		var yPos = 0;
      var el = p_el;

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
  	},
    emptyStepList : function() {
      this.stepCounter = 0;
      this.stepList = [];
    },
    updateStepList : function(p_list) {
      this.emptyStepList();
      for (let i = 0; i < p_list.length; i++) {
        this.createStep(p_list[i]);
      }
    },
    goToStep : function(p_index) {
      this.stepSelected = p_index;
      this.renderStep();
    },
    // Template
    createStep : function({
      p_title = 'Omnis',
      p_message = 'Example',
      p_target = null
    }) {
			var v_control = this;
			var v_index = v_control.stepCounter;

			v_control.stepCounter++;

			var v_step = {
				id: v_control.id + '_step_' + v_index,
        title: p_title,
        message: p_message,
        target: p_target
			};

      console.log('adding step', v_step);

      this.stepList.push(v_step);

    },
    renderStep : function() {
      if (this.stateActive) {
        var v_control = this;
        var v_step_item = this.stepList[this.stepSelected];

        var v_title = '';
        if (v_step_item.title)
          v_title += '<div class="omnis__step__title card-title p-2"><h5 class="mb-0">' + v_step_item.title + '</h5></div>';

        var v_message = '';
        if (v_step_item.message)
          v_message += '<div class="omnis__step__body card-body p-2">' + v_step_item.message + '</div>';

        var v_step_btn_next = '';
        if (this.stepSelected < this.stepCounter - 1)
          v_step_btn_next += '<button id="omnis_step_btn_next" type="button" class="btn btn-sm btn-primary ml-2">Next</button>';

        var v_step_btn_previous = '';
        if (this.stepSelected > 0)
          v_step_btn_previous += '<button id="omnis_step_btn_previous" type="button" class="btn btn-sm btn-primary mr-2">Previous</button>';

        var v_step_btn_close = '<button id="omnis_step_btn_close" type="button" class="btn btn-sm btn-danger ml-auto">End walkthrough</button>';

        var v_step_html =
        '<div class="omnis__step card">' +
          v_title +
          v_message +
          '<div class="omnis__step__footer card-footer d-flex align-items-center p-2">' +
            v_step_btn_previous +
            v_step_btn_next +
            v_step_btn_close +
          '</div>' +
        '</div>';

        this.divElement.innerHTML = v_step_html;


        var v_next_btn = document.getElementById('omnis_step_btn_next');
        if (v_next_btn !== undefined && v_next_btn !== null)
          v_next_btn.onclick = function(){v_control.goToStep(v_control.stepSelected + 1)};

        var v_previous_btn = document.getElementById('omnis_step_btn_previous');
        if (v_previous_btn !== undefined && v_previous_btn !== null)
          v_previous_btn.onclick = function(){v_control.goToStep(v_control.stepSelected - 1)};

        var v_close_btn = document.getElementById('omnis_step_btn_close');
        if (v_close_btn !== undefined && v_close_btn !== null)
          v_close_btn.onclick = function(){v_control.setStateDisabled()};

        this.divElement.style.display = 'block';

        this.updateOmnisPosition();
      }
      else {
        this.divElement.style.display = 'none';
      }
    },
    setStateEnabled: function() {
      this.stateActive = true;
      this.renderStep();
    },
    setStateDisabled: function() {
      this.stateActive = false;
      this.renderStep();
    },
    updateOmnisPosition : function() {
      var v_target = this.stepList[this.stepSelected].target;
      var v_target_position = this.getPosition(v_target);

      this.divElement.style.top = v_target_position.y + 20 + 'px';
      if (v_target_position.x >= (window.innerWidth / 2))
        this.divElement.style.left = v_target_position.x - this.divElement.offsetWidth - 10 + 'px';
      else
        this.divElement.style.left = v_target_position.x + v_target.offsetWidth + 10 + 'px';
    }
  }

  v_omnisControl.divElement = document.createElement('div');
  v_omnisControl.divElement.setAttribute('id', v_omnisControl.id);
  v_omnisControl.divElement.setAttribute('style', 'position:fixed; width:240px; max-width: 90vw; display:none; z-index: 99999999; box-shadow: 1px 0px 3px rgba(0,0,0,0.15); transition: 0.45s;');
  document.body.appendChild(v_omnisControl.divElement);

  return v_omnisControl;

}
