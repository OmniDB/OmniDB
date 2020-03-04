/*
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

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

  	//td.style.background = 'rgb(234, 237, 249)';

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

    //td.style.background ='rgb(102, 183, 45)';
  	//td.style.color = '#000';

  	//td.style.background = 'rgb(206, 255, 209)';

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

  	//td.style.background = 'rgb(255, 251, 215)';

  	//td.style.background ='rgb(224, 184, 57)';
  	//td.style.color = '#000';

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

  	//td.style.background = 'rgb(255, 255, 255)';
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

  	//td.style.background = 'rgb(255, 255, 255)';
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

  	//td.style.background = 'rgb(255, 213, 213)';
  	//td.style.background = 'rgb(183, 46, 46)';
  	//td.style.color = '#000';

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

  	//td.style.background = 'rgb(242, 242, 242)';

  	td.className ='cellReadOnly';
}


function yellowRenderer(instance, td, row, col, prop, value, cellProperties) {
	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
	  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
	  }
	  else {
	  	Handsontable.renderers.TextRenderer.apply(this, arguments);
	  }

  	//td.style.background = 'rgb(255, 251, 215)';
  	//td.style.background ='rgb(224, 184, 57)';
  	//td.style.color = '#000';

  	td.className ='cellEdit';
}

function blueRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
	  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
	  }
	  else {
	  	Handsontable.renderers.TextRenderer.apply(this, arguments);
	  }

  	//td.style.background = 'rgb(234, 237, 249)';

  	td.className ='cellEven';
}

function whiteRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
	  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
	  }
	  else {
	  	Handsontable.renderers.TextRenderer.apply(this, arguments);
	  }

  	//td.style.background = 'rgb(255, 255, 255)';
  	td.className ='cellOdd';
}

function redRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
	  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
	  }
	  else {
	  	Handsontable.renderers.TextRenderer.apply(this, arguments);
	  }

  	//td.style.background = 'rgb(255, 213, 213)';
  	//td.style.background = 'rgb(183, 46, 46)';
  	//td.style.color = '#000';

  	td.className ='cellRemove';
}

function grayRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
	  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
	  }
	  else {
	  	Handsontable.renderers.TextRenderer.apply(this, arguments);
	  }

  	//td.style.background = 'rgb(242, 242, 242)';

  	td.className ='cellReadOnly';
}

function greenRenderer(instance, td, row, col, prop, value, cellProperties) {

	if (cellProperties.__proto__.type=="dropdown" || cellProperties.__proto__.type=="autocomplete") {
	  	Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
	  }
	  else {
	  	Handsontable.renderers.TextRenderer.apply(this, arguments);
	  }

  	//td.style.background = 'rgb(206, 255, 209)';

  	//td.style.background ='rgb(102, 183, 45)';
  	//td.style.color = '#000';

  	td.className ='cellNew';

}

function grayEmptyRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = '';

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

  	//td.style.background = 'rgb(242, 242, 242)';

  	td.className ='cellReadOnly';
}

function newRowRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = '+';
	td.style.textAlign = 'center';

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

  	//td.style.background = 'rgb(242, 242, 242)';

  	td.className ='cellReadOnly';
}

function columnsActionRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = "<i title='Remove' class='fas fa-times action-grid action-close' onclick='dropColumnAlterTable()'></i>";

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

  	//td.style.background = 'rgb(242, 242, 242)';

  	td.className ='cellReadOnly';
}

function editDataActionRenderer(instance, td, row, col, prop, value, cellProperties) {

	arguments[5] = "<i title='Remove' class='fas fa-times action-grid action-close' onclick='deleteRowEditData()'></i>";

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);

  	//td.style.background = 'rgb(242, 242, 242)';

  	td.className ='cellReadOnly';

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
