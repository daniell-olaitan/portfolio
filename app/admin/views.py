#!/usr/bin/env python3
from models import db
from utils import APIRequest
from app.admin import admin
from models.user import User
from models.article import Article
from models.contact import Contact
from models.contribution import Contribution
from models.experience import Experience
from models.feature import Feature
from models.git_ref import GitRef
from models.project import Project
from models.service import Service
from models.work import Work
from models.user_profile import UserProfile
from app.api.v1.auth.auth import Auth
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required
)
from flask import (
    render_template,
    abort,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response
)
from flask.typing import ResponseReturnValue
from app.admin.forms import LoginForm

user_auth = Auth()
api_request = APIRequest('http://localhost:5000/v1')
model_map = {
    'articles': Article,
    'contacts': Contact,
    'contributions': Contribution,
    'experiences': Experience,
    'features': Feature,
    'works': Work,
    'projects': Project,
    'profiles': UserProfile,
    'users': User,
    'services': Service,
    'gitrefs': GitRef
}


@admin.context_processor
def inject_user_profile():
    from os import getenv

    email = getenv('USER_EMAIL') or 'daniell.olaitan@gmail.com'
    user = db.fetch_object(User, email=email)

    profile = user.profile.to_json()
    current_user = user.to_json()
    current_user['profile'] = profile

    services = [service.to_json() for service in user.profile.services]
    contacts = [contact.to_json() for contact in user.profile.contacts]
    current_user['profile']['services'] = services
    current_user['profile']['contacts'] = contacts

    return dict(current_user=current_user)


@admin.route('/', methods=['GET', 'POST'])
def login() -> ResponseReturnValue:
    form = LoginForm()
    if form.validate_on_submit():
        try:
            login_details = request.form.to_dict()
            validation_error = User.validate_user_details(
                email=login_details['email'],
                password=login_details['password']
            )
        except Exception as err:
            abort(400)

        if validation_error:
            abort(422)

        try:
            user = user_auth.authenticate_user(
                login_details['email'], login_details['password']
            )
        except ValueError as _:
            flash('Email not registered', 'error')
            abort(400)

        if user:
            access_token = create_access_token(identity=user.id)
            response = make_response(redirect(url_for('admin.dashboard')))
            set_access_cookies(response, access_token)

            return response

        flash('password is incorrect', 'error')
        abort(400)
    return render_template('auth/login.html', form=form)


@admin.route('forgot-password', methods=['GET', 'POST'])
def forgot_password() -> ResponseReturnValue:
    import requests
    from app.admin.forms import ForgotPasswordForm

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        form_data = request.form.to_dict()
        del form_data['csrf_token']
        resp = requests.post(
            'http://127.0.0.1:5000/v1/auth/forgot-password',
            data=form_data
        )

        if resp.status_code == 200:
            flash('An otp has been sent to your email', 'info')
            return redirect(url_for('admin.reset_password'))

        flash(resp.json()['data']['error'], 'error')

    meta = {
        'title': 'Forgot Password',
        'heading': 'Enter Email to receive OTP',
        'action_url': url_for('admin.forgot_password'),
        'action': 'Send OTP'
    }
    return render_template('auth/auth_form.html', form=form, meta=meta)


@admin.route('reset-password', methods=['GET', 'POST'])
def reset_password() -> ResponseReturnValue:
    import requests
    from app.admin.forms import ResetPasswordForm

    form = ResetPasswordForm()
    if form.validate_on_submit():
        form_data = request.form.to_dict()
        del form_data['csrf_token']
        resp = requests.post(
            'http://127.0.0.1:5000/v1/auth/reset-password',
            data=form_data,
        )

        if resp.status_code == 200:
            flash('password reset complete, proceed to log in', 'success')
            return redirect(url_for('admin.login'))

        flash(resp.json()['data']['error'], 'error')

    meta = {
        'title': 'Reset Password',
        'heading': 'Reset Password',
        'action_url': url_for('admin.reset_password'),
        'action': 'Reset Password'
    }
    return render_template('auth/auth_form.html', form=form, meta=meta)


