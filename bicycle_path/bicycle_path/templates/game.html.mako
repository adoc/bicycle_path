<%inherit file="root.html.mako" />

<div class="container">
    <div class="jumbotron">
        <div class="page-header"><h1>Table Games</h1></div>
        <h2>Just a temporary demo site for Coda's Card Game Engine.</h2>
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

    <div class="page-header">
        <h1>You</h1>
        <p>Bankroll: <span class="bankroll">${player.bankroll}</span></p>
    </div>


    <style>
    /*move dis*/
    .wager,
    .play {
        list-style-type: none;
        display: none;
    }

    .wager li,
    .play li {
        float: left;
        margin-right: 4px;
        height: 30px;
    }

    .game_table .well {
        min-height: 300px;
        width: 900px;
    }

    .well .player {
        
        min-width: 148px;
        min-height: 103px;
        border: 1px solid #555;
        margin: 0 4px;
    }

    .is_player {
        border: 4px solid #555 !important;
    }

    .well .dealer {
        min-height: 103px;
    }

    .dealer .hand {
        margin: 0 auto;
    }
    </style>


    <div id="bj1" class="game_table" data-id="">
        <div class="page-header">
            <h1 style="float: left; margin-right: 20px;">Blackjack Table</h1>
            <div class="sit" style="margin-top: 23px; display: none; float: left;">
                <a href="#" onclick="player_sit(this); return false;" class="btn btn-sm btn-primary" role="button">Sit</a>
            </div>
            <div class="leave" style="margin-top: 23px; display: none; float: left;">
                <a href="#" onclick="player_leave(this); return false;" class="btn btn-sm btn-warning" role="button">Leave</a>
            </div>
            <div class="clearfix"></div>
            <a name="table1"></a>
            <h3 class="step"></h3>
            <p>Timeout: <span class="timeout"></span></p>
        </div>

        <div class="well">
            <div class="dealer"></div>
            <div class="clearfix"></div>

            <div style="margin: 4px 4px;">
                <div style="float: left;" class="player player5"></div>
                <div style="float: right;" class="player player0"></div>
            </div>
            <div class="clearfix"></div>

            <div style="margin: 4px 72px;">
                <div style="float: left;" class="player player4"></div>
                <div style="float: right;" class="player player1"></div>
            </div>
            <div class="clearfix"></div>

            <div style="margin: 4px 136px;">
                <div style="float: left;" class="player player3"></div>
                <div style="float: right;" class="player player2"></div>
            </div>
            <div class="clearfix"></div>
        </div>
        <div class="clearfix"></div>

            <div class="sit" style="margin-top: 23px; display: none; float: left;">
                <a href="#" onclick="player_sit(this); return false;" class="btn btn-sm btn-primary" role="button">Sit</a>
            </div>
            <div class="leave" style="margin-top: 23px; display: none; float: left;">
                <a href="#" onclick="player_leave(this); return false;" class="btn btn-sm btn-warning" role="button">Leave</a>
            </div>

        <ul class="wager">
            <li><h4>Wagers</h4></li>
            <li><a class="btn btn-sm btn-default" href="#" onclick="player_wager(this, 1); return false;" >$1</a></li>
            <li><a class="btn btn-sm btn-default" href="#" onclick="player_wager(this, 10); return false;" >$10</a></li>
            <li><a class="btn btn-sm btn-default" href="#" onclick="player_wager(this, 100); return false;" >$100</a></li>
            <li><a class="btn btn-sm btn-default" href="#" onclick="player_wager(this, 1000); return false;" >$1000</a></li>
            <li><a class="btn btn-sm btn-default" href="#" onclick="player_wager_reset(this); return false;" >Clear</a></li>
        </ul>
        <div class="clearfix"></div>

        <ul class="play">
            <li><a class="btn btn-sm btn-success" href="#" onclick="player_hit(this); return false;" >Hit</a></li>
            <li><a class="btn btn-sm btn-warning" href="#" onclick="player_double(this); return false;" >Double</a></li>
            <li><a class="btn btn-sm btn-primary" href="#" onclick="player_stand(this); return false;" >Stand</a></li>
        </ul>
        <div class="clearfix"></div>
        
    </div>
</div>


<div style="min-height: 400px" class="container">

</div>
<%def name="scripts()">
    <script type="text/javascript" src="${request.static_url('bicycle_path:static/js/game.js')}"></script>
</%def>