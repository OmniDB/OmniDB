'use strict';

// registers the extension on a cytoscape lib ref
var getLayout = require('./layout');

var register = function( cytoscape ){
  var layout = getLayout( cytoscape );

  cytoscape('layout', 'spread', layout);
};

if( typeof cytoscape !== 'undefined' ){ // expose to global cytoscape (i.e. window.cytoscape)
  register( cytoscape );
}

module.exports = register;
