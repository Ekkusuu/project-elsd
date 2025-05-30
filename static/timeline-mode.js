define('ace/mode/timeline', function(require, exports, module) {
    "use strict";

    var oop = require("ace/lib/oop");
    var TextMode = require("ace/mode/text").Mode;
    var TimelineHighlightRules = require("ace/mode/timeline_highlight_rules").TimelineHighlightRules;
    var TimelineCompletions = require("ace/mode/timeline_completions").TimelineCompletions;
    var CstyleBehaviour = require("ace/mode/behaviour/cstyle").CstyleBehaviour;

    var Mode = function() {
        this.HighlightRules = TimelineHighlightRules;
        this.$completer = new TimelineCompletions();
        this.$behaviour = new CstyleBehaviour();
    };
    oop.inherits(Mode, TextMode);

    (function() {
        this.lineCommentStart = "//";
        this.blockComment = {start: "/*", end: "*/"};
        
        this.getCompletions = function(state, session, pos, prefix) {
            return this.$completer.getCompletions(state, session, pos, prefix);
        };
        
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

define('ace/mode/timeline_completions', function(require, exports, module) {
    "use strict";

    var oop = require("ace/lib/oop");

    var TimelineCompletions = function() {};

    (function() {
        this.keywords = [
            "event",
            "period",
            "timeline",
            "relationship",
            "main",
            "export",
            "if",
            "else",
            "for",
            "in",
            "modify"
        ];

        this.properties = [
            "title",
            "date",
            "start",
            "end",
            "importance",
            "from",
            "to",
            "type",
            "year",
            "month",
            "day"
        ];

        this.constants = [
            "high",
            "medium",
            "low",
            "cause-effect",
            "contemporaneous",
            "precedes",
            "follows",
            "includes",
            "excludes",
            "true",
            "false",
            "BCE",
            "CE"
        ];

        this.getCompletions = function(state, session, pos, prefix) {
            var token = session.getTokenAt(pos.row, pos.column);
            var line = session.getLine(pos.row);
            var completions = [];

            // Add all possible completions
            var allWords = [].concat(
                this.keywords.map(function(word) {
                    return {
                        caption: word,
                        value: word,
                        meta: "keyword",
                        score: 1000
                    };
                }),
                this.properties.map(function(word) {
                    return {
                        caption: word,
                        value: word,
                        meta: "property",
                        score: 900
                    };
                }),
                this.constants.map(function(word) {
                    return {
                        caption: word,
                        value: word,
                        meta: "constant",
                        score: 800
                    };
                })
            );

            // Context-aware completions
            if (line.trim().endsWith("importance =") || line.trim().endsWith("importance=")) {
                // Only show importance values
                return this.constants
                    .filter(word => ["high", "medium", "low"].includes(word))
                    .map(word => ({
                        caption: word,
                        value: word,
                        meta: "importance",
                        score: 1000
                    }));
            }

            if (line.trim().endsWith("type =") || line.trim().endsWith("type=")) {
                // Only show relationship types
                return this.constants
                    .filter(word => ["cause-effect", "contemporaneous", "precedes", "follows", "includes", "excludes"].includes(word))
                    .map(word => ({
                        caption: word,
                        value: word,
                        meta: "relationship type",
                        score: 1000
                    }));
            }

            // Inside a block, suggest properties
            if (line.trim().endsWith("{")) {
                return this.properties.map(word => ({
                    caption: word,
                    value: word + " = ",
                    meta: "property",
                    score: 1000
                }));
            }

            // Default to all completions
            return allWords;
        };

    }).call(TimelineCompletions.prototype);

    exports.TimelineCompletions = TimelineCompletions;
}); 