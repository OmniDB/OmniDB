/*MIT License

Copyright (c) 2017 Israel Barth Rubio

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
SOFTWARE.*/

/// <summary>
/// Function to handle dragover event while dragging popups.
/// </summary>
/// <param name="p_event">Javascript Event Object.</param>
var gv_popUpdragOverFunction = function(p_event) {
    p_event.preventDefault();

    return false;
}

/// <summary>
/// Function to handle drop event while dragging popups.
/// </summary>
/// <param name="p_event">Javascript Event Object.</param>
var gv_popUpDropFunction = function(p_event) {
    var v_parameters = p_event.dataTransfer.getData('text/plain').split(',');
    var v_popUpContainer = document.getElementById(v_parameters[2]);

    if(v_popUpContainer != null) {
	    if(v_popUpContainer.classList.contains('minimized-popup-container')) {
			return false;
		}

		var v_left = (p_event.clientX + parseInt(v_parameters[0], 10));

		//Doesn't allow hide on left
		if(v_left + v_popUpContainer.offsetWidth < 55) {
			v_left = -(v_popUpContainer.offsetWidth - 55);
		}

		//Doesn't allow hide on right
		if(window.innerWidth - v_left < 55) {
			v_left = window.innerWidth - 55;
		}

		v_popUpContainer.style.left = v_left + 'px';

		var v_top = (p_event.clientY + parseInt(v_parameters[1], 10));

		//Doesn't allow hide on top
		if(v_top + v_popUpContainer.offsetHeight < 55) {
			v_top = -(v_popUpContainer.offsetHeight - 55);
		}

		//Doesn't allow hide on bottom
		if(window.innerHeight - v_top < 110) {
			v_top = window.innerHeight - 110;
		}

	    v_popUpContainer.style.top = v_top + 'px';

	    if(v_popUpContainer.v_popUpObject != null) {
	    	v_popUpContainer.v_popUpObject.config.left = v_popUpContainer.style.left;
	    	v_popUpContainer.v_popUpObject.config.top = v_popUpContainer.style.top;

	    	if(v_popUpContainer.v_popUpObject.closePopUp != null) {
	    		var v_top = (v_popUpContainer.offsetTop + ((v_popUpContainer.offsetHeight - 125) / 2)) + 'px';
	    		var v_left = (v_popUpContainer.offsetLeft + ((v_popUpContainer.offsetWidth - 205) / 2)) + 'px';

	    		v_popUpContainer.v_popUpObject.closePopUp.changePosition(v_top, v_left);
	    		v_popUpContainer.v_popUpObject.closePopUp.turnActive();
			}

	    	if(v_popUpContainer.v_popUpObject.callbacks.afterDrag != null) {
				v_popUpContainer.v_popUpObject.callbacks.afterDrag(v_popUpContainer.v_popUpObject);
			}
	    }
	}

	p_event.preventDefault();

	return false;
}

/// <summary>
/// Function to handle keydown event on document body.
/// </summary>
/// <param name="p_event">Javascript Event Object.</param>
var gv_popUpKeyDownFunction = function(p_event) {
	if(p_event.keyCode == 17) {//Ctrl
		this.isCtrlPressed = true;
	}
}

/// <summary>
/// Function to handle keyup event on document body.
/// </summary>
/// <param name="p_event">Javascript Event Object.</param>
var gv_popUpKeyUpFunction = function(p_event) {
	if(p_event.keyCode == 17) {//Ctrl
		this.isCtrlPressed = false;
	}
}

/// <summary>
/// Function to handle click event on document body.
/// </summary>
/// <param name="p_event">Javascript Event Object.</param>
var gv_popUpClickFunction = function(p_event) {
	var v_popUpList = document.querySelectorAll('.popup-container');

	for(var i = 0; i < v_popUpList.length; i++) {
		if(!v_popUpList[i].classList.contains('hidden-popup') && v_popUpList[i].v_popUpObject != null) {
			v_popUpList[i].v_popUpObject.unselect();
		}
	}
}

