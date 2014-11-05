/* 
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['socketio', 'config'],
    function(io, Config) {

        var opts = {
            resource: Config.socketResource
        }

        // Let's connect to the socket.
        var Sockets = {
            engine: io.connect('/engine', opts),
            dealer: io.connect('/dealer', opts),
            seats: io.connect('/seats', opts),
            tableControls: io.connect('/table_controls', opts),
            wagerControls: io.connect('/wager_controls', opts),
            playerStatus: io.connect('/player_status', opts),
            gameControls: io.connect('/game_controls', opts)
        };

        // Gracefully disconnect the socket.
        $(window).bind("beforeunload", function() {
            Sockets.seats.disconnect();
            Sockets.dealer.disconnect();
            Sockets.tableControls.disconnect();
            Sockets.wagerControls.disconnect();
            Sockets.gameControls.disconnect();
            Sockets.playerStatus.disconnect();
            Sockets.engine.disconnect();
        });

        return Sockets;
    }
);