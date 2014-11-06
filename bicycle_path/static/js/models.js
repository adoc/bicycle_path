/* 
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['backbone', 'backbone_socketio', 'sockets'],
    function(Backbone, BackboneSocketio, Sockets) {

        var Models = {
            Game: BackboneSocketio.Model.extend({
                socket: Sockets.engine
            }),
            Card: Backbone.Model.extend(),
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
            TableControls: BackboneSocketio.Model.extend({
                socket: Sockets.tableControls
            }),
            WagerControls: BackboneSocketio.Model.extend({
                socket: Sockets.wagerControls
            }),
            GameControls: BackboneSocketio.Model.extend({
                socket: Sockets.gameControls
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