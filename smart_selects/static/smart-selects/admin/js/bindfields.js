(function ($) {
    "use strict";

    function initItem(item) {
        var empty_label, chainfield = "#id_" + $(item).attr("data-chainfield"),
            url = $(item).attr("data-url"),
            id = "#" + $(item).attr("id"),
            value = JSON.parse($(item).attr("data-value")),
            auto_choose = $(item).attr("data-auto_choose");
        if ($(item).hasClass("chained-fk")) {
            empty_label = $(item).attr("data-empty_label");
            chainedfk.init(chainfield, url, id, value, empty_label, auto_choose);
        } else if ($(item).hasClass("chained")) {
            chainedm2m.init(chainfield, url, id, value, auto_choose);
        } else if ($(item).hasClass("filtered")) {
            // For the ManyToMany using horizontal=True added after the page load
            // using javascript.
            id = id.replace('_from', ''); // we need to remove the _from part
            chainedm2m.init(chainfield, url, id, value, auto_choose);
        }
    }

    $(window).on('load', function () {
        $.each($(".chained"), function (index, item) {
            initItem(item);
        });
        $.each($(".filtered"), function (index, item) {
            if (item.hasAttribute('data-chainfield')) {
                initItem(item);
            }
        });
    });

    $(document).ready(function () {
        $.each($(".chained-fk"), function (index, item) {
            initItem(item);
        });
    });

    function initFormset(chained) {
        var re = /\d+/g,
            prefix,
            match,
            chainfield = $(chained).attr("data-chainfield"),
            chainedId = $(chained).attr("id");
        if (chainfield.indexOf("__prefix__") > -1) {
            /*
             If we have several inlines with the same name, they will get an index, so we need to ignore that and get
             the last numeric value in the id
             */
            do {
                match = re.exec(chainedId);
                if (match) {
                    prefix = match[0];
                }
            } while (match);

            chainfield = chainfield.replace("__prefix__", prefix);
            $(chained).attr("data-chainfield", chainfield);
        }
        initItem(chained);
    }

    $(document).on('formset:added', function (event, _row) {
        // Fired every time a new inline formset is created

        var chainedFK, chainedM2M, filteredM2M;
        var $row = _row || $(event.target);

        // For the ForeingKey
        chainedFK = $row.find(".chained-fk");
        $.each(chainedFK, function (index, chained) {
            initFormset(chained);
        });

        // For the ManyToMany
        chainedM2M = $row.find(".chained");
        $.each(chainedM2M, function (index, chained) {
            initFormset(chained);
        });

        // For the ManyToMany using horizontal=True added after the page load
        // using javascript.
        filteredM2M = $row.find(".filtered");
        $.each(filteredM2M, function (index, filtered) {
            if (filtered.hasAttribute('data-chainfield')) {
                initFormset(filtered);
            }
        });
    });
}(jQuery || django.jQuery));
