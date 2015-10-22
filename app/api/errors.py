from flask import jsonify, make_response
from .     import api


@api.app_errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': e}), 404)


@api.app_errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify({'error': e}), 500)
