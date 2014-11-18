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

    <div id="bj1" class="game_table" data-id="">

##      Temporary
        <div class="seats_wrap"></div>
        <div class="clearfix"></div>

    </div>

</div>
##  Just a temporary empty footer.
<div style="min-height: 14px" class="container"></div>

## Temp rotation/"deal" test.
## <div id="rotateme" style="position: absolute; top: 100px; left: 100px;" class="card _2c"></div>

##  Hook script for this page. This will most likely no longer be the entry point once this project matures.
<%def name="style()">
    <link rel="stylesheet" href="${request.static_url('bicycle_path:static/theming/base/game.css')}">
    <link rel="stylesheet" href="${request.static_url('bicycle_path:static/theming/base/cards.bicycle.css')}">
</%def>
<%def name="scripts()">
    <script type="text/javascript">
    "use strict";

    /* Front End Entry Point. */
    require(['jquery', 'backbone_socketio', 'config', 'models', 'views', 'animated_views', 'sockets', 'animations'],
        function ($, BackboneSocketio, Config, Models, Views, AnimatedViews, Sockets) {

            // setTimeout(function() {$("#rotateme").dealCardTo({x: 500, y:500, done: function() {console.log("ani done")}});}, 1000);


            // Tricky AMD usage to make the Theme module (Config.themeName) dynamic.
            require([Config.themeModuleName], 
                function(Theme) {

                    // Get engine list.
                    BackboneSocketio.socketRequest(Sockets.engine, "list", {}, {
                        success: function (data) {
                            var engine_id = data[0]; // First available engine (game) for now.


                            var game = new Views.GameView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(game.$el);
                            game.render();

                            /*
                            var table_status = new Views.TableStatusView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(table_status.$el);

                            var dealer = new Views.DealerView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(dealer.$el);

                            var seats = new AnimatedViews.SeatsView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(seats.$el);

                            var hands = new Views.HandsView({
                                socket_id: engine_id
                            });

                            var table_controls = new Views.TableControlsView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(table_controls.$el);

                            var wager_controls = new Views.WagerControlsView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(wager_controls.$el);

                            var game_controls = new Views.GameControlsView({
                                socket_id: engine_id
                            });
                            $("#bj1").append(game_controls.$el);
                            */

                        }
                    });

                }
            );

        }
    );
    </script>
</%def>