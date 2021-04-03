from datetime import datetime

import pytest

from app import create_app
from app.models import User, db, CountdownResult, Cite


test_user_email = 'some_random_user@domain.com'


@pytest.fixture(scope='function')
def user():
    user = User(test_user_email, 'password', 'Tomas', False)
    return user


@pytest.fixture(scope='function')
def countdown_result():
    countdown_result = CountdownResult(datetime.fromisoformat('2021-01-01'),
                                       datetime.fromisoformat('2021-01-02'), True, None)
    return countdown_result


@pytest.fixture(scope='function')
def countdown_result_filters():
    filters = {'filter': {'countdown_status': 'all', 'start_date': None, 'finish_date': None},
               'sorters': None,
               'page': 1,
               'page_size': 1000}
    return filters


@pytest.fixture(scope='function')
def cite():
    cite = Cite('Some important and brilliant cite text.')
    return cite


@pytest.fixture(scope='function')
def app(user):
    app = create_app('testing')
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return app  # Note that we changed return for yield, see below for why


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password,
        csrf_token=''
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)
