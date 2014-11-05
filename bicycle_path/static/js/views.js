/*  views.js
    Main Game Views.
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['require', 'config', 'models'],
    function(require, Config, Models) {

        var Views = {};

        // Tricky AMD usage to make the Theme (Config.themeName) dynamic.
        require(['underscore', 'backbone', Config.themeModuleName],
            function(_, Backbone, Theme) {

                var BaseView = Backbone.View.extend({
                    __name__: "BaseView",
                    // TODO: Clean this up.No more extending to
                    //      this.context. Use the models!
                    render: function(context) {
                        // Not sure if this is right. (It wasn't!)
                        // _.extend(this.context, context || {});

                        var page = this.template(_.extend({
                                                Config: Config,
                                                // ctx: this.context
                                            }, this));

                        this.$el.html(page);
                        return this;
                    },
                    // Fetch and render.
                    // TODO: Should be deprecated.
                    /*
                    update: function(callback) {
                        var self = this;
                        this.model.fetch({
                            success: function() {
                                // Extend the model attributes in to the
                                //  view context.
                                _.extend(self.context, self.model.attributes);
                                self.render();
                                if (callback) {
                                    callback();
                                }
                            }
                        });
                    },
                    */
                    initialize: function() {
                        var self = this;

                        if (this.model instanceof Backbone.Model) {
                            this.model.on("change", function(data) {
                                // Re-render the view on model change.
                                self.render();
                                if (Config.debug === true) {    // Debug Info.
                                    console.log(self.__name__, data.attributes);
                                }
                            });
                        } else if (this.model instanceof Backbone.Collection) {
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
                        if (this.model.hasOwnProperty("watch")) {
                            this.model.watch();
                        }
                    },
                    constructor: function(opts) {
                        var self = this;
                        opts || (opts = {});

                        // Extend any opts in to this view.
                        _.extend(this, opts);

                        // Build model and pass `opts` in to it.
                        // Again, crappy and unneeded!
                        this.model = new this.modelClass({}, opts);

                        // Build subviews and pass `opts` in to it.
                        _.each(this.subViews, function(value, key) {
                            self[key] = function () {
                                //opts.model = self.model; // SubViews
                                return new value(opts);
                            }
                        });

                        // Make sure this is available to child instances.
                        this.getCardAsset = function(card) {
                            /* Given a `card` string ("KA"), return the card image file
                            name ("ka.png"). */
                            var cardFile = join_ext(card.toLowerCase(),
                                                    Theme.cardImageExt);
                            return join_path(Theme.cardImageFolder, cardFile);
                        }

                        Backbone.View.apply(this, arguments);
                    }
                });

                Views.HandView = BaseView.extend({
                    __name__: "HandView", // For debug only.
                    className: "hand",
                    tagName: "div",
                    template: Theme.handTemplate,
                    modelClass: Models.Hand
                });

                Views.DealerView = BaseView.extend({
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
                        BaseView.prototype.initialize.apply(this, arguments);
                        this.handView = new this.HandView();

                        // TODO: There must be a way to abstract this,
                        //  but this is fine for now.
                        // Update subview model.
                        this.model.on("change", function(data) {
                            self.handView.model.reset(data.attributes.hand);
                        });
                    },
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        this.$el.append(this.handView.$el);
                        return this;
                    }
                });

                Views.SingleSeatView = BaseView.extend({
                    __name__: "SingleSeatView",
                    className: "seat",
                    tagName: "div",
                    template: Theme.seatTemplate,
                    modelClass: Models.Seat,
                    subViews: {
                        HandView: Views.HandView
                    },
                    initialize: function() {
                        var self = this;
                        BaseView.prototype.initialize.apply(this, arguments);
                        this.handView = new this.HandView();

                        // TODO: There must be a way to abstract this,
                        //  but this is fine for now.
                        // Update subview model.
                        this.model.on("change", function(data) {
                            self.handView.model.reset(data.attributes.hand);
                        });
                    },
                    render: function(context) {
                        context || (context={
                                            wager: {
                                                amount: 0
                                            },
                                            hand_total: 0
                                        });

                        BaseView.prototype.render.apply(this, arguments);
                        this.$el.append(this.handView.$el);
                        return this;
                    }
                });

                Views.SeatsView = BaseView.extend({
                    __name__: "SeatsView",
                    modelClass: Models.Seats,
                    subViews: {
                        SingleSeatView: Views.SingleSeatView
                    },
                    initialize: function () {
                        var self = this;
                        this.model.on("change", function (data) {
                            console.log("SeatsView Change", data.attributes);
                            self.render(data.attributes);
                        });
                        this.model.watch();
                    },
                    render: function(context) {
                        for (var i=0; i < context.seats.length; i++) {
                            var seatView = new this.SingleSeatView();
                            $(".player_"+i+"_wrap", this.el).html(
                                    seatView.render(context.seats[i]).$el);
                        }
                        return this;
                    }
                });

                // Status Views.
                Views.TableStatusView = BaseView.extend({
                    __name__: "TableStatusView",
                    template: Theme.tableStatusTemplate,
                    className: "table_status",
                    tagName: "div"
                });

                Views.PlayerStatusView = BaseView.extend({
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

                // Controls
                Views.TableControlsView = BaseView.extend({
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
                    initialize: function () {
                        var self = this;
                        this.model.on("change", function(data) {
                            console.log("TableControlsView Change",
                                        data.attributes);
                            self.render(data.attributes);
                        });
                        this.model.watch();
                    },
                    sit: function(ev) {
                        var self = this;

                        this.model.request("sit", {
                            success: function(data) {
                                self.render({in_game: data});
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

                Views.WagerControlsView = BaseView.extend({
                    __name__: "WagerControlsView",
                    template: Theme.wagerControlsTemplate,
                    modelClass: Models.WagerControls,
                    className: "wager_controls", // This needs to be abstracted!
                    tagName: "ul", // This needs to be abstracted!
                    events: {
                        "click .wager": "wager",
                        "click .wager_clear": "clear"
                    },
                    context: {
                        wager: {
                            amount: 0
                        }
                    },
                    initialize: function () {
                        var self = this;

                        this.model.watch();

                        this.model.on("change", function(data) {
                            console.log("WagerControlsView Change", data.attributes);

                            self.render(data.attributes);
                        });
                    },
                    wager: function(ev) {
                        var self=this,
                            amount = parseInt(
                                        ev.target.getAttribute('data-amount'));

                        this.model.request("wager", {
                            data: {
                                amount: amount
                            },
                            success: function(data) {
                                self.render(data);
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
                Views.GameControlsView = BaseView.extend({
                    __name__: "GameControlsView",
                    template: Theme.gameControlsTemplate,
                    className: "game_controls", // This needs to be abstracted!
                    tagName: "ul", // This needs to be abstracted!
                    events: {
                        "click .game_hit": "hit",
                        "click .game_stand": "stand",
                        "click .game_double": "double",
                        "click .game_split": "split",
                        "click .game_surrender": "surrender"
                    },
                    hit: function(ev) {
                        var self = this;
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('hit'),
                            success: function(data) {
                                console.log('hit', data);
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`hit` error!");
                            }
                        });

                        return false;
                    },
                    double: function(ev) {
                        var self = this;
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('double'),
                            success: function(data) {
                                console.log('double', data);
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`double` error!");
                            }
                        });

                        return false;
                    },
                    stand: function(ev) {
                        var self = this;
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('stand'),
                            success: function(data) {
                                console.log('stand', data);
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`stand` error!");
                            }
                        });

                        return false;
                    }
                });

                Views.DebugControlsView = BaseView.extend({
                    __name__: "DebugControlsView",
                    template: Theme.debugControlsTemplate,
                    className: "debug_controls",
                    tagName: "div",
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

                // Main Game View
                /*
                this has to be reworked. game state changes should no re-render
                the entire thing.
                */
                Views.GameView = BaseView.extend({
                    __name__: "GameView",
                    template: Theme.gameTemplate,
                    className: "game",
                    modelClass: Models.Game,
                    subViews: {
                        DealerView: Views.DealerView,
                        TableStatusView: Views.TableStatusView,
                        SeatsView: Views.SeatsView,
                        DebugControlsView: Views.DebugControlsView,
                        TableControlsView: Views.TableControlsView,
                        PlayerStatusView: Views.PlayerStatusView,
                        WagerControlsView: Views.WagerControlsView,
                        GameControlsView: Views.GameControlsView
                    },
                    initialize: function () {
                        var self = this;
                        // Simply update the view when the model changes.
                        /* This is very basic and will need to be expanded to
                        include animations and other datasets from the engine.*/
                        
                        this.model.on("change", function(data) {
                            self.render(data.attributes);
                        });

                        this.model.watch();

                        this.dealerView = new this.DealerView();
                        this.tableStatusView = new this.TableStatusView();

                    },
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        context = _.extend(context || {}, this.model.attributes);

                        // Render Dealer and Table Status.
                        //var dealerView = new this.DealerView(),
                        //    tableStatusView = new this.TableStatusView();

                        $(".dealer_wrap", this.$el).append(
                                    this.dealerView.render(context.dealer).$el);
                        $(".table_status_wrap", this.$el).append(
                                    this.tableStatusView.render(context).$el);

                        // Render Players.
                        /*
                        for (var i=0; i < context.seats.length; i++) {
                            var seatView = new this.SeatsView();
                            $(".player_"+i+"_wrap", this.$el).append(
                                    seatView.render(context.seats[i]).$el);
                        }*/
                        var seatsView = new this.SeatsView();

                        //console.log(this.el);
                        seatsView.el = this.el;
                        //seatsView.render(context.seats);

                        // Construct controls subviews.
                        var controlsEl = $(".controls", this.$el),
                            debugControlsView = new this.DebugControlsView(),
                            tableControlsView = new this.TableControlsView();

                        controlsEl.append(debugControlsView.render().$el);
                        controlsEl.append(tableControlsView.render().$el);

                        var current_player = context.seats[context.current_player || 0];

                        var playerStatusView = new this.PlayerStatusView();
                        controlsEl.append(playerStatusView.render(current_player).$el);

                        /*
                        if (context.in_game === true &&
                                context.accept_wager === true) {
                            var wagerControlsView = new this.WagerControlsView();
                            controlsEl.append(wagerControlsView.render(current_player.wager).$el);
                        }*/

                        var wagerControlsView = new this.WagerControlsView();
                        controlsEl.append(wagerControlsView.render().$el);


                        if (current_player) {
                            var gameControlsView = new this.GameControlsView();
                            controlsEl.append(gameControlsView.render().$el);
                        }
                        return this;
                    }
                });
            }
        );

        return Views;
    }
);