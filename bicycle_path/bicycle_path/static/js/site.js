/*
*/

function apiWrapper(url, foundCallback, notFoundCallback, errorCallback) {
    $.ajax({
        url: url,
        success: function (data, xhr) {
            if (data) {
                foundCallback(data);
            } else {
                errorCallback(xhr);
            }
        },
        error: function (xhr) {
            if (xhr.status == 404) {
                notFoundCallback();
            } else {
                errorCallback(xhr);
            }
        }
    });
}


function postWrapper(url, data, foundCallback, notFoundCallback, errorCallback) {
    $.ajax({
        url: url,
        data: data,
        type: "POST",
        success: function (data, xhr) {
            if (data) {
                foundCallback(data);
            } else {
                errorCallback(xhr);
            }
        },
        error: function (xhr) {
            if (xhr.status == 404) {
                notFoundCallback();
            } else {
                errorCallback(xhr);
            }
        }
    });
}


// '/api/v1/engines/'+engine+'/'+action


// Polling for now. Will implement websockets later.
// Poll the api
function poll(url, poll_success, interval) {
    var self = this;
    var interval = interval || 1000;

    this.__timer = null;

    function error(data) {
        console.error('Error in polling: ' + data);
        self.cancel();
    }

    function poll() {
        apiWrapper(url, 
            function (data) {
                poll_success(data);
            }, error, error)
    }

    this.start = function() {
        self.cancel();
        self.__timer = window.setInterval(poll, interval)
    }
    
    this.cancel = function() {
        clearInterval(self.__timer);
    }

    poll();
    this.start();
}