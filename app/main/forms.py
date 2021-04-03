from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [DataRequired(message='Name is required.')])
    email = StringField('Email', [Email(message='Not a valid email address.'),
                                  DataRequired(message='Email is required.')])
    message = TextAreaField('Message', [DataRequired(message='Message is required.'),
                                        Length(min=4, message='Your message should be'
                                                              ' between 4 and 200 characters.', max=200)])
    recaptcha = RecaptchaField()

    def __repr__(self):
        return f"ContactForm(name={self.name.data}, email={self.email.data}, message={self.message.data})"
