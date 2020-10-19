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

function createOmnis() {
  return {
    id: 'omnis',
    div: null,
    template:
    `<svg
        class="animated-omnis"

        version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px" y="0px"
        width="40px" height="40px"
        viewBox="0 0 82.333 82.333" enable-background="new 0 0 82.333 82.333"
        xml:space="preserve"
    >
        <g class="animated-omnis__icon-grid animated-omnis__group--to-blue">
            <path fill="#878FC6" d="M57.694,31.129c-1.484-2.352-3.474-4.342-5.825-5.823c0.646,1.263,1.214,2.643,1.691,4.129
                C55.049,29.915,56.43,30.486,57.694,31.129z"/>
            <path fill="#878FC6" d="M43.292,22.507v5.234c2.323,0.072,4.553,0.333,6.649,0.762c-0.969-2.344-2.205-4.237-3.614-5.531
                C45.343,22.736,44.331,22.58,43.292,22.507z"/>
            <path fill="#878FC6" d="M57.692,50.87c-1.265,0.644-2.643,1.215-4.132,1.691c-0.477,1.489-1.046,2.867-1.691,4.132
                C54.221,55.211,56.21,53.221,57.692,50.87z"/>
            <path fill="#878FC6" d="M60.188,44.681c-0.359-0.742-0.612-1.537-0.744-2.381h-4.192c-0.072,2.322-0.332,4.551-0.756,6.645
                c2.344-0.969,4.238-2.207,5.532-3.618C60.08,45.11,60.145,44.9,60.188,44.681z"/>
            <path fill="#878FC6" d="M60.029,36.675c-1.293-1.414-3.187-2.652-5.534-3.624c0.424,2.097,0.684,4.325,0.756,6.647h4.192
                c0.132-0.844,0.385-1.639,0.747-2.378C60.145,37.101,60.08,36.889,60.029,36.675z"/>
            <path fill="#878FC6" d="M52.168,42.3h-8.875v8.873c2.79-0.092,5.421-0.475,7.782-1.094C51.693,47.718,52.076,45.09,52.168,42.3z"/>
            <path fill="#878FC6" d="M43.292,39.699h8.875c-0.092-2.79-0.475-5.421-1.094-7.782c-2.361-0.619-4.992-1.002-7.782-1.094V39.699z"
                />
            <path fill="#878FC6" d="M43.292,59.493c1.039-0.072,2.05-0.229,3.036-0.466c1.409-1.296,2.645-3.187,3.614-5.531
                c-2.096,0.427-4.327,0.687-6.649,0.759V59.493z"/>
            <path fill="#878FC6" d="M29.499,48.945c-0.427-2.094-0.687-4.322-0.759-6.645H23.5c0.071,1.036,0.228,2.046,0.462,3.026
                C25.257,46.741,27.152,47.976,29.499,48.945z"/>
            <path fill="#878FC6" d="M40.695,22.507c-1.038,0.072-2.05,0.229-3.034,0.465c-1.409,1.294-2.645,3.188-3.612,5.528
                c2.096-0.426,4.324-0.687,6.646-0.759V22.507z"/>
            <path fill="#878FC6" d="M40.695,30.823c-2.789,0.092-5.419,0.475-7.779,1.094c-0.621,2.361-1.002,4.992-1.094,7.782h8.873V30.823z"
                />
            <path fill="#878FC6" d="M32.123,25.304c-2.353,1.481-4.344,3.472-5.827,5.822c1.265-0.643,2.645-1.214,4.135-1.691
                C30.91,27.947,31.479,26.566,32.123,25.304z"/>
            <path fill="#878FC6" d="M40.695,59.493v-5.238c-2.322-0.072-4.552-0.332-6.646-0.759c0.967,2.345,2.202,4.238,3.612,5.531
                C38.646,59.263,39.657,59.42,40.695,59.493z"/>
            <path fill="#878FC6" d="M23.499,39.699h5.241c0.071-2.322,0.332-4.551,0.759-6.647c-2.348,0.969-4.243,2.21-5.538,3.624
                C23.727,37.656,23.571,38.665,23.499,39.699z"/>
            <path fill="#878FC6" d="M32.123,56.695c-0.644-1.265-1.213-2.643-1.691-4.131c-1.489-0.478-2.868-1.049-4.133-1.691
                C27.781,53.223,29.771,55.213,32.123,56.695z"/>
            <path fill="#878FC6" d="M40.695,42.3h-8.873c0.092,2.79,0.475,5.418,1.094,7.779c2.359,0.619,4.99,1.002,7.779,1.094V42.3z"/>
        </g>
        <g class="animated-omnis__icon-external animated-omnis__group--to-blue">
            <g class="animated-omnis__icon-external__rings">
                <path fill="#878FC6" d="M36.436,14.434c0.642,1.11,0.979,2.306,1.082,3.505c1.451-0.281,2.944-0.438,4.477-0.438
                    c10.299,0,19.03,6.635,22.203,15.854c1.094-0.513,2.301-0.823,3.59-0.823c0.431,0,0.846,0.064,1.26,0.127
                    c-3.561-11.562-14.325-19.967-27.052-19.967c-2.165,0-4.264,0.266-6.291,0.726C35.961,13.743,36.223,14.065,36.436,14.434z"/>
                <path fill="#878FC6" d="M21.771,59.104c0.646-1.115,1.519-2.007,2.513-2.695c-3.58-4.107-5.765-9.463-5.783-15.339
                    c0-0.022-0.006-0.044-0.006-0.068c0-0.019,0.005-0.036,0.005-0.055c0.013-5.874,2.193-11.227,5.766-15.339
                    c-0.99-0.689-1.854-1.593-2.497-2.706c-0.211-0.366-0.356-0.747-0.508-1.127c-4.685,5.052-7.572,11.795-7.572,19.227
                    c0,7.436,2.889,14.179,7.576,19.228C21.415,59.851,21.561,59.468,21.771,59.104z"/>
                <path fill="#878FC6" d="M67.787,49.47c-1.289,0-2.499-0.311-3.592-0.826c-3.175,9.222-11.901,15.853-22.2,15.853
                    c-1.535,0-3.031-0.159-4.483-0.438c-0.103,1.202-0.432,2.401-1.072,3.515c-0.212,0.368-0.472,0.687-0.728,1.01
                    c2.023,0.46,4.121,0.725,6.283,0.725c12.728,0,23.492-8.403,27.055-19.965C68.632,49.405,68.218,49.47,67.787,49.47z"/>
            </g>
            <g class="animated-omnis__icon-external__spheres animated-omnis__group--to-darkblue">
                <path fill="#525678" d="M73.462,41.001c0-3.137-2.539-5.678-5.676-5.678s-5.683,2.541-5.683,5.678s2.546,5.674,5.683,5.674
                    S73.462,44.138,73.462,41.001z"/>
                <path fill="#525678" d="M26.262,13.754c-2.718,1.566-3.647,5.033-2.079,7.753c1.566,2.715,5.042,3.645,7.757,2.079
                    c2.718-1.568,3.645-5.045,2.079-7.755C32.446,13.116,28.979,12.181,26.262,13.754z"/>
                <path fill="#525678" d="M26.267,68.256c2.72,1.568,6.187,0.639,7.755-2.076c1.566-2.715,0.636-6.189-2.077-7.755
                    c-2.72-1.571-6.191-0.639-7.752,2.074C22.622,63.219,23.549,66.691,26.267,68.256z"/>
            </g>
        </g>
    </svg>`
  }
}

