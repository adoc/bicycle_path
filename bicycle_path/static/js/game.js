/*
*/

function engine_url(engine_id, action) {
    return '/api/v1/engines/'+engine_id+'/'+action
}


var card_theme = "/static/assets/oxygen/";
var card_ext = ".png";
var card_width = 74;

// Generates a "hand" widget.
// Can migrate this to underscore templating.
function hand_view(hand) {
    var hand_tmpl = '<div class="hand" style="width: %width%px;">%cards%</div>';
    var card_tmpl = '<img src="'+card_theme+'%card%'+card_ext+'" />';
    var cards = '';

    for (i=0; i<hand.length; i++) {
        cards += card_tmpl.replace('%card%', hand[i].toLowerCase());
    }

    return hand_tmpl.replace('%cards%', cards).replace('%width%', card_width * hand.length);
}

function wager_view(wager) {
    return "<div>Wager: <span>"+wager.amount+"</span></div>"
}

function total_view(total) {
    return "<div>Total: <span>"+total+"</span></div>"
}

var step_translations = {
    'PrepareStep': "Please take a seat.",
    'WagerStep': "Have a seat and place your bets.",
    'PlayerStep': "Let's play!",
    'ResolveStep': "Round Over!",
    'CleanupStep': ""
};


function translate_step(step) {
    if (step_translations.hasOwnProperty(step))
        return step_translations[step];
    else
        return step
}


function poll_success(data) {
    update_table_view(data);
}


function update_table_view(data) {

    $("#bj1").attr('data-id', data.engine_id);

    /* Update Controls UI
       ================== */
    // update site/leave buttons.
    if (data.in_game === true){
        $("#bj1 .sit").hide();
        $("#bj1 .leave").show();
    } else{
        $("#bj1 .sit").show();
        $("#bj1 .leave").hide();
    }


    if (data.in_game === true &&
        (data.step == "PrepareStep" || data.step == "WagerStep" || data.step == "InsuranceStep"
        || data.step == "ResolveStep")) {
        $("#bj1 .wager").show();
    } else {
        $("#bj1 .wager").hide();
    }


    if (data.in_seat > -1) {
        $("#bj1 .player"+data.in_seat).addClass('is_player')
    }


    if (data.your_turn === true) {
        $("#bj1 .play").show();
    } else {
        $("#bj1 .play").hide();
    }

    $("#bj1 .step").html(translate_step(data.step));
    $("#bj1 .timeout").html(data.timeout);
    $("#bj1 .dealer").html(hand_view(data.table.dealer_hand) +
                            total_view(data.dealer_total));
    
    
    for (var i=0; i<6; i++) {
        $("#bj1 .player"+i).html(hand_view(data.table.hands[i]) +
            wager_view(data.table.wagers[i]) +
            total_view(data.shown_totals[i]));
    }
}


function player_sit(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');
    
    apiWrapper('/api/v1/engines/'+engine_id+'/sit', function(result) {
        console.log("Good boy! " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}

function player_leave(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    apiWrapper('/api/v1/engines/'+engine_id+'/leave', function(result) {
        console.log("Awww, bye then. " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}

function player_wager(el, amount) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    postWrapper('/api/v1/engines/'+engine_id+'/wager', {amount: amount}, function(result) {
        console.log("Placed a bet! " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


function player_hit(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    apiWrapper('/api/v1/engines/'+engine_id+'/hit', function(result) {
        console.log("Hit! " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


function player_stand(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    apiWrapper('/api/v1/engines/'+engine_id+'/stand', function(result) {
        console.log("Stand! " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


function player_double(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    apiWrapper('/api/v1/engines/'+engine_id+'/double', function(result) {
        console.log("Double! " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


function debug_pause(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    apiWrapper('/api/v1/engines/'+engine_id+'/pause', function(result) {
        console.log("Double! " + result)
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


$(document).ready(function() {

    apiWrapper('/api/v1/engines', 
        function(data) {
            var engine_id = data[0]; // First available engine
            window.poller_observer = poll(engine_url(engine_id, 'observe'), poll_success);
        },
        function() { console.error("404"); },
        function() { console.error('error'); }
    );

    //$('#bj1').html(hand_view(['AS','AD','AC','AH', 'xx']));

});