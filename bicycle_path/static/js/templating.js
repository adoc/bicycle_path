/*  templating.js
    Templating System.
    (c) 2010 - 2014 C. Nicholas Long
*/

/*
The beauty in this templating "system" is that it allows for
any sub templates to be rendered individually or as part
of rendering the entire chain.
*/

define(['underscore', 'config','theming'],
    function(_, Config, Theming) {

        var Templating = function(opts) {
            _.extend(this, {
                _templateString: ''
            }, opts || {});
            return this;
        };

        /* General render function that passes various objects and
        state used by the templates.*/
        // TODO: Removing the function params.
        Templating.prototype.render = function(namespace) {
            namespace = namespace || {};
            var template = _.template(this._templateString);
            return template(_.extend({
                                    Theming: Theming,
                                    Config: Config,
                                    ctx: namespace
                                }, this)));
            };

        return Templating;
    }
);