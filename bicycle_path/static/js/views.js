/*  views.js
    Main Game Views.
    (c) 2010 - 2014 C. Nicholas Long
*/

"use strict";

define(['require', 'config', 'models'],
    function(require, Config, Model) {

        var Views = {};

        // Tricky AMD usage to make the Theme (Config.themeName) dynamic.
        require(['jquery', 'underscore',  'backbone', Config.themeModuleName],
            function($, _, Backbone, Theme) {

                var BaseView = Backbone.View.extend({
                    context: {},
                    render: function(context) {
                        // Not sure if this is right.
                        _.extend(this.context, context || {});

                        var page = this.template(_.extend({
                                                Config: Config,
                                                ctx: this.context
                                            }, this));

                        this.$el.html(page);
                        return this;
                    },
                    // Fetch and render.
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
                    initialize: function() {
                        this.on("update_context", function(ev) {
                            this.render();
                        });
                    },
                    constructor: function(opts) {
                        var self = this,
                            args = arguments;

                        // Extend any opts in to this view.
                        _.extend(this, opts);

                        // Build subviews and pass `opts` in to it.
                        _.each(this.subViews, function(value, key) {
                            self[key] = function () {
                                return new value(opts);
                            }
                        });

                        // Build model and pass `opts` in to it.
                        if (this.modelClass) {
                            // console.log(this);
                            this.model = new this.modelClass({}, opts);
                        }

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

                // Player Card Views.
                Views.HandView = BaseView.extend({
                    className: "hand",
                    tagName: "div",
                    context: [],
                    template: Theme.handTemplate
                });

                Views.SeatView = BaseView.extend({
                    className: "seat",
                    tagName: "div",
                    template: Theme.seatTemplate,
                    modelClass: Model.Seat,
                    subViews: {
                        HandView: Views.HandView
                    },
                    context: {
                        wager: {
                            amount: 0
                        },
                        hand_total: 0
                    },
                    render: function(context) {
                        // console.log("PlayerView context", context);
                        BaseView.prototype.render.apply(this, arguments);

                        var handView = new this.HandView();
                        this.$el.append(handView.render());
                        return this;
                    }
                });

                Views.DealerView = BaseView.extend({
                    className: "dealer",
                    tagName: "div",
                    template: Theme.dealerTemplate,
                    modelClass: Model.Dealer,
                    subViews: {
                        HandView: Views.HandView
                    },
                    initialize: function () {

                    },
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        var handView = new this.HandView();
                        this.$el.append(handView.render());
                        return this;
                    }
                });

                // Status Views.
                Views.TableStatusView = BaseView.extend({
                    template: Theme.tableStatusTemplate,
                    className: "table_status",
                    tagName: "div"
                });

                Views.PlayerStatusView = BaseView.extend({
                    template: Theme.playerStatusTemplate,
                    className: "player_status",
                    modelClass: Model.PlayerStatus,
                    initialize: function () {
                        var self = this;

                        this.model.watch();

                        this.model.on("change", function(data) {
                            // console.log("TableControlsView Change", data.attributes);
                            self.render(data.attributes);
                        });
                    }
                });

                // Controls
                Views.TableControlsView = BaseView.extend({
                    template: Theme.tableControlsTemplate,
                    className: "table_controls",
                    tagName: "div",
                    events: {
                        "click .table_sit": "sit",
                        "click .table_leave": "leave",
                        "click .table_leave_cancel": "sit"
                    },
                    modelClass: Model.TableControls,
                    initialize: function () {
                        var self = this;

                        this.model.watch();

                        this.model.on("change", function(data) {
                            // console.log("TableControlsView Change", data.attributes);
                            self.render(data.attributes);
                        });
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
                    template: Theme.wagerControlsTemplate,
                    modelClass: Model.WagerControls,
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
                Views.GameView = BaseView.extend({
                    template: Theme.gameTemplate,
                    className: "game",
                    modelClass: Model.Game,
                    subViews: {
                        DealerView: Views.DealerView,
                        TableStatusView: Views.TableStatusView,
                        SeatView: Views.SeatView,
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
                    },
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        context = _.extend(context || {}, this.model.attributes);

                        // Render Dealer and Table Status.
                        var dealerView = new this.DealerView(),
                            tableStatusView = new this.TableStatusView();

                        $(".dealer_wrap", this.$el).append(dealerView.render(context.dealer).$el);
                        $(".table_status_wrap", this.$el).append(tableStatusView.render(context).$el);

                        // Render Players.
                        for (var i=0; i < context.seats.length; i++) {
                            var playerView = new this.SeatView();
                            $(".player_"+i+"_wrap", this.$el).append(
                                    playerView.render(context.seats[i]).$el);
                        }

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