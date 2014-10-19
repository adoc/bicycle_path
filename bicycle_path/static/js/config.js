/*  config.js
    Application Configuration.
    (c) 2010 - 2014 C. Nicholas Long
*/

define(['underscore'],
    function(_) {

        return {
            apiRoot: '/api/v1',
            themeName: 'base.theme'
        };

        return _.extend(config, {
            // This goes elsewhere.
            engine_url: function (id, action) {
                return join_path(config.apiRoot, 'engines', id, action);
            }
        });
    }
);