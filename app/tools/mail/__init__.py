from flask import url_for, render_template, current_app
from flask_mail import Message, Mail

from app.models import User

mail = Mail()


def send_message(message: Message):
    """Sends a message with default email provider.

    Args:
        message: Message, a message which will be send
    """
    try:
        message_recipients = _filter_not_allowed_email_addresses_to_send(message.recipients)
        message.recipients = message_recipients
        current_app.logger.info('Trying to send email to recipients: %s',
                                message_recipients)
        mail.send(message)
        current_app.logger.info('Email sent to %s successfully.', message_recipients)
    except Exception as e:
        current_app.logger.error('There was an error during message'
                                 'sending to addresses: %s . Error: %s', message_recipients, e)


def send_text_message(to: str, subject: str, text: str):
    """Sends simple txt message to given recipient.

    Args:
        to: str, an email address
        subject: subject of a message
        text: message text
    """

    message = Message(subject=subject, body=text, recipients=[to])
    send_message(message)


def send_activation_mail(user: User):
    subject = "Timely: Activate your account"
    sender = "Timely Team"
    link = url_for('auth.activate_account',
                   token=user.activation_token,
                   _external=True)
    message_content = {"subject": subject,
                       "sender": sender,
                       "recipients": [user.email],
                       "template": "mail/activate_account",
                       "kwargs": {"user_name": user.name, "activation_link": link}}

    message = create_message(message_content)
    send_message(message)


def send_password_reset_mail(user: User):
    subject = "Timely: Reset your account password"
    link = url_for('auth.update_password',
                   token=user.password_reset_token,
                   email=user.email,
                   _external=True)
    message_content = {"subject": subject,
                       "recipients": [user.email],
                       "template": "mail/reset_account_password",
                       "kwargs": {"user_name": user.name, "activation_link": link}}

    message = create_message(message_content)
    send_message(message)


def create_message(content):
    msg = Message(
        content["subject"],
        sender=current_app.config['MAIL_ADDRESS'],
        recipients=content["recipients"]
    )
    msg.html = render_template(content["template"] + ".html", **content["kwargs"])

    return msg


def _filter_not_allowed_email_addresses_to_send(recipient_emails):
    """Filter recipient emails by not allowed email addresses.

    We can't send email messages to e.g. test account defined in config.

    Args:
        recipient_emails: arr[str], a string array which represents email recipient addresses

    Returns:
        True if can send email
        False otherwise
    """
    blocked_emails = []
    if current_app.config['PRODUCTION']:
        blocked_emails.append(current_app.config['TEST_USER_EMAIL'])

    return list(filter(lambda email: email not in blocked_emails, recipient_emails))
