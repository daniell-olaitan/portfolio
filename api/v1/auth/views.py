#!/usr/bin/python3
import requests
import typing as t
from models import db
from api.v1.auth import auth
from models.user import User
from secrets import token_urlsafe
from urllib.parse import urlencode
from models.invalid_token import InvalidToken
from flask.typing import ResponseReturnValue
from api.v1.auth.auth import Auth
from api import (
    jwt,
    google_document_cfg
)
from flask import (
    request,
    jsonify,
    session,
    current_app,
    redirect,
    url_for
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required
)

user_auth = Auth()


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(
    jwt_header: t.Mapping[str, str],
    jwt_payload: t.Mapping[str, str]
) -> bool:
    """
    Check if user has logged out
    """
    jti = jwt_payload['jti']
    return InvalidToken.verify_jti(jti)


@jwt.expired_token_loader
def expired_token_callback(
    jwt_header: t.Mapping[str, str],
    jwt_payload: t.Mapping[str, str]
) -> ResponseReturnValue:
    """
    Check if access_token has expired
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'token has expired'},
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(
    jwt_header: t.Mapping[str, str],
    jwt_payload: t.Mapping[str, str]
) -> ResponseReturnValue:
    """
    Check if access_token has been revoked
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'token has been revoked'},
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(_) -> ResponseReturnValue:
    """
    Handle unauthorized access
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'missing access token'},
    }), 401


@auth.route('/register', methods=['POST'])
def register_user() -> ResponseReturnValue:
    """
    Register a new user
    """
    try:
        user_details = request.get_json()
        validation_error = User.validate_user_details(
            name=user_details['name'],
            email=user_details['email'],
            password=user_details['password']
        )

        if validation_error:
            return jsonify({
                'status': 'fail',
                'data': validation_error
            }), 422

        try:
            user = user_auth.register_user(
                user_details['name'],
                user_details['email'],
                user_details['password']
            )

            return jsonify({
                'status': 'success',
                'data': user.to_json()
            }), 201
        except ValueError as e:
            return jsonify({
                'status': 'fail',
                'data': {'email': str(e)}
            }), 400
    except Exception:
        return jsonify({
            'status': 'fail',
            'data': {
                'user_details': 'invalid user details'
            }
        }), 400


@auth.route('/login', methods=['POST'])
def login() -> ResponseReturnValue:
    """
    Log in a user
    """
    try:
        login_details = request.get_json()
        validation_error = User.validate_user_details(
            email=login_details['email'],
            password=login_details['password']
        )

        if validation_error:
            return jsonify({
                'status': 'fail',
                'data': validation_error
            }), 422

        try:
            user = user_auth.authenticate_user(
                login_details['email'], login_details['password']
            )

            if user:
                access_token = create_access_token(identity=user.id)
                return jsonify({
                    'status': 'success',
                    'data': {
                        'user': user.to_json(),
                        'access_token': access_token
                    }
                })

            return jsonify({
                'status': 'fail',
                'data': {'password': 'password is incorrect'}
            }), 400
        except ValueError as e:
            return jsonify({
                'status': 'fail',
                'data': {'email': str(e)}
            }), 400
    except:
        return jsonify({
            'status': 'fail',
            'data': {
                'user_details': 'invalid user details'
            }
        }), 400


@auth.route('/google-login', methods=['GET'])
def google_register() -> ResponseReturnValue:
    """
    Login in through Google
    """
    session['oauth2_state'] = token_urlsafe(16)
    url = google_document_cfg['authorization_endpoint'] + '?' + urlencode({
        'client_id': current_app.config['GOOGLE_CLIENT_ID'],
        'redirect_uri': url_for('auth.login_callback', _external=True),
        'response_type': 'code',
        'scope': ' '.join(google_document_cfg['scopes_supported']),
        'state': session['oauth2_state'],
    })

    return redirect(url)


@auth.route('/login-callback')
def login_callback() -> ResponseReturnValue:
    """
    Login call back for Google OAuth
    """
    error_payload = {
        'status': 'fail',
        'data': {'user_details': 'authentication failed'}
    }

    if 'error' in request.args:
        return jsonify(error_payload), 400

    if request.args.get('state', None):
        if request.args['state'] != session.get('oauth2_state'):
            return jsonify(error_payload), 400

    if 'code' not in request.args:
        return jsonify(error_payload), 400

    try:
        response = requests.post(google_document_cfg['token_endpoint'], data={
            'client_id': current_app.config['GOOGLE_CLIENT_ID'],
            'client_secret': current_app.config['GOOGLE_CLIENT_SECRET'],
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': url_for('auth.login_callback', _external=True),
        }, headers={'Accept': 'application/json'})

        if response.status_code != 200:
            return jsonify(error_payload), 400

        oauth2_token = response.json().get('access_token')
        if not oauth2_token:
            return jsonify(error_payload), 400

        response = requests.get(google_document_cfg['userinfo_endpoint'], headers={
            'Authorization': 'Bearer ' + oauth2_token,
            'Accept': 'application/json',
        })

        if response.status_code != 200:
            return jsonify(error_payload), 400

        try:
            res = {}
            userinfo_response = response.json()
            user_email = userinfo_response['email']
            user_name = userinfo_response['name']

            res.update(
                name=user_name,
                email=user_email,
            )

            user = db.fetch_object_by(User, email=user_email)
            if not user:
                user = db.add_object(User, name=user_name, email=user_email)

            else:
                user = user[0]

            return jsonify({
                'status': 'success',
                'data': {
                    'access_token': create_access_token(user.id),
                    'user': user.to_json()
                }
            }), 200
        except Exception:
            return jsonify(error_payload), 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@auth.route('/logout')
@jwt_required()
def logout() -> ResponseReturnValue:
    """
    Log out user
    """
    jti = get_jwt()['jti']
    db.add_object(InvalidToken, jti=jti)

    return jsonify({
        'status': 'success',
        'data': None
    }), 200
