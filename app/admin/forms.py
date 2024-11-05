from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    FileField,
    SubmitField,
    EmailField,
    URLField,
    DateField,
    PasswordField
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
)
from flask_wtf.file import FileAllowed


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email address', validators=[DataRequired()])
    submit = SubmitField('Send Reset Link')


class ResetPasswordForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')]
    )

    submit = SubmitField('Reset Password')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')]
    )

    submit = SubmitField('Change Password')


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={'rows': 5})
    image_url = FileField(
        'Project Image (Images only)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')],
    )

    video_url = FileField(
        'Project Demo Video',
        validators=[FileAllowed(['mp4', 'mov', 'avi'], 'Video files only!')]
    )

    project_url = StringField('Project URL', render_kw={'placeholder': 'optional'})
    github_url = StringField('Github URL', render_kw={'placeholder': 'optional'})
    skills = StringField(
        'Skills',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    submit = SubmitField('Save')


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Save')


class ContactForm(FlaskForm):
    name = StringField('Type', validators=[DataRequired()])
    url = URLField('URL', validators=[DataRequired()])
    submit = SubmitField('Save')


class ServiceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={'rows': 5})
    submit = SubmitField('Save')


class ExperienceForm(FlaskForm):
    result = TextAreaField('Result', validators=[DataRequired()], render_kw={'rows': 5})
    submit = SubmitField('Save')


class FeatureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={'rows': 5})
    submit = SubmitField('Save')


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'rows': 5})
    tags = StringField(
        'Tags',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    submit = SubmitField('Save')


class ProfileForm(FlaskForm):
    location = StringField('Location', render_kw={'placeholder': 'optional'})
    tagline = TextAreaField('Tagline', render_kw={'placeholder': 'optional', 'rows': 5})
    bio = TextAreaField('Bio', render_kw={'placeholder': 'optional', 'rows': 5})
    image_url = FileField(
        'Profile Picture (Images only)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')],
    )

    work_header = TextAreaField('Work Header', render_kw={'placeholder': 'optional', 'rows': 5})
    project_header = TextAreaField('Project Header', render_kw={'placeholder': 'optional', 'rows': 5})
    article_header = TextAreaField('Article Header', render_kw={'placeholder': 'optional', 'rows': 5})
    contribution_header = TextAreaField('Contribution Header', render_kw={'placeholder': 'optional', 'rows': 5})
    resume = FileField('Resume (PDF only)', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Save')


class ContributionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    repo_url = StringField('Repo URL', validators=[DataRequired()])
    contribution_type = StringField('Contribution Type', render_kw={'placeholder': 'optional'})
    role = StringField('Role', render_kw={'placeholder': 'optional'})
    date = DateField('Date')
    descriptions = StringField(
        'Descriptions',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    impacts = StringField(
        'Impacts',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    technologies = StringField(
        'Tools Used',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    skills = StringField(
        'Skills',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    submit = SubmitField('Save')


class GitRefForm(FlaskForm):
    status = StringField('Status', validators=[DataRequired()])
    commit_id = StringField('Commit ID', validators=[DataRequired()])
    pull_request_url = StringField('Pull Request URL', validators=[DataRequired()])
    issue_url = StringField('Issue URL', render_kw={'placeholder': 'optional'})
    submit = SubmitField('Save')


class WorkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={'rows': 5})
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    skills = StringField(
        'Skills',
        validators=[DataRequired()],
        render_kw={'placeholder': 'separate each by ::'}
    )

    image_url = FileField(
        'Project Image (Images only)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]
    )

    submit = SubmitField('Save')


forms = {
    'contacts': {
        'form': ContactForm,
        'inuw': ['user_profile_id'],
        'outuw': [],
        'edithead': 'Edit Contact',
        'addhead': 'Add Contact'

    },
    'services': {
        'form': ServiceForm,
        'inuw': ['user_profile_id'],
        'outuw': [],
        'edithead': 'Edit Service',
        'addhead': 'Add Service'

    },
    'users': {
        'form': UserForm,
        'inuw': ['profile_id'],
        'outuw': [],
        'edithead': 'Edit User',
        'addhead':'',
    },
    'profiles': {
        'form': ProfileForm,
        'inuw': ['user_id'],
        'outuw': ['image_url', 'resume'],
        'edithead': 'Edit Profile',
        'addhead': ''
    },
    'articles': {
        'form': ArticleForm,
        'inuw': ['user_id'],
        'outuw': [],
        'edithead': 'Edit Article',
        'addhead': 'Add Article'
    },
    'experiences': {
        'form': ExperienceForm,
        'inuw': ['work_id'],
        'outuw': [],
        'edithead': 'Edit Experience',
        'addhead': 'Add Experience'
    },
    'features': {
        'form': FeatureForm,
        'inuw': ['project_id'],
        'outuw': [],
        'edithead': 'Edit Feature',
        'addhead': 'Add Feature'
    },
    'contributions': {
        'form': ContributionForm,
        'inuw': ['user_id', 'date'],
        'outuw': [],
        'edithead': 'Edit Open Source Contribution',
        'addhead': 'Add Open Source Contribution'
    },
    'gitrefs': {
        'form': GitRefForm,
        'inuw': ['contribution_id'],
        'outuw': [],
        'edithead': ' Edit Github Reference',
        'addhead': 'Add Github Referece'
    },
    'works': {
        'form': WorkForm,
        'inuw': ['user_id', 'start_date', 'end_date'],
        'outuw': ['image_url'],
        'edithead': 'Edit Work',
        'addhead': 'Add Work'
    },
    'projects': {
        'form': ProjectForm,
        'inuw': ['user_id'],
        'outuw': ['image_url', 'video_url'],
        'edithead': 'Edit Project',
        'addhead': 'Add Project'
    }
}
