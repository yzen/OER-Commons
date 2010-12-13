oer.accordions = {};

oer.accordions.config = ($.hoverintent = {
    sensitivity: 7,
    interval: 100
});

$.event.special.hoverintent = {
    setup: function() {
        $(this).bind("mouseover", jQuery.event.special.hoverintent.handler);
    },
    teardown: function() {
        $(this).unbind("mouseover", jQuery.event.special.hoverintent.handler);
    },
    handler: function(event) {
        event.type = "hoverintent";
        var self = this,
        args = arguments,
        target = $(event.target),
        cX, cY, pX, pY;

        config = oer.accordions.config;

        function track(event) {
            cX = event.pageX;
            cY = event.pageY;
        };

        pX = event.pageX;
        pY = event.pageY;
        function clear() {
            target.unbind("mousemove", track).unbind("mouseout", arguments.callee);
            clearTimeout(timeout);
        }

        function handler() {
            if ( ( Math.abs(pX-cX) + Math.abs(pY-cY) ) < config.sensitivity ) {
                clear();
                jQuery.event.handle.apply(self, args);
            } else {
                pX = cX;
                pY = cY;
                timeout = setTimeout(handler, config.interval);
            }
        }

        var timeout = setTimeout(handler, config.interval);
        target.mousemove(track).mouseout(clear);
        return true;
    }
};