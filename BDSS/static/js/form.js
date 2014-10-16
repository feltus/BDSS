var buildForm = function(inputs) {
    var form = $('<form role="form"></form>');
    var buildFunction;
    var input;

    var capitalize = function(w) { return w.charAt(0).toUpperCase() + w.slice(1); };

    for (var id in inputs) {
        if (inputs.hasOwnProperty(id)) {
            buildFunction = eval('build' + inputs[id].type.charAt(0).toUpperCase() + inputs[id].type.slice(1) + 'Input');
            input = buildFunction(
                id,
                id.split('_').map(capitalize).join(' '),
                inputs[id].description,
                inputs[id].default);
            form.append(input);
        }
    }
    return form;
};

var wrapInput = function(input, label, description) {
    var group = $('<div class="form-group">' +
                '<label for="' + input.attr('name') + '">' + label + '</label>' +
                '</div>');
    group.append(input);
    if (description) {
        group.append($('<p class="help-block">' + description + '</p>'));
    }
    return group;
};

var buildStringInput = function(name, label, description, defaultValue) {
    var input = $('<input class="form-control" type="text" id="' + name + '" name="' + name + '">');
    if (defaultValue) {
        input.attr('placeholder', defaultValue);
    }
    return wrapInput(input, label, description);
};

var buildTextInput = function(name, label, description, defaultValue) {
    var input = $('<textarea class="form-control" rows="3" id="' + name + '" name="' + name + '"></textarea>');
    if (defaultValue) {
        input.attr('placeholder', defaultValue);
    }
    return wrapInput(input, label, description);
};

var buildIntegerInput = function(name, label, description, defaultValue) {
    var input = $('<input class="form-control" type="number" id="' + name + '" name="' + name + '" min="1" step="1">');
    if (defaultValue) {
        input.val(defaultValue);
    }
    return wrapInput(input, label, description);
};
