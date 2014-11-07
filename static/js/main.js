(function ($) {
    'use strict';

    var resultList = $('#results');

    function search(searchTerm) {
        var options = {
            url: '/search',
            type: 'GET',
            data: {
                q: searchTerm
            }
        };
        return $.ajax(options);
    }

    function populateResultList(response) {
        var html = '', results, result;

        resultList.empty();

        if (response.error) {
            $('.error').show().empty().text(response.error);
            return;
        }

        results = response.results;

        if (results.length === 0) {
            $('.no-results-message').show();
            return;
        }

        for (var i = 0; i < results.length; i++) {
            result = results[i];
            html = '<div class="list-group">'
                + '<a href="'+result.url+'" class="list-group-item">'
                + '<h4 class="list-group-item-heading">'+result.name+'</h4>'
                + '<p class="list-group-item-text">'+result.description+'</p>'
                + '</a>'
                + '</div>';
            resultList.append(html);
        }
    }

    $(function () {
        $('#go').on('submit', function (e) {
            e.preventDefault();

            var searchTerm = $('#search-term').val();

            $('.no-results-message').hide();
            $('.error').hide();
            var request = search(searchTerm);
            request.done(populateResultList);
        });
    });
}(jQuery));
