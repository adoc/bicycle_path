/*  views.js
    Main Game Views.
    (c) 2010 - 2014 C. Nicholas Long
*/


define(['underscore', 'config', 'templating'],
    function(_, Config, Templating) {

        // BaseView Pseudoclass. Inherits from Templating.
        var BaseView = function(opts) {
            _.extend(this, {
            }, opts || {});
            return this;
        };
        BaseView.prototype = new Templating();

        // Base Game Views.
        var HandView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.handTemplate
            }, opts || {});
            return this;
        };
        HandView.prototype = new BaseView();

        var PlayerView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.playerTemplate,
                handView: new HandView();
            }, opts || {});
            return this;
        };
        PlayerView.prototype = new BaseView();

        var DealerView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.dealerTemplate,
                handView: new HandView();
            }, opts || {});
            return this;
        };
        DealerView.prototype = new BaseView();

        var TableStatusView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.tableStatusTemplate
            }, opts || {});
            return this;
        };
        tableStatusView.prototype = new BaseView();

        var PlayerStatusView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.playerStatusTemplate
            }, opts || {});
            return this;
        };
        PlayerStatusView.prototype = new BaseView();


        // Controls
        var TableControlsView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.tableControlsTemplate
            }, opts || {});
            return this;
        };
        TableControlsView.prototype = new BaseView();

        var WagerControlsView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.wagerControlsTemplate
            }, opts || {});
            return this;
        };
        WagerControlsView.prototype = new BaseView();

        var GameControlsView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.gameControlsTemplate
            }, opts || {});
            return this;
        }
        GameControlsView.prototype = new BaseView();

        var DebugControlsView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.debugControlsTemplate
            }, opts || {});
            return this;
        };
        DebugControlsView.prototype = new BaseView();


        // Main Game View
        var GameView = function(opts) {
            _.extend(this, {
                _templateString: Config.Theme.gameTemplate,
                debugControlsView: new DebugControlsView(),
                dealerView: new DealerView(),
                playerView: new PlayerView(),
                tableStatusView: new TableStatusView(),
                playerStatusView: new PlayerStatusView(),
                tableControlsView: new TableControlsView(),
                wagerControlsView: new WagerControlsView(),
                gameControlsView: new GameControlsView()
            }, opts || {});
            return this;
        };
        GameView.prototype = new BaseView();

        return {
            HandView: HandView,
            PlayerView: PlayerView,
            DealerView: DealerView,
            TableStatusView: TableStatusView,
            PlayerStatusView: PlayerStatusView,
            TableControlsView: TableControlsView,
            WagerControlsView: WagerControlsView,
            GameControlsView: GameControlsView,
            DebugControlsView: DebugControlsView,
            GameView: GameView
        };

    }
);