$(document).ready(function() {

    $('#signin-btn').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var submitButton = $(this);
        submitButton.attr('disabled', 'disabled');
        var spinner = $('<span class="glyphicon glyphicon-refresh spin"></span>');
        spinner.prependTo(submitButton);

        submitButton.closest('form').find('input').each(function() {
            hideError($(this));
        });

        var request = {
            email: $('#email').val(),
            password: $('#password').val()
        };

        $.ajax('/signin', {
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

                var response = JSON.parse(jqXHR.responseText);
                if (response.hasOwnProperty('errors')) {
                    for (var field in response.errors) {
                        if (response.errors.hasOwnProperty(field)) {
                            var fieldErrors = response.errors[field];
                            if (fieldErrors instanceof Array) {
                                showError($('#' + field), fieldErrors.join('<br>'));
                            } else {
                                showError($('#' + field), fieldErrors);
                            }
                        }
                    }
                }
            }
        });
    });

});
