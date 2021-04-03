from flask.testing import FlaskClient


def test_page_is_valid(test_client: FlaskClient):
    # given a flask app

    # when we access a page
    response = test_client.get('/features')

    # we should get a valid page
    assert response
    assert response.status_code == 200

    # some text on page
    assert b'Features' in response.data