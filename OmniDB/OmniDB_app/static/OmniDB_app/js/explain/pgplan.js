try {
    var React = require('react');
    var ReactDOM = require('react-dom');
} catch (e) {}

var NodeExplain = function (rn, text) {
    var self = this;
    this.rn = rn;
    this.text = text;
    this.level = null;
    this.parent_node = null;
    this.kids = [];
    this.cost = null;
    this.exclusive_cost = null;
    this.time = null;
    this.loops = null;
    this.inclusive_time = null;
    this.exclusive_time = null;
    this.subplan = false;
    this.cte = false;
    this.cte_id = null;
    this.parent_cte = null;
    this.never_executed = false;

    // d3 related
    this.name = rn;
    this.value = 10;
    this.parent = null;
    //

    this.parseParam = function (pattern) {
        var val = self.text.match(pattern);
        if (val && val.length > 0) {
            val = val[1].split('..');
            if (val && val.length == 2) {
                return val;
            }
        }
        return null;
    };

    this.parseText = function () {
        self.cost = self.parseParam(/cost=([^\s]*)/);
        self.exclusive_cost = self.cost ? self.cost[1] : null;
        self.time = self.parseParam(/actual time=([^\s]*)/);

        var loops = self.text.match(/loops=([0-9]*)/);
        loops = loops ? loops[1] : null;
        self.loops = loops;

        self.inclusive_time = self.time ? self.time[1] * self.loops : null;
        self.exclusive_time = self.inclusive_time;

        self.never_executed = self.text.match(/\(never executed\)/) != null;

        if (self.text.match(/\(+/) != null) {
            // if at least one bracket
            self.node_description = self.text.match(/\s*[->]*(.*?)[\(]/)[1];
            self.node_details = self.text.match(/[\(].*/)[0];
        } else {
            // row without bracket is a details row
            self.node_description = null;
            self.node_details = self.text.match(/^[\s]*(.*)/)[1];
        }
        // collapsiblle nodes are started from "->", "InitPlan", "SubPlan"
        self.collapsible = self.text.match(/\s*->/) === null ? false : true;

        if (self.text.match(/^[\s]*InitPlan/) != null || self.text.match(/^[\s]*SubPlan/) != null) {
            self.subplan = true;
            self.collapsible = true;
            self.node_description = self.text.trim();
            self.node_details = null;
        }

        // detect CTE
        if (self.text.match(/\s*CTE/) != null && self.text.match(/\s*CTE Scan/) === null) {
            self.cte = true;
            self.collapsible = true;
            self.subplan = true;
            self.node_description = self.text.match(/^[\s]*(.*)/)[1];
            self.node_details = null;
            self.cte_id = self.text.match(/\s*CTE ([^\s]*)/)[1];
        }

        // detect parent CTE
        if (self.text.match(/\s*CTE Scan/) != null) {
            self.parent_cte = self.text.match(/\s*CTE Scan on ([^\s]*)/)[1];
        }

        // detect level
        var level = self.text.match(/^[\s]*->/);
        if (self.rn == 0) {
            // root node
            self.node_level = 0;
        } else if (level != null && level.length > 0) {
            // plan node
            self.node_level = level[0].length - 2;
        } else {
            // details node
            self.node_level = self.text.match(/^[\s]*/)[0].length;
        }
    };

    this.setParent = function (parent_node) {
        self.parent_node = parent_node;

        if (parent_node != null) {
            self.parent_node.addChild(self);
            self.parent = parent_node.name;
        } else {
            self.parent = null;
        }

        if (parent_node != null && self.cost != null) {
            self.parent_node.deductCost(self.cost[1]);
        }
        if (parent_node != null && self.exclusive_time != null) {
            self.parent_node.deductTime(self.inclusive_time);
        }
    };

    this.addChild = function (node) {
        self.kids.push(node);
    };

    this.deductCost = function (cost) {
        self.exclusive_cost = self.exclusive_cost - cost;
    };

    this.deductTime = function (time) {
        self.exclusive_time = self.exclusive_time - time;
    };

    this.hideSwitchChildren = function (is_hidden) {
        this.hidden = is_hidden;
        if (this.kids) {
            this.kids.forEach(function (item) {
                item.hideSwitchChildren(is_hidden);
            });
        }
    };

    self.parseText();
    return self;
};

var PGPlanNodes = function (records) {

    var nodes = [];
    var ctes = [];
    var subplans = [];

    var getParent = function (node) {
        var ret = null;
        nodes.forEach(function (item) {
            if (item.node_level < node.node_level) {
                ret = item;
            }
        });
        return ret;
    };

    // find parent for each node and fill CTEs list
    records.forEach(function (record, rn) {
        var node = new NodeExplain(rn, record[0]);
        var parent_node = getParent(node);
        node.setParent(parent_node);
        nodes.push(node);
        if (node.cte) {
            ctes.push(node);
        }
        if (node.subplan && !node.cte) {
            subplans.push(node);
        }
    });

    var deductCte = function (deducted_node, subtrahend) {
        if (subtrahend.kids.length < 1) {
            return;
        }
        if (subtrahend.kids[0].cost) {
            deducted_node.deductCost(subtrahend.kids[0].cost[1]);
        }
        if (subtrahend.kids[0].inclusive_time) {
            deducted_node.deductTime(subtrahend.kids[0].inclusive_time);
        }
    };

    // Deduct CTE and SubPlan cost/time
    ctes.forEach(function (ctenode) {

        // CTE Scan includes the cost of CTE, so needs to be deducted
        nodes.forEach(function (node) {
            if (node.parent_cte == ctenode.cte_id) {
                // cte scan node
                deductCte(node, ctenode);
            }
        });

        // if parent node of CTE is not CTE Scan, then deduct CTE cost from it
        if (ctenode.parent_node.parent_cte == null) {
            deductCte(ctenode.parent_node, ctenode);
        }
    });

    subplans.forEach(function (subplan_node) {
        if (subplan_node.parent_node != null) {
            deductCte(subplan_node.parent_node, subplan_node);
        }
    });

    // replace records with nodes objects
    nodes.forEach(function (node, idx) {
        records[idx] = node;
    });

    // calculate cost/time percentage for each node and parse the details about the nodes
    var summary_record = records[0];
    var total_cost = summary_record.cost ? summary_record.cost[1] : null;
    var total_time = summary_record.inclusive_time;

    records.forEach(function (record, idx) {
        var exclusive_cost = record.exclusive_cost ? record.exclusive_cost : null;

        var inclusive_cost_percentage = record.cost ? record.cost[1] / total_cost * 100 : null;
        var inclusive_time_percentage = record.time ? record.time[1] * record.loops / total_time * 100 : null;
        var cost_percentage = exclusive_cost ? exclusive_cost / total_cost * 100 : null;
        var time_percentage = record.exclusive_time ? record.exclusive_time / total_time * 100 : null;

        var val = record[0];

        record.cost_percentage = cost_percentage;
        record.inclusive_cost_percentage = inclusive_cost_percentage;
        record.time_percentage = time_percentage;
        record.inclusive_time_percentage = inclusive_time_percentage;
    });

    return records;
};

var PGPlan = React.createClass({

    getInitialState: function () {
        return {
            data: this.props.nodes,
            show_row_number: true,
            view: 'plain',
            subview: null,
            highlight: true,
            viewport_size: {
                width: 960,
                height: 500
            }
        };
    },

    componentDidMount: function () {
        if (this.state.view == "tree") {
            this.mountTree();
        }
    },

    componentDidUpdate: function () {
        if (this.state.view == "tree") {
            this.mountTree();
        }
    },

    componentWillReceiveProps: function (newprops) {
        this.setState({ data: newprops.nodes });
    },

    collapseSwitch: function (record_idx) {
        var data = this.state.data;

        var is_collapsed = !data[record_idx].collapsed;

        data[record_idx].collapsed = is_collapsed;

        data[record_idx].kids.forEach(function (node) {
            data[node.rn].hideSwitchChildren(is_collapsed);
            data[node.rn].collapsed = false;
        });

        this.setState({ data: data });
    },

    switchRowNumber: function () {
        this.setState({ show_row_number: !this.state.show_row_number });
    },

    switchView: function (view, subview) {
        this.setState({ view: view, subview: subview });
    },

    switchHighlight: function () {
        this.setState({ highlight: !this.state.highlight });
    },

    renderRecord(record, idx) {

        var self = this;

        if (record.hidden) {
            return null;
        }

        var val = record[0];

        if (record.time_percentage != null) {
            var exclusive_percentage = record.time_percentage;
            var inclusive_percentage = record.inclusive_time_percentage;
        } else {
            var exclusive_percentage = record.cost_percentage;
            var inclusive_percentage = record.inclusive_cost_percentage;
        }

        if (record.never_executed) {
            var exclusive_color = "rgba(51, 122, 183, 0.4)";
            var inclusive_color = "rgba(51, 122, 183, 0.1)";
        } else {
            var exclusive_color = "rgba(251, 2, 2, 0.4)";
            var inclusive_color = "rgba(251, 2, 2, 0.1)";
        }

        if (exclusive_percentage === null) {
            exclusive_percentage = 0;
        }
        if (inclusive_percentage === null) {
            inclusive_percentage = 0;
        }

        var exclusive_gradient = exclusive_color + ", " + exclusive_color + " " + exclusive_percentage + "%, ";
        var inclusive_gradient = inclusive_color + " " + exclusive_percentage + "%, " + inclusive_color + " " + inclusive_percentage + "%, ";
        var transparent_gradient = "transparent " + inclusive_percentage + "%, transparent 100%";

        var style = "-webkit-linear-gradient(left, " + exclusive_gradient + inclusive_gradient + transparent_gradient + ")";

        // wrap explain plan nodes with span tag
        if (idx == 0 && this.state.highlight) {
            // 1st row is always a node
            var val = React.createElement(
                'span',
                null,
                React.createElement(
                    'span',
                    { className: 'explain-plan-header-title' },
                    record.node_description
                ),
                React.createElement(
                    'span',
                    { className: 'explain-plan-details' },
                    record.node_details
                )
            );
        } else {
            var spaces = React.createElement(
                'span',
                null,
                " ".repeat(record.node_level)
            );
            if (record.collapsible && !record.subplan) {
                var record_style = "explain-plan-collapsible-record";

                if (record.collapsed) {
                    var collapse_icon = "glyphicon-circle-arrow-up";
                    var collapse_note = "[subtree skipped]";
                } else {
                    var collapse_icon = "glyphicon-circle-arrow-right";
                    var collapse_note = null;
                }

                var collapse = React.createElement(
                    'span',
                    null,
                    React.createElement('span', { className: "glyphicon " + collapse_icon + " explain-plan-node-arrow", onClick: function () {
                            self.collapseSwitch(idx);
                        } }),
                    React.createElement(
                        'span',
                        { className: 'explain-plan-node-arrow-hidden' },
                        '->'
                    )
                );
            } else {
                var record_style = "explain-plan-record";
                var collapse = null;
                var collapse_note = null;
            }

            if (record.cte) {
                var record_style = "explain-plan-cte-record";
            }
            ///////

            if (this.state.highlight) {
                var val = React.createElement(
                    'span',
                    null,
                    spaces,
                    collapse,
                    React.createElement(
                        'span',
                        { className: 'explain-plan-node-title' },
                        record.node_description
                    ),
                    React.createElement(
                        'span',
                        { className: 'explain-plan-details' },
                        record.node_details
                    ),
                    React.createElement(
                        'span',
                        { className: 'explain-plan-node-skipped-note' },
                        collapse_note
                    )
                );
            } else {
                var val = React.createElement(
                    'span',
                    null,
                    record.text
                );
                var style = "";
            }
        }

        if (this.state.show_row_number) {
            rn = React.createElement(
                'td',
                { className: 'record-rownum' },
                idx + 1
            );
        } else {
            rn = React.createElement('td', { className: 'record-rownum' });
        }

        return React.createElement(
            'tr',
            { key: "plan-record-" + idx, className: record_style },
            rn,
            React.createElement(
                'td',
                { style: { backgroundImage: style } },
                val
            )
        );
        //<td> {record.inclusive_time} </td>
        //<td> {record.exclusive_time} </td>
        //<td> {record.time_percentage} % </td>
    },

    render: function () {
        var self = this;

        if (this.state.view == "tree") {
            return this.renderTree();
        }

        var self = this;
        var data = this.state.data;
        var plan_records = [];

        if (typeof data == "undefined") {
            return null;
        }

        data.forEach(function (record, idx) {
            plan_records.push(self.renderRecord(record, idx));
        });
        return React.createElement(
            'div',
            null,
            self.renderViewSwitcher(),
            React.createElement(
                'table',
                { className: 'table-resultset table table-hover' },
                React.createElement(
                    'thead',
                    null,
                    React.createElement(
                        'tr',
                        null,
                        React.createElement(
                            'th',
                            null,
                            React.createElement(
                                'span',
                                { className: 'explain-plan-rownum-switch', onClick: self.switchRowNumber },
                                '#'
                            )
                        ),
                        React.createElement(
                            'th',
                            null,
                            React.createElement(
                                'span',
                                { className: 'explain-plan-rownum-switch', onClick: self.switchHighlight },
                                ' QUERY PLAN '
                            )
                        )
                    )
                ),
                React.createElement(
                    'tbody',
                    null,
                    plan_records
                )
            )
        );
    },

    renderViewSwitcher: function () {
        var self = this;
        if (self.state.view == "tree") {
            var zoom = React.createElement(
                'span',
                null,
                React.createElement('span', { className: 'glyphicon glyphicon-zoom-out explain-plan-view-switcher', onClick: self.zoomOut }),
                React.createElement('span', { className: 'glyphicon glyphicon-zoom-in explain-plan-view-switcher', onClick: self.zoomIn })
            );
        } else {
            var zoom = null;
        }
        return React.createElement(
            'div',
            { className: 'explain-plan-toolbar' },
            React.createElement('span', { className: 'glyphicon glyphicon-th-list explain-plan-view-switcher', onClick: function () {
                    self.switchView("plain");
                } }),
            React.createElement('span', { className: 'glyphicon glyphicon-tree-deciduous explain-plan-view-switcher', onClick: function () {
                    self.switchView("tree");
                } }),
            React.createElement('span', { className: 'glyphicon glyphicon-tree-conifer explain-plan-view-switcher', onClick: function () {
                    self.switchView("tree", "conifer");
                } }),
            zoom
        );
    },

    zoomIn: function () {
        this.setState({ viewport_size: {
                width: this.state.viewport_size.width + 100,
                height: this.state.viewport_size.height + 200
            } });
    },

    zoomOut: function () {
        this.setState({ viewport_size: {
                width: this.state.viewport_size.width - 100,
                height: this.state.viewport_size.height - 200
            } });
    },

    renderTree: function () {
        var self = this;
        return React.createElement(
            'div',
            { treetype: self.state.subview },
            self.renderViewSwitcher(),
            React.createElement('div', { ref: 'treeMountPoint', className: 'explain-plan-mount-div', viewport_width: self.state.viewport_size.width })
        );
    },

    mountTree: function () {
        var self = this;
        var treeData = [this.state.data[0]];

        // Generate the tree diagram
        var margin = { top: 20, right: 120, bottom: 20, left: 220 },
            width = self.state.viewport_size.width - margin.right - margin.left,
            height = self.state.viewport_size.height - margin.top - margin.bottom;

        var i = 0;

        var tree = d3.layout.cluster();

        tree.size([height, width]).children(function (d) {
            // filter out details records
            var kids = [];
            if (d.kids) {
                d.kids.forEach(function (item) {
                    if (item.collapsible) {
                        kids.push(item);
                    }
                });
            }
            return kids;
        });

        var diagonal = d3.svg.diagonal().projection(function (d) {
            return [d.y, d.x];
        });

        d3.select(this.refs.treeMountPoint).select("svg").remove(); // remove proviously rendered svg
        var svg = d3.select(this.refs.treeMountPoint).append("svg").attr("height", height).attr("width", width).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        root = treeData[0];
        update(root);

        function update(source) {

            // Compute tree layout.
            var nodes = tree.nodes(root),
                links = tree.links(nodes);

            // compute CTE links
            var ctes = {};
            var cte_links = [];
            nodes.forEach(function (node) {
                if (node.cte) {
                    ctes[node.cte_id] = node;
                }
            });
            nodes.forEach(function (node) {
                // don't merge it to the above loop as CTE Scan can appear before CTE
                if (node.parent_cte) {
                    cte_links.push({
                        source: node,
                        target: ctes[node.parent_cte]
                    });
                }
            });

            if (self.state.subview == "conifer") {
                // Normalize for fixed-depth.
                nodes.forEach(function (d) {
                    d.y = d.depth * 180;
                });
            }

            // Declare the nodes…
            var node = svg.selectAll("g.node").data(nodes, function (d) {
                return d.id || (d.id = ++i);
            });

            // Enter the nodes.
            var maxY = 0;
            var maxX = 0;
            var nodeEnter = node.enter().append("g").attr("class", "node").attr("transform", function (d) {
                maxX = d.x > maxX ? d.x : maxX;
                maxY = d.y > maxY ? d.y : maxY;
                return "translate(" + d.y + "," + d.x + ")";
            });

            nodeEnter.append("circle").attr("r", function (d) {
                var ret = d.time_percentage ? d.time_percentage * 0.5 : d.cost_percentage * 0.5;
                if (ret < 3) {
                    return 3;
                } else {
                    return ret;
                }
            }).attr("class", function (d) {
                if (d.never_executed) {
                    return "explain-plan-tree-circle explain-plan-tree-circle-never-executed";
                } else {
                    return "explain-plan-tree-circle";
                }
            });

            nodeEnter.append("text").attr("x", function (d) {
                return d.children || d._children ? (d.value + 4) * -1 : d.value + 4;
            }).attr("dy", function (d) {
                if (!d.parent || !d.children) {
                    return ".35em";
                } else {
                    return "1.5em";
                }
            }).attr("class", "explain-plan-tree-node-text").attr("text-anchor", function (d) {
                if (!d.parent) {
                    return "end";
                }
                if (!d.children) {
                    return "start";
                }
                return "middle";
            }).text(function (d) {
                return d.node_description;
            });

            // Declare the links…
            var link = svg.selectAll("path.link").data(links, function (d) {
                return d.target.id;
            });

            // Enter the links.
            link.enter().insert("path", "g").attr("class", "link explain-plan-tree-link").attr("d", diagonal);

            // remove initial CTE links
            d3.select(self.refs.treeMountPoint).selectAll("path.link").filter(function (d) {
                return d.target.cte;
            }).remove();

            // declare proper CTE links
            var cte_link = svg.selectAll("path.link").data(cte_links, function (d) {
                return d.source.id;
            });

            // Enter cte links.
            cte_link.enter().insert("path", "g").attr("class", "link explain-plan-tree-link explain-plan-cte-link").attr("d", function (d) {
                return diagonal(d);
            });

            // Adjust viewport size according to the built tree
            d3.select(self.refs.treeMountPoint).selectAll("svg").attr("width", maxY + 1000).attr("height", maxX + 100);

            // Adjust parent div height to display entire svg
            d3.select(self.refs.treeMountPoint).attr("style", "height: " + (maxX + 100) + "px");
        }
    }
});

try {
    module.exports = {
        "PGPlan": PGPlan,
        "PGPlanNodes": PGPlanNodes
    };
} catch (e) {}
