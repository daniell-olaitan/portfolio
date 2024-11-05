#!/usr/bin/python3
import requests
from models import db
from app.api.v1.auth import auth
from models.user import User
from secrets import token_urlsafe
from urllib.parse import urlencode
from models.invalid_token import InvalidToken
from flask.typing import ResponseReturnValue
from app.api.v1.auth.auth import Auth
from utils import get_provider_cfg
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
google_document_cfg = get_provider_cfg()


@auth.route('/register', methods=['POST'])
def register_user() -> ResponseReturnValue:
    """
    Register a new user
    """
    from models.user_profile import UserProfile

    try:
        user_details = request.form.to_dict()

        validation_error = User.validate_user_details(
            name=user_details['name'],
            email=user_details['email'],
            password=user_details['password'],
            phone=user_details['phone']
        )
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'fail',
            'data': {
                'error': 'wrong input format'
            }
        }), 400

    if validation_error:
        return jsonify({
            'status': 'fail',
            'data': validation_error
        }), 422

    user = db.fetch_object(User, email=user_details['email'])
    if user:
        return jsonify({
            'status': 'fail',
            'data': {'error': str(err)}
        }), 400

    user = db.add_object(
        User,
        name=user_details['name'],
        email=user_details['email'],
        password=user_details['password'],
        phone=user_details['phone']
    )

    _ = db.add_object(UserProfile, user_id=user.id)
    user = db.fetch_object(User, id=user.id)
    return jsonify({
        'status': 'success',
        'data': user.to_json()
    }), 201


@auth.route('/login', methods=['POST'])
def login() -> ResponseReturnValue:
    """
    Log in a user
    """
    try:
        login_details = request.form.to_dict()
        validation_error = User.validate_user_details(
            email=login_details['email'],
            password=login_details['password']
        )
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': 'wrong input format'
            }
        }), 400

    if validation_error:
        return jsonify({
            'status': 'fail',
            'data': validation_error
        }), 422

    try:
        user = user_auth.authenticate_user(
            login_details['email'], login_details['password']
        )
    except ValueError as err:
        return jsonify({
            'status': 'fail',
            'data': {'error': str(err)}
        }), 400

    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'status': 'success',
            'data': {
                'user': user.to_json(),
                'access_token': access_token
            }
        }), 200

    return jsonify({
        'status': 'fail',
        'data': {'error': 'password is incorrect'}
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

            user = db.fetch_object(User, email=user_email)
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
        'data': {}
    }), 200


@auth.route('/forgot-password', methods=['POST'])
def forgot_password() -> ResponseReturnValue:
    from os import getenv
    from tasks import send_async_email
    from flask import render_template

    if request.content_type != 'application/x-www-form-urlencoded':
        return jsonify({
            'status': 'fail',
            'data': {'error': 'wrong input format'}
        }), 400

    email = request.form['email']
    if not email:
        return jsonify({
            'status': 'fail',
            'data': 'email is required'
        }), 422

    user = db.fetch_object(User, email=email)
    if not user:
        return jsonify({
            'status': 'fail',
            'data': {'error': 'email not registered'}
        }), 400

    otp = user_auth.generate_otp()
    user_auth.save_otp(email, otp)

    msg_body = render_template(
        'auth/password_reset_email.txt',
        user_name=user.name,
        otp=otp
    )

    email_data = {
        'subject': 'Reset Your Password',
        'sender': getenv('MAIL_SENDER'),
        'recipients': [user.email],
        'msg_body': msg_body
    }

    _ = send_async_email.delay(email_data)
    return jsonify({
        'status': 'success',
        'data': {'message': 'email has been sent'}
    }), 200


@auth.route('/reset-password', methods=['POST'])
def reset_password() -> ResponseReturnValue:
    if request.content_type != 'application/x-www-form-urlencoded':
        return jsonify({
            'status': 'fail',
            'data': {'error': 'wrong input format'}
        }), 400

    status = all([
        request.form.get('otp'),
        request.form.get('email'),
        request.form.get('new_password')
    ])

    if not status:
        return jsonify({
            'status': 'fail',
            'data': {'error': 'all the fields are required'}
        }), 422

    if user_auth.verify_otp(request.form['email'], request.form['otp']):
        user = db.fetch_object(User, email=request.form['email'])
        if not user:
            return jsonify({
                'status': 'fail',
                'data': {'error': 'email not registered'}
            }), 404

        user = db.update_object(User, id=user.id, password=request.form['new_password'])
        return jsonify({
            'status': 'success',
            'data': {
                'message': 'password changed'
            }
        }), 200

    return jsonify({
        'status': 'fail',
        'data': {'error': 'wrong otp or has expired'}
    }), 400


@auth.route('/change-password', methods=['POST'])
@jwt_required()
def change_password() -> ResponseReturnValue:
    from flask_jwt_extended import get_jwt_identity

    if request.content_type != 'application/x-www-form-urlencoded':
        return jsonify({
            'status': 'fail',
            'data': {'error': 'wrong input format'}
        }), 400

    status = all([
        request.form.get('current_password'),
        request.form.get('new_password')
    ])

    if not status:
        return jsonify({
            'status': 'fail',
            'data': {'error': 'all the fields are required'}
        }), 422

    user = db.fetch_object(User, id=get_jwt_identity())
    if user_auth.authenticate_user(user.email, request.form['current_password']):
        user = db.update_object(User, id=user.id, password=request.form['new_password'])
        return jsonify({
            'status': 'success',
            'data': {
                'message': 'password changed'
            }
        }), 200

    return jsonify({
        'status': 'fail',
        'data': {'error': 'wrong current password'}
    }), 400
