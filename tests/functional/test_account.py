from flask import Flask
from flask.testing import FlaskClient

from app.models import User, db
from tests.conftest import login


def test_not_showing_page_without_logging_in(test_client: FlaskClient):
    # given an account page and not logged in user

    # when we want to access account page
    response = test_client.get('/account')

    # we are getting 302 and redirection to login page
    assert response.status_code == 302
    assert response.location.endswith('/login')


def test_show_page_after_logging_in(user: User, app: Flask):
    # given na registered user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    with app.test_client() as test_client:
        # when the user is logged in and go to acivities page
        login_response = login(test_client, user.email, 'password')
        response = test_client.get('/account')

        # then on the page we can see additional button to sync
        # and we get a valid page
        assert response
        assert response.status_code == 200
        # some text on page
        assert b'Account details' in response.data
        assert b'Update account details' in response.data
        assert b'Delete account' in response.data


def test_deleting_user_account_with_invalid_data(user: User, app: Flask):
    # given na registered user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    with app.test_client() as test_client:
        # when the user is logged in and tries to delete account with invalid email
        login_response = login(test_client, user.email, 'password')
        response = test_client.post('/account/delete',
                                    data={'email': 'some_random_mail_xyz91919293@gmail.com'})

        # then he's getting a redirection to account page
        assert response
        assert response.status_code == 302


def test_deleting_user_account_with_valid_data(user: User, app: Flask):
    # given na registered user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    with app.test_client() as test_client:
        # when the user is logged in and tries to delete account with valid email
        # and then try to log in again
        _ = login(test_client, user.email, 'password')
        account_removal_response = test_client.post('/account/delete',
                                    data={'email': user.email})
        login_response = login(test_client, user.email, 'password')


        # then he's getting a redirection to home page
        assert account_removal_response
        assert account_removal_response.status_code == 302

        # and he can't log in again
        assert login_response
        assert login_response.status_code == 200
        assert b'You are logged out' in login_response.data