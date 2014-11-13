/*  config.js
    Application Configuration.
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['underscore'],
    function(_) {
        return {
            socketResource: 'api/v1/sock',
            themeModuleName: 'base.theme',
            debug: false,
            animations: {
                dealRotation: 720,
                dealDuration: 1000,
                dealEasing: "easeOutCubic"
            }
        };
    }
);
