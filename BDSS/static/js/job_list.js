var labelClassMap = {
    'pending': 'default',
    'in_progress': 'primary',
    'completed': 'success',
    'failed': 'danger'
};

var statusLabel = function(status) {
    return '<span class="label label-' + labelClassMap[status] + '">' + status + '</span>';
};

var bindToggleDataLinks = function() {
    $('a.show-data').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        $(this).addClass('hidden');
        $(this).siblings('a.hide-data').removeClass('hidden');
        $(this).siblings('ul.data-list').removeClass('hidden');
    });

    $('a.hide-data').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        $(this).addClass('hidden');
        $(this).siblings('a.show-data').removeClass('hidden');
        $(this).siblings('ul.data-list').addClass('hidden');
    });
};

$(document).ready(function() {
    $.ajax('/api/jobs', {
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#placeholder').remove();
            var list = $('#jobs-list');
            list.removeClass('hidden');
            data.jobs.forEach(function(job) {
                $('<li>' +
                    '<h4>' + job.name + '</h4>' +
                    'Status: ' + statusLabel(job.status) + '<br>' +
                    'Data: <a class="show-data" href="#">Show ' + job.required_data.length + ' URLs</a><a class="hide-data hidden" href="#">Hide URLs</a>' +
                    '<ul class="data-list hidden">' +
                    job.required_data.map(function(d) { return '<li>' + d.data_url + ' ' + statusLabel(d.status) + '</li>'; }).join('') +
                    '</ul>' +
                '</li>').appendTo(list);
            });

            bindToggleDataLinks();
        }
    });
});
