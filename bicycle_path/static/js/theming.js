/*  theming.js
    Application Theming.
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['underscore', 'config'],
    function(_, Config) {
        return {
            cardAsset: function(card) {
                /* Given a `card` string ("KA"), return the card image file
                name ("ka.png").
                */
                var cardFile = join_ext(card.toLowerCase(),
                                        Config.Theme.cardImageExt);
                return join_path(Config.Theme.cardImageFolder, CardFile);
            }
        };
    }
);