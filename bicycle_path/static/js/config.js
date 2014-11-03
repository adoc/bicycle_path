/*  config.js
    Application Configuration.
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['underscore'],
    function(_) {
        return {
            apiRoot: '/api/v1',
            socketResource: 'api/v1/sock',
            engineUri: 'engines',
            themeModuleName: 'base.theme'
        };
    }
);
