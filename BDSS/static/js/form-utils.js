(function($) {

    $.fn.clearFieldErrors = function() {
        this.find('.form-group.has-error').each(function() {
            $(this).removeClass('has-error');
            $(this).find('.help-block.err-msg').remove();
        });
        return this;
    };

    $.fn.showFieldErrors = function(errors) {
        if (typeof errors === 'string') {
            errors = [errors];
        }

        if (errors instanceof Array) {
            if (errors.length > 0) {
                var group = $(this).closest('.form-group');
                group.addClass('has-error');
                group.append($('<p class="help-block err-msg">' + errors.join('<br>') + '</p>'));
            }
        } else {
            for (var field in errors) {
                if (errors.hasOwnProperty(field)) {
                    var input = $(this).find('[name="' + field + '"]');
                    if (input.length !== 0) {
                        input.showFieldErrors(errors[field]);
                    } else {
                        input = $(this).find('[name="' + field + '[]"]');
                        for (var index in errors[field]) {
                            if (errors[field].hasOwnProperty(index)) {
                                input.eq(index).showFieldErrors(errors[field][index]);
                            }
                        }
                    }
                }
            }
        }
    };

    $.fn.clearFormErrors = function() {
        this.find('.alert.form-error').remove();
    };

    $.fn.showFormErrors = function(errors) {
        this.prepend($('<div class="alert alert-danger form-error">' + errors.join('<br>') + '</div>'));
    };

    var getInputElmValue = function(elm) {
        var type = null;
        var tag = elm.prop('tagName');
        if (tag === 'input') {
            type = elm.attr('type').toLowerCase();
        } else {
            type = tag.toLowerCase();
        }

        if (type === 'fieldset' || type === 'form') {
            var value = {};

            var inputs = elm.find('input, button, select, textarea, fieldset');
            for (var i = 0; i < inputs.length; i++) {
                var child_elm = inputs.eq(i);

                var field_name = child_elm.attr('name');

                if (child_elm.prop('tagName') === 'BUTTON' ||
                    child_elm.attr('type') === 'submit' ||
                    child_elm.attr('type') === 'button')
                {
                    continue;
                }

                if (value.hasOwnProperty(field_name)) {
                    continue;
                }

                var is_array = field_name.slice(-2) === '[]';
                field_name = field_name.replace(/\[\]$/, '');

                if (is_array) {
                    value[field_name] = elm.find('[name="' + field_name + '[]"]').map(function() {
                        return getInputElmValue($(this));
                    }).get();
                } else {
                    value[field_name] = getInputElmValue(child_elm);
                }
            }

            return value;

        } else if (type === 'checkbox') {
            return elm[0].checked;
        } else if (type === 'radio') {
            return elm.closest('form').find('input:radio[name="' + elm.attr('name') + '"]:checked').val();
        } else {
            return elm.val();
        }
    };

    $.fn.getValue = function() {
        return getInputElmValue($(this));
    };

    $.fn.setLoadingState = function(loading) {
        if (loading && this.find('span.spin').length === 0) {
            this.attr('disabled', 'disabled');
            var spinner = $('<span class="glyphicon glyphicon-refresh spin" style="margin-right:10px;"></span>');
            spinner.prependTo(this);
        } else {
            this.removeAttr('disabled');
            this.find('span.spin').remove();
        }
    };

    $.fn.initForm = function(url, options) {

        var settings = $.extend({
            onsuccess: function(response) {
                console.log(response);
            },
            onerror: function(jqXHR) {
                console.warn('submit failed');
                console.warn(jqXHR.responseText);
            },
            build_request: function(form_value) {
                return form_value;
            }
        }, options);

        var form = this;

        this.find('[type="submit"]').on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            form.clearFormErrors();
            form.clearFieldErrors();

            var submitButton = $(this);
            submitButton.setLoadingState(true);

            var request = settings.build_request(form.getValue());

            $.ajax(url, {
                type: 'POST',
                data: JSON.stringify(request),
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function(response) {
                    submitButton.setLoadingState(false);
                    settings.onsuccess(response);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    submitButton.setLoadingState(false);
                    if (jqXHR.status >= 400 && jqXHR.status < 600) {
                        try {
                            var response = JSON.parse(jqXHR.responseText);
                            if (response.hasOwnProperty('field_errors')) {
                                form.showFieldErrors(response.field_errors);
                            }
                            if (response.hasOwnProperty('form_errors')) {
                                form.showFormErrors(response.form_errors);
                            }
                        } catch (e) {}
                    }

                    settings.onerror(jqXHR, textStatus, errorThrown);
                }
            });
        });
    };

})(jQuery);

var showError = function(input, msg) {
    var group = $(input).closest('.form-group');
    group.addClass('has-error');
    var helpP = group.find('.help-block.err-msg');
    if (helpP.length === 0) {
        helpP = $('<p class="help-block err-msg"></p>');
        group.append(helpP);
    }
    helpP.html(msg);
};

var hideError = function(input) {
    var group = $(input).closest('.form-group');
    group.removeClass('has-error');
    group.find('.help-block.err-msg').remove();
};

var requireValue = function(input, msg) {
    msg = msg || 'A value is required.';
    if ($(input).val().length === 0) {
        showError(input, msg);
        return false;
    } else {
        hideError(input);
        return true;
    }
};
