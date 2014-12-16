from flask import Response

import json

## Filter request params to prevent mass assignment.
#  @param params Dictionary containing request params.
#  @param allowed_keys Collection of keys.
#  @return Dictionary containing only the values of params whose keys are
#   present in allowed_keys.
def filter_params(params, allowed_keys):
    return {k:v for (k, v) in params.iteritems() if k in allowed_keys}

## Create a Flask response containing JSON output.
def json_response(obj, status=200):
    return Response(json.dumps(obj), status=status, mimetype='application/json')
