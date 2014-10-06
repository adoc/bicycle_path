<%inherit file="root.html.mako" />

<div class="container">
    <div class="jumbotron">
        <h1>Temporary Game Spot</h1>
        <p>Just a temporary blackjack game. Enjoy!</p>
        <p><a href="#table1" class="btn btn-success btn-lg" role="button">Go Play! &raquo;</a>&nbsp;<a href="#" class="btn btn-primary btn-lg" role="button">Learn more &raquo;</a></p>
    </div>

    <div class="page-header">
        <h1>You</h1>
        <p>Bankroll: <span class="bankroll">${player.bankroll}</span></p>
    </div>

    <div id="bj1" class="game_table" data-id="">
        <div class="page-header">
            <h1 style="float: left; margin-right: 20px;">Blackjack Table #1</h1>
            <div class="sit" style="margin-top: 23px; display: none; float: left;">
                <a href="#" onclick="player_sit(this); return false;" class="btn btn-sm btn-success" role="button">Sit</a>
            </div>
            <div class="leave" style="margin-top: 23px; display: none; float: left;">
                <a href="#" onclick="player_leave(this); return false;" class="btn btn-sm btn-warning" role="button">Leave</a>
            </div>
            <div class="clearfix"></div>
            <a name="table1"></a>
            <h3 class="step"></h3>
            <p>Timeout: <span class="timeout"></span></p>
        </div>
        <div class="jumbotron">
            <div class="dealer">
            </div>
            <div class="player1">
            </div>
        </div>
    </div>
</div>

<%def name="scripts()">
    <script type="text/javascript" src="${request.static_url('bicycle_path:static/js/game.js')}"></script>
    <script>
        window.in_games = ${in_games|n};
    </script>
</%def>