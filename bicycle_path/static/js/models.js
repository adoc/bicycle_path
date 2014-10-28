/* 
    (c) 2010 - 2014 C. Nicholas Long
*/

"use strict";

define(['jquery', 'underscore', 'backbone', 'socketio'],
    function($, _, Backbone, io) {

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


        /* Mimics a very simple Request/Response dynamic through a
        socket.
        */
        function socketRequest(socket, method, data, options) {
            data || (data = {});
            options || (options = {});
            options.timeout || (options.timeout = 10000);
            options.success || (options.success = function () {});
            options.timeoutFail || (options.timeoutFail = function() {
                throw "'socketRequest' expected a response ";
            });

            var self = this,
                syncId = _.uniqueId(method),
                timeoutTimer = setTimeout(options.timeoutFail, options.timeout);

            socket.once("response_"+syncId, function(responseData) {
                clearTimeout(timeoutTimer);
                options.success(responseData);
            });

            // Send the command through the socket.
            socket.emit(method, _.extend({
                    request_id: syncId,
                }, data));
        }

        /* Interesting idea to unify Backbone.Model and socketio
        Several implementations already exist but seem to run in to trouble
        of trying to do "too much".
        */
        var SocketioModel = Backbone.Model.extend({
            constructor: function (attributes, options) {
                options || (options = {});
                if (options.socketio) {
                    this.socketio = options.socketio;
                }
                if (options.controller) {
                    this.controller = options.controller;
                }

                Backbone.Model.apply(this, arguments);
            },
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

                socketRequest(this.socketio, method, {
                    ns: model.url(),
                    id: this.id,
                    data: this.changed
                    }, {
                    success: success
                });

                return;
            }
        });


        var Player = BaseViewModel.extend({
            urlRoot: "player"
        });

        var Game = SocketioModel.extend({
            urlRoot: "game"
        });


        return {Player: Player,
                Game: Game};

    }
); 