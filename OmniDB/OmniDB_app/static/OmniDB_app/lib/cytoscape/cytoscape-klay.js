(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("klayjs"));
	else if(typeof define === 'function' && define.amd)
		define(["klayjs"], factory);
	else if(typeof exports === 'object')
		exports["cytoscapeKlay"] = factory(require("klayjs"));
	else
		root["cytoscapeKlay"] = factory(root["$klay"]);
})(this, function(__WEBPACK_EXTERNAL_MODULE_4__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var klay = __webpack_require__(4);
var assign = __webpack_require__(1);
var defaults = __webpack_require__(2);

var klayNSLookup = {
  'addUnnecessaryBendpoints': 'de.cau.cs.kieler.klay.layered.unnecessaryBendpoints',
  'alignment': 'de.cau.cs.kieler.alignment',
  'aspectRatio': 'de.cau.cs.kieler.aspectRatio',
  'borderSpacing': 'borderSpacing',
  'compactComponents': 'de.cau.cs.kieler.klay.layered.components.compact',
  'compactionStrategy': 'de.cau.cs.kieler.klay.layered.nodeplace.compactionStrategy',
  'contentAlignment': 'de.cau.cs.kieler.klay.layered.contentAlignment',
  'crossingMinimization': 'de.cau.cs.kieler.klay.layered.crossMin',
  'cycleBreaking': 'de.cau.cs.kieler.klay.layered.cycleBreaking',
  'debugMode': 'de.cau.cs.kieler.debugMode',
  'direction': 'de.cau.cs.kieler.direction',
  'edgeLabelSideSelection': 'de.cau.cs.kieler.klay.layered.edgeLabelSideSelection',
  // <broken> 'de.cau.cs.kieler.klay.layered.edgeNodeSpacingFactor': options.edgeNodeSpacingFactor,
  'edgeRouting': 'de.cau.cs.kieler.edgeRouting',
  'edgeSpacingFactor': 'de.cau.cs.kieler.klay.layered.edgeSpacingFactor',
  'feedbackEdges': 'de.cau.cs.kieler.klay.layered.feedBackEdges',
  'fixedAlignment': 'de.cau.cs.kieler.klay.layered.fixedAlignment',
  'greedySwitchCrossingMinimization': 'de.cau.cs.kieler.klay.layered.greedySwitch',
  'hierarchyHandling': 'de.cau.cs.kieler.hierarchyHandling',
  'inLayerSpacingFactor': 'de.cau.cs.kieler.klay.layered.inLayerSpacingFactor',
  'interactiveReferencePoint': 'de.cau.cs.kieler.klay.layered.interactiveReferencePoint',
  'layerConstraint': 'de.cau.cs.kieler.klay.layered.layerConstraint',
  'layoutHierarchy': 'de.cau.cs.kieler.layoutHierarchy',
  'linearSegmentsDeflectionDampening': 'de.cau.cs.kieler.klay.layered.linearSegmentsDeflectionDampening',
  'mergeEdges': 'de.cau.cs.kieler.klay.layered.mergeEdges',
  'mergeHierarchyCrossingEdges': 'de.cau.cs.kieler.klay.layered.mergeHierarchyEdges',
  'noLayout': 'de.cau.cs.kieler.noLayout',
  'nodeLabelPlacement': 'de.cau.cs.kieler.nodeLabelPlacement',
  'nodeLayering': 'de.cau.cs.kieler.klay.layered.nodeLayering',
  'nodePlacement': 'de.cau.cs.kieler.klay.layered.nodePlace',
  'portAlignment': 'de.cau.cs.kieler.portAlignment',
  'portAlignmentEastern': 'de.cau.cs.kieler.portAlignment.east',
  'portAlignmentNorth': 'de.cau.cs.kieler.portAlignment.north',
  'portAlignmentSouth': 'de.cau.cs.kieler.portAlignment.south',
  'portAlignmentWest': 'de.cau.cs.kieler.portAlignment.west',
  'portConstraints': 'de.cau.cs.kieler.portConstraints',
  'portLabelPlacement': 'de.cau.cs.kieler.portLabelPlacement',
  'portOffset': 'de.cau.cs.kieler.offset',
  'portSide': 'de.cau.cs.kieler.portSide',
  'portSpacing': 'de.cau.cs.kieler.portSpacing',
  'postCompaction': 'de.cau.cs.kieler.klay.layered.postCompaction',
  'priority': 'de.cau.cs.kieler.priority',
  'randomizationSeed': 'de.cau.cs.kieler.randomSeed',
  'routeSelfLoopInside': 'de.cau.cs.kieler.selfLoopInside',
  'separateConnectedComponents': 'de.cau.cs.kieler.separateConnComp',
  'sizeConstraint': 'de.cau.cs.kieler.sizeConstraint',
  'sizeOptions': 'de.cau.cs.kieler.sizeOptions',
  'spacing': 'de.cau.cs.kieler.spacing',
  'splineSelfLoopPlacement': 'de.cau.cs.kieler.klay.layered.splines.selfLoopPlacement',
  'thoroughness': 'de.cau.cs.kieler.klay.layered.thoroughness',
  'wideNodesOnMultipleLayers': 'de.cau.cs.kieler.klay.layered.wideNodesOnMultipleLayers'
};

var mapToKlayNS = function mapToKlayNS(klayOpts) {
  var keys = Object.keys(klayOpts);
  var ret = {};

  for (var i = 0; i < keys.length; i++) {
    var key = keys[i];
    var nsKey = klayNSLookup[key];
    var val = klayOpts[key];

    ret[nsKey] = val;
  }

  return ret;
};

var klayOverrides = {
  interactiveReferencePoint: 'CENTER' // Determines which point of a node is considered by interactive layout phases.
};

var getPos = function getPos(ele) {
  var parent = ele.parent();
  var k = ele.scratch('klay');
  var p = {
    x: k.x,
    y: k.y
  };

  if (parent.nonempty()) {
    var kp = parent.scratch('klay');

    p.x += kp.x;
    p.y += kp.y;
  }

  return p;
};

var makeNode = function makeNode(node, options) {
  var dims = node.layoutDimensions(options);
  var padding = node.numericStyle('padding');

  var k = {
    _cyEle: node,
    id: node.id(),
    padding: {
      top: padding,
      left: padding,
      bottom: padding,
      right: padding
    }
  };

  if (!node.isParent()) {
    k.width = dims.w;
    k.height = dims.h;
  }

  node.scratch('klay', k);

  return k;
};

var makeEdge = function makeEdge(edge, options) {
  var k = {
    _cyEle: edge,
    id: edge.id(),
    source: edge.data('source'),
    target: edge.data('target'),
    properties: {}
  };

  var priority = options.priority(edge);

  if (priority != null) {
    k.properties.priority = priority;
  }

  edge.scratch('klay', k);

  return k;
};

var makeGraph = function makeGraph(nodes, edges, options) {
  var klayNodes = [];
  var klayEdges = [];
  var klayEleLookup = {};
  var graph = {
    id: 'root',
    children: [],
    edges: []
  };

  // map all nodes
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    var k = makeNode(n, options);

    klayNodes.push(k);

    klayEleLookup[n.id()] = k;
  }

  // map all edges
  for (var _i = 0; _i < edges.length; _i++) {
    var e = edges[_i];
    var _k = makeEdge(e, options);

    klayEdges.push(_k);

    klayEleLookup[e.id()] = _k;
  }

  // make hierarchy
  for (var _i2 = 0; _i2 < klayNodes.length; _i2++) {
    var _k2 = klayNodes[_i2];
    var _n = _k2._cyEle;

    if (!_n.isChild()) {
      graph.children.push(_k2);
    } else {
      var parent = _n.parent();
      var parentK = klayEleLookup[parent.id()];

      var children = parentK.children = parentK.children || [];

      children.push(_k2);
    }
  }

  for (var _i3 = 0; _i3 < klayEdges.length; _i3++) {
    var _k3 = klayEdges[_i3];
    var _e = _k3._cyEle;
    var parentSrc = _e.source().parent();
    var parentTgt = _e.target().parent();

    // put all edges in the top level for now
    // TODO does this cause issues in certain edgecases?
    if (false) {
      var kp = klayEleLookup[parentSrc.id()];

      kp.edges = kp.edges || [];

      kp.edges.push(_k3);
    } else {
      graph.edges.push(_k3);
    }
  }

  return graph;
};

function Layout(options) {
  var klayOptions = options.klay;

  this.options = assign({}, defaults, options);

  this.options.klay = assign({}, defaults.klay, klayOptions, klayOverrides);
}

Layout.prototype.run = function () {
  var layout = this;
  var options = this.options;

  var eles = options.eles;
  var nodes = eles.nodes();
  var edges = eles.edges();

  var graph = makeGraph(nodes, edges, options);

  klay.layout({
    graph: graph,
    options: mapToKlayNS(options.klay),
    success: function success() {},
    error: function error(_error) {
      throw _error;
    }
  });

  nodes.filter(function (n) {
    return !n.isParent();
  }).layoutPositions(layout, options, getPos);

  return this;
};

Layout.prototype.stop = function () {
  return this; // chaining
};

Layout.prototype.destroy = function () {
  return this; // chaining
};

module.exports = Layout;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


// Simple, internal Object.assign() polyfill for options objects etc.

module.exports = Object.assign != null ? Object.assign.bind(Object) : function (tgt) {
  for (var _len = arguments.length, srcs = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
    srcs[_key - 1] = arguments[_key];
  }

  srcs.filter(function (src) {
    return src != null;
  }).forEach(function (src) {
    Object.keys(src).forEach(function (k) {
      return tgt[k] = src[k];
    });
  });

  return tgt;
};

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var defaults = {
  nodeDimensionsIncludeLabels: false, // Boolean which changes whether label dimensions are included when calculating node dimensions
  fit: true, // Whether to fit
  padding: 20, // Padding on fit
  animate: false, // Whether to transition the node positions
  animateFilter: function animateFilter(node, i) {
    return true;
  }, // Whether to animate specific nodes when animation is on; non-animated nodes immediately go to their final positions
  animationDuration: 500, // Duration of animation in ms if enabled
  animationEasing: undefined, // Easing of animation if enabled
  transform: function transform(node, pos) {
    return pos;
  }, // A function that applies a transform to the final node position
  ready: undefined, // Callback on layoutready
  stop: undefined, // Callback on layoutstop
  klay: {
    // Following descriptions taken from http://layout.rtsys.informatik.uni-kiel.de:9444/Providedlayout.html?algorithm=de.cau.cs.kieler.klay.layered
    addUnnecessaryBendpoints: false, // Adds bend points even if an edge does not change direction.
    aspectRatio: 1.6, // The aimed aspect ratio of the drawing, that is the quotient of width by height
    borderSpacing: 20, // Minimal amount of space to be left to the border
    compactComponents: false, // Tries to further compact components (disconnected sub-graphs).
    crossingMinimization: 'LAYER_SWEEP', // Strategy for crossing minimization.
    /* LAYER_SWEEP The layer sweep algorithm iterates multiple times over the layers, trying to find node orderings that minimize the number of crossings. The algorithm uses randomization to increase the odds of finding a good result. To improve its results, consider increasing the Thoroughness option, which influences the number of iterations done. The Randomization seed also influences results.
    INTERACTIVE Orders the nodes of each layer by comparing their positions before the layout algorithm was started. The idea is that the relative order of nodes as it was before layout was applied is not changed. This of course requires valid positions for all nodes to have been set on the input graph before calling the layout algorithm. The interactive layer sweep algorithm uses the Interactive Reference Point option to determine which reference point of nodes are used to compare positions. */
    cycleBreaking: 'GREEDY', // Strategy for cycle breaking. Cycle breaking looks for cycles in the graph and determines which edges to reverse to break the cycles. Reversed edges will end up pointing to the opposite direction of regular edges (that is, reversed edges will point left if edges usually point right).
    /* GREEDY This algorithm reverses edges greedily. The algorithm tries to avoid edges that have the Priority property set.
    INTERACTIVE The interactive algorithm tries to reverse edges that already pointed leftwards in the input graph. This requires node and port coordinates to have been set to sensible values.*/
    direction: 'UNDEFINED', // Overall direction of edges: horizontal (right / left) or vertical (down / up)
    /* UNDEFINED, RIGHT, LEFT, DOWN, UP */
    edgeRouting: 'ORTHOGONAL', // Defines how edges are routed (POLYLINE, ORTHOGONAL, SPLINES)
    edgeSpacingFactor: 0.5, // Factor by which the object spacing is multiplied to arrive at the minimal spacing between edges.
    feedbackEdges: false, // Whether feedback edges should be highlighted by routing around the nodes.
    fixedAlignment: 'NONE', // Tells the BK node placer to use a certain alignment instead of taking the optimal result.  This option should usually be left alone.
    /* NONE Chooses the smallest layout from the four possible candidates.
    LEFTUP Chooses the left-up candidate from the four possible candidates.
    RIGHTUP Chooses the right-up candidate from the four possible candidates.
    LEFTDOWN Chooses the left-down candidate from the four possible candidates.
    RIGHTDOWN Chooses the right-down candidate from the four possible candidates.
    BALANCED Creates a balanced layout from the four possible candidates. */
    inLayerSpacingFactor: 1.0, // Factor by which the usual spacing is multiplied to determine the in-layer spacing between objects.
    layoutHierarchy: false, // Whether the selected layouter should consider the full hierarchy
    linearSegmentsDeflectionDampening: 0.3, // Dampens the movement of nodes to keep the diagram from getting too large.
    mergeEdges: false, // Edges that have no ports are merged so they touch the connected nodes at the same points.
    mergeHierarchyCrossingEdges: true, // If hierarchical layout is active, hierarchy-crossing edges use as few hierarchical ports as possible.
    nodeLayering: 'NETWORK_SIMPLEX', // Strategy for node layering.
    /* NETWORK_SIMPLEX This algorithm tries to minimize the length of edges. This is the most computationally intensive algorithm. The number of iterations after which it aborts if it hasn't found a result yet can be set with the Maximal Iterations option.
    LONGEST_PATH A very simple algorithm that distributes nodes along their longest path to a sink node.
    INTERACTIVE Distributes the nodes into layers by comparing their positions before the layout algorithm was started. The idea is that the relative horizontal order of nodes as it was before layout was applied is not changed. This of course requires valid positions for all nodes to have been set on the input graph before calling the layout algorithm. The interactive node layering algorithm uses the Interactive Reference Point option to determine which reference point of nodes are used to compare positions. */
    nodePlacement: 'BRANDES_KOEPF', // Strategy for Node Placement
    /* BRANDES_KOEPF Minimizes the number of edge bends at the expense of diagram size: diagrams drawn with this algorithm are usually higher than diagrams drawn with other algorithms.
    LINEAR_SEGMENTS Computes a balanced placement.
    INTERACTIVE Tries to keep the preset y coordinates of nodes from the original layout. For dummy nodes, a guess is made to infer their coordinates. Requires the other interactive phase implementations to have run as well.
    SIMPLE Minimizes the area at the expense of... well, pretty much everything else. */
    randomizationSeed: 1, // Seed used for pseudo-random number generators to control the layout algorithm; 0 means a new seed is generated
    routeSelfLoopInside: false, // Whether a self-loop is routed around or inside its node.
    separateConnectedComponents: true, // Whether each connected component should be processed separately
    spacing: 20, // Overall setting for the minimal amount of space to be left between objects
    thoroughness: 7 // How much effort should be spent to produce a nice layout..
  },
  priority: function priority(edge) {
    return null;
  } // Edges with a non-nil value are skipped when geedy edge cycle breaking is enabled
};

module.exports = defaults;

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var impl = __webpack_require__(0);

// registers the extension on a cytoscape lib ref
var register = function register(cytoscape) {
  if (!cytoscape) {
    return;
  } // can't register if cytoscape unspecified

  cytoscape('layout', 'klay', impl); // register with cytoscape.js
};

if (typeof cytoscape !== 'undefined') {
  // expose to global cytoscape (i.e. window.cytoscape)
  register(cytoscape);
}

module.exports = register;

/***/ }),
/* 4 */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_4__;

/***/ })
/******/ ]);
});