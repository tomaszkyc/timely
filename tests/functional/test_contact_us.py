from flask.testing import FlaskClient


def test_page_is_valid(test_client: FlaskClient):
    # given a flask app

    # when we access a page
    response = test_client.get('/contact-us')

    # we should get a valid page
    assert response
    assert response.status_code == 200

    # some text on page
    assert b'Contact us' in response.data
    assert b'Name' in response.data
    assert b'Email' in response.data
    assert b'Message' in response.data
    assert b'Send' in response.data