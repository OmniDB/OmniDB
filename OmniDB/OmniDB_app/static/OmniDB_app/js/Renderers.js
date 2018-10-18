/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
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
		if (value == 'UNKNOWN')
  		td.style.background = 'rgb(249, 195, 255)';
		else if (value == 'OK')
			td.style.background = 'rgb(200, 255, 195)';
		else if (value == 'WARNING')
			td.style.background = 'rgb(255, 252, 195)';
		else if (value == 'CRITICAL')
			td.style.background = 'rgb(255, 195, 195)';
		else
			td.style.background = 'rgb(242, 242, 242)';

}
