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
                defaults: {
                    hand: [],
                    wager: {amount: 0},
                    hand_total: 0
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
            Hand: Backbone.Collection.extend({
                model: Models.Card
            }),
            Seats: BackboneSocketio.Collection.extend({
                model: Models.Seat,
                socket: Sockets.seats
            })
        };

        return _.extend({}, Models, Collections);

    }
); 