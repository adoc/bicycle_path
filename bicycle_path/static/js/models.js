/* 
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['backbone', 'backbone_socketio', 'sockets'],
    function(Backbone, BackboneSocketio, Sockets) {

        var Models = {
            /*Game: BackboneSocketio.Model.extend({
                socket: Sockets.engine
            }),*/
            // Breaking a Backbone.Model a bit to be a one-value model.
            Card: Backbone.Model.extend({
                constructor: function(value, options) {
                    Backbone.Model.prototype.constructor.call(
                            this, {'_value': value}, options);
                },
                get: function() {
                    return Backbone.Model.prototype.get.call(this, "_value");
                }
            }),
            Dealer: BackboneSocketio.Model.extend({
                socket: Sockets.dealer
            }),
            Seat: Backbone.Model.extend({
                idAttribute: "_id",
                defaults: {
                    bankroll: null,
                    seat_pref: null,
                    wager: {
                        amount: 0
                    }
                }
            }),
            PlayerStatus: BackboneSocketio.Model.extend({
                socket: Sockets.playerStatus
            }),
            TableStatus: BackboneSocketio.Model.extend({
                socket: Sockets.tableStatus
            }),
            TableControls: BackboneSocketio.Model.extend({
                socket: Sockets.tableControls
            }),
            WagerControls: BackboneSocketio.Model.extend({
                socket: Sockets.wagerControls
            }),
            GameControls: BackboneSocketio.Model.extend({
                socket: Sockets.gameControls
            }),
            DebugControls: BackboneSocketio.Model.extend({
                socket: Sockets.debugControls
            })
        };

        var Collections = {
            // Keep better track of changes to this model in order to trigger
            // animations.
            Hand: Backbone.Collection.extend({
                model: Models.Card
            })
        };

        _.extend(Collections, {
            Hands: BackboneSocketio.Collection.extend({
                model: Collections.Hand,
                socket: Sockets.hands
            }),
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
            Seats: BackboneSocketio.Collection.extend({
                model: Models.Seat,
                socket: Sockets.seats
            })
        });

        return _.extend({}, Models, Collections);

    }
); 