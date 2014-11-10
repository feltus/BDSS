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
