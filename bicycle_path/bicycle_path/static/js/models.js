/* 
    (c) 2010 - 2014 C. Nicholas Long
*/

define(['jquery', 'underscore', 'backbone'],
    function($, _, Backbone) {

        var BaseViewModel = Backbone.Model.extend({
            url: function() {
                return this.controller.url(this.action);
            },
            _url: function () {
                return this.controller.url();
            },
            constructor: function(opts) {
                var self = this,
                    args = arguments;

                // Extend any opts in to this view.
                _.extend(this, opts);

                Backbone.Model.apply(this, arguments);
            }
        });

        var Player = BaseViewModel.extend({
            action: "player"
        });

        var Game = BaseViewModel.extend({
            action: "poll"
        });

        return {Player: Player,
                Game: Game};

    }
); 