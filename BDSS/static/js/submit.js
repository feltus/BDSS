/*global buildForm*/
$(document).ready(function() {

    // Show description and build options form for initial transfer method.
    var transferMethodSelect = $('#data-transfer-method');
    var selectedMethod = transferMethodSelect.val();
    var methodOption = transferMethodSelect.find('option[value="' + selectedMethod + '"]');
    transferMethodSelect.siblings('.help-block').html(methodOption.data('method').description);
    $('#transfer-method-options').empty().append(buildForm(methodOption.data('method').options));

    // Show new description and rebuild options form when the transfer method is changed.
    transferMethodSelect.on('change', function() {
        var selectedMethod = $(this).val();
        var methodOption = $(this).find('option[value="' + selectedMethod + '"]');
        $(this).siblings('.help-block').html(methodOption.data('method').description);
        $('#transfer-method-options').empty().append(buildForm(methodOption.data('method').options));
    });

    // Show description for initial destination.
    var destinationSelect = $('#data-destination');
    var selectedDestination = destinationSelect.val();
    var destinationOption = destinationSelect.find('option[value="' + selectedDestination + '"]');
    destinationSelect.siblings('.help-block').html(destinationOption.data('destination').description);

    // Show new description when the destination is changed.
    destinationSelect.on('change', function() {
        var selectedDestination = $(this).val();
        var destinationOption = $(this).find('option[value="' + selectedDestination + '"]');
        $(this).siblings('.help-block').html(destinationOption.data('destination').description);
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
                data_transfer_method: $('#data-transfer-method').val(),
                data_transfer_method_options: transferMethodOptions,
                data_destination: $('#data-destination').val(),
                destination_directory: $('#destination-directory').val(),
                required_data: $('.url-input').map(function() { return { data_url: $(this).val() }; }).get()
            }
        };

        console.log(request);

        $.ajax('/jobs', {
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
