from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, flash, current_app

from app.auth.views import current_user
from app.main.forms import ContactForm
from app.tools import mail

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
def home():
    return render_template('home/home.html')


@main.route("/features")
def features():
    return render_template('features/features.html')


@main.route("/contact-us", methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()

    # if the user is authenticated we can
    # add for him some details to makes things faster
    # and easier
    if current_user.is_authenticated():
        form.name.data = current_user.name
        form.email.data = current_user.email

    if form.validate_on_submit():
        subject = f"New support request from {form.email.data} at {datetime.utcnow()}"
        text = str(form)
        to = current_app.config['SUPPORT_CONTACT_EMAIL']
        mail.send_text_message(to, subject, text)
        flash("Thank you for contacting us. We will handle the request as soon as possible.", "success")
        return redirect(url_for('main.contact_us'))
    return render_template('contact-us/contact-us.html',
                           form=form)


@main.route("/activities")
def activities():
    return render_template('activities/activities.html')
