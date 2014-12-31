$(document).ready(function() {

    $('#gen-key-form').initForm('/keys', {
        onsuccess: function() {
            window.location.reload();
        }
    });

    var buildInlineAlert = function(message) {
        return $('<div class="alert alert-dismissable alert-inline pull-right" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close"">' +
                '<span aria-hidden="true">&times;</span>' +
            '</button>' +
            message +
        '</div>');
    };

    $('.test-key-btn').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var btn = $(this);
        btn.setLoadingState(true);
        btn.siblings('.alert').remove();

        $.ajax({
            url: '/keys/' + btn.data('key-id') + '/test',
            dataType: 'json',
            success: function() {
                btn.setLoadingState(false);
                var msg = buildInlineAlert('Success');
                msg.addClass('alert-success').insertAfter(btn);
            },
            error: function(jqXHR) {
                btn.setLoadingState(false);
                var response = jqXHR.responseJSON;
                var msg = buildInlineAlert(response.error || 'Unknown error');
                msg.addClass('alert-danger').insertAfter(btn);
            }
        });
    });

});
