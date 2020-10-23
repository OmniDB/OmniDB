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

function checkSessionMessage() {

	execAjax('/check_session_message/',
				JSON.stringify({}),
        function(p_return) {
          if (p_return.v_data!='')
          	showAlert(p_return.v_data);
        },
        null,
    'box');

}

/// <summary>
/// Startup function.
/// </summary>
$(function () {
  v_message_modal_animating = false;
  v_message_modal_queued = false;
	v_message_modal_queued_function = null;
  v_shown_callback = null;
  $('#modal_message').on('hide.bs.modal', function (e) {
    v_message_modal_animating = true;
  });
  $('#modal_message').on('show.bs.modal', function (e) {
    v_message_modal_animating = true;
  });
  $('#modal_message').on('hidden.bs.modal', function (e) {
		document.getElementById('modal_message_content').innerHTML = '';
    v_message_modal_animating = false;
    if (v_message_modal_queued == true) {
			if (v_message_modal_queued_function!=null)
				v_message_modal_queued_function();
      $('#modal_message').modal();
		}
    v_message_modal_queued = false;
		v_message_modal_queued_function = null;
  });
  $('#modal_message').on('shown.bs.modal', function (e) {
    v_message_modal_animating = false;
    if (v_shown_callback) {
      v_shown_callback();
      v_shown_callback = null;
    }
  });
});

function showMessageModal(p_content_function, p_large) {

	var v_dialog = document.getElementById('modal_message_dialog');

	if (p_large==null || p_large==false) {
		v_dialog.classList.remove('modal-xl');
	}
	else {
		v_dialog.classList.add('modal-xl');
	}

  if (!v_message_modal_animating) {
		if (p_content_function!=null)
			p_content_function();
    $('#modal_message').modal();
	}
  else {
    v_message_modal_queued = true;
		v_message_modal_queued_function = p_content_function;
	}

}

function showError(p_message) {
  var v_content_div = document.getElementById('modal_message_content');
  var v_button_yes = document.getElementById('modal_message_yes');
  var v_button_ok = document.getElementById('modal_message_ok');
  var v_button_no = document.getElementById('modal_message_no');
  var v_button_cancel = document.getElementById('modal_message_cancel');

  v_content_div.innerHTML = p_message;

  v_button_yes.style.display = 'none';
  v_button_ok.style.display = '';
  v_button_no.style.display = 'none';
  v_button_cancel.style.display = 'none';

  showMessageModal();

  setTimeout(function() {
    v_button_yes.focus();
  },500);

}


function showAlert(p_info, p_funcYes = null, p_large = null)
{

	var v_create_content_function = function() {
	  var v_content_div = document.getElementById('modal_message_content');
	  var v_button_yes = document.getElementById('modal_message_yes');
	  var v_button_ok = document.getElementById('modal_message_ok');
	  var v_button_no = document.getElementById('modal_message_no');
	  var v_button_cancel = document.getElementById('modal_message_cancel');

	  v_content_div.innerHTML = p_info;

		v_button_ok.onclick = function() {
	    if (p_funcYes!=null)
			  p_funcYes();
		};

	  v_button_yes.style.display = 'none';
	  v_button_ok.style.display = '';
	  v_button_no.style.display = 'none';
	  v_button_cancel.style.display = 'none';

	}


	showMessageModal(v_create_content_function, p_large);


}


function showConfirm(p_info,p_funcYes = null,p_funcNo = null, p_shownCallback = null, p_large = null)
{
	var v_create_content_function = function() {
	  if (p_shownCallback != null)
	    v_shown_callback = p_shownCallback;

	  var v_content_div = document.getElementById('modal_message_content');
	  var v_button_yes = document.getElementById('modal_message_yes');
	  var v_button_ok = document.getElementById('modal_message_ok');
	  var v_button_no = document.getElementById('modal_message_no');
	  var v_button_cancel = document.getElementById('modal_message_cancel');

	  v_content_div.innerHTML = p_info;

		v_button_ok.onclick = function() {
			p_funcYes();
		};

		v_button_cancel.onclick = function() {
			if (p_funcNo)
				p_funcNo();
		};

	  v_button_yes.style.display = 'none';
	  v_button_no.style.display = 'none';
	  v_button_ok.style.display = '';
	  v_button_cancel.style.display = '';
	}

	showMessageModal(v_create_content_function, p_large);

}

function showConfirm2(p_info,p_funcYes,p_funcNo)
{
  var v_content_div = document.getElementById('modal_message_content');
  var v_button_yes = document.getElementById('modal_message_yes');
  var v_button_ok = document.getElementById('modal_message_ok');
  var v_button_no = document.getElementById('modal_message_no');
  var v_button_cancel = document.getElementById('modal_message_cancel');

  v_content_div.innerHTML = p_info;

  v_button_yes.onclick = function() {
		p_funcYes();
	};

  v_button_no.onclick = function() {
    if (p_funcNo != null) {
  		p_funcNo();
    }
	};

	v_button_cancel.onclick = function() {
	};

  v_button_yes.style.display = '';
  v_button_no.style.display = '';
  v_button_ok.style.display = 'none';
  v_button_cancel.style.display = '';


	showMessageModal();

}

function showConfirm3(p_info,p_funcYes,p_funcNo)
{

  var v_content_div = document.getElementById('modal_message_content');
  var v_button_yes = document.getElementById('modal_message_yes');
  var v_button_ok = document.getElementById('modal_message_ok');
  var v_button_no = document.getElementById('modal_message_no');
  var v_button_cancel = document.getElementById('modal_message_cancel');

  v_content_div.innerHTML = p_info;

  v_button_yes.onclick = function() {
		p_funcYes();
	};

  v_button_no.onclick = function() {
    if (p_funcNo != null) {
  		p_funcNo();
    }
	};

  v_button_yes.style.display = '';
  v_button_no.style.display = '';
  v_button_ok.style.display = 'none';
  v_button_cancel.style.display = 'none';


	showMessageModal();

}
