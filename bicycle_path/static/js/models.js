/* 
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['backbone', 'backbone_socketio', 'sockets'],
    function(Backbone, BackboneSocketio, Sockets) {

        var Models = {};
        var Collections = {};

        // Breaking a Backbone.Model a bit to be a one-value model.
        Models.Card = Backbone.Model.extend({
            constructor: function(value, options) {
                Backbone.Model.prototype.constructor.call(
                        this, {'_value': value}, options);
            },
            get: function() {
                return Backbone.Model.prototype.get.call(this, "_value");
            }
        });

        Models.Seat = Backbone.Model.extend({
            idAttribute: "_id",
            defaults: {
                bankroll: null,
                seat_pref: null,
                wager: {
                    amount: 0
                }
            }
        });

        Collections.Cards = Backbone.Collection.extend({
            model: Models.Card,
            constructor: function () {
                // Hack to update the constructor name for debug/console log.
                // (Not sure why this works!)
                Backbone.Collection.apply(this, arguments);
            }
        })

        Models.Hand = Backbone.Model.extend({
            idAttribute: "_id",
            defaults: {
                hand: [],
                hand_total: 0 // Blackjack specific.
            },
            constructor: function () {
                // Hack to update the constructor name for debug/console log.
                // (Not sure why this works!)
                Backbone.Model.apply(this, arguments);
            },
            initialize: function () {
                var self = this;

                // Set the nested "hand" model.
                function setNestedHand() {
                    self.set({
                        hand: new Collections.Cards(self.get("hand"))
                    },{
                        silent: true
                    });
                }

                this.on("add change", function () {
                    setNestedHand();
                });
            }
        });

        Models.Dealer = BackboneSocketio.Model.extend({
            socket: Sockets.dealer,
            defaults: {
                bankroll_view: "nada",
                hand: [],
                hand_total: 0
            },
            initialize: function () {
                var self = this;
                this.on("add change", function (data) {
                    console.log("Dealer add/change", arguments);
                });
            }
        });

        Models.PlayerStatus = BackboneSocketio.Model.extend({
            socket: Sockets.playerStatus
        });

        Models.TableStatus = BackboneSocketio.Model.extend({
            socket: Sockets.tableStatus
        });

        Models.TableControls = BackboneSocketio.Model.extend({
            socket: Sockets.tableControls
        });

        Models.WagerControls = BackboneSocketio.Model.extend({
            socket: Sockets.wagerControls
        });

        Models.GameControls = BackboneSocketio.Model.extend({
            socket: Sockets.gameControls
        });

        Models.DebugControls = BackboneSocketio.Model.extend({
            socket: Sockets.debugControls
        });

        Collections.Hands = BackboneSocketio.Collection.extend({
            model: Models.Hand,
            socket: Sockets.hands,
            constructor: function () {
                // Hack to update the constructor name for debug/console log.
                // (Not sure why this works!)
                BackboneSocketio.Collection.apply(this, arguments);
            },
            /*
            initialize: function () {

                this.on("reset", function(self) {
                    console.log("reset", self);
                });
            }
            */
        });

        Collections.Seats = BackboneSocketio.Collection.extend({
            model: Models.Seat,
            socket: Sockets.seats
        });

        /*
        var Collections = {
            // Keep better track of changes to this model in order to trigger
            // animations.

            // Deprecating.
            Hand: Backbone.Collection.extend({
                model: Models.Card
            })
        };
        */

        /*
        Backbone.Collection.extend({
            model: Models.Card,
            oldState: [],
            initialize: function() {
                var self = this;
                Backbone.Collection.prototype.initialize.apply(this,
                                                               arguments);
                this.on("reset", function(data) {

                    if (self.oldState.length > 0 && data.models.length === 0) {
                        self.oldState = [];
                        // How can we percolate these events??
                        // Add this to a queue of actions in the view??
                        console.log("model discard trigger", self);
                        self.trigger("discard");
                    } else if (data.models.length > self.oldState.length) {
                        // var off = data.models.length - self.oldState.length;
                        
                        
                        for (var i=self.oldState.length; i < data.models.length; i++) {
                            self.trigger("deal", data.models[i]);
                        }
                        self.oldState = data.models;
                    }

                });
            }
        }),
        */

        return _.extend({}, Models, Collections);
    }
); 