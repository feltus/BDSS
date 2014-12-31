/*global buildForm*/
$(document).ready(function() {

    // Show new description and rebuild options form when the transfer method is changed.
    var transferMethodSelect = $('#data_transfer_method');
    var updateTransferMethod = function() {
        var selectedMethod = transferMethodSelect.val();
        var methodOption = transferMethodSelect.find('option[value="' + selectedMethod + '"]');
        transferMethodSelect.siblings('.help-block').html(methodOption.data('method').description);
        $('#transfer_method_options').empty().populate(methodOption.data('method').options);
    };
    transferMethodSelect.on('change', updateTransferMethod);
    updateTransferMethod();

    // Show new description when the destination is changed.
    var destinationSelect = $('#data_destination');
    var updateDestination = function() {
        var selectedDestination = destinationSelect.val();
        var destinationOption = destinationSelect.find('option[value="' + selectedDestination + '"]');
        destinationSelect.siblings('.help-block').html(destinationOption.data('destination').description);
    };
    destinationSelect.on('change', updateDestination);
    updateDestination();


    $('#url_manifest')
        // Set value to null on click so that selecting the same file will
        // still trigger the change event.
        .on('click', function() { $(this).val(null); })
        .on('change', function(e) {
            console.log(e);

            // Confirm replacing current URL inputs
            var numUrlsEntered = $('fieldset[name="required_data[]"]').length;
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
                            return '<li>' +
                                    '<fieldset name="required_data[]">' +
                                        '<div class="form-group">' +
                                        '<input type="hidden" name="data_url" value="' + url + '">' +
                                        '<p class="control-label">' + url + '</p>' +
                                        '</div>' +
                                    '</fieldset>' +
                                '</li>';
                        }));

                    fileInput.removeAttr('disabled');
                };

                reader.readAsText(f);
            }
        });

    $('#job-form').initForm('/jobs', {
        build_request: function(form_value) {
            console.log(form_value);
            if (!form_value.hasOwnProperty('required_data')) {
                form_value.required_data = [];
            }
            delete form_value.url_manifest;
            return { job: form_value };
        },
        onsuccess: function() {
            window.location = '/jobs';
        }
    });
});
