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
            player: io.connect('/player', opts),
            tableControls: io.connect('/table_controls', opts)
        };

        // Gracefully disconnect the socket.
        $(window).bind("beforeunload", function() {
            Sockets.engine.disconnect();
            Sockets.player.disconnect();
            Sockets.tableControls.disconnect();
        });

        return Sockets;
    }
);