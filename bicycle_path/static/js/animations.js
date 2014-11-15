/* 
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['underscore', 'jquery', 'jquery_ui', 'config'],
    function(_, $, $ui, Config) {
        // http://stackoverflow.com/a/17348698
        /* IE 9+ */
        $.fn.rotate = function(degrees) {
            $(this).css({'-webkit-transform' : 'rotate('+ degrees +'deg)',
                         '-moz-transform' : 'rotate('+ degrees +'deg)',
                         '-ms-transform' : 'rotate('+ degrees +'deg)',
                         'transform' : 'rotate('+ degrees +'deg)'});
            return $(this);
        };

        require([Config.themeModuleName], 
            function(Theme) {

                $.fn.dealCardTo = function(opts) {
                    var self = this;
                    opts || (opts = {});
                    opts.x || (opts.x = 0);
                    opts.y || (opts.y = 0);
                    opts.done || (opts.done = function() {});

                    this.animate({
                        degrees: Theme.animations.dealRotation,
                        left: opts.x.toString() + "px",
                        top: opts.y.toString() + "px"
                    },{
                        duration: Theme.animations.dealDuration,
                        easing: Theme.animations.dealEasing,
                        step: function(now, tween) {
                            if (tween.prop === "degrees") {
                                self.rotate(now);
                            }
                        },
                        done: opts.done
                    });
                }
            }
        );
    }
);