function createOmnisUiAssistant({p_callback_end = false, p_omnis, p_steps = []}) {

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
    callback_end: p_callback_end,
		id: 'omnis_control_' + Date.now(),
		stateActive: v_state_active,
    stepCounter: 0,
    stepList: [],
    stepSelected: null,
    z_index: 999999,
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
    self_destruct: function() {
      var v_control = this;
      v_control.setStateDisabled();
      document.getElementById('omnidb__main').removeChild(v_control.divElement);
      for (let i = 0; i < v_control.stepList.length; i++) {
        if (v_control.stepList[i].callback_end !== false) {
          v_control.stepList[i].callback_end();
        }
      }
      if (this.callback_end) {
        this.callback_end();
      }
      var v_omnis_div = p_omnis.div;
      v_omnis_div.style.top = p_omnis.root.getBoundingClientRect().height - 45 + 'px';
      v_omnis_div.style.left = p_omnis.root.getBoundingClientRect().width - 45 + 'px';
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
    goToStep : async function(p_index) {
      for (let i = 0; i < this.stepList.length; i++) {
        if (p_index !== i) {
          if (this.stepList[i].callback_end !== false) {
            this.stepList[i].callback_end();
          }
        }
      }
      if (this.stepList[p_index].callback_start) {
        this.stepList[p_index].callback_start();
      }
      var v_control = this;
      v_control.stepSelected = p_index;

      var v_step_item = await v_control.renderStep();
      // console.log('update position after ' + v_step_item.update_delay);
      if (v_step_item !== 'stop') {

        var get_v_target = new Promise(resolve => {
          setTimeout(function(){
            var v_next_btn = document.getElementById('omnis_step_btn_next');
            if (v_next_btn !== undefined && v_next_btn !== null) {
              v_next_btn.onclick = function(){/*console.log(v_next_btn);*/v_control.goToStep(v_control.stepSelected + 1)};
            }

            // console.log('getting the target...');
            var v_target;
            if (typeof v_step_item.target === 'function') {
              v_target = v_step_item.target();
            }
            else {
              v_target = v_step_item.target;
            }

            // console.log('target',v_target);
            v_control.updateOmnisPosition(v_target,v_step_item.position);
            resolve(v_target);

          }, v_step_item.update_delay);


        });

        await get_v_target.then(function(v_target){
          if (v_step_item.clone_target && v_target) {
            let v_update_delay = v_step_item.update_delay;

            if (v_target !== null) {
              // console.log('v_target', v_target);
              let v_target_bounding_rect = v_target.getBoundingClientRect();
              let v_target_bounding_rect_left = v_target_bounding_rect.x + 'px';
              let v_target_bounding_rect_top = v_target_bounding_rect.y + 'px';
              let v_target_bounding_rect_width = v_target_bounding_rect.width + 'px';
              // Account for getBoundingClientRect slowness.
              setTimeout(function(){
                // console.log('v_target_rect_positions', v_target_bounding_rect);
                var v_cloned_element = v_target.cloneNode(true);
                v_cloned_element.setAttribute('id','omnis_temp_clone');
                v_control.divClonedElement.style.left = v_target_bounding_rect_left;
                v_control.divClonedElement.style.top = v_target_bounding_rect_top;
                v_cloned_element.style.width = v_target_bounding_rect_width;
                v_control.updateClonedElementContent(v_cloned_element);
                v_control.divBackdropElement.style.display = '';
                v_cloned_element.addEventListener('click',function(){v_control.goToStep(v_control.stepSelected + 1)});
              },50);
            }
            else {
              // Emptying the divClonedElement.
              v_control.divClonedElement.innerHTML = '';
              v_control.divClonedElement.style.left = '';
              v_control.divClonedElement.style.top = '';
              v_control.divBackdropElement.style.display = 'none';
            }
          }
          else {
            // Emptying the divClonedElement.
            v_control.divClonedElement.innerHTML = '';
            v_control.divClonedElement.style.left = '';
            v_control.divClonedElement.style.top = '';
            v_control.divBackdropElement.style.display = 'none';
          }


          var v_previous_btn = document.getElementById('omnis_step_btn_previous');
          if (v_previous_btn !== undefined && v_previous_btn !== null) {
            v_previous_btn.onclick = function(){v_control.goToStep(v_control.stepSelected - 1)};
          }

          var v_close_btn = document.getElementById('omnis_step_btn_close');
          if (v_close_btn !== undefined && v_close_btn !== null) {
            v_close_btn.onclick = function(){
              v_control.self_destruct();
            }
          }

          if (v_control.stepList[v_control.stepSelected].callback_after_update_start) {
            v_control.stepList[v_control.stepSelected].callback_after_update_start();
          }
        });

      }
    },
    // Template
    createStep : function({
      p_callback_after_update_start = false,
      p_callback_end = false,
      p_callback_start = false,
      p_clone_target = false,
      p_message = 'Example',
      p_next_button = true,
      p_position = ()=>{return false},
      p_target = null,
      p_title = 'Omnis',
      p_update_delay = 0
    }) {
			var v_control = this;
			var v_index = v_control.stepCounter;

			v_control.stepCounter++;

			var v_step = {
        callback_after_update_start: p_callback_after_update_start,
        callback_end: p_callback_end,
        callback_start: p_callback_start,
        clone_target: p_clone_target,
				id: v_control.id + '_step_' + v_index,
        message: p_message,
        next_button: p_next_button,
        position: p_position(),
        target: p_target,
        title: p_title,
        update_delay: p_update_delay
			};


      this.stepList.push(v_step);

    },
    renderStep : function() {
      if (this.stateActive) {
        var v_control = this;
        var v_step_item = this.stepList[this.stepSelected];
        // Emptying the divClonedElement.
        v_control.divClonedElement.innerHTML = '';
        v_control.divClonedElement.style.left = '';
        v_control.divClonedElement.style.top = '';
        v_control.divBackdropElement.style.display = '';
        // Emptying the divWavesElement.
        v_control.divWavesElement.innerHTML = '';

        var v_title = '';
        if (v_step_item.title) {
          v_title += '<div class="omnis__step__title card-title p-2 mt-2 mb-0"><h5 class="mb-0">' + v_step_item.title + '</h5></div>';
        }

        var v_message = '';
        if (v_step_item.message) {
          v_message += '<div class="omnis__step__body card-body p-2 mb-4">' + v_step_item.message + '</div>';
        }

        var v_step_btn_next = '';
        if (this.stepList[this.stepSelected].next_button && this.stepSelected < this.stepCounter - 1) {
          v_step_btn_next += '<button id="omnis_step_btn_next" type="button" class="btn btn-sm omnidb__theme__btn--primary ml-2">Next</button>';
        }

        // Temporarily disabling previous button.
        // TODO: implement a better goto method when going to previous steps, allowing the UI not to break because of callbacks.
        var v_step_btn_previous = '';
        // if (this.stepSelected > 0) {
        //   v_step_btn_previous += '<button id="omnis_step_btn_previous" type="button" class="btn btn-sm omnidb__theme__btn--secondary mr-2">Previous</button>';
        // }

        var v_step_btn_close = '<button id="omnis_step_btn_close" type="button" class="btn btn-sm btn-danger ml-auto">End walkthrough</button>';

        var v_step_title =
        '<div class="mb-4 text-center" style="position: relative;">' +
          // '<div style="background: none; display: inline-block; height: 64px; width:64px;">' + v_animated_omnis + '</div>' +
          v_title +
        '</div>';

        var v_step_html =
        '<div class="omnis__step card">' +
          v_step_title +
          v_message +
          '<div class="omnis__step__footer card-footer d-flex align-items-center p-2">' +
            v_step_btn_previous +
            v_step_btn_next +
            v_step_btn_close +
          '</div>' +
        '</div>';

        this.divCardElement.innerHTML = v_step_html;

        this.divElement.style.display = 'block';

        return new Promise(resolve => {
          resolve(v_step_item);
        });
      }
      else {
        this.divElement.style.display = 'none';
        // Emptying the divWavesElement.
        this.divWavesElement.innerHTML = '';

        return new Promise(resolve => {
          resolve('stop');
        });
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
    updateClonedElementContent: function(p_content_element) {
      var v_control = this;
      var v_cloned_element = v_control.divClonedElement;
      var v_waves_element = v_control.divWavesElement;
      v_cloned_element.innerHTML = '';
      v_waves_element.innerHTML = '';
      v_cloned_element.appendChild(p_content_element);
      v_waves_element.innerHTML =
      '<span id="' + v_control.id + '_cloned_element_waves" class="omnis__cloned-element__waves">' +
        '<span></span>' +
        '<span></span>' +
        '<span></span>' +
        '<span></span>' +
      '</span>';
      let v_target = (typeof v_control.stepList[v_control.stepSelected].target === 'function')
      ? v_control.stepList[v_control.stepSelected].target()
      : v_control.stepList[v_control.stepSelected].target;
      let v_cloned_element_bounding_rect = v_target.getBoundingClientRect();
      v_waves_element.style.left = v_cloned_element_bounding_rect.x + 'px';
      v_waves_element.style.top = v_cloned_element_bounding_rect.y + 'px';
      v_waves_element.style.width = v_cloned_element_bounding_rect.width + 'px';
      v_waves_element.style.height = v_cloned_element_bounding_rect.height + 'px';
      v_waves_element.style.display = 'block';
      var v_cloned_element_waves = document.getElementById(v_control.id + '_cloned_element_waves');
    },
    updateOmnisPosition : function(p_target, p_pos = false) {
      try {
        let v_root = document.getElementById('omnidb__main');
        let v_window_width = v_root.offsetWidth;
        let v_window_width_half = Math.round(v_window_width / 2);
        let v_window_height = v_root.offsetHeight;
        let v_window_height_half = Math.round(v_window_height / 2);
        var v_control = this;
        var v_target = p_target;
        if (!v_target) {
          v_target = (typeof v_control.stepList[v_control.stepSelected].target === 'function')
          ? v_control.stepList[v_control.stepSelected].target()
          : v_control.stepList[v_control.stepSelected].target;
        }
        var v_target_position;
        var v_target_offset_width = 0;
        if (p_pos) {
          v_target_position = {x:p_pos.x, y:p_pos.y}
        }
        else if (v_target) {
          v_target_position = v_control.getPosition(v_target);
          v_target_offset_width = v_target.offsetWidth;
        }
        else {
          v_target_position = {x:v_window_width - 5, y:v_window_height - 5}
        }
        var v_omnis_div = p_omnis.div;

        // Target contextual cases for positioning:
        // Right side of the screen.
        if (v_target_position.x >= v_window_width_half) {
          v_omnis_div.style.left = v_target_position.x - 56 + 'px';
          v_control.divCardElement.style.left = v_target_position.x - v_control.divCardElement.offsetWidth - 56 + 'px';
          // Above vertical middle of the screen.
          if (v_target_position.y <= v_window_height_half) {
            v_omnis_div.style.top = v_target_position.y + 16 + 'px';
            v_control.divCardElement.style.top = v_target_position.y + 20 + 'px';
          }
          // Below vertical middle of the screen.
          else {
            v_omnis_div.style.top = v_target_position.y - 56 + 'px';
            v_control.divCardElement.style.top = v_target_position.y - v_control.divCardElement.offsetHeight - 20 + 'px';
          }
        }
        // Left side of the screen.
        else {
          v_omnis_div.style.left = v_target_position.x + v_target_offset_width + 16 + 'px';
          v_control.divCardElement.style.left = v_target_position.x + v_target_offset_width + 56 + 'px';
          // Above vertical middle of the screen.
          if (v_target_position.y <= v_window_height_half) {
            v_omnis_div.style.top = v_target_position.y + 16 + 'px';
            v_control.divCardElement.style.top = v_target_position.y + 20 + 'px';
          }
          // Below vertical middle of the screen.
          else {
            v_omnis_div.style.top = v_target_position.y - 56 + 'px';
            v_control.divCardElement.style.top = v_target_position.y - v_control.divCardElement.offsetHeight - 20 + 'px';
          }
        }
      }
      catch(e) {
        console.warn('omnis-ui-assistant couldnt process the positioning of the target. Details:');
        console.warn(e);
      }
    }
  }

  v_omnisControl.divCardElement = document.createElement('div');
  v_omnisControl.divCardElement.setAttribute('style', 'position:fixed; width:280px; max-width: 90vw; z-index: ' + v_omnisControl.z_index + 3 + '; box-shadow: 1px 0px 3px rgba(0,0,0,0.15); transition: all 0.45s ease 0.1s;');

  v_omnisControl.divClonedElement = document.createElement('div');
  v_omnisControl.divClonedElement.setAttribute('style', 'position:absolute; width:0px; height:0px; overflow:visible; z-index:' + v_omnisControl.z_index + 2 + ';');

  v_omnisControl.divWavesElement = document.createElement('div');
  v_omnisControl.divWavesElement.setAttribute('style', 'position:absolute; width:0px; height:0px; overflow:visible; z-index:' + v_omnisControl.z_index + 1 + ';');

  v_omnisControl.divBackdropElement = document.createElement('div');
  v_omnisControl.divBackdropElement.setAttribute('style', 'position:fixed; width:100vw; height:100vh; top: 0; left: 0; z-index:' + v_omnisControl.z_index + '; background-color:rgba(0,0,0,0.25);');

  v_omnisControl.divElement = document.createElement('div');
  v_omnisControl.divElement.setAttribute('id', v_omnisControl.id);

  v_omnisControl.divElement.appendChild(v_omnisControl.divCardElement);
  v_omnisControl.divElement.appendChild(v_omnisControl.divClonedElement);
  v_omnisControl.divElement.appendChild(v_omnisControl.divWavesElement);
  v_omnisControl.divElement.appendChild(v_omnisControl.divBackdropElement);
  document.getElementById('omnidb__main').appendChild(v_omnisControl.divElement);

  return v_omnisControl;

}
