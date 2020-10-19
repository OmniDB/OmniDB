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

function BsJsonComponent( config ) {

  this.target = config.target;
  this.data = config.data;
  this.template = 'jsonBuilder--' + config.template;

  this.getItems = ( items ) => {

    let item,
    itemsArray = new Array;

    for (var key in items) {
      item = {
        name: key,
        type: typeof items[key],
        value: items[key]
      }
      if ( item.type === 'array' || item.type === 'object' ) {
        item.children = this.getItems( item.value );
      }
      itemsArray.push(item);
    }

    return itemsArray;

  }

  this.items = this.getItems( this.data );

  this.render = () => {

    let el = this.renderList( this.items ),
        elWrapper = document.createElement('DIV');

    elWrapper.classList = [ this.template ];

    elWrapper.append(el);

    this.target.append( elWrapper );

  }

  this.renderLabel = ( item ) => {

    let label = document.createElement('LABEL');
    labelText = document.createElement('SPAN');
    labelText.append( item.name );

    labelText.classList = ['jsonBuilder__label-value'];

    label.append( labelText );

    label.classList = ['jsonBuilder__label d-flex align-items-center mb-1'];

    return label;

  }

  this.renderList = ( children ) => {

    let list = document.createElement('UL');

    for (let i = 0; i < children.length; i++) {

      let item = children[i],
          listItem = document.createElement('LI'),
          label = this.renderLabel( item );

      listItem.classList = ['jsonBuilder__li'];
      listItem.append( label );

      if (item.type === 'string' || item.type === 'number' || item.type === 'boolean') {

        let content = document.createElement('SPAN');

        content.classList = ['jsonBuilder__li-value'];
        content.append( item.value );

        listItem.append( content );

      }
      else if ( item.type === 'array' || item.type === 'object' ) {

        listItem.append( this.renderList( item.children ) )

      }

      list.classList = ['jsonBuilder__ul'];

      list.append( listItem );
    }

    return list;

  }

  this.update = () => {
    this.target.innerHTML = null;
    this.render();
  }

}
