/*  views.js
    Main Game Views.
    (c) 2010 - 2014 C. Nicholas Long
*/

define(['require', 'config'],
    function(require, Config) {

        var Views = {};

        // Tricky AMD usage to make the Theme dynamic.
        require(['jquery', 'underscore',  'backbone', Config.themeName],
            function($, _, Backbone, Theme) {
                console.log('did');

                // BaseView Pseudoclass. Inherits from Templating.
                var BaseView = Backbone.View.extend({
                    _render: function(context) {
                        console.log(this);
                        return this.template(_.extend({
                                                Config: Config,
                                                ctx: context || {}
                                            }, this));
                    },
                    constructor: function() {
                        // Make sure this is available to child instances.
                        this.getCardAsset = function(card) {
                            /* Given a `card` string ("KA"), return the card image file
                            name ("ka.png").
                            */
                            var cardFile = join_ext(card.toLowerCase(),
                                                    Theme.cardImageExt);
                            // console.log(join_path(Theme.cardImageFolder, cardFile));
                            return join_path(Theme.cardImageFolder, cardFile);
                        }
                        Backbone.View.apply(this, arguments);
                    }
                });

                // Player Card Views.
                Views.HandView = BaseView.extend({
                    className: "hand",
                    template: Theme.handTemplate
                });

                Views.PlayerView = BaseView.extend({
                    className: "player",
                    template: Theme.playerTemplate,
                    handView: new Views.HandView()
                });

                Views.DealerView = BaseView.extend({
                    className: "dealer",
                    template: Theme.dealerTemplate,
                    handView: new Views.HandView()
                });

                // Status Views.
                Views.TableStatusView = BaseView.extend({
                    template: Theme.tableStatusTemplate,
                    className: "table_status"
                });

                Views.PlayerStatusView = BaseView.extend({
                    template: Theme.playerStatusTemplate,
                    className: "player_status"
                });

                // Controls
                Views.TableControlsView = BaseView.extend({
                    template: Theme.tableControlsTemplate,
                    className: "table_controls"
                });

                Views.WagerControlsView = BaseView.extend({
                    template: Theme.wagerControlsTemplate,
                    className: "wager_controls"
                });

                Views.GameControlsView = BaseView.extend({
                    template: Theme.gameControlsTemplate,
                    className: "game_controls"
                });

                Views.DebugControlsView = BaseView.extend({
                    template: Theme.debugControlsTemplate,
                    className: "debug_controls",
                    events: {
                        "click .debug_pause": "pause",
                        "click .debug_start": "start"
                    },
                    pause: function(ev) {
                        $.ajax({url: ""});
                    },
                    start: function(ev) {
                        $.ajax({url: ""});
                    }
                });

                // Main Game View
                Views.GameView = BaseView.extend({
                    template: Theme.gameTemplate,
                    className: "game",
                    debugControlsView: new Views.DebugControlsView(),
                    dealerView: new Views.DealerView(),
                    playerView: new Views.PlayerView(),
                    tableStatusView: new Views.TableStatusView(),
                    playerStatusView: new Views.PlayerStatusView(),
                    tableControlsView: new Views.TableControlsView(),
                    wagerControlsView: new Views.WagerControlsView(),
                    gameControlsView: new Views.GameControlsView()
                });
            }
        );

        /*
        // Let's get the theme as dictated by the config.
        require([Config.themeName], function(Theme) {
            HandView.prototype.template = Theme.handTemplate;
            PlayerView.prototype.template = Theme.playerTemplate;
            DealerView.prototype.template = Theme.dealerTemplate;
            TableStatusView.prototype.template = Theme.tableStatusTemplate;
            PlayerStatusView.prototype.template = Theme.playerStatusTemplate;
            TableControlsView.prototype.template = Theme.tableControlsTemplate;
            WagerControlsView.prototype.template = Theme.wagerControlsTemplate;
            GameControlsView.prototype.template = Theme.gameControlsTemplate;
            DebugControlsView.prototype.template = Theme.debugControlsTemplate;
            GameView.prototype.template = Theme.gameTemplate;
        });
        */

        return Views;
    }
);