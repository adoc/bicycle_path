/*  
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['underscore',
        "text!/static/theming/base/game.html.tmpl",
        "text!/static/theming/base/seat.html.tmpl",
        "text!/static/theming/base/seats.html.tmpl",
        "text!/static/theming/base/dealer.html.tmpl",
        "text!/static/theming/base/hand.html.tmpl",
        "text!/static/theming/base/table.status.html.tmpl",
        "text!/static/theming/base/player.status.html.tmpl",
        "text!/static/theming/base/debug.controls.html.tmpl",
        "text!/static/theming/base/table.controls.html.tmpl",
        "text!/static/theming/base/wager.controls.html.tmpl",
        "text!/static/theming/base/blackjack.game.controls.tmpl"],
    function(_, gameTemplate, seatTemplate, seatsTemplate, dealerTemplate,
            handTemplate, tableStatusTemplate, playerStatusTemplate,
            debugControlsTemplate, tableControlsTemplate, wagerControlsTemplate,
            gameControlsTemplate) {

        var baseTheme = {
            cardImageFolder: "static/assets/bicycle",
            cardImageExt: "png",

            gameTemplate: _.template(gameTemplate),
            seatTemplate: _.template(seatTemplate),
            seatsTemplate: _.template(seatsTemplate),
            dealerTemplate: _.template(dealerTemplate),
            handTemplate: _.template(handTemplate),
            tableStatusTemplate: _.template(tableStatusTemplate),
            playerStatusTemplate: _.template(playerStatusTemplate),
            debugControlsTemplate: _.template(debugControlsTemplate),
            tableControlsTemplate: _.template(tableControlsTemplate),
            wagerControlsTemplate: _.template(wagerControlsTemplate),
            gameControlsTemplate: _.template(gameControlsTemplate),

            stepTranslations: {
                'PrepareStep': "Please take a seat.",
                'WagerStep': "Have a seat and place your bets.",
                'PlayerStep': "Let's play!",
                'ResolveStep': "Round Over!",
                'CleanupStep': ""
            }
        };

        return baseTheme;
    }
);