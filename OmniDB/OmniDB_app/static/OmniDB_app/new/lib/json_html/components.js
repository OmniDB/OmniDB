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
