#!/usr/bin/env python3
from app import create_app
from os import getenv
from flask import jsonify
from flask.typing import ResponseReturnValue

app = create_app(getenv('CONFIG') or 'testing')


# HTTP Error Handlers
@app.errorhandler(404)
def not_found(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'not found'
        }
    }), 404


#index routes
@app.route('/status', methods=['GET'])
def app_status() -> ResponseReturnValue:
    """
    Get the status of the application
    """
    return jsonify({
        'status': 'success',
        'data': {
            'app_status': 'active'
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
