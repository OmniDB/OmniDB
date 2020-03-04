ace.define("ace/theme/omnidb",["require","exports","module","ace/lib/dom"], function(require, exports, module) {

exports.isDark = false;
exports.cssClass = "ace-omnidb";
exports.cssText = ".ace-omnidb .ace_gutter {\
background: #f6f6f6;\
color: #4D4D4C\
}\
.ace-omnidb .ace_print-margin {\
width: 1px;\
background: #f6f6f6\
}\
.ace-omnidb {\
background-color: #FFFFFF;\
color: #4D4D4C\
}\
.ace-omnidb .ace_cursor {\
color: #AEAFAD\
}\
.ace-omnidb .ace_marker-layer .ace_selection {\
background: #D6D6D6\
}\
.ace-omnidb.ace_multiselect .ace_selection.ace_start {\
box-shadow: 0 0 3px 0px #FFFFFF;\
}\
.ace-omnidb .ace_marker-layer .ace_step {\
background: rgb(255, 255, 0)\
}\
.ace-omnidb .ace_marker-layer .ace_bracket {\
margin: 0 0 0 -1px;\
border: 1px solid rgba(128, 102, 8, 0.36);\
background-color: #FFE587;\
}\
.ace-omnidb .ace_marker-layer .ace_active-line {\
background: #EFEFEF\
}\
.ace-omnidb .ace_gutter-active-line {\
background-color : #dcdcdc\
}\
.ace-omnidb .ace_marker-layer .ace_selected-word {\
border: 1px solid #D6D6D6\
}\
.ace-omnidb .ace_invisible {\
color: #D1D1D1\
}\
.ace-omnidb .ace_keyword,\
.ace-omnidb .ace_meta,\
.ace-omnidb .ace_storage,\
.ace-omnidb .ace_storage.ace_type,\
.ace-omnidb .ace_support.ace_type {\
color: #4A6BF1\
}\
.ace-omnidb .ace_keyword.ace_operator {\
color: #3E999F\
}\
.ace-omnidb .ace_constant.ace_character,\
.ace-omnidb .ace_constant.ace_language,\
.ace-omnidb .ace_constant.ace_numeric,\
.ace-omnidb .ace_keyword.ace_other.ace_unit,\
.ace-omnidb .ace_support.ace_constant,\
.ace-omnidb .ace_variable.ace_parameter {\
color: #F5871F\
}\
.ace-omnidb .ace_constant.ace_other {\
color: #666969\
}\
.ace-omnidb .ace_invalid {\
color: #FFFFFF;\
background-color: #C82829\
}\
.ace-omnidb .ace_invalid.ace_deprecated {\
color: #FFFFFF;\
background-color: #8959A8\
}\
.ace-omnidb .ace_fold {\
background-color: #4271AE;\
border-color: #4D4D4C\
}\
.ace-omnidb .ace_entity.ace_name.ace_function,\
.ace-omnidb .ace_support.ace_function,\
.ace-omnidb .ace_variable {\
color: #4271AE\
}\
.ace-omnidb .ace_support.ace_class,\
.ace-omnidb .ace_support.ace_type {\
color: #C99E00\
}\
.ace-omnidb .ace_heading,\
.ace-omnidb .ace_markup.ace_heading,\
.ace-omnidb .ace_string {\
color: #718C00\
}\
.ace-omnidb .ace_entity.ace_name.ace_tag,\
.ace-omnidb .ace_entity.ace_other.ace_attribute-name,\
.ace-omnidb .ace_meta.ace_tag,\
.ace-omnidb .ace_string.ace_regexp,\
.ace-omnidb .ace_variable {\
color: #C82829\
}\
.ace-omnidb .ace_comment {\
color: #8E908C\
}\
.ace-omnidb .ace_indent-guide {\
background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAE0lEQVQImWP4////f4bdu3f/BwAlfgctduB85QAAAABJRU5ErkJggg==) right repeat-y\
}";

var dom = require("../lib/dom");
dom.importCssString(exports.cssText, exports.cssClass);
});