@admin.route('change-password', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def change_password() -> ResponseReturnValue:
    from app.admin.forms import ChangePasswordForm

    form = ChangePasswordForm()
    if form.validate_on_submit():
        form_data = request.form.to_dict()
        del form_data['csrf_token']
        res, res_stat = api_request.make_post_request(
            '/auth/change-password',
            form_data,
            request.files
        )

        if res_stat == 200:
            flash('password changed successfully', 'success')
        else:
            flash(res['error'], 'error')

        return redirect(url_for('admin.profile'))
    return render_template('auth/change_password.html', form=form)


@admin.route('/edit-item/<string:item>/<string:item_id>', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def edit_item(item: str, item_id: str) -> ResponseReturnValue:
    import os
    from portfolio import app
    from app.admin.forms import forms
    from utils import handle_files

    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'features': 'projects',
        'experiences': 'works',
        'gitrefs': 'contributions',
        'articles': None
    }

    if item not in [
        'contacts', 'services', 'gitrefs', 'articles', 'profiles', 'projects',
            'users', 'works', 'experiences', 'contributions', 'features']:
        abort(404)

    form_dict = forms[item]
    form_def = form_dict['form']
    form_ins = form_def()
    form = {
        'action_url': url_for('admin.edit_item', item=item, item_id=item_id),
        'heading': form_dict['edithead']
    }

    if request.method == 'GET':
        resource = db.fetch_object(model_map[item], id=item_id)
        if not resource:
            abort(404)

        resource = resource.to_json()
        item_data = {}
        for key, value in resource.items():
            if key in form_dict['inuw']:
                continue

            if key in ['skills', 'tags', 'technologies', 'impacts', 'descriptions']:
                item_data[key] = '::'.join(value)
            else:
                item_data[key] = value

        form_ins = form_def(
            **item_data
        )


    if form_ins.validate_on_submit():
        resource_details = request.form.to_dict()
        del resource_details['csrf_token']
        resource = db.fetch_object(model_map[item], id=item_id)
        if not resource:
            abort(404)

        try:
            details = handle_files(resource_details, request.files)
            for field, value in resource.to_json().items():
                for key in ['image', 'picture', 'video', 'resume']:
                    if key in field:
                        if value and details.get(field):
                            file_path = os.path.join(app.root_path,
                                os.getenv('UPLOAD_DIRECTORY'),
                                value
                            )
                            if os.path.exists(file_path):
                                os.remove(file_path)

            resource = db.update_object(model_map[item], item_id, **details)
            resource = resource.to_json()
        except Exception as _:
            abort(400)

        for key, val in resource.items():
            if key.endswith('_id'):
                parent_id = val
                break

        if item in ['users', 'profiles', 'contacts', 'services']:
            page = url_for('admin.profile')
        elif item in ['works', 'projects', 'contributions', 'articles']:
            res_obj = {
                'item': item,
                'item_id': item_id,
                'sub_item': item_codes[item]
            }

            page = url_for('admin.view_item', **res_obj)
        else:
            res_obj = {
                'item': item_codes[item],
                'item_id': parent_id,
                'sub_item': item
            }

            page = url_for('admin.view_item', **res_obj)

        return redirect(page)

    form['fields'] = form_ins
    return render_template('item_form.html', form=form)


@admin.route('/delete-item/<string:item>/<string:item_id>', methods=['GET'])
@jwt_required(locations='cookies')
def delete_item(item: str, item_id: str) -> ResponseReturnValue:
    if item not in [
        'contacts', 'gitrefs', 'articles', 'projects', 'services',
            'works', 'experiences', 'contributions', 'features']:
        abort(404)

    resource = db.fetch_object(model_map[item], id=item_id)
    if not resource:
        abort(404)

    try:
        db.remove_object(model_map[item], item_id)
    except Exception as _:
        abort(400)

    return redirect(request.referrer or url_for('admin.dashboard'))


@admin.route(
    '/create-item/<string:parent>/<string:parent_id>/<string:item>',
    methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def create_item(parent: str, parent_id: str, item: str) -> ResponseReturnValue:
    from app.admin.forms import forms
    from utils import handle_files

    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'articles': None
    }

    relationship_map = {
        'contacts': 'user_profile_id',
        'services': 'user_profile_id',
        'articles': 'user_id',
        'experiences': 'work_id',
        'features': 'project_id',
        'contributions': 'user_id',
        'gitrefs': 'contribution_id',
        'works': 'user_id',
        'projects': 'user_id'
    }

    if parent not in ['works', 'projects', 'users', 'profiles', 'contributions']:
        abort(404)

    if item not in [
        'contacts', 'gitrefs', 'articles', 'projects', 'services',
            'works', 'experiences', 'contributions', 'features']:
        abort(404)

    form_dict = forms[item]
    form_def = form_dict['form']
    form_ins = form_def()
    form = {
        'action_url': url_for('admin.create_item', parent=parent, parent_id=parent_id, item=item),
        'heading': form_dict['addhead'],
        'fields': form_ins
    }

    if form_ins.validate_on_submit():
        resource_details = request.form.to_dict()
        del resource_details['csrf_token']
        parent_resource = db.fetch_object(model_map[parent], id=parent_id)
        if not parent_resource:
            abort(404)

        resource_details[relationship_map[item]] = parent_id
        try:
            details = handle_files(resource_details, request.files)
            resource = db.add_object(model_map[item], **details)
            resource = resource.to_json()
        except ValueError as _:
            abort(400)

        if parent == 'users':
            res_obj = {
                'item': item,
                'item_id': resource['id'],
                'sub_item': item_codes[item]
            }

            page = url_for('admin.view_item', **res_obj)
        elif parent == 'profiles':
            page = url_for('admin.profile')
        else:
            res_obj = {
                'item': parent,
                'item_id': parent_id,
                'sub_item': item
            }

            page = url_for('admin.view_item', **res_obj)

        return redirect(page)
    return render_template('item_form.html', form=form)


@admin.route('/profile', methods=['GET'])
@jwt_required(locations='cookies')
def profile() -> ResponseReturnValue:
        return render_template('user_details.html')


@admin.route('/view-item/<string:item>/<string:item_id>/<string:sub_item>', methods=['GET'])
@admin.route('/view-item/<string:item>/<string:item_id>', methods=['GET'])
@jwt_required(locations='cookies')
def view_item(item: str, item_id: str, sub_item: str = None) -> ResponseReturnValue:
    from utils import encode_details

    if item not in ['projects', 'contributions', 'works', 'articles']:
        abort(404)

    if sub_item:
        if sub_item not in ['gitrefs', 'experiences', 'features']:
            abort(404)

    parent_resource = db.fetch_object(model_map[item], id=item_id)
    if not parent_resource:
        abort(404)

    title = parent_resource.pop('name') if parent_resource.get('name') else parent_resource.pop('title')
    resource = encode_details(item, parent_resource)
    if sub_item:
        if sub_item == 'gitrefs':
            attr = 'git_refs'
        else:
            attr = sub_item

        resources = getattr(parent_resource, attr) or []
        resources = [resource.to_json() for resource in resources]
        sub_resource = {
            'item_name': sub_item,
            'heading': sub_item.capitalize(),
            'sub_items': [encode_details(sub_item, s_res) for s_res in resources]
        }

        return render_template(
            'item_details.html',
            title=title,
            resource=resource,
            sub_resource=sub_resource
        )
    else:
        return render_template(
            'item_details.html',
            title=title,
            resource=resource,
        )


@admin.route('/dashboard', methods=['GET'])
@jwt_required(locations='cookies')
def dashboard() -> ResponseReturnValue:
    from flask_jwt_extended import get_jwt_identity

    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'articles': None
    }

    resource = {}
    parent_resource = db.fetch_object(User, id=get_jwt_identity())
    if not parent_resource:
        abort(404)

    for item in item_codes.keys():
        resources = getattr(parent_resource, item) or []
        resources = [resource.to_json() for resource in resources]

        heading = item.capitalize()
        resource[heading] = {}
        resource[heading]['item'] = resources
        resource[heading]['item_name'] = item
        resource[heading]['sub_item'] = item_codes[item]

    return render_template('dashboard.html', resource=resource)


