from models import db
from typing import Dict
from urllib.parse import quote
from app.frontend import frontend
from flask.typing import ResponseReturnValue
from flask import (
    url_for,
    render_template
)


@frontend.app_template_filter('urlencode')
def urlencode_filter(value: str) -> str:
    return quote(value)


@frontend.context_processor
def inject_now() -> Dict:
    from datetime import datetime
    return {'now': datetime.now}


@frontend.errorhandler(404)
def handle_404(_: Exception) -> ResponseReturnValue:
    return render_template(url_for('frontend.error'))


@frontend.context_processor
def inject_user_profile():
    from os import getenv
    from models.user import User

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


@frontend.route('/contact-me', methods=['GET', 'POST'])
def contact_me() -> ResponseReturnValue:
    pass


@frontend.route('/error', methods=['GET'])
def error() -> ResponseReturnValue:
    return render_template('error.html')


@frontend.route('/', methods=['GET'])
def home() -> ResponseReturnValue:
    headers = [
        {'name': 'me', 'url': url_for('frontend.home'), 'selected': True},
        {'name': 'projects', 'url': url_for('frontend.get_projects')},
        {'name': 'work', 'url': url_for('frontend.get_works')},
        {'name': 'articles', 'url': url_for('frontend.get_articles')},
        {'name': 'open source contribution', 'url': url_for('frontend.get_contributions')}
    ]

    return render_template('home.html', headers=headers)


@frontend.route('/projects', methods=['GET'])
def get_projects() -> ResponseReturnValue:
    from os import getenv
    from models.user import User

    email = getenv('USER_EMAIL') or 'daniell.olaitan@gmail.com'
    user = db.fetch_object(User, email=email)
    headers = [
        {'name': 'me', 'url': url_for('frontend.home')},
        {'name': 'projects', 'url': url_for('frontend.get_projects'), 'selected': True},
        {'name': 'work', 'url': url_for('frontend.get_works')},
        {'name': 'articles', 'url': url_for('frontend.get_articles')},
        {'name': 'open source contribution', 'url': url_for('frontend.get_contributions')}
    ]

    projects = []
    for project in user.projects:
        features = [feature.to_json() for feature in project.features]
        print(project.title)
        project = project.to_json()
        project['features'] = features
        projects.append(project)

    return render_template('projects.html', headers=headers, projects=projects)


@frontend.route('/works', methods=['GET'])
def get_works() -> ResponseReturnValue:
    from os import getenv
    from models.user import User

    email = getenv('USER_EMAIL') or 'daniell.olaitan@gmail.com'
    user = db.fetch_object(User, email=email)
    headers = [
        {'name': 'me', 'url': url_for('frontend.home')},
        {'name': 'projects', 'url': url_for('frontend.get_projects')},
        {'name': 'work', 'url': url_for('frontend.get_works'), 'selected': True},
        {'name': 'articles', 'url': url_for('frontend.get_articles')},
        {'name': 'open source contribution', 'url': url_for('frontend.get_contributions')}
    ]

    works = []
    for work in user.works:
        experiences = [experience.to_json() for experience in work.experiences]
        work = work.to_json()
        work['experiences'] = experiences
        works.append(work)

    return render_template('works.html', headers=headers, works=works)


@frontend.route('/articles', methods=['GET'])
def get_articles() -> ResponseReturnValue:
    from os import getenv
    from models.user import User

    email = getenv('USER_EMAIL') or 'daniell.olaitan@gmail.com'
    user = db.fetch_object(User, email=email)
    headers = [
        {'name': 'me', 'url': url_for('frontend.home')},
        {'name': 'projects', 'url': url_for('frontend.get_projects')},
        {'name': 'work', 'url': url_for('frontend.get_works')},
        {'name': 'articles', 'url': url_for('frontend.get_articles'), 'selected': True},
        {'name': 'open source contribution', 'url': url_for('frontend.get_contributions')}
    ]

    articles = [article.to_json() for article in user.articles]
    return render_template('articles.html', headers=headers, articles=articles)


@frontend.route('/articles/<string:article_id>', methods=['GET'])
def get_article(article_id: str) -> ResponseReturnValue:
    from models.article import Article

    article = db.fetch_object(Article, id=article_id)
    if not article:
        return render_template(url_for('frontend.error'))

    article = article.to_json()
    headers = [
        {'name': 'me', 'url': url_for('frontend.home')},
        {'name': 'projects', 'url': url_for('frontend.get_projects')},
        {'name': 'work', 'url': url_for('frontend.get_works')},
        {'name': 'articles', 'url': url_for('frontend.get_articles'), 'selected': True},
        {'name': 'open source contribution', 'url': url_for('frontend.get_contributions')}
    ]

    return render_template('article.html', headers=headers, article=article)


@frontend.route('/contributions', methods=['GET'])
def get_contributions() -> ResponseReturnValue:
    from os import getenv
    from models.user import User

    email = getenv('USER_EMAIL') or 'daniell.olaitan@gmail.com'
    user = db.fetch_object(User, email=email)
    headers = [
        {'name': 'me', 'url': url_for('frontend.home')},
        {'name': 'projects', 'url': url_for('frontend.get_projects')},
        {'name': 'work', 'url': url_for('frontend.get_works')},
        {'name': 'articles', 'url': url_for('frontend.get_articles')},
        {
            'name': 'open source contribution',
            'url': url_for('frontend.get_contributions'),
            'selected': True
        }
    ]

    contributions = []
    for contribution in user.contributions:
        gitrefs = [gitref.to_json() for gitref in contribution.git_refs]
        contribution = contribution.to_json()
        contribution['gitrefs'] = gitrefs
        contributions.append(contribution)

    return render_template('contributions.html', headers=headers, contributions=contributions)
