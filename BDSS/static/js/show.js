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

var showJobInfo = function(job) {
    console.log(job);

    $('#job-title').text(job.name);

    var info_html =  'Status: ' + statusLabel(job.status) + '<br>';

    if (job.status == 'in_progress') {
        info_html += 'Started: ' + job.started_at + '<br>';
    } else if (job.status == 'completed' || job.status == 'failed') {
        info_html += job.status.charAt(0) + job.status.slice(1) + ' in ' + job.measured_time.toFixed(2) + ' seconds<br>';
    }

    $('#job-info').html(info_html);

    var data_list = $('#data-list');
    data_list.empty();
    job.required_data.forEach(function(d) {
        var li_html = '<li>' +
            statusLabel(d.status) + d.data_url + '<br>';

        if (d.status == 'in_progress') {
            li_html += 'Started at ' + d.started_at;
        } else if (d.status == 'failed') {
            li_html += 'Failed after ' + d.transfer_time.toFixed(2) + ' seconds. (' + d.error + ')';
        } else if (d.status == 'completed') {
            li_html += 'Downloaded ' + d.transfer_size + ' bytes in ' + d.transfer_time.toFixed(2) + ' seconds';
        }

        li_html += '</li>';

        data_list.append($(li_html));
    });
};

var loadJobInfo = function(job_id) {
    $('#job-title, #job-info, #data-list').addClass('hidden');
    $('#placeholder').removeClass('hidden');
    $.ajax('/api/jobs/' + job_id, {
        dataType: 'json',
        success: function(data) {
            showJobInfo(data.job);
            $('#job-title, #job-info, #data-list').removeClass('hidden');
            $('#placeholder').addClass('hidden');
        }
    });
};

$(document).ready(function() {
    var job_id = parseInt(window.location.hash.slice(1));
    if (!isNaN(job_id)) {
        loadJobInfo(job_id);
    } else {
        alert('Invalid job ID');
    }
});

$(window).on('hashchange', function() {
    var job_id = parseInt(window.location.hash.slice(1));
    if (!isNaN(job_id)) {
        loadJobInfo(job_id);
    } else {
        alert('Invalid job ID');
    }
});
