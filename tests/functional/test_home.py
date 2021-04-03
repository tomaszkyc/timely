from flask import Flask
from flask.testing import FlaskClient

from app.auth.views import current_user
from app.models import User, db
from tests.conftest import login, logout


def test_home_page(test_client: FlaskClient):
    # given a flask app

    # when we access a main page
    response = test_client.get('/')

    # we should get a valid main page
    assert response
    assert response.status_code == 200
    # title on a webpage
    assert b'Let\'s do some countdown' in response.data


def test_home_page_without_logging(test_client: FlaskClient):
    # given a flask app

    # when we access a main page
    response = test_client.get('/')

    # we should get a valid main page
    assert response
    assert response.status_code == 200
    # title on a webpage
    assert not b'Logout' in response.data
    assert not b'Your account' in response.data
    assert b'Sign in' in response.data


def test_home_page_with_logging(test_client: FlaskClient, user: User, app: Flask):
    # given na registered user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # when the user is logged in
    response = login(test_client, user.email, 'password')

    # then the page shows and he can see pages which only can be seen
    # by logged in user
    assert response.status_code == 200
    assert b'Logout' in response.data
    assert b'Your account' in response.data
    assert current_user.email == user.email


def test_home_page_after_logout(user: User, app: Flask):
    # given na registered user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    with app.test_client() as test_client:

        # when the user is logged in and then logout
        login_response = login(test_client, user.email, 'password')
        logout_response = logout(test_client)

        # then the page shows and he can see pages which only can be seen
        # by logged in user
        assert logout_response.status_code == 200
        assert not b'Your account' in logout_response.data
        assert current_user.email != user.email
