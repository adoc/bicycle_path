/*  blackjack.js
    Blackjack Game.
    (c) 2010 - 2014 C. Nicholas Long
*/

define(['jquery', 'underscore', 'site', 'config', 'bootstrap'],
    function($, _, Site, Config) {
        return {
            boot: function() {
                console.log(Config.engine_url('12345', 'bet'));
            }
        };
    }
);