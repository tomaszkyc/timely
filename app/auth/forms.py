import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, ValidationError

from app.models import User


def validate_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user:
        raise ValidationError("Email already exists.")


class PasswordComplexityCheck(object):
    def __init__(self, require_upper_letter=True, require_special_sign=True, require_number=True, min_length=8):
        self.require_upper_letter = require_upper_letter
        self.require_special_sign = require_special_sign
        self.require_number = require_number
        self.min_length = min_length
        self._build_warning_message()

    def _build_warning_message(self):
        requirements = []
        if self.require_special_sign:
            requirements.append('1 special sign')
        if self.require_upper_letter:
            requirements.append('1 upper letter')
        if self.require_number:
            requirements.append('1 number')
        if self.min_length:
            requirements.append('minimum length: %d signs' % self.min_length)

        if requirements:
            warning_message = ('Password should meet the criteria %s' % ', '.join(requirements))
        else:
            warning_message = ''
        self.message = warning_message

    def __call__(self, form, field):
        password = field.data

        valid_password = True

        if len(password) < self.min_length:
            valid_password = False

        if self.require_number and not any(char.isdigit() for char in password):
            valid_password = False

        if self.require_special_sign and not re.search('[^A-Za-z0-9]', password):
            valid_password = False

        if self.require_upper_letter and not any(char.isupper() for char in password):
            valid_password = False

        if not valid_password:
            raise ValidationError(self.message)


class SignInForm(FlaskForm):
    """Sign in form."""
    email = StringField('Email', validators=[Email(message='Not a valid email address.'),
                                             DataRequired('Email is required.')])
    password = PasswordField('Password', validators=[DataRequired('Password is required.')])


class RegisterForm(FlaskForm):
    """Register form."""
    name = StringField('Name', validators=[DataRequired('Your name is required.')])
    email = StringField('Email', validators=[Email(message='Not a valid email address.'),
                                             DataRequired('Email is required.'),
                                             validate_email])
    password = PasswordField('Password', validators=[DataRequired('Password is required.'), PasswordComplexityCheck()])


class PasswordResetForm(FlaskForm):
    """Password reset form."""
    email = StringField('Email', validators=[Email(message='Not a valid email address.'),
                                             DataRequired('Email is required.')])


class PasswordUpdateForm(FlaskForm):
    """Password update form."""
    password = PasswordField('Password', validators=[DataRequired('Password is required.'), PasswordComplexityCheck()])


class ChangeAccountDetailsForm(FlaskForm):
    """Change account details form."""
    name = StringField('Name', validators=[DataRequired('Your name is required.')])
    email = StringField('Email', validators=[Email(message='Not a valid email address.')])
    password = PasswordField('Password', validators=[])

    def __init__(self, user=None):
        super(ChangeAccountDetailsForm, self).__init__()

        if user:
            self.name.data = user.name
            self.email.data = user.email


class DeleteAccountForm(FlaskForm):
    """Delete account form."""
    email = StringField('Email', validators=[Email(message='Not a valid email address.'),
                                             DataRequired('Email is required.')])
