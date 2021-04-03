from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, url_for, redirect, session, flash, g, has_request_context, \
    make_response, Response
from flask_restful import abort
from werkzeug.local import LocalProxy

from app.auth.forms import SignInForm, RegisterForm, PasswordResetForm, PasswordUpdateForm, ChangeAccountDetailsForm, \
    DeleteAccountForm
from app.models import User, db
from app.tools.mail import send_activation_mail, send_password_reset_mail

auth = Blueprint('auth', __name__, template_folder='templates')

current_user = LocalProxy(lambda: get_current_user())


def login_user(user):
    session["user_id"] = user.id


def logout_user():
    session.pop("user_id")


def login_required(f):
    @wraps(f)
    def _login_required(*args, **kwargs):
        if current_user.is_anonymous():
            flash("You need to be logged in to access this page", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return _login_required


def authorized_or_403(f):
    @wraps(f)
    def _authorized_or_403(*args, **kwargs):
        if current_user.is_anonymous():
            abort(Response('You are not allowed to access the resource.', 403))
        return f(*args, **kwargs)

    return _authorized_or_403


@auth.app_context_processor
def inject_current_user():
    if has_request_context():
        return dict(current_user=get_current_user())
    return dict(current_user="")


def get_current_user() -> User:
    _current_user = getattr(g, "_current_user", None)
    if _current_user is None:
        if session.get("user_id"):
            user = User.query.get(session.get("user_id"))
            if user:
                _current_user = g._current_user = user
    if _current_user is None:
        _current_user = User()
    return _current_user


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated():
        flash("You've already signed in.", "success")
        return redirect(url_for('main.home'))
    form = SignInForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user)

                # save activity info in db
                user.last_success_login = datetime.utcnow()
                db.session.commit()

                return redirect(url_for('main.home'))
            else:
                flash("Your username or password is not correct. Check it and try again.", "danger")
                # clear form fields
                form.email.data = None
                form.password.data = None

                # save activity info in db
                user.last_failure_login = datetime.utcnow()
                db.session.commit()

        else:
            flash("Your username or password is not correct. Check it and try again.", "danger")
            # clear form fields
            form.email.data = None
            form.password.data = None

    return render_template('sign-in.html', form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form_data = request.form

        user = User(form_data['email'], form_data['password'], form_data['name'])

        # add user to db
        db.session.add(user)
        db.session.commit()

        # generate user activation token
        user.create_token_for('activation')
        db.session.commit()

        # send email message with activation link
        send_activation_mail(user)

        flash("Your account is waiting for activation. Please check your email.", "success")
        return redirect(url_for("main.home"))

    return render_template('register.html', form=form)


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    return _do_logout_and_redirect_to_home_page()


def _do_logout_and_redirect_to_home_page():
    """Private function to not duplicate code which is
    responsible for user log out."""
    response = make_response(redirect(url_for("main.home")))
    response.set_cookie("user_id", "", max_age=0)
    logout_user()
    flash("You are logged out", "success")
    return response


@auth.route("/account", methods=['GET'])
@login_required
def account():
    change_account_details_form = ChangeAccountDetailsForm(current_user)
    delete_account_form = DeleteAccountForm()

    return render_template('account/account.html', change_account_details_form=change_account_details_form,
                           delete_account_form=delete_account_form)


@auth.route("/account/update", methods=['POST'])
@login_required
def account_update():
    change_account_details_form = ChangeAccountDetailsForm()
    delete_account_form = DeleteAccountForm()

    if change_account_details_form.validate_on_submit():

        # check if new email from form doesn't exist
        new_email = change_account_details_form.email.data
        old_mail = current_user.email
        if new_email != old_mail and User.is_user_with_email_exist(new_email):
            flash("User with given email exists. Please try a different address", "danger")
            return render_template('account/account.html', change_account_details_form=change_account_details_form)

        # update user properties
        current_user.name = change_account_details_form.name.data
        current_user.email = change_account_details_form.email.data

        new_password = change_account_details_form.password.data
        if new_password:
            current_user.password = new_password

        db.session.commit()
        return render_template('account/account.html', change_account_details_form=change_account_details_form,
                               delete_account_form=delete_account_form)

    return render_template('account/account.html', change_account_details_form=change_account_details_form)


@auth.route("/activate/<token>")
def activate_account(token):
    user = User.query.filter_by(activation_token=token).first()
    if user and user.activate_user_account(token):
        db.session.commit()
        flash("Your account is confirmed. Welcome " + user.name + "!", "success")
    else:
        flash("The confirmation link is not valid or it has expired", "danger")
    return redirect(url_for("main.home"))


@auth.route("/password_reset", methods=['POST', 'GET'])
def password_reset():
    if current_user.is_authenticated():
        return redirect(url_for("main.home"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            user.create_token_for('password_reset')
            db.session.commit()
            send_password_reset_mail(user)
        flash('If your email exists in our database you will receive the reset link. Check your inbox')
        return redirect(url_for('main.home'))

    return render_template('password-reset.html', form=form)


@auth.route("/update_password/<token>/<email>", methods=['POST', 'GET'])
def update_password(token, email):
    if current_user.is_authenticated():
        return redirect(url_for("main.home"))

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password_reset_token(token):
        flash("The password reset link is not valid or it has expired.", "danger")
        return redirect(url_for("main.home"))

    form = PasswordUpdateForm()
    if form.validate_on_submit():
        new_password = form.password.data
        user.set_password(new_password)
        user.password_reset_hash = ""
        user.password_reset_token = None
        db.session.commit()

        flash("New password is set! You can now login to the account.", "success")
        return redirect(url_for("auth.login"))

    flash("Hi " + user.name + "! You can now set a new password for the account.", "success")
    return render_template("update-password.html", form=form, token=token, email=email)


@auth.route("/account/delete", methods=['POST'])
@login_required
def account_delete():
    delete_account_form = DeleteAccountForm()
    if delete_account_form.validate_on_submit():
        email_from_form = delete_account_form.email.data
        if current_user.email != email_from_form:
            flash("Can't remove an account - given email doesn't match your email.", "danger")
            return redirect(url_for('auth.account'))

        # here we can delete user account
        if current_user.admin:
            flash("Can't remove application admin account.", "danger")
            return redirect(url_for('auth.account'))

        db.session.delete(current_user)
        db.session.commit()
        return _do_logout_and_redirect_to_home_page()

    return redirect(url_for('auth.account'))