/// <summary>
/// Creates a popup control.
/// </summary>
/// <param name="p_id">The id to be given to this popup control.</param>
/// <paramref name="p_id">Takes a String.
/// <param name="p_startZIndex">The starting z-index for popups. Each created popup will increment this value.</param>
/// <paramref name="p_startZIndex">Takes a number.
/// <returns>Popup control javascript object</returns>
function createPopUpControl(p_id, p_startZIndex) {
	if(p_startZIndex != null && (typeof p_startZIndex != 'number' || p_startZIndex < 0)) {
		return null;
	}

	//Create object to be returned
	var v_popUpControlObject = {
		actualZIndex: ((p_startZIndex == null) ? 1 : p_startZIndex),
		closePopUp: null,
		containerElement: document.body,
		id: ((p_id == null) ? 'popup_control_0' : 'popup_control_' + p_id),
		idCounter: 0,
		popUpList: [],
		maximizing: false, //If a maximizeAllSelected is running
		minimizedPopUpsContainerElement: null, // Where popups are placed when minimized
		minimizing: false, //If a minimizeAllSelected is running
		startZIndex: ((p_startZIndex == null) ? 1 : p_startZIndex),
		tag: {//Object to save useful things
		},
		/// <summary>
		/// Creates a popup.
		/// </summary>
		/// <param name="p_id">The id to be given to this popup.</param>
		/// <paramref name="p_id">Takes a String.
		/// <param name="p_title">The text to be displayed in the header.</param>
		/// <paramref name="p_title">Takes a string.
		/// <param name="p_innerHtml">The content to be displayed in the details.</param>
		/// <paramref name="p_innerHtml">Takes a string
		/// <param name="p_config">Some configurations of the popup.</param>
		/// <paramref name="p_title">Takes javascript object with the following structure: {width: String, height: String, resizable: boolean, draggable: boolean, top: String, left: String, forceClose: boolean}.
		/// <param name="p_callbacks">Some callbacks when actions are executed in the popup.</param>
		/// <paramref name="p_callbacks">Takes javascript object with the following structure: {beforeMinimize: function, afterMinimize: function, beforeMaximize: function, afterMaximize: function, beforeClose: function, afterClose: function, beforeDrag: function, afterDrag: function, beforeResize: function, afterResize: function, closeCallbacks: {yesFunction: function, noFunction: function, cancelFunction: function}, beforeSelect, afterSelect, beforeUnselect, afterUnselect}.
		/// <returns>Popup javascript object</returns>
		addPopUp: function(p_id, p_title, p_innerHtml, p_config, p_callbacks) {
			var v_parent = this;

			if(p_id == null) {
				v_parent.idCounter++;
			}

			//Create object to be returned
			var v_popUpObject = {
				activePopUp: false,
				callbacks: {
					beforeMinimize: null,//function(){},
					afterMinimize: null,//function(){},
					beforeMaximize: null,//function(){},
					afterMaximize: null,//function(){},
					beforeClose: null,//function(){},
					afterClose: null,//function(){},
					beforeDrag: null,//function(){},
					afterDrag: null,//function(){},
					beforeResize: null,//function(){},
					afterResize: null,//function(){},
					closeCallbacks: {
						yesFunction: null,//function(){},
						noFunction: null,//function(){},
						cancelFunction: null,//function(){},
					},
					beforeSelect: null,//function(){},
					afterSelect: null,//function(){},
					beforeUnselect: null,//function(){},
					afterUnselect: null,//function(){},
				},
				closeElement: null,
				closePopUp: null,
				config: {
					defaultWidth: '300px',
					width: '300px',
					defaultHeight: '300px',
					height: '300px',
					resizable: true,
					draggable: true,
					defaultTop: '10%',
					top: '10%',
					defaultLeft: '10%',
					left: '10%',
					forceClose: false
				},
				containerElement: null,
				contentElement: null,
				headerElement: null,
				id: ((p_id == null) ? String(v_parent.idCounter) : p_id),
				selected: false,
				innerHtml: p_innerHtml,
				maximizeElement: null,
				minimized: false,
				minimizeElement: null,
				parent: v_parent,
				tag: {
				},
				title: p_title,
				titleElement: null,
				visible: true,
				zIndex: v_parent.actualZIndex++,
				/// <summary>
				/// Change popup position in the screen.
				/// </summary>
				/// <param name="p_top">New top position.</param>
				/// <paramref name="p_top">Takes a string.
				/// <param name="p_left">New left position.</param>
				/// <paramref name="p_left">Takes a string.
				changePosition: function(p_top, p_left) {
					if(p_top != null && typeof p_top == 'string') {
						this.config.top = p_top;
						this.containerElement.style.top = this.config.top;
					}

					if(p_left != null && typeof p_left == 'string') {
						this.config.left = p_left;
						this.containerElement.style.left = this.config.left;
					}
				},
				/// <summary>
				/// Changes popup size in the screen.
				/// </summary>
				/// <param name="p_width">New width.</param>
				/// <paramref name="p_width">Takes a string.
				/// <param name="p_height">New height.</param>
				/// <paramref name="p_height">Takes a string.
				changeSize: function(p_width, p_height) {
					if(p_width != null && typeof p_width == 'string') {
						this.config.width = p_width;
						this.containerElement.style.width = this.config.width;
					}

					if(p_height != null && typeof p_height == 'string') {
						this.config.height = p_height;
						this.containerElement.style.height = this.config.height;
					}
				},
				/// <summary>
				/// Removes the popup.
				/// </summary>
				/// <param name="p_forceClose">If the popup should be removed or if user should be asked about it before removing.</param>
				/// <paramref name="p_forceClose">Takes a boolean.
				/// <param name="p_callbacks">If the popup should be removed or if user should be asked about it before removing.</param>
				/// <paramref name="p_callbacks">Takes a javascript object with functions, using the following structure: {yesFunction, noFunction, cancelFunction}.
				close: function(p_forceClose, p_callbacks) {
					//Check if it is a multi-selection close before proceeding
					if(this.parent.countSelected() > 0 && this.parent.closePopUp == null) {//If there are popups selected, user wasn't asked about removing all yet and this makes part of selection
						if(this.selected) {
							this.parent.closeAllSelected();
							return;
						}
						else {
							this.parent.unselectAllSelected();
						}
					}

					if(!p_forceClose) {
						if(this.closePopUp != null) {
							this.closePopUp.turnActive();
							return;
						}

						var v_popUpToBeClosed = this;

						var v_html =
							'<div>' +
							'    Do you want to save data before closing this popup?' +
							'</div>' +
							'<br />' +
							'<div>' +
							'    <button id="button_close_yes_' + this.id + '">Yes</button>' +
							'    <button id="button_close_no_' + this.id + '">No</button>' +
							'    <button id="button_close_cancel_' + this.id + '">Cancel</button>' +
							'</div>';

						//If the popup to be closed is minimized, maximize it
						if(this.minimized) {
							this.maximize();
						}

						//The popup asking if user wants to remove this popup should be centered inside this popup, so check it
						if(this.containerElement.offsetWidth < 255) {
							this.changeSize('255px', null);
						}

						if(this.containerElement.offsetHeight < 175) {
							this.changeSize(null, '175px');
						}

						//Disable header buttons while close popup is open
						if(!this.closeElement.classList.contains('disabled-button')) {
							this.closeElement.classList.add('disabled-button');
							this.closeElement.disabled = true;
						}

						if(!this.minimizeElement.classList.contains('disabled-button')) {
							this.minimizeElement.classList.add('disabled-button');
							this.minimizeElement.disabled = true;
						}

						//Make it not resizable
						if(this.config.resizable) {
							//$(this.containerElement).resizable('disable');
							$(this.containerElement).resizable('destroy');
						}

						var v_config = {
							width: '300px',
							height: '125px',
							resizable: false,
							draggable: false,
							top: (this.containerElement.offsetTop + ((this.containerElement.offsetHeight - 125) / 2)) + 'px',
							left: (this.containerElement.offsetLeft + ((this.containerElement.offsetWidth - 205) / 2)) + 'px',
							forceClose: true
						};

						var v_callbacks = null;

						var v_closePopUp = this.parent.addPopUp(
							'close_' + this.id,
							'Attention!',
							v_html,
							v_config,
							v_callbacks
						);

						this.closePopUp = v_closePopUp;

						v_closePopUp.closeElement.classList.add('hidden-button');
						v_closePopUp.minimizeElement.classList.add('hidden-button');

						var v_closeYes = document.getElementById('button_close_yes_' + this.id);

						v_closeYes.addEventListener(
							'mousedown',
							function(p_popUpToBeClosed, p_callback, p_event) {
								p_event.stopPropagation();//In order to avoid bugs while closing popup

								if(p_callback != null && typeof p_callback == 'function') {
									p_callback(p_popUpToBeClosed);
								}

								p_popUpToBeClosed.close(true);
								p_popUpToBeClosed.closePopUp.close(true);
								p_popUpToBeClosed.closePopUp = null;

							}.bind(v_closeYes, v_popUpToBeClosed, ((p_callbacks != null && p_callbacks.yesFunction != null) ? p_callbacks.yesFunction : this.callbacks.closeCallbacks.yesFunction))
						);

						v_closeYes.addEventListener(
							'keydown',
							function(p_event) {
								if(p_event.keyCode == 13) {//Enter
									p_event.preventDefault();
									this.dispatchEvent(new Event('mousedown'));
								}
							}
						);

						v_closeYes.focus();

						var v_closeNo = document.getElementById('button_close_no_' + this.id);

						v_closeNo.addEventListener(
							'mousedown',
							function(p_popUpToBeClosed, p_callback, p_event) {
								p_event.stopPropagation();//In order to avoid bugs while closing popup

								if(p_callback != null && typeof p_callback == 'function') {
									p_callback(p_popUpToBeClosed);
								}

								p_popUpToBeClosed.close(true);
								p_popUpToBeClosed.closePopUp.close(true);
								p_popUpToBeClosed.closePopUp = null;
							}.bind(v_closeNo, v_popUpToBeClosed, ((p_callbacks != null && p_callbacks.noFunction != null) ? p_callbacks.noFunction : this.callbacks.closeCallbacks.noFunction))
						);

						v_closeNo.addEventListener(
							'keydown',
							function(p_event) {
								if(p_event.keyCode == 13) {//Enter
									p_event.preventDefault();
									this.dispatchEvent(new Event('mousedown'));
								}
							}
						);

						var v_closeCancel = document.getElementById('button_close_cancel_' + this.id);

						v_closeCancel.addEventListener(
							'mousedown',
							function(p_popUpToBeClosed, p_callback, p_event) {
								p_event.stopPropagation();//In order to avoid bugs while closing popup

								if(p_callback != null && typeof p_callback == 'function') {
									p_callback(p_popUpToBeClosed);
								}

								p_popUpToBeClosed.closePopUp.close(true);
								p_popUpToBeClosed.closePopUp = null;

								//Make it resizable again
								if(p_popUpToBeClosed.config.resizable) {
									//$(this.containerElement).resizable('enable');

									$(p_popUpToBeClosed.containerElement).resizable({
										start: function(p_event, p_ui) {
											if(p_event.target.v_popUpObject != null) {
												if(p_event.target.v_popUpObject.callbacks.beforeResize != null) {
													p_event.target.v_popUpObject.callbacks.beforeResize(p_event.target.v_popUpObject);
												}
											}
										},
										stop: function(p_event, p_ui) {
											if(p_event.target.v_popUpObject != null) {
												p_event.target.v_popUpObject.config.width = p_event.target.style.width;

												if(p_event.target.offsetWidth < 175) {
													p_event.target.v_popUpObject.changeSize('175px', null);
												}

												p_event.target.v_popUpObject.config.height = p_event.target.style.height;

												if(p_event.target.offsetHeight < 50) {
													p_event.target.v_popUpObject.changeSize(null, '50px');
												}

												if(p_event.target.v_popUpObject.callbacks.afterResize != null) {
													p_event.target.v_popUpObject.callbacks.afterResize(p_event.target.v_popUpObject);
												}
											}
										}
									});
								}

								if(p_popUpToBeClosed.closeElement.classList.contains('disabled-button')) {
									p_popUpToBeClosed.closeElement.classList.remove('disabled-button');
									p_popUpToBeClosed.closeElement.disabled = false;
								}

								if(p_popUpToBeClosed.minimizeElement.classList.contains('disabled-button')) {
									p_popUpToBeClosed.minimizeElement.classList.remove('disabled-button');
									p_popUpToBeClosed.minimizeElement.disabled = false;
								}

								p_popUpToBeClosed.turnActive();
							}.bind(v_closeCancel, v_popUpToBeClosed, ((p_callbacks != null && p_callbacks.cancelFunction != null) ? p_callbacks.cancelFunction : this.callbacks.closeCallbacks.cancelFunction))
						);

						v_closeCancel.addEventListener(
							'keydown',
							function(p_event) {
								if(p_event.keyCode == 13) {//Enter
									p_event.preventDefault();
									this.dispatchEvent(new Event('mousedown'));
								}
							}
						);

						return;
					}

					if(this.callbacks.beforeClose != null) {
						this.callbacks.beforeClose(this);
					}

					this.containerElement.remove();
					this.parent.popUpList.splice(this.parent.popUpList.indexOf(this), 1);
					this.parent.actualZIndex--;

					if(this.parent.popUpList.length > 0 && this.id.indexOf('close_') != 0) {//In order to avoid runtime bugs caused by events
						this.parent.popUpList[this.parent.popUpList.length - 1].turnActive();
					}

					if(this.callbacks.afterClose != null) {
						this.callbacks.afterClose(this);
					}
				},
				/// <summary>
				/// Hides the popup.
				/// </summary>
				hide: function() {
					if(this.visible) {
						this.visible = false;

						if(!this.containerElement.classList.contains('hidden-popup')) {
							this.containerElement.classList.add('hidden-popup');
						}
					}
				},
				/// <summary>
				/// Maximize the popup.
				/// </summary>
				maximize: function() {
					if(this.closePopUp != null) {
						return;
					}

					//Check if it is a multi-selection maximize before proceeding
					if(this.parent.countSelected() > 0 && !this.parent.maximizing) {//If there are popups selected and maximize all wasn't called yet
						if(this.selected) {
							this.parent.maximizeAllSelected();
							return;
						}
						else {
							this.parent.unselectAllSelected();
						}
					}

					if(this.minimized) {
						if(this.callbacks.beforeMaximize != null) {
							this.callbacks.beforeMaximize(this);
						}

						this.minimized = false;

						/*//Restore maximized configurations
						this.containerElement.style.zIndex = this.zIndex;
						this.containerElement.style.width = this.config.width;
						this.containerElement.style.height = this.config.height;
						this.containerElement.style.top = this.config.top;
						this.containerElement.style.left = this.config.left;*/

						//Set maximized configurations
						this.config.width = this.config.defaultWidth;
						this.config.height = this.config.defaultHeight;
						this.config.top = this.config.defaultTop;
						this.config.left = this.config.defaultLeft;

						this.containerElement.style.zIndex = this.zIndex;
						this.containerElement.style.width = this.config.width;
						this.containerElement.style.height = this.config.height;
						this.containerElement.style.top = this.config.top;
						this.containerElement.style.left = this.config.left;

						if(this.containerElement.classList.contains('minimized-popup-container')) {
							this.containerElement.classList.remove('minimized-popup-container');
						}

						if(this.contentElement.classList.contains('hidden-content')) {
							this.contentElement.classList.remove('hidden-content');
						}

						if(this.titleElement.classList.contains('minimized-popup-header-title')) {
							this.titleElement.classList.remove('minimized-popup-header-title');
						}

						if(this.minimizeElement.classList.contains('hidden-button')) {
							this.minimizeElement.classList.remove('hidden-button');
						}

						if(!this.maximizeElement.classList.contains('hidden-button')) {
							this.maximizeElement.classList.add('hidden-button');
						}

						//Make it resizable again
						if(this.config.resizable) {
							//$(this.containerElement).resizable('enable');

							$(this.containerElement).resizable({
								start: function(p_event, p_ui) {
									if(p_event.target.v_popUpObject != null) {
										if(p_event.target.v_popUpObject.callbacks.beforeResize != null) {
											p_event.target.v_popUpObject.callbacks.beforeResize(p_event.target.v_popUpObject);
										}
									}
								},
								stop: function(p_event, p_ui) {
									if(p_event.target.v_popUpObject != null) {
										p_event.target.v_popUpObject.config.width = p_event.target.style.width;

										if(p_event.target.offsetWidth < 175) {
											p_event.target.v_popUpObject.changeSize('175px', null);
										}

										p_event.target.v_popUpObject.config.height = p_event.target.style.height;

										if(p_event.target.offsetHeight < 50) {
											p_event.target.v_popUpObject.changeSize(null, '50px');
										}

										if(p_event.target.v_popUpObject.callbacks.afterResize != null) {
											p_event.target.v_popUpObject.callbacks.afterResize(p_event.target.v_popUpObject);
										}
									}
								}
							});
						}

						//Append to body
						this.parent.containerElement.appendChild(this.containerElement);

						this.turnActive();

						if(this.callbacks.afterMaximize != null) {
							this.callbacks.afterMaximize(this);
						}
					}
				},
				/// <summary>
				/// minimize the popup.
				/// </summary>
				minimize: function() {
					if(this.closePopUp != null) {
						return;
					}

					//Check if it is a multi-selection minimize before proceeding
					if(this.parent.countSelected() > 0 && !this.parent.minimizing) {//If there are popups selected and minimize all wasn't called yet
						if(this.selected) {
							this.parent.minimizeAllSelected();
							return;
						}
						else {
							this.parent.unselectAllSelected();
						}
					}

					if(!this.minimized) {
						if(this.callbacks.beforeMinimize != null) {
							this.callbacks.beforeMinimize(this);
						}

						this.minimized = true;

						//Clean maximized configurations
						this.containerElement.style.zIndex = '';
						this.containerElement.style.width = '';
						this.containerElement.style.height = '';
						this.containerElement.style.top = '';
						this.containerElement.style.left = '';

						if(!this.containerElement.classList.contains('minimized-popup-container')) {
							this.containerElement.classList.add('minimized-popup-container');
						}

						if(!this.contentElement.classList.contains('hidden-content')) {
							this.contentElement.classList.add('hidden-content');
						}

						if(!this.titleElement.classList.contains('minimized-popup-header-title')) {
							this.titleElement.classList.add('minimized-popup-header-title');
						}

						if(!this.minimizeElement.classList.contains('hidden-button')) {
							this.minimizeElement.classList.add('hidden-button');
						}

						if(this.maximizeElement.classList.contains('hidden-button')) {
							this.maximizeElement.classList.remove('hidden-button');
						}

						//Make it not resizable
						if(this.config.resizable) {
							//$(this.containerElement).resizable('disable');
							$(this.containerElement).resizable('destroy');
						}

						//Append to where minimized popups should be displayed
						this.parent.minimizedPopUpsContainerElement.appendChild(this.containerElement);

						if(this.callbacks.afterMinimize != null) {
							this.callbacks.afterMinimize(this);
						}
					}
				},
				/// <summary>
				/// Selects the popup.
				/// </summary>
				select: function() {
					if(!this.selected) {
						if(this.callbacks.beforeSelect != null) {
							this.callbacks.beforeSelect(this);
						}

						this.selected = true;

						if(!this.containerElement.classList.contains('selected-popup')) {
							this.containerElement.classList.add('selected-popup');
						}

						if(this.callbacks.afterSelect != null) {
							this.callbacks.afterSelect(this);
						}
					}
				},
				/// <summary>
				/// Changes the content of the popup.
				/// </summary>
				/// <param name="p_innerHtml">The content to be displayed in the details.</param>
				/// <paramref name="p_innerHtml">Takes a string
				setContent: function(p_innerHtml) {
					this.innerHtml = p_innerHtml;
					this.contentElement.innerHTML = p_innerHtml;
				},
				/// <summary>
				/// Changes the title of the popup.
				/// </summary>
				/// <param name="p_title">The text to be displayed in the header.</param>
				/// <paramref name="p_title">Takes a string.
				setTitle: function(p_title) {
					this.title = p_title;
					this.titleElement.innerHTML = p_title;
					this.titleElement.title = p_title;
				},
				/// <summary>
				/// Shows the popup.
				/// </summary>
				show: function() {
					if(!this.visible) {
						this.visible = true;

						if(this.containerElement.classList.contains('hidden-popup')) {
							this.containerElement.classList.remove('hidden-popup');
						}
					}
				},
				/// <summary>
				/// Turns this popup the active one among popups of the controller.
				/// </summary>
				turnActive: function() {
					if(this.parent.getActivePopUp() == this) {
						return;
					}

					this.parent.orderPopUpsByZIndex();

					var v_newPopUpList = [];

					//Other popups go to background
					for(var i = 0; i < this.parent.popUpList.length; i++) {
						if(this.parent.popUpList[i] != this) {
							if(this.parent.popUpList[i].containerElement.classList.contains('active-popup')) {
								this.parent.popUpList[i].containerElement.classList.remove('active-popup');
							}

							if(!this.parent.popUpList[i].containerElement.classList.contains('inactive-popup')) {
								this.parent.popUpList[i].containerElement.classList.add('inactive-popup');
							}

							this.parent.popUpList[i].zIndex = this.parent.startZIndex + i;
							this.parent.popUpList[i].containerElement.style.zIndex = this.parent.popUpList[i].zIndex;
							this.parent.popUpList[i].activePopUp = false;
							v_newPopUpList.push(this.parent.popUpList[i]);
						}
					}

					//This popup goes to foreground
					if(this.containerElement.classList.contains('inactive-popup')) {
						this.containerElement.classList.remove('inactive-popup');
					}

					if(!this.containerElement.classList.contains('active-popup')) {
						this.containerElement.classList.add('active-popup');
					}

					this.zIndex = this.parent.actualZIndex;
					this.containerElement.style.zIndex = this.zIndex
					this.activePopUp = true;
					v_newPopUpList.push(this);

					this.parent.popUpList = v_newPopUpList;

					if(this.closePopUp != null) {
						this.closePopUp.turnActive();
					}

					if(this.id.indexOf('close_') == 0) {
						var v_buttonYes = document.getElementById('button_close_yes_' + this.id.substring(6, this.id.length));//Discard 'close_' from string start

						if(v_buttonYes != null) {//In order to avoid bugs between events and focusing
							setTimeout(
								function() {
									v_buttonYes.focus();
								},
								10
							);
						}
					}
				},
				/// <summary>
				/// Unselects the popup.
				/// </summary>
				unselect: function() {
					if(this.selected) {
						if(this.callbacks.beforeUnselect != null) {
							this.callbacks.beforeUnselect(this);
						}

						this.selected = false;

						if(this.containerElement.classList.contains('selected-popup')) {
							this.containerElement.classList.remove('selected-popup');
						}

						if(this.callbacks.afterUnselect != null) {
							this.callbacks.afterUnselect(this);
						}
					}
				}
			};

			//Check configuration parameters
			if(p_config != null && typeof p_config == 'object') {
				if(p_config.width != null && typeof p_config.width == 'string') {
					v_popUpObject.config.defaultWidth = p_config.width;
					v_popUpObject.config.width = p_config.width;
				}

				if(p_config.height != null && typeof p_config.height == 'string') {
					v_popUpObject.config.defaultHeight = p_config.height;
					v_popUpObject.config.height = p_config.height;
				}

				if(p_config.resizable != null && typeof p_config.resizable == 'boolean') {
					v_popUpObject.config.resizable = p_config.resizable;
				}

				if(p_config.draggable != null && typeof p_config.draggable == 'boolean') {
					v_popUpObject.config.draggable = p_config.draggable;
				}

				if(p_config.top != null && typeof p_config.top == 'string') {
					v_popUpObject.config.defaultTop = p_config.top;
					v_popUpObject.config.top = p_config.top;
				}

				if(p_config.left != null && typeof p_config.left == 'string') {
					v_popUpObject.config.defaultLeft = p_config.left;
					v_popUpObject.config.left = p_config.left;
				}

				if(p_config.forceClose != null && typeof p_config.forceClose == 'boolean') {
					v_popUpObject.config.forceClose = p_config.forceClose;
				}
			}

			//Check callback parameters
			if(p_callbacks != null && typeof p_callbacks == 'object') {
				if(p_callbacks.beforeMinimize != null && typeof p_callbacks.beforeMinimize == 'function') {
					v_popUpObject.callbacks.beforeMinimize = p_callbacks.beforeMinimize;
				}

				if(p_callbacks.afterMinimize != null && typeof p_callbacks.afterMinimize == 'function') {
					v_popUpObject.callbacks.afterMinimize = p_callbacks.afterMinimize;
				}

				if(p_callbacks.beforeMaximize != null && typeof p_callbacks.beforeMaximize == 'function') {
					v_popUpObject.callbacks.beforeMaximize = p_callbacks.beforeMaximize;
				}

				if(p_callbacks.afterMaximize != null && typeof p_callbacks.afterMaximize == 'function') {
					v_popUpObject.callbacks.afterMaximize = p_callbacks.afterMaximize;
				}

				if(p_callbacks.beforeClose != null && typeof p_callbacks.beforeClose == 'function') {
					v_popUpObject.callbacks.beforeClose = p_callbacks.beforeClose;
				}

				if(p_callbacks.afterClose != null && typeof p_callbacks.afterClose == 'function') {
					v_popUpObject.callbacks.afterClose = p_callbacks.afterClose;
				}

				if(p_callbacks.beforeDrag != null && typeof p_callbacks.beforeDrag == 'function') {
					v_popUpObject.callbacks.beforeDrag = p_callbacks.beforeDrag;
				}

				if(p_callbacks.afterDrag != null && typeof p_callbacks.afterDrag == 'function') {
					v_popUpObject.callbacks.afterDrag = p_callbacks.afterDrag;
				}

				if(p_callbacks.beforeResize != null && typeof p_callbacks.beforeResize == 'function') {
					v_popUpObject.callbacks.beforeResize = p_callbacks.beforeResize;
				}

				if(p_callbacks.afterResize != null && typeof p_callbacks.afterResize == 'function') {
					v_popUpObject.callbacks.afterResize = p_callbacks.afterResize;
				}

				if(p_callbacks.closeCallbacks != null && typeof p_callbacks.closeCallbacks == 'object') {
					if(p_callbacks.closeCallbacks.yesFunction != null && typeof p_callbacks.closeCallbacks.yesFunction == 'function') {
						v_popUpObject.callbacks.closeCallbacks.yesFunction = p_callbacks.closeCallbacks.yesFunction;
					}

					if(p_callbacks.closeCallbacks.noFunction != null && typeof p_callbacks.closeCallbacks.noFunction == 'function') {
						v_popUpObject.callbacks.closeCallbacks.noFunction = p_callbacks.closeCallbacks.noFunction;
					}

					if(p_callbacks.closeCallbacks.cancelFunction != null && typeof p_callbacks.closeCallbacks.cancelFunction == 'function') {
						v_popUpObject.callbacks.closeCallbacks.cancelFunction = p_callbacks.closeCallbacks.cancelFunction;
					}
				}

				if(p_callbacks.beforeSelect != null && typeof p_callbacks.beforeSelect == 'function') {
					v_popUpObject.callbacks.beforeSelect = p_callbacks.beforeSelect;
				}

				if(p_callbacks.afterSelect != null && typeof p_callbacks.afterSelect == 'function') {
					v_popUpObject.callbacks.afterSelect = p_callbacks.afterSelect;
				}

				if(p_callbacks.beforeUnselect != null && typeof p_callbacks.beforeUnselect == 'function') {
					v_popUpObject.callbacks.beforeUnselect = p_callbacks.beforeUnselect;
				}

				if(p_callbacks.afterUnselect != null && typeof p_callbacks.afterUnselect == 'function') {
					v_popUpObject.callbacks.afterUnselect = p_callbacks.afterUnselect;
				}
			}

			//Create popup container
			var v_containerElement = document.createElement('aside');
			v_containerElement.id = 'popup_' + v_popUpObject.id;
			v_containerElement.style.zIndex = v_popUpObject.zIndex;
			v_containerElement.classList.add('popup-container');
			v_containerElement.style.width = v_popUpObject.config.width;
			v_containerElement.style.height = v_popUpObject.config.height;
			v_containerElement.style.top = v_popUpObject.config.top;
			v_containerElement.style.left = v_popUpObject.config.left;
			v_containerElement.draggable = v_popUpObject.config.draggable;

			//Turn it draggable, if this is the case
			if(v_containerElement.draggable) {
				v_containerElement.addEventListener(
					'dragstart',
					function(p_event) {
						var v_style = window.getComputedStyle(p_event.target, null);

						p_event.dataTransfer.setData(
					    	'text/plain',
					    	(parseInt(v_style.getPropertyValue('left'), 10) - p_event.clientX) + ',' + (parseInt(v_style.getPropertyValue('top'), 10) - p_event.clientY) + ',' + this.id
					    );

						if(this.classList.contains('minimized-popup-container')) {
							return false;
						}

						if(this.v_popUpObject.callbacks.beforeDrag != null) {
							this.v_popUpObject.callbacks.beforeDrag(this.v_popUpObject);
						}

						this.v_popUpObject.turnActive();
					}
				);
			}

			//Popup clicked goes to foreground
			v_containerElement.addEventListener(
				'mousedown',
				function(p_event) {
					p_event.stopPropagation();

					/*Removed in order to avoid bugs
					var v_activePopUp = this.v_popUpObject.parent.getActivePopUp();

					if(v_activePopUp != null && !v_activePopUp.selected && v_activePopUp.id.indexOf('close_') != 0) {
						this.v_popUpObject.parent.getActivePopUp().select();
					}*/

					if(this.v_popUpObject.parent.containerElement.isCtrlPressed && this.v_popUpObject.id.indexOf('close_') != 0 && this.v_popUpObject.closePopUp == null) {
						if(this.v_popUpObject.selected) {
							this.v_popUpObject.unselect();
						}
						else {
							this.v_popUpObject.select();
						}
					}
					else {
						this.v_popUpObject.parent.unselectAllSelected();
						this.v_popUpObject.turnActive();
					}
				}
			);

			//Popup clicked goes to foreground
			/*Removed in order to avoid bugs
			v_containerElement.addEventListener(
				'mouseup',
				function(p_event) {
					p_event.stopPropagation();

					var v_activePopUp = this.v_popUpObject.parent.getActivePopUp();

					if(this.v_popUpObject.closePopUp != null) {
						this.v_popUpObject.parent.unselectAllSelected();
						this.v_popUpObject.turnActive();
					}
				}
			);*/

			//Turn it resizable, it this is the case
			if(v_popUpObject.config.resizable) {
				v_containerElement.classList.add('resizable-popup-container');

				$(v_containerElement).resizable({
					start: function(p_event, p_ui) {
						if(p_event.target.v_popUpObject != null) {
							if(p_event.target.v_popUpObject.callbacks.beforeResize != null) {
								p_event.target.v_popUpObject.callbacks.beforeResize(p_event.target.v_popUpObject);
							}
						}
					},
					stop: function(p_event, p_ui) {
						if(p_event.target.v_popUpObject != null) {
							p_event.target.v_popUpObject.config.width = p_event.target.style.width;

							if(p_event.target.offsetWidth < 175) {
								p_event.target.v_popUpObject.changeSize('175px', null);
							}

							p_event.target.v_popUpObject.config.height = p_event.target.style.height;

							if(p_event.target.offsetHeight < 50) {
								p_event.target.v_popUpObject.changeSize(null, '50px');
							}

							if(p_event.target.v_popUpObject.callbacks.afterResize != null) {
								p_event.target.v_popUpObject.callbacks.afterResize(p_event.target.v_popUpObject);
							}
						}
					}
				});
			}

			v_containerElement.addEventListener(
				'mouseover',
				function(p_event) {
					if(this.v_popUpObject.config.draggable) {
						var v_current = p_event.target;
						var v_preventDrag;

						while(v_current != this && !v_preventDrag) {
							if(v_current.classList.contains('popup-prevent-container-drag')) {
								v_preventDrag = true;
							}

							v_current = v_current.parentElement;
						}

						if(v_preventDrag) {
							this.removeAttribute('draggable');
						}
						else {
							this.draggable = true;
						}
					}
				}
			);

			v_containerElement.addEventListener(
				'mouseout',
				function(p_event) {
					if(this.v_popUpObject.config.draggable) {
						this.draggable = true;
					}
				}
			);

			v_containerElement.v_popUpObject = v_popUpObject;

			v_popUpObject.containerElement = v_containerElement;
			v_popUpControlObject.containerElement.appendChild(v_containerElement);

			//Create header bar
			var v_headerElement = document.createElement('div');
			v_headerElement.classList.add('popup-header');

			v_headerElement.addEventListener(
				'dblclick',
				function(p_event) {
					p_event.stopPropagation();

					var v_popUpObject = this.parentElement.v_popUpObject;

					if(v_popUpObject != null) {
						if(v_popUpObject.closePopUp != null || (v_popUpObject.closePopUp == null && v_popUpObject.id.indexOf('close_') == 0)) {
							return;
						}

						if(v_popUpObject.minimized) {
							v_popUpObject.maximize();
						}

						v_popUpObject.turnActive();
						v_popUpObject.changePosition(v_popUpObject.config.defaultTop, v_popUpObject.config.defaultLeft);
						v_popUpObject.changeSize(v_popUpObject.config.defaultWidth, v_popUpObject.config.defaultHeight);
					}
				}
			);

			v_containerElement.appendChild(v_headerElement);
			v_popUpObject.headerElement = v_headerElement;

			//Create title div
			var v_titleElement = document.createElement('div');
			v_titleElement.classList.add('popup-header-title');
			v_titleElement.innerHTML = v_popUpObject.title;
			v_titleElement.title = v_popUpObject.title;

			v_headerElement.appendChild(v_titleElement);
			v_popUpObject.titleElement = v_titleElement;

			//Create button group div
			var v_headerButtonGroupElement = document.createElement('div');
			v_headerButtonGroupElement.classList.add('popup-header-button-group');
			v_headerElement.appendChild(v_headerButtonGroupElement);

			//Create close button
			var v_closeElement = document.createElement('button');
			v_closeElement.classList.add('popup-header-button');
			v_closeElement.innerHTML = 'X';

			v_closeElement.addEventListener(
				'mousedown',
				function(p_event) {
					p_event.stopPropagation();

					if(this.parentElement.parentElement.parentElement.v_popUpObject != null) {
						this.parentElement.parentElement.parentElement.v_popUpObject.close(this.parentElement.parentElement.parentElement.v_popUpObject.config.forceClose);
					}
				}
			);

			v_headerButtonGroupElement.appendChild(v_closeElement);
			v_popUpObject.closeElement = v_closeElement;

			//Create maximize button
			var v_maximizeElement = document.createElement('button');
			v_maximizeElement.classList.add('popup-header-button');
			v_maximizeElement.classList.add('hidden-button');
			v_maximizeElement.innerHTML = '[]';

			v_maximizeElement.addEventListener(
				'mousedown',
				function(p_event) {
					p_event.stopPropagation();

					if(this.parentElement.parentElement.parentElement.v_popUpObject != null) {
						this.parentElement.parentElement.parentElement.v_popUpObject.maximize();
					}
				}
			);

			v_headerButtonGroupElement.appendChild(v_maximizeElement);
			v_popUpObject.maximizeElement = v_maximizeElement;

			//Create minimize button
			var v_minimizeElement = document.createElement('button');
			v_minimizeElement.classList.add('popup-header-button');
			v_minimizeElement.innerHTML = '_';

			v_minimizeElement.addEventListener(
				'mousedown',
				function(p_event) {
					p_event.stopPropagation();

					if(this.parentElement.parentElement.parentElement.v_popUpObject != null) {
						this.parentElement.parentElement.parentElement.v_popUpObject.minimize();
					}
				}
			);

			v_headerButtonGroupElement.appendChild(v_minimizeElement);
			v_popUpObject.minimizeElement = v_minimizeElement;

			//Create content (details) div
			var v_contentElement = document.createElement('div');
			v_contentElement.classList.add('popup-content');
			v_contentElement.innerHTML = v_popUpObject.innerHtml;

			v_popUpObject.contentElement = v_contentElement;
			v_containerElement.appendChild(v_contentElement);

			v_parent.popUpList.push(v_popUpObject);

			//Turns this popup the active one (foreground)
			v_popUpObject.turnActive();

			return v_popUpObject;
		},
		/// <summary>
		/// Removes all selected popups.
		/// </summary>
		closeAllSelected: function() {
			if(this.closePopUp != null) {
				this.closePopUp.turnActive();
				return;
			}

			var v_html =
				'<div>' +
				'    Do you want to close all selected popups?' +
				'</div>' +
				'<br />' +
				'<div style="text-align: center;">' +
				'    <button id="button_close_all_' + this.id + '_yes">Yes</button>' +
				'    <button id="button_close_all_' + this.id + '_no">No</button>' +
				'</div>';

			var v_config = {
				width: '265px',
				height: '125px',
				resizable: false,
				draggable: false,
				top: '40%',
				left: '40%',
				forceClose: true
			};

			var v_callbacks = null;

			var v_closePopUp = this.addPopUp(
				'close_all_' + this.id,
				'Attention!',
				v_html,
				v_config,
				v_callbacks
			);

			this.closePopUp = v_closePopUp;

			v_closePopUp.closeElement.classList.add('hidden-button');
			v_closePopUp.minimizeElement.classList.add('hidden-button');

			var v_closeYes = document.getElementById('button_close_all_' + this.id + '_yes');

			v_closeYes.addEventListener(
				'mousedown',
				function(p_event) {
					p_event.stopPropagation();//In order to avoid bugs while closing popup

					var v_popUpControl = this.parentElement.parentElement.parentElement.v_popUpObject.parent;

					if(v_popUpControl != null) {
						var v_selectedPopUps = v_popUpControl.getSelectedPopUps();

						for(var i = 0; i < v_selectedPopUps.length; i++) {
							v_selectedPopUps[i].close(true);
						}

						this.parentElement.parentElement.parentElement.v_popUpObject.close(true);//Close this popup
						v_popUpControl.closePopUp = null;
					}
				}
			);

			v_closeYes.focus();

			var v_closeNo = document.getElementById('button_close_all_' + this.id + '_no');

			v_closeNo.addEventListener(
				'mousedown',
				function(p_event) {
					p_event.stopPropagation();//In order to avoid bugs while closing popup

					var v_popUpControl = this.parentElement.parentElement.parentElement.v_popUpObject.parent;

					if(v_popUpControl != null) {
						this.parentElement.parentElement.parentElement.v_popUpObject.close(true);//Close this popup
						v_popUpControl.closePopUp = null;
					}
				}
			);
		},
		/// <summary>
		/// Count how many popups are selected under this controller.
		/// </summary>
		/// <returns>An integer representing how many are selected.</returns>
		countSelected: function() {
			return this.getSelectedPopUps().length;
		},
		/// <summary>
		/// Get the active popup under this controller.
		/// </summary>
		/// <returns>An javascript object representing the popup or null.</returns>
		getActivePopUp: function() {
			for(var i = 0; i < this.popUpList.length; i++) {
				if(this.popUpList[i].activePopUp) {
					return this.popUpList[i];
				}
			}

			return null;
		},
		/// <summary>
		/// Get the popup corresponding to given id, if it exists.
		/// </summary>
		/// <param name="p_id">The id to be searched.</param>
		/// <paramref name="p_id">Takes a String.
		/// <returns>An javascript object representing the popup or null.</returns>
		getPopUpById: function(p_id) {
			for(var i = 0; i < this.popUpList.length; i++) {
				if(this.popUpList[i].id == p_id) {
					return this.popUpList[i];
				}
			}

			return null;
		},
		/// <summary>
		/// Get all selected popups under this controller.
		/// </summary>
		/// <returns>An array containing all selected popups.</returns>
		getSelectedPopUps: function() {
			var v_selectedPopUps = [];

			for(var i = 0; i < this.popUpList.length; i++) {
				if(this.popUpList[i].selected) {
					v_selectedPopUps.push(this.popUpList[i]);
				}
			}

			return v_selectedPopUps;
		},
		/// <summary>
		/// Get all selected popups under this controller.
		/// </summary>
		/// <returns>An array containing all selected popups.</returns>
		getSelectedPopUps: function() {
			var v_selectedPopUps = [];

			for(var i = 0; i < this.popUpList.length; i++) {
				if(this.popUpList[i].selected) {
					v_selectedPopUps.push(this.popUpList[i]);
				}
			}

			return v_selectedPopUps;
		},
		/// <summary>
		/// Hides everything in this popup controller.
		/// </summary>
		hideAll: function() {
			if(!this.minimizedPopUpsContainerElement.classList.contains('hidden-minimized-popups-container')) {
				this.minimizedPopUpsContainerElement.classList.add('hidden-minimized-popups-container');
			}

			for(var i = 0; i < this.popUpList.length; i++) {
				this.popUpList[i].hide();
			}
		},
		/// <summary>
		/// Maximizes all selected popups.
		/// </summary>
		maximizeAllSelected: function() {
			this.maximizing = true;

			var v_top = 0;
			var v_left = 0;

			var v_width = (window.innerWidth * 0.6) + 'px';
			var v_height = (window.innerHeight * 0.6) + 'px';

			var v_selectedPopUps = this.getSelectedPopUps();

			for(var i = 0; i < v_selectedPopUps.length; i++) {
				v_selectedPopUps[i].maximize();

				if(i < 6) {
					v_top += 5;
					v_left += 5;
				}

				v_selectedPopUps[i].changePosition(v_top + '%', v_left + '%');
				v_selectedPopUps[i].changeSize(v_width, v_height);
			}

			v_selectedPopUps[v_selectedPopUps.length - 1].turnActive();

			this.maximizing = false;
		},
		/// <summary>
		/// Minimizes all selected popups.
		/// </summary>
		minimizeAllSelected: function() {
			this.minimizing = true;

			var v_selectedPopUps = this.getSelectedPopUps();

			for(var i = 0; i < v_selectedPopUps.length; i++) {
				v_selectedPopUps[i].minimize();
			}

			this.minimizing = false;
		},
		/// <summary>
		/// Order popups of this controller by z-index.
		/// </summary>
		orderPopUpsByZIndex: function() {
			this.popUpList.sort(function(a, b) {
				return (a.zIndex > b.zIndex) ? 1 : ((b.zIndex > a.zIndex) ? -1 : 0);
			});
		},
		/// <summary>
		/// Removes everything in this popup controller.
		/// </summary>
		destroy: function() {
			var v_this = this;

			//Removes all popus
			while(this.popUpList.length > 0) {
				this.popUpList[0].close(true);
			}

			this.minimizedPopUpsContainerElement.remove();

			for(v_key in v_this) {
				v_this[v_key] = null;
			}
		},
		/// <summary>
		/// Shows everything in this popup controller.
		/// </summary>
		showAll: function() {
			if(this.minimizedPopUpsContainerElement.classList.contains('hidden-minimized-popups-container')) {
				this.minimizedPopUpsContainerElement.classList.remove('hidden-minimized-popups-container');
			}

			for(var i = 0; i < this.popUpList.length; i++) {
				this.popUpList[i].show();
			}
		},
		/// <summary>
		/// Unselects all selected popups.
		/// </summary>
		unselectAllSelected: function() {
			var v_selectedPopUps = this.getSelectedPopUps();

			for(var i = 0; i < v_selectedPopUps.length; i++) {
				v_selectedPopUps[i].unselect();
			}
		},
	};

	window.addEventListener(
		'resize',
		function(p_popUpControlObject, p_event) {
			if(p_popUpControlObject.popUpList == null) {//If popup control was destroyed
				return;
			}

			for(var i = 0; i < p_popUpControlObject.popUpList.length; i++) {
				//Doesn't allow hide on right
				if(window.innerWidth - p_popUpControlObject.popUpList[i].containerElement.offsetLeft < 55) {
					p_popUpControlObject.popUpList[i].changePosition(null, (window.innerWidth - 55) + 'px');
				}

				//Doesn't allow hide on bottom
				if(window.innerHeight - p_popUpControlObject.popUpList[i].containerElement.offsetTop < 110) {
					p_popUpControlObject.popUpList[i].changePosition((window.innerHeight - 110) + 'px', null);
				}
			}
		}.bind(window, v_popUpControlObject),
		false
	);

	v_popUpControlObject.containerElement.removeEventListener(
		'dragover',
		gv_popUpdragOverFunction,
		false
	);

	v_popUpControlObject.containerElement.addEventListener(
		'dragover',
		gv_popUpdragOverFunction,
		false
	);

	v_popUpControlObject.containerElement.removeEventListener(
		'drop',
		gv_popUpDropFunction,
		false
	);

	v_popUpControlObject.containerElement.addEventListener(
		'drop',
		gv_popUpDropFunction,
		false
	);

	v_popUpControlObject.containerElement.removeEventListener(
		'keydown',
		gv_popUpKeyDownFunction,
		false
	);

	v_popUpControlObject.containerElement.addEventListener(
		'keydown',
		gv_popUpKeyDownFunction,
		false
	);

	v_popUpControlObject.containerElement.removeEventListener(
		'keyup',
		gv_popUpKeyUpFunction,
		false
	);

	v_popUpControlObject.containerElement.addEventListener(
		'keyup',
		gv_popUpKeyUpFunction,
		false
	);

	v_popUpControlObject.containerElement.removeEventListener(
		'mousedown',
		gv_popUpClickFunction,
		false
	);

	v_popUpControlObject.containerElement.addEventListener(
		'mousedown',
		gv_popUpClickFunction,
		false
	);

	//Creates the div where minimized popups will be placed
	var v_minimizedPopUpsContainerElement = document.createElement('div');
	v_minimizedPopUpsContainerElement.id = v_popUpControlObject.id + '_minimized_popups_container';
	v_minimizedPopUpsContainerElement.style.zIndex = p_startZIndex - 1;
	v_minimizedPopUpsContainerElement.classList.add('minimized-popups-container');

	v_popUpControlObject.containerElement.appendChild(v_minimizedPopUpsContainerElement);
	v_popUpControlObject.minimizedPopUpsContainerElement = v_minimizedPopUpsContainerElement;

	v_popUpControlObject.v_popUpControlObject = v_popUpControlObject;

	return v_popUpControlObject;
}
