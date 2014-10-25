/* 
    (c) 2010 - 2014 C. Nicholas Long
*/

define(['jquery', 'underscore', 'backbone', 'socketio', 'config'],
    function($, _, Backbone, io, config) {
        
        var Controller = function (opts) {
            /* Controller is similar to a `Model` in that it handles
            generating a `url`. Attempt to use Backbone internal patterns
            to implement this. */

            _.extend(this, opts);
        };

        // 
        _.extend(Controller.prototype, Backbone.Events, {
            url: function () {
                var args = Array.prototype.slice.call(arguments, 0);
                return join_path.apply(join_path, 
                            [config.apiRoot].concat(args));
            }
        });

        Controller.extend = Backbone.Model.extend; /* Has nothing to do with
                                                    `Model` just a place to 
                                                    get the `extend` func.*/

        // 
        var Engine = Controller.extend({
            id: '',
            // generally /api/v1/engine/{id}/{action}
            url: function() {
                var args = Array.prototype.slice.call(arguments, 0);
                return Controller.prototype.url.apply(Controller.prototype,
                            [config.engineUri, this.id].concat(args));
            }
        });

        return {Engine: Engine};
    }
);