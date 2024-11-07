#!/usr/bin/env python3
from app import create_app
from os import getenv
from flask import jsonify
from celery import Celery
from flask.typing import ResponseReturnValue

app = create_app(getenv('CONFIG') or 'default')
celery = Celery(app.name, broker=getenv('CELERY_BROKER_URL'))


# HTTP Error Handlers
@app.errorhandler(404)
def not_found(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'not found'
        }
    }), 404


@app.errorhandler(403)
def unathorized(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'you are forbidden to perform this action'
        }
    }), 403


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


@app.route('/view-file/<string:filename>', methods=['GET'])
def serve_file(filename: str) -> ResponseReturnValue:
    from flask import send_from_directory

    return send_from_directory(getenv('UPLOAD_DIRECTORY'), filename, as_attachment=False)


@app.route('/download-file/<string:filename>', methods=['GET'])
def download_file(filename: str) -> ResponseReturnValue:
    from flask import send_from_directory

    return send_from_directory(getenv('UPLOAD_DIRECTORY'), filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
