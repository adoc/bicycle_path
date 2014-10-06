/*
*/

var card_theme = "/static/assets/oxygen/";
var card_ext = ".png";

// Generates a "hand" widget.
// Can migrate this to underscore templating.
function hand_view(hand) {
    var hand_tmpl = '<div class="hand">%cards%</div>';
    var card_tmpl = '<img src="'+card_theme+'%card%'+card_ext+'" />';
    var cards = '';

    for (i=0; i<hand.length; i++) {
        cards += card_tmpl.replace('%card%', hand[i].toLowerCase());
    }

    return hand_tmpl.replace('%cards%', cards);
}


var step_translate = {
    'PrepareStep': "Seating other players!",
    'WagerStep': "Place your bets!"
};


function poll_success(engine_id, data) {
    update_table_view(engine_id, data);
}

function poll_game_success(engine_id, data) {
    console.log(data);
}


function update_table_view(engine_id, data) {
    update_seating_view(engine_id);
    $("#bj1 .step").html(data[0]);
    $("#bj1 .timeout").html(data[1].timeout);
    $("#bj1 .dealer").html(hand_view(data[1].table.dealer_hand));
    $("#bj1 .player1").html(hand_view(data[1].table.hands[0]));
}


function update_seating_view(engine_id) {
    $("#bj1").attr('data-id', engine_id);

    if (window.in_games.indexOf(engine_id) > -1){
        $("#bj1 .sit").hide();
        $("#bj1 .leave").show();
    } else{
        $("#bj1 .sit").show();
        $("#bj1 .leave").hide();
    }
}


function player_sit(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');
    
    apiWrapper('/api/v1/engines/'+engine_id+'/sit', function(result) {
        update_seating_view(engine_id);
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


function player_leave(el) {
    var engine_id = $(el).parents('.game_table').attr('data-id');

    apiWrapper('/api/v1/engines/'+engine_id+'/leave', function(result) {
        update_seating_view(engine_id);
    },
    function() { console.error("404"); },
    function() { console.error('error'); }
    );
}


$(document).ready(function() {

    apiWrapper('/api/v1/engines', 
        function(data) {
            var engine_id = data[0]; // First available engine
            update_seating_view(engine_id);
            window.poller_observer = poll_engine(engine_id, poll_success, 'observe');
            window.poller_game= poll_engine(engine_id, poll_game_success, 'game', 5000)
        },
        function() { console.error("404"); },
        function() { console.error('error'); }
    );

    //$('#bj1').html(hand_view(['AS','AD','AC','AH', 'xx']));

});