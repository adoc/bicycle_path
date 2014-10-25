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
    </div>

</div>
##  Just a temporary empty footer.
<div style="min-height: 14px" class="container"></div>
##  Hook script for this page. This will most likely no longer be the entry point once this project matures.
<%def name="style()">
    <link rel="stylesheet" href="${request.static_url('bicycle_path:static/theming/base/game.css')}">
</%def>
<%def name="scripts()">
    <script type="text/javascript">
    /* Front End Entry Point. */
    require(['jquery', 'config', 'models', 'views', 'controllers', 'socketio'],
        function ($, Config, Models, Views, Controllers, io) {
            require([Config.themeModuleName, 'blackjack'], 
                function(Theme, blackjack) {

                    // Just a hack to get the engine id.
                    apiWrapper('/api/v1/engines', 
                        function(data) {
                            var engine_id = data[0]; // First available engine

                            // Need to figure out a way to abstract the engine url in to all the actions.
                            // It doesn't work like a traditional backbone model, but we need to find
                            // the best hack to make it happen.
                            e1 = new Controllers.Engine({"id": engine_id});

                            g1 = new Views.GameView({"controller": e1});

                            // g1.update(function() { $("#bj1").append(g1.$el); });
                            $("#bj1").append(g1.$el);


                            // m1 = new Models.Game({"controller": e1});
                            // console.log(m1.url());

                            /*
                            p1 = new Views.PlayerView({"controller": e1});
                            p1.update();
                             $("#bj1").append(p1.$el);
                            debugView = new Views.DebugControlsView({"controller": e1});
                            $("#bj1").append(debugView.render().$el);
                            playerModel = new Models.PlayerModel({"controller": e1});
                            console.log(playerModel.url());
                            */
                            // console.log('', e1.url('sock'));


                            var engineSock = io.connect('/engine', {resource: 'api/v1/sock'});

                            $(window).bind("beforeunload", function() {
                                engineSock.disconnect();
                            });

                            engineSock.on('disconnect', function() {
                                console.log("DISCONNECT");
                            });

                            engineSock.on('pulse', function(d) {
                                console.log(d);
                            });

                            engineSock.emit('join', engine_id);

                        },
                        function() { console.error("404"); },
                        function() { console.error('error'); }
                    );
                }
            );
        }
    );
    </script>
</%def>