@admin.route('/fetch-items/<string:item>', methods=['GET'])
@jwt_required(locations='cookies')
def fetch_items(item: str) -> ResponseReturnValue:
    from flask_jwt_extended import get_jwt_identity

    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'articles': None
    }

    if item not in item_codes:
        abort(404)

    parent_resource = db.fetch_object(User, id=get_jwt_identity())
    if not parent_resource:
        abort(404)

    resources = getattr(parent_resource, item) or []
    resources = [resource.to_json() for resource in resources]
    heading = item.capitalize()

    return render_template(
        'items.html',
        items=resources,
        item_name=item,
        sub_item=item_codes[item],
        heading=heading
    )


@admin.route('/logout', methods=['GET'])
@jwt_required(locations='cookies')
def logout() -> ResponseReturnValue:
    from flask_jwt_extended import get_jwt
    from models.invalid_token import InvalidToken

    jti = get_jwt()['jti']
    _ = db.add_object(InvalidToken, jti=jti)

    return redirect(url_for('admin.login'))


# HTTP Error Handlers
@admin.errorhandler(400)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_400.html')


@admin.errorhandler(401)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_401.html')


@admin.errorhandler(403)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_403.html')


@admin.errorhandler(404)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_404.html')


@admin.errorhandler(422)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_422.html')


@admin.errorhandler(500)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_500.html')
