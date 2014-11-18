/*  views.js
    Main Game Views.
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['underscore', 'backbone', 'require', 'config', 'models'],
    function(_, Backbone, require, Config, Models) {

        var Views = {};

        // Tricky AMD usage to make the Theme module (Config.themeName) dynamic.
        require([Config.themeModuleName],
            function(Theme) {

                Views.BaseView = Backbone.View.extend({
                    __name__: "BaseView",
                    // TODO: Clean this up.No more extending to
                    //      this.context. Use the models!
                    render: function(context) {
                        // Not sure if this is right. (It wasn't!)
                        // _.extend(this.context, context || {});

                        if (this.template) {
                            this.$el.html(this.template(_.extend({
                                            Config: Config,
                                        }, this)));
                        }
                        return this;
                    },
                    constructor: function(constructorOpts) {
                        var self = this;
                        constructorOpts || (constructorOpts = {});

                        // Extend any constructorOpts in to this view.
                        _.extend(this, constructorOpts);

                        // Build model and pass `constructorOpts` in to it.
                        // Again, crappy and unneeded!
                        if (this.modelClass &&
                                this.modelClass.prototype instanceof Backbone.Model) {
                            this.model = new this.modelClass(null, constructorOpts);
                        } else if (this.modelClass &&
                                this.modelClass.prototype instanceof Backbone.Collection) {
                            this.model = new this.modelClass(null, constructorOpts);
                        }

                        // Build subviews and pass `constructorOpts` in to it.
                        _.each(this.subViews, function(value, key) {
                            self[key] = function (opts) {
                                return new value(_.extend({}, constructorOpts, opts));
                            }
                        });

                        Backbone.View.apply(this, arguments);
                    },
                    initialize: function(opts) {
                        var self = this;
                        opts || (opts = {});

                        if (this.model && this.model instanceof Backbone.Model) {
                            this.model.on("change", function(data) {
                                // Re-render the view on model change.
                                self.render();
                                if (Config.debug === true) {    // Debug Info.
                                    console.log(self.__name__, data.attributes);
                                }
                            });
                        } else if (this.model && this.model instanceof Backbone.Collection) {
                            this.model.on("reset", function(data) {
                                // Re-render the view on model change.
                                self.render();
                                if (Config.debug === true) {    // Debug Info.
                                    console.log(self.__name__, data);
                                }
                            });
                        }

                        // Watch the socket via the model if socket
                        //  enabled.
                        if (this.model &&
                                typeof this.model.watch !== "undefined" && opts.socket_id) {
                            this.model.watch();
                        }
                    }
                });

                /* The Seat View. Includes player "name", "wager" amount,
                "bankroll" and other metadata about the Seat.
                Listens to the model "remove" and "add" events for rendering.
                */
                Views.SeatView = Views.BaseView.extend({
                    __name__: "SeatView",
                    className: "seat",
                    tagName: "div",
                    template: Theme.seatTemplate,
                    modelRemove: function () {
                        this.render();
                    },
                    modelAdd: function () {
                        this.render();
                    },
                    initialize: function() {
                        var self = this;
                        Views.BaseView.prototype.initialize.apply(this,
                                                                  arguments);
                        this.model.on("remove", function() {
                            self.modelRemove();
                        });
                        this.model.on("add", function() {
                            self.modelAdd();
                        });
                    }
                });

                /* All the Seats at this table. Handles instantiation of
                SeatView and percolating model events to it.
                Listens to the model "reset" and "add" events.
                */
                Views.SeatsView = Views.BaseView.extend({
                    __name__: "SeatsView",
                    el: ".seats_wrap",
                    template: Theme.seatsTemplate,
                    modelClass: Models.Seats,
                    subViews: {
                        SeatView: Views.SeatView
                    },
                    seats: [],
                    initialize: function () {
                        var self = this;

                        /* The `Seats` model is reset after the first
                        initiation of the socket namespace. The `SeatViews`
                        are initialized here and the view is rendered.
                        */
                        this.model.on("reset", function (data) {
                            self.seats = [];
                            for (var i=0; i < self.model.length; i++) {
                                var model = self.model.models[i],
                                    seat = new self.SeatView({model: model});
                                seat.model.trigger("add");
                                self.seats.push(seat);
                            }

                            self.render();
                        });

                        /* Percolates the `Seats` model "add" event to the
                        `SeatView`. Reinitialize the `SeatView` to rebind
                        events.
                        */
                        this.model.on("add", function (model) {
                            var idx = self.model.indexOf(model),
                                seat = self.seats[idx];
                            seat.model = model;
                            seat.initialize(); // Re_initialize the seat to re-bind events.
                            seat.model.trigger("add"); // Percolate the "add" event.
                        });

                        this.model.watch();
                    },
                    /* Render the seats.
                    (This should only occur once.)
                    */
                    render: function() {
                        Views.BaseView.prototype.render.apply(this, arguments);
                        for (var i=0; i < this.seats.length; i++) {
                            $(".player_wrap.player_"+i, this.el).html(
                                        this.seats[i].$el);
                        }
                        return this;
                    }
                });

                /*
                */
                Views.HandView = Views.BaseView.extend({
                    __name__: "HandView", // For debug only.
                    className: "hand",
                    tagName: "div",
                    template: Theme.handTemplate
                });

                Views.DealerView = Views.BaseView.extend({
                    __name__: "DealerView",
                    className: "dealer",
                    tagName: "div",
                    template: Theme.dealerTemplate,
                    modelClass: Models.Dealer,
                    subViews: {
                        HandView: Views.HandView
                    },
                    initialize: function () {
                        var self = this;
                        Views.BaseView.prototype.initialize.apply(this, arguments);

                        console.log(this.model);

                        this.handView = new this.HandView({model: this.model});

                        /*
                        this.model.on("reset", function(data) {
                            console.log("DealerView reset");
                        });
                        */

                        // TODO: There must be a way to abstract this,
                        //  but this is fine for now.
                        // Update subview model.
                        this.model.on("change", function(data) {
                            //self.handView.model.reset(data.attributes.hand);
                            console.log("DealerView change");
                            self.render();
                        });

                    },
                    render: function() {
                        Views.BaseView.prototype.render.apply(this, arguments);
                        this.$el.append(this.handView.$el);
                        return this;
                    }
                });

                Views.HandsView = Views.BaseView.extend({
                    el: ".seats_wrap",
                    modelClass: Models.Hands,
                    subViews: {
                        HandView: Views.HandView
                    },
                    hands: [],
                    initialize: function () {
                        var self = this;

                        this.model.on("reset", function (data) {
                            for (var i=0; i < self.model.length; i++) {
                                var model = self.model.models[i], // `Hand` Model.
                                    hand = new self.HandView({model: model});
                                hand.model.trigger("change");
                                self.hands.push(hand);
                            }
                            self.render();
                        });

                        this.model.watch();
                    },
                    render: function () {
                        for (var i=0; i < this.hands.length; i++) {
                            $(".player_wrap.player_"+i, this.el).append(
                                        this.hands[i].$el);
                        }
                        return this;
                    }
                });

                Views.PlayerStatusView = Views.BaseView.extend({
                    __name__: "PlayerStatusView",
                    template: Theme.playerStatusTemplate,
                    className: "player_status",
                    modelClass: Models.PlayerStatus,
                    initialize: function () {
                        var self = this;

                        this.model.watch();

                        this.model.on("change", function(data) {
                            self.render(data.attributes);
                        });
                    }
                });

                Views.TableStatusView = Views.BaseView.extend({
                    __name__: "TableStatusView",
                    template: Theme.tableStatusTemplate,
                    className: "table_status",
                    tagName: "div",
                    modelClass: Models.TableStatus,
                    countDown: function() {},
                    initialize: function() {
                        var self = this;
                        Views.BaseView.prototype.initialize.apply(this, arguments);

                        this.model.on("change", function(data) {
                            clearInterval(self.countDown);
                            self.countDown = simple_countdown({
                                timeout: self.model.get("timeout"),
                                tick: function(timeout) {
                                    self.model.set("timeout", timeout);
                                },
                                done: function() {
                                    clearInterval(self.countDown);
                                }
                            });
                        });
                    }
                });

                Views.TableControlsView = Views.BaseView.extend({
                    __name__: "TableControlsView",
                    template: Theme.tableControlsTemplate,
                    className: "table_controls",
                    tagName: "div",
                    events: {
                        "click .table_sit": "sit",
                        "click .table_leave": "leave",
                        "click .table_leave_cancel": "sit"
                    },
                    modelClass: Models.TableControls,
                    sit: function(ev) {
                        var self = this;

                        this.model.request("sit", {
                            data: {
                                name: $("input[name='name']", this.$el).val()
                            },
                            success: function(data) {
                                self.render({
                                            in_game: data,
                                        });
                            }
                        });

                        return false;
                    },
                    leave: function(ev) {
                        var self = this;

                        this.model.request("leave", {
                            success: function(data) {
                                self.render({in_game: !data});
                            }
                        });

                        return false;
                    }
                });

                Views.WagerControlsView = Views.BaseView.extend({
                    __name__: "WagerControlsView",
                    template: Theme.wagerControlsTemplate,
                    modelClass: Models.WagerControls,
                    className: "wager_controls", // This needs to be abstracted!
                    tagName: "ul", // This needs to be abstracted!
                    events: {
                        "click .wager": "wager",
                        "click .wager_clear": "clear"
                    },
                    wager: function(ev) {
                        var self=this,
                            amount = parseInt(
                                        ev.target.getAttribute('data-amount'));

                        this.model.request("wager", {
                            data: {
                                amount: amount
                            }
                        });

                        return false;
                    },
                    clear: function(ev) {
                        var self=this;
                        this.model.request("clear", {
                            success: function(data) {
                                self.render(data);
                            }
                        });

                        return false;
                    }
                });

                // blackjack game to be abstracted later.
                Views.GameControlsView = Views.BaseView.extend({
                    __name__: "GameControlsView",
                    template: Theme.gameControlsTemplate,
                    className: "game_controls", // This needs to be abstracted!
                    tagName: "ul", // This needs to be abstracted!
                    modelClass: Models.GameControls,
                    events: {
                        "click .game_hit": "hit",
                        "click .game_stand": "stand",
                        "click .game_double": "double",
                        "click .game_split": "split",
                        "click .game_surrender": "surrender"
                    },
                    /*
                    render: function() {
                        if (this.model.get("show") === true) {
                            Views.BaseView.prototype.render.apply(this, arguments);
                        } else {
                            this.$el.html("");
                        }
                    },
                    */
                    hit: function(ev) {
                        this.model.request("hit");
                        return false;
                    },
                    double: function(ev) {
                        this.model.request("double");
                        return false;
                    },
                    stand: function(ev) {
                        this.model.request("stand");
                        return false;
                    }
                });

                Views.DebugControlsView = Views.BaseView.extend({
                    __name__: "DebugControlsView",
                    template: Theme.debugControlsTemplate,
                    className: "debug_controls",
                    tagName: "div",
                    modelClass: Models.DebugControls,
                    events: {
                        "click .debug_pause": "pause",
                        "click .debug_start": "start"
                    },
                    pause: function(ev) {
                        var self = this;
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('pause'),
                            success: function(data) {
                                self.context.paused = data;
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`pause` error!");
                            }
                        });

                        return false;
                    },
                    start: function(ev) {
                        var self = this;
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('start'),
                            success: function(data) {
                                self.context.paused = !data;
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`start` error!");
                            }
                        });

                        return false;
                    }
                });

                Views.GameView = Views.BaseView.extend({
                    __name__: "GameView",
                    template: Theme.gameTemplate,
                    className: "game",
                    subViews: {
                        TableStatusView: Views.TableStatusView,
                        PlayerStatusView: Views.PlayerStatusView,
                        DealerView: Views.DealerView,
                        SeatsView: Views.SeatsView,
                        HandsView: Views.HandsView,
                        DebugControlsView: Views.DebugControlsView,
                        TableControlsView: Views.TableControlsView,
                        WagerControlsView: Views.WagerControlsView,
                        GameControlsView: Views.GameControlsView
                    },
                    initialize: function () {
                        this.tableStatusView = new this.TableStatusView();
                        this.playerStatusView = new this.PlayerStatusView();
                        this.dealerView = new this.DealerView();
                        this.seatsView = new this.SeatsView();
                        this.handsView = new this.HandsView();
                        this.debugControlsView = new this.DebugControlsView();
                        this.tableControlsView = new this.TableControlsView();
                        this.wagerControlsView = new this.WagerControlsView();
                        this.gameControlsView = new this.GameControlsView();
                    },
                    render: function() {
                        Views.BaseView.prototype.render.apply(this, arguments);

                        $(".player_status_wrap", this.$el).html(
                                    this.playerStatusView.$el);

                        $(".dealer_wrap", this.$el).html(
                                    this.dealerView.$el);

                        $(".table_status_wrap", this.$el).html(
                                    this.tableStatusView.$el);

                        $(".seats_wrap", this.$el).html(this.seatsView.$el);

                        $(".seats_wrap", this.$el).append(this.handsView.$el);

                        var $controls = $(".controls", this.$el);
                        $controls.html("");
                        $controls.append(this.debugControlsView.$el);
                        $controls.append(this.tableControlsView.$el);
                        $controls.append(this.wagerControlsView.$el);
                        $controls.append(this.gameControlsView.$el);

                        return this;
                    }
                });
            }
        );

        return Views;
    }
);