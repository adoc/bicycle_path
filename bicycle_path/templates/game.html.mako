## Mako template for the main game page.
<%inherit file="root.html.mako" />
<div class="container">
<%doc>
    <div class="jumbotron">
        <div class="page-header"><h1>Table Games</h1></div>
        <h2>Just a temporary Alpha testing site for Coda's Card Game Engine.</h2>
        <p><a href="#table1" class="btn btn-primary btn-lg" role="button">Go Play! &raquo;</a></p>
        <br />
        <div class="page-header"><h2>FAQ</h2></div>
        <p><strong>Is this working and without bugs?</strong></p>
        <p>Absolutely not! This is most likely not working and chock full of bugs!</p>
        <br />
        <p><strong>Will you remember my winnings?</strong></p>
        <p>No way! And to reset your losses, just clear your cookies!</p>
        <br />
        <p><strong>Hey I was in the middle of a game and everything reset! WTF?</strong></p>
        <p>We know! This is called "development".</p>
        <br />
        <p><strong>Hey this is pretty cool! Will this be released?</strong></p>
        <p>Yup! That's the plan.</p>
        <br />
        <div class="page-header"><h2>Thank You</h2></div>
        <p>Please continue to enjoy this completely free and no hassle game! :P</p>
        <br />
        <p><a href="#table1" class="btn btn-primary btn-lg" role="button">Go Play! &raquo;</a></p>
    </div>
</%doc>
##  The game table will be loaded from it's own template and placed in to this div.

    <div id="bj1" class="game_table" data-id=""></div>

</div>
##  Just a temporary empty footer.
<div style="min-height: 14px" class="container"></div>
##  Hook script for this page. This will most likely no longer be the entry point once this project matures.
<%def name="style()">
    <link rel="stylesheet" href="${request.static_url('bicycle_path:static/theming/base/game.css')}">
</%def>
<%def name="scripts()">
    <script type="text/javascript">
    "use strict";

    /* Front End Entry Point. */
    require(['jquery', 'backbone_socketio', 'config', 'models', 'views', 'sockets'],
        function ($, BackboneSocketio, Config, Models, Views, Sockets) {

            // AMD Trick to ensure the theme module is loaded before instantiating the game.
            require([Config.themeModuleName], 
                function(Theme) {

                    // Get engine list.
                    BackboneSocketio.socketRequest(Sockets.engine, "list", {}, {
                        success: function (data) {
                            var engine_id = data[0]; // First available engine (game) for now.

                            /*
                            window.g1 = new Views.GameView({
                                model_id: engine_id
                            });
                            $("#bj1").append(g1.$el);

                            window.table_controls = new Views.TableControlsView({
                                model_id: engine_id
                            });
                            $("#bj1").append(table_controls.$el);

                            window.wager_controls = new Views.WagerControlsView({
                                model_id: engine_id
                            });
                            $("#bj1").append(wager_controls.$el);

                            window.dealer = new Views.DealerView({
                                model_id: engine_id
                            });
                            $("#bj1").append(dealer.$el);
                            */

                            var seats = new Views.SeatsView();
                            $("#bj1").append(seats.$el);
                            $("#bj1").append("<br />");

                            seats.model.reset([{
                                                    hand: ["AS"],
                                                    wager: {
                                                        amount: 0
                                                    },
                                                    hand_total: 0
                                            }, {
                                                    hand: ["ks", "2c"],
                                                    wager: {
                                                        amount: 0
                                                    },
                                                    hand_total: 0
                                            }]);

                            
                            //seats.render();

                            //console.log(seats.model);

                        }
                    });

                }
            );
        }
    );
    </script>
</%def>