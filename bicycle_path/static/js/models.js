/* 
    (c) 2010 - 2014 C. Nicholas Long
*/

"use strict";

define(['jquery', 'underscore', 'backbone', 'sockets'],
    function($, _, Backbone, Sockets) {

        // Deprecated but good reference??
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

        /* Interesting idea to unify Backbone.Model and socketio
        Several implementations already exist but seem to run in to trouble
        of trying to do "too much".
        */
        //
        var SocketioModel = Backbone.Model.extend({
            //
            constructor: function (attributes, options) {
                options || (options = {});
                if (options.socket) this.socket = options.socket;
                if (options.controller) this.controller = options.controller;
                if (options.model_id) this.id = options.model_id;

                Backbone.Model.apply(this, arguments);
            },
            //
            request: function (method, options) {
                socketRequest(this.socket, method, {
                    ns: this.url(),
                    id: this.id
                    }, options);
            },
            //
            sync: function (method, model, options) {
                var self = this,
                    success;

                if (method == "read") {
                    success = function (data) {
                        self.set(data);
                        if (options.success) {
                            options.success(model, null, options);
                        }
                    }
                }

                socketRequest(this.socket, method, {
                    ns: model.url(),
                    id: this.id,
                    data: this.changed
                    }, {
                    success: success
                });
            },
            // Watch the model and receive a "change" event when updated.
            watch: function (options) {
                var self = this;

                // Join on inintialize. This can probably be moved elsewhere.
                socketRequest(this.socket, 'watch', {
                    id: this.id
                },{
                    success: function(data) {
                        self.socket.on("change",
                            function (data) {
                                // console.log("Model change", data);
                                self.set(data);
                            }
                        );
                    }
                });
            }
        });

        var Seat = BaseViewModel.extend({
            //urlRoot: "player",
            socket: Sockets.seat
        });

        var Dealer = BaseViewModel.extend({
            socket: Sockets.dealer
        });

        var Game = SocketioModel.extend({
            urlRoot: "game",
            socket: Sockets.engine
        });

        var PlayerStatus = SocketioModel.extend({
            urlRoot: "player_status",
            socket: Sockets.playerStatus
        });

        var TableControls =  SocketioModel.extend({
            urlRoot: 'table_controls',
            socket: Sockets.tableControls
        });

        var WagerControls = SocketioModel.extend({
            urlRoot: 'wager_controls',
            socket: Sockets.wagerControls
        });

        return {Seat: Seat,
                Game: Game,
                PlayerStatus: PlayerStatus,
                TableControls: TableControls,
                WagerControls: WagerControls};

    }
); 