/*  views.js
    Main Game Views.
    (c) 2010 - 2014 C. Nicholas Long
*/


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
                        // Possibly removing this.
                        /*
                        _.each(this.subviews, function(value, key) {
                            self[key] = new value(opts);
                        });
                        */

                        if (this.modelClass) {
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
                    template: Theme.handTemplate
                });

                Views.PlayerView = BaseView.extend({
                    className: "player",
                    tagName: "div",
                    template: Theme.playerTemplate,
                    modelClass: Model.Player,
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        var handView = new Views.HandView({controller: this.controller});
                        this.$el.append(handView.render());
                        return this;
                    }
                });

                Views.DealerView = BaseView.extend({
                    className: "dealer",
                    tagName: "div",
                    template: Theme.dealerTemplate,
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        var handView = new Views.HandView({controller: this.controller});
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
                    className: "player_status"
                });

                // Controls
                Views.TableControlsView = BaseView.extend({
                    template: Theme.tableControlsTemplate,
                    className: "table_controls",
                    tagName: "div",
                    events: {
                        "click .table_sit": "sit",
                        "click .table_leave": "leave"
                    },
                    sit: function(ev) {
                        var self = this;



                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('sit'),
                            success: function(data) {
                                //this.context.in_game = data;
                                //self.trigger('update_context');

                                self.render({in_game: data});
                            },
                            error: function() {
                                console.log("`sit` error!");
                            }
                        });

                        return false;
                    },
                    leave: function(ev) {
                        var self = this;

                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('leave'),
                            success: function(data) {
                                this.context.in_game = !data;
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`leave` error!");
                            }
                        });

                        return false;
                    }
                });

                Views.WagerControlsView = BaseView.extend({
                    template: Theme.wagerControlsTemplate,
                    className: "wager_controls", // This needs to be abstracted!
                    tagName: "ul", // This needs to be abstracted!
                    events: {
                        "click .wager": "wager",
                        "click .wager_reset": "wager_reset"
                    },
                    wager: function(ev) {
                        var amount = parseInt(
                                        ev.target.getAttribute('data-amount'));
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('wager'),
                            data: {amount: amount},
                            success: function(data) {
                                console.log('wager', data);
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`wager` error!");
                            }
                        });

                        return false;
                    },
                    wager_reset: function(ev) {
                        // All these Ajax calls can be wrapped.
                        $.ajax({
                            url: this.controller.url('wager_reset'),
                            success: function(data) {
                                console.log('wager_reset', data);
                                self.trigger('update_context');
                            },
                            error: function() {
                                console.log("`wager_reset` error!");
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
                    render: function(context) {
                        BaseView.prototype.render.apply(this, arguments);
                        context = _.extend(context || {}, this.model.attributes);

                        // Render Dealer and Table Status.
                        var dealerView = new Views.DealerView({controller: this.controller}),
                            tableStatusView = new Views.TableStatusView({controller: this.controller});
                        $(".dealer_wrap", this.$el).append(dealerView.render(context.dealer).$el);
                        $(".table_status_wrap", this.$el).append(tableStatusView.render(context).$el);

                        // Render Players.
                        for (var i=0; i < context.seats.length; i++) {
                            var playerView = new Views.PlayerView({controller: this.controller});
                            $(".player_"+i+"_wrap", this.$el).append(
                                    playerView.render(context.seats[i]).$el);
                        }

                        // Construct controls subviews.
                        var controlsEl = $(".controls", this.$el),
                            debugControlsView = new Views.DebugControlsView({controller: this.controller}),
                            tableControlsView = new Views.TableControlsView({controller: this.controller});
                        controlsEl.append(debugControlsView.render().$el);
                        controlsEl.append(tableControlsView.render().$el);

                        var current_player = context.seats[context.current_player || 0];

                        var playerStatusView = new Views.PlayerStatusView({controller: this.controller});
                        controlsEl.append(playerStatusView.render(current_player).$el);

                        if (context.in_game === true &&
                                context.accept_wager === true) {
                            var wagerControlsView = new Views.WagerControlsView({controller: this.controller});
                            controlsEl.append(wagerControlsView.render(current_player.wager).$el);
                        }

                        if (current_player) {
                            var gameControlsView = new Views.GameControlsView({controller: this.controller});
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