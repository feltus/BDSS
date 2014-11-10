var NUM_URLS = 1;
var buildUrlInput = function() {
    NUM_URLS += 1;

    return $('<div class="form-group url-input-group">' +
            '<div class="input-group">' +
                '<label class="sr-only" for="url' + NUM_URLS + '">Data URL</label>' +
                '<input type="text" class="url-input form-control" id="url' + NUM_URLS + '">' +
                '<span class="input-group-btn">' +
                    '<button class="btn btn-danger remove-url-btn" type="button">&times;</button>' +
                '</span>' +
            '</div>' +
        '</div>');
};

var bindRemoveUrlButtonHandler = function() {
    $('.remove-url-btn').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        $(this).closest('.form-group').remove();

        if ($('.url-input').length === 1) {
            $('.remove-url-btn').attr('disabled', true);
        } else {
            $('.remove-url-btn').removeAttr('disabled');
        }
    });
};

$(document).ready(function() {

    var transferMethods = null;
    $.ajax('/api/data_transfer_methods', {
        dataType: 'json',
        success: function(response) {
            transferMethods = response.methods;
            var select = $('#data-transfer-method');
            select
                .html(response.methods.map(function(m) { return '<option value="' + m.id + '" data-description="' + m.description + '">' + m.label + '</option>'; }))
                .on('change', function() {
                    var selectedMethod = transferMethods.filter(function(m) { return m.id == select.find('option:selected').val(); })[0];
                    $(this).siblings('.help-block').html(selectedMethod.description);
                    $('#transfer-method-options').empty().append(buildForm(selectedMethod.options));
                });
            var selectedMethod = transferMethods.filter(function(m) { return m.id == select.find('option:selected').val(); })[0];
            select.siblings('.help-block').html(selectedMethod.description);
            $('#transfer-method-options').empty().append(buildForm(selectedMethod.options));
        }, error: function() {
            console.warn('Unable to retrieve data transfer methods');
        }
    });


    $.ajax('/api/data_destinations', {
        dataType: 'json',
        success: function(response) {
            var select = $('#data-destination');
            select
                .html(response.destinations.map(function(m) { return '<option value="' + m.id + '" data-description="' + m.description + '">' + m.label + '</option>'; }))
                .on('change', function() {
                    $(this).siblings('.help-block').html($(this).find('option:selected').data('description'));
                })
                .siblings('.help-block').html(select.find('option:selected').data('description'));
        }, error: function() {
            console.warn('Unable to retrieve data destinations');
        }
    });

    $('#add-url-btn').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var inputGroup = buildUrlInput();
        inputGroup.insertBefore($('#add-url-group'));
        $('.remove-url-btn').removeAttr('disabled');
        bindRemoveUrlButtonHandler();
    });

    $('#url-manifest')
        // Set value to null on click so that selecting the same file will
        // still trigger the change event.
        .on('click', function() { $(this).val(null); })
        .on('change', function(e) {
            console.log(e);

            // Confirm replacing current URL inputs
            var numUrlsEntered = $('.url-input').filter(function() { return $(this).val().length > 0; }).length;
            if (numUrlsEntered > 0 && !confirm('Replace current URLs with those from file?')) {
                return;
            }

            var fileInput = $(this);

            if (e.target.files.length > 0) {

                fileInput.attr('disabled', true);

                $('#url-list li').remove();

                var f = e.target.files[0];
                var reader = new FileReader();
                reader.onerror = function() {
                    alert('Error reading manifest file');
                    console.error(e.target.error);
                    fileInput.removeAttr('disabled');
                };
                reader.onload = function(e) {
                    var data = e.target.result;
                    console.log(data);

                    $('#url-list').html(data.split('\n')
                        .map($.trim)
                        .filter(function(line) { return line.length > 0; })
                        .map(function(url) {
                            return '<li><input type="hidden" class="url-input" value="' + url + '">' + url + '</li>';
                        }));

                    fileInput.removeAttr('disabled');
                };

                reader.readAsText(f);
            }
        });

    $('#submit-request-btn').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var submitButton = $(this);
        submitButton.attr('disabled', 'disabled');
        var spinner = $('<span class="glyphicon glyphicon-refresh spin"></span>');
        spinner.prependTo(submitButton);

        // Validate URLs
        $('.url-input').each(function() {
            var url = $(this).val().toLowerCase();
            if (url.length === 0) {
                showError(this, 'A valid URL is required.');
            }
            else if (!url.match(/^(http|ftp)s?:\/\//)) {
                showError(this, 'Invalid URL. URLs must be either HTTP or FTP.');
            } else {
                hideError(this);
            }
        });

        requireValue($('#job-name'), 'A job name is required.');

        // Validate email address
        var emailInput = $('#email');
        var email = emailInput.val();
        if (requireValue(emailInput, 'A valid email address is required.')) {
            if (!email.match(/.+@.+\..+/)) {
                showError(emailInput, 'Invalid email address');
            } else {
                hideError(emailInput);
            }
        }

        requireValue($('#destination-directory'), 'A directory is required.');

        var inputValid = ($('.err-msg').length === 0);
        if (!inputValid) {
            spinner.remove();
            submitButton.removeAttr('disabled');
            return;
        }

        var transferMethodOptions = {};
        $('#transfer-method-options').find('input, textarea').each(function() {
            console.log($(this).attr('id') + ' => ' + $(this).val());
            transferMethodOptions[$(this).attr('id')] = $(this).val();
        });

        // Build request
        var request = {
            job: {
                name: $('#job-name').val(),
                email: email,
                data_transfer_method: $('#data-transfer-method').val(),
                data_transfer_method_options: transferMethodOptions,
                data_destination: $('#data-destination').val(),
                destination_directory: $('#destination-directory').val(),
                required_data: $('.url-input').map(function() { return { data_url: $(this).val() }; }).get()
            }
        };

        console.log(request);

        $.ajax('/api/jobs', {
            type: 'POST',
            data: JSON.stringify(request),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            success: function(response) {
                spinner.remove();
                submitButton.removeAttr('disabled');
                console.log(response);
                window.location = '/';
            },
            error: function(jqXHR, textStatus, errorThrown) {
                spinner.remove();
                submitButton.removeAttr('disabled');
                console.warn(errorThrown);
            }
        });

        console.log(request);
    });
});
