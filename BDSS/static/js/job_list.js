var labelClassMap = {
    'pending': 'default',
    'in_progress': 'primary',
    'completed': 'success',
    'failed': 'danger'
};

var titleize = function(str) {
    return str.split('_').map(function(s) { return s.charAt(0).toUpperCase() + s.slice(1); }).join(' ');
};

var statusLabel = function(status) {
    return '<span class="label label-' + labelClassMap[status] + '">' + titleize(status) + '</span>';
};

var statuses = ['pending', 'in_progress', 'completed', 'failed'];

$(document).ready(function() {
    $.ajax('/api/jobs', {
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#placeholder').remove();
            var list = $('#jobs-list');
            list.removeClass('hidden');
            data.jobs.forEach(function(job) {
                var status_url_count = {};
                statuses.forEach(function(status) {
                    status_url_count[status] = job.required_data.filter(function(d) { return (d.status == status); }).length;
                });
                var li_html = '<li>' +
                    '<h4><a href="show.html#' + job.job_id + '">' + job.name + '</a></h4>' +
                    'Status: ' + statusLabel(job.status) + '<br>';

                    if (job.status == 'in_progress') {
                        li_html += 'Started: ' + job.started_at + '<br>';
                    } else if (job.status == 'completed' || job.status == 'failed') {
                        li_html += job.status.charAt(0) + job.status.slice(1) + ' in ' + job.measured_time.toFixed(2) + ' seconds<br>';
                    }

                    li_html += '' + job.required_data.length + ' data files (';

                    li_html += statuses
                        .filter(function(s) { return status_url_count[s] > 0; })
                        .map(function(s) { return status_url_count[s] + ' ' + titleize(s); })
                        .join(', ');

                    li_html += ')';
                li_html += '</li>';

                $(li_html).appendTo(list);
            });
        }
    });
});
