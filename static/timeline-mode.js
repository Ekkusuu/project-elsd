define('ace/mode/timeline', function(require, exports, module) {
    "use strict";

    var oop = require("ace/lib/oop");
    var TextMode = require("ace/mode/text").Mode;
    var TimelineHighlightRules = require("ace/mode/timeline_highlight_rules").TimelineHighlightRules;

    var Mode = function() {
        this.HighlightRules = TimelineHighlightRules;
    };
    oop.inherits(Mode, TextMode);

    (function() {
        this.lineCommentStart = "//";
        this.blockComment = {start: "/*", end: "*/"};
        
        this.$id = "ace/mode/timeline";
    }).call(Mode.prototype);

    exports.Mode = Mode;
});

define('ace/mode/timeline_highlight_rules', function(require, exports, module) {
    "use strict";

    var oop = require("ace/lib/oop");
    var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

    var TimelineHighlightRules = function() {
        // Keywords from your grammar
        var keywords = (
            "\\b(event|period|timeline|relationship|main|export|if|else|for|in|modify)\\b"
        );

        var properties = (
            "\\b(title|date|start|end|importance|from|to|type|year|month|day)\\b"
        );

        var constants = (
            "\\b(high|medium|low|cause-effect|contemporaneous|precedes|follows|includes|excludes|true|false|BCE|CE)\\b"
        );

        this.$rules = {
            "start": [{
                token: "comment",
                regex: "\\/\\/.*$"
            }, {
                token: "comment",
                regex: "\\/\\*",
                next: "comment"
            }, {
                token: "string",
                regex: '"(?:[^"\\\\]|\\\\.)*?"'
            }, {
                token: "constant.numeric",
                regex: "\\b\\d+\\b"
            }, {
                token: "keyword",
                regex: keywords
            }, {
                token: "support.function",
                regex: properties
            }, {
                token: "constant.language",
                regex: constants
            }, {
                token: "keyword.operator",
                regex: "[=,;{}]"
            }, {
                token: "text",
                regex: "\\s+"
            }],
            "comment": [{
                token: "comment",
                regex: "\\*\\/",
                next: "start"
            }, {
                defaultToken: "comment"
            }]
        };
    };

    oop.inherits(TimelineHighlightRules, TextHighlightRules);
    exports.TimelineHighlightRules = TimelineHighlightRules;
}); 