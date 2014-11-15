/*  common.js
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

// Configure Require.js
require.config({
    baseUrl: "static/js",
    paths: {
        jquery: 'lib/jquery.min',
        jquery_ui: 'lib/jquery-ui.min',
        underscore: 'lib/underscore.min',
        backbone: 'lib/backbone.min',
        // backbone_nested: 'lib/backbone-nested.min',
        // backbone_relational: 'lib/backbone-relational',
        socketio: 'lib/socket.io.min',
        backbone_socketio: 'lib/backbone.socket.io',
        bootstrap: 'lib/bootstrap.min',
        text: 'lib/text.min',
    },
    shim: {
        /*backbone_nested: {
            deps: ['backbone']
        }*/
        backbone_relational: {
            deps: ['backbone']
        }
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
if(typeof(String.prototype.trim) === "undefined") {
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
};

window.join_ext = function(base, ext) {
    base = base.trim();
    ext = ext.trim();
    if (ext.startsWith('.')) {
        return base + ext;
    } else {
        return base + '.' + ext;
    }
};

window.simple_countdown = function(options) {
    options || (options = {});
    options.tick || (options.tick = function() {});
    options.done || (options.done = function() {});
    options.timeout || (options.timeout = 0);
    options.interval || (options.interval = 1000);
    
    return setInterval(function(){
            options.timeout -= 1;
            options.tick(options.timeout);
            if (options.timeout <= 0) {
                options.done();
            }
        }, options.interval);
};