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

function blueHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.className ='cellEven';
}

function greenHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.className ='cellNew';
}

function yellowHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.className ='cellEdit';
}



function whiteHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.className ='cellOdd';
}

function whiteRightHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.style.textAlign ='right';
}

function redHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.className ='cellRemove';
}

function grayHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="password") {
  	Handsontable.renderers.PasswordRenderer.apply(this, arguments);
  }
  else if (cellProperties.__proto__.type=="checkbox") {
	  Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
  }
  else {
	  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }

	td.className ='cellReadOnly';
}


function yellowRenderer(instance, td, row, col, prop, value, cellProperties) {
	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

	td.className ='cellEdit';
}

function blueRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

	td.className ='cellEven';
}

function whiteRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

	td.className ='cellOdd';
}

function redRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

	td.className ='cellRemove';
}

function grayRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

	td.className ='cellReadOnly';
}

function greenRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

	td.className ='cellNew';

}

function grayEmptyRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = '';

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

	td.className ='cellReadOnly';
}

function newRowRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = '+';
	td.style.textAlign = 'center';

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

	td.className ='cellReadOnly';
}

function columnsActionRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = "<i title='Remove' class='fas fa-times action-grid action-close text-danger' onclick='dropColumnAlterTable()'></i>";

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

	td.className ='cellReadOnly';
}

function editDataActionRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = "<div class='text-center'><i title='Remove' class='fas fa-times action-grid action-close text-danger' onclick='deleteRowEditData()'></i></div>";

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

	td.className ='cellReadOnly';

}

function showPluginDataActionRenderer(instance, td, row, col, prop, value, cellProperties) {
	if (arguments[5].includes('fa-check-circle')) {
		arguments[5] = arguments[5].replace('fa-check-circle', ' fa-check-circle omnidb__theme__text--primary ');
	}
	else if (arguments[5].includes('fa-exclamation-triangle')) {
		arguments[5] = arguments[5].replace('fa-exclamation-triangle', ' fa-exclamation-triangle text-warning ');
	}
	else if (arguments[5].includes('fa-times')) {
		arguments[5] = arguments[5].replace('fa-times', ' fa-times text-danger ');
	}
	var v_actions_html = '<div class="text-center">' + arguments[5] + '</div>';
	arguments[5] = v_actions_html;
	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

	// td.className ='cellReadOnly';

}

function monitorStatusRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
  }
  else {
  	Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  }
	if (value == 'unknown')
		td.setAttribute('style', 'background-color: rgb(165, 84, 175) !important');
	else if (value == 'ok' || value == 'recovery')
		td.setAttribute('style', 'background-color: rgb(74, 183, 65) !important');
	else if (value == 'warning')
		td.setAttribute('style', 'background-color: rgb(255, 161, 45) !important');
	else if (value == 'critical')
		td.setAttribute('style', 'background-color: rgb(232, 79, 79) !important');

	td.style.color = 'white';
	td.style['text-align'] = 'center';
}
