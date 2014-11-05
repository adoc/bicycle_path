/*  common.js
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

// Configure Require.js
require.config({
    baseUrl: "static/js",
    paths: {
        jquery: 'lib/jquery.min',
        underscore: 'lib/underscore.min',
        backbone: 'lib/backbone.min',
        socketio: 'lib/socket.io.min',
        backbone_socketio: 'lib/backbone.socket.io',
        bootstrap: 'lib/bootstrap.min',
        text: 'lib/text.min',
    },
    shim: {
    }
});

/* General lib includes from my gist. (https://gist.github.com/adoc) */

// http://stackoverflow.com/a/1608546
function construct(constructor, args) {
    function F() {
        return constructor.apply(this, args);
    }
    F.prototype = constructor.prototype;
    return new F();
}

// src: http://stackoverflow.com/a/646643
// Add `startsWith` and `endsWith` to the String prototype.
if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

if (typeof String.prototype.endsWith != 'function') {
    String.prototype.endsWith = function (str){
        return this.slice(-str.length) == str;
    };
}

// src: http://stackoverflow.com/a/1418059
// Add a whitespace strip to the String prototype.
if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

window.join_path = function(a) {
    /* Direct port of Python std posixpath.join.
    src: https://hg.python.org/cpython/file/v2.7.3/Lib/posixpath.py:60
    */
    var path = a;
    for(var i=1; i<arguments.length; i++) {
        var b = arguments[i];
        if(typeof b !== 'undefined' && b.startsWith('/')) {
            path = b;
        } else if (typeof path !== 'undefined' &&
                        (path == '' || path.endsWith('/'))) {
            path = path.concat(b);
        } else if (typeof b !== 'undefined') {
            path = path.concat('/' + b);
        }
    }
    return path;
}

window.join_ext = function(base, ext) {
    base = base.trim();
    ext = ext.trim();
    if (ext.startsWith('.')) {
        return base + ext;
    } else {
        return base + '.' + ext;
    }
}

// TEmp hack out!
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