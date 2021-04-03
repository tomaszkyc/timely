from flask import Flask
from flask.testing import FlaskClient

from app.models import User, db
from tests.conftest import login


def test_show_page_without_logging_in(test_client: FlaskClient):
    # given a flask app

    # when we access a page
    response = test_client.get('/activities')

    # we should get a valid page
    assert response
    assert response.status_code == 200

    # some text on page
    assert b'Your activities' in response.data

    # shouldn't see a button to sync data to db
    assert not b'sync-countdown-results-btn' in response.data


def test_show_page_after_logging_in(user: User, app: Flask):
    # given na registered user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    with app.test_client() as test_client:
        # when the user is logged in and go to acivities page
        login_response = login(test_client, user.email, 'password')
        response = test_client.get('/activities')

        # then on the page we can see additional button to sync
        # and we get a valid page
        assert response
        assert response.status_code == 200
        # some text on page
        assert b'Your activities' in response.data

        # should see a button to sync data to db
        assert b'sync-countdown-results-btn' in response.data
