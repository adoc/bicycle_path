/*  config.js
    Application Configuration.
    (c) 2010 - 2014 C. Nicholas Long
*/

define(['underscore'],
    function(_) {

        var baseTheme = {
            cardImageFolder: "static/assets/oxygen",
            cardImageExt: "png",

            gameTemplate: require("text!static/theming/base/game.html.tmpl"),
            playerTemplate: require("text!static/theming/base/player.html.tmpl"),
            dealerTemplate: require("text!static/theming/base/dealer.html.tmpl"),
            handTemplate: require("text!static/theming/base/hand.html.tmpl"),
            tableStatusTemplate: require("text!static/theming/base/table.status.html.tmpl"),
            playerStatusTemplate: require("text!static/theming/base/player.status.html.tmpl"),
            debugControlsTemplate: require("text!static/theming/base/debug.controls.html.tmpl"),
            tableControlsTemplate: require("text!static/theming/base/table.controls.html.tmpl"),
            wagerControlsTemplate: require("text!static/theming/base/wager.controls.html.tmpl"),
            gameControlsTemplate: require("text!static/theming/base/blackjack/game.controls.tmpl"), // Notice we are using blackjack controls by default.
            stepTranslations: {
                'PrepareStep': "Please take a seat.",
                'WagerStep': "Have a seat and place your bets.",
                'PlayerStep': "Let's play!",
                'ResolveStep': "Round Over!",
                'CleanupStep': ""
            }
        };

        return {
            apiRoot: '/api/v1',
            Theme: baseTheme
        };

        return _.extend(config, {
            // This goes elsewhere.
            engine_url: function (id, action) {
                return join_path(config.apiRoot, 'engines', id, action);
            }
        });
    }
);