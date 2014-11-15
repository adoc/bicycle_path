/* 
    (c) 2010 - 2014 C. Nicholas Long
*/
"use strict";

define(['config', 'animations', 'views'],
    function(Config, _A, Views) {

        var AnimatedViews = {};

        // Tricky AMD usage to make the Theme module (Config.themeName) dynamic.
        require([Config.themeModuleName], 
            function(Theme) {

                AnimatedViews.SeatView = Views.SeatView.extend({
                    modelRemove: function () {
                        var self = this;
                        if (self.model.id > 0) {
                            self.$el.removeClass("occupied", {
                                duration: Theme.seatDuration,
                                easing: Theme.seatEasing,
                                complete: function () {
                                    self.render();
                                }
                            });
                        } else {
                            self.render();
                        }
                    },
                    modelAdd: function () {
                        var self = this;
                        if (self.model.id > 0) {
                            self.$el.addClass("occupied", {
                                duration: Theme.seatDuration,
                                easing: Theme.seatEasing,
                                complete: function () {
                                    self.render();
                                }
                            });
                        } else {
                            self.render();
                        }
                    }
                });

                AnimatedViews.SeatsView = Views.SeatsView.extend({
                    subViews: {
                        SeatView: AnimatedViews.SeatView
                    }
                });

            }
        );

        return AnimatedViews;

    }
);