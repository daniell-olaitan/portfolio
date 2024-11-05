#!/usr/bin/env python3
from app.admin import admin
from utils import (
    APIRequest,
    login_required
)
from flask import (
    render_template,
    abort,
    request,
    redirect,
    url_for,
    flash,
    session
)
from flask.typing import ResponseReturnValue
from app.admin.forms import LoginForm

api_request = APIRequest('http://127.0.0.1:5000/v1')


@admin.route('/', methods=['GET', 'POST'])
def login() -> ResponseReturnValue:
    form = LoginForm()
    if form.validate_on_submit():
        form_data = request.form.to_dict()
        del form_data['csrf_token']
        res, res_stat = api_request.make_post_request('/auth/login', form_data, request.files)
        if res_stat == 200:
            session['current_user'] = res['user']
            session['access_token'] = res['access_token']
            session['auth'] = {
                'Authorization': f"Bearer {res['access_token']}"
            }

            return redirect(url_for('admin.dashboard'))
        flash(res['error'], 'error')
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
@login_required
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
@login_required
def edit_item(item: str, item_id: str) -> ResponseReturnValue:
    from app.admin.forms import forms

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
        res, res_stat = api_request.make_get_request(f"/{item}/{item_id}")
        item_data = {}
        if res_stat == 200:
            for key, value in res.items():
                if key in form_dict['inuw']:
                    continue

                if key in ['skills', 'tags', 'technologies', 'impacts', 'descriptions']:
                    item_data[key] = '::'.join(value)
                else:
                    item_data[key] = value

            form_ins = form_def(
                **item_data
            )
        else:
            abort(res_stat)

    if form_ins.validate_on_submit():
        payload = request.form.to_dict()
        del payload['csrf_token']
        files = {key: (file.filename, file.stream, file.mimetype) for key, file in request.files.items()}
        res, res_stat = api_request.make_patch_request(
            f"/{item}/{item_id}",
            payload=payload,
            file_load=files
        )

        if res_stat == 200:
            for key, val in res.items():
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
@login_required
def delete_item(item: str, item_id: str) -> ResponseReturnValue:
    if item not in [
        'contacts', 'gitrefs', 'articles', 'projects', 'services',
            'works', 'experiences', 'contributions', 'features']:
        abort(404)

    _, res_stat = api_request.make_delete_request(f"/{item}/{item_id}")
    if res_stat == 200:
        return redirect(request.referrer or url_for('admin.dashboard'))

    abort(res_stat)


@admin.route(
    '/create-item/<string:parent>/<string:parent_id>/<string:item>',
    methods=['GET', 'POST'])
@login_required
def create_item(parent: str, parent_id: str, item: str) -> ResponseReturnValue:
    from app.admin.forms import forms

    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'articles': None
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
        payload = request.form.to_dict()
        del payload['csrf_token']
        files = {key: (file.filename, file.stream, file.mimetype) for key, file in request.files.items()}
        res, res_stat = api_request.make_post_request(
            f"/{parent}/{parent_id}/{item}",
            payload=payload,
            file_load=files
        )

        if res_stat == 201:
            if parent == 'users':
                res_obj = {
                    'item': item,
                    'item_id': res['id'],
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
@login_required
def profile() -> ResponseReturnValue:
    resp = api_request.make_get_request(f"/profiles/{session['current_user']['profile_id']}")
    resp1 = api_request.make_get_request(f"/profiles/{session['current_user']['profile_id']}/contacts")
    resp2 = api_request.make_get_request(f"/profiles/{session['current_user']['profile_id']}/services")
    if all([resp[1] == 200, resp1[1] == 200, resp2[1] == 200]):
        return render_template(
            'user_details.html',
            user=session['current_user'],
            profile=resp[0],
            contacts=resp1[0],
            services=resp2[0]
        )
    else:
        if resp[1] != 200:
            abort(resp[1])
        elif resp1[1] != 200:
            abort(resp1[1])
        else:
            abort(resp2[1])


@admin.route('/view-item/<string:item>/<string:item_id>/<string:sub_item>', methods=['GET'])
@admin.route('/view-item/<string:item>/<string:item_id>', methods=['GET'])
@login_required
def view_item(item: str, item_id: str, sub_item: str = None) -> ResponseReturnValue:
    from utils import encode_details

    if item not in ['projects', 'contributions', 'works', 'articles']:
        abort(404)

    if sub_item:
        if sub_item not in ['gitrefs', 'experiences', 'features']:
            abort(404)

    if sub_item:
        res, res_stat = api_request.make_get_request(f"/{item}/{item_id}")
        sub_res, sub_res_stat = api_request.make_get_request(f"/{item}/{item_id}/{sub_item}")

        if all([res_stat == 200, sub_res_stat == 200]):
            title = res.pop('name') if res.get('name') else res.pop('title')
            resource = encode_details(item, res)
            sub_resource = {
                'item_name': sub_item,
                'heading': sub_item.capitalize(),
                'sub_items': [encode_details(sub_item, s_res) for s_res in sub_res]
            }

            return render_template(
                'item_details.html',
                title=title,
                current_user=session['current_user'],
                resource=resource,
                sub_resource=sub_resource
            )
    else:
        res, res_stat = api_request.make_get_request(f"/{item}/{item_id}")

        if res_stat == 200:
            title = res.pop('name') if res.get('name') else res.pop('title')
            resource = encode_details(item, res)
            return render_template(
                'item_details.html',
                title=title,
                current_user=session['current_user'],
                resource=resource,
            )
    abort(res_stat)


@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard() -> ResponseReturnValue:
    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'articles': None
    }

    resource = {}
    current_user = session['current_user']
    firstname = current_user['name'].split(' ')[0]
    for item in item_codes.keys():
        res, res_stat = api_request.make_get_request(f"/users/{session['current_user']['id']}/{item}")
        if res_stat == 200:
            heading = item.capitalize()
            resource[heading] = {}
            resource[heading]['item'] = res
            resource[heading]['item_name'] = item
            resource[heading]['sub_item'] = item_codes[item]
        else:
            abort(res_stat)

    return render_template(
        'dashboard.html',
        firstname=firstname,
        resource=resource
    )


@admin.route('/fetch-items/<string:item>', methods=['GET'])
@login_required
def fetch_items(item: str) -> ResponseReturnValue:
    item_codes = {
        'projects': 'features',
        'works': 'experiences',
        'contributions': 'gitrefs',
        'articles': None
    }

    if item not in item_codes:
        abort(404)

    res, res_stat = api_request.make_get_request(f"/users/{session['current_user']['id']}/{item}")
    if res_stat == 200:
        heading = item.capitalize()
        return render_template(
            'items.html',
            current_user=session['current_user'],
            items=res,
            item_name=item,
            sub_item=item_codes[item],
            heading=heading
        )
    abort(res_stat)


@admin.route('/logout', methods=['GET'])
@login_required
def logout() -> ResponseReturnValue:
    import requests

    res = requests.get('http://127.0.0.1:5000/v1/auth/logout', headers={
        'Authorization': f"Bearer {session['access_token']}"
    })

    if res.status_code == 401 or res.status_code == 200:
        return redirect(url_for('admin.login'))

    abort(res.status_code)


# HTTP Error Handlers
@admin.errorhandler(401)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_401.html')


@admin.errorhandler(403)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_403.html')


@admin.errorhandler(404)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_404.html')


@admin.errorhandler(500)
def unauthorozed(_: Exception) -> ResponseReturnValue:
    return render_template('errors/error_500.html')
