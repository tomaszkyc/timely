import pytest
from flask import Flask
from werkzeug.security import check_password_hash

from app.models import User, db, CountdownResult, get_db_column, Cite
from app.tools.auth import _check_token
from tests.conftest import test_user_email


def test_new_user(user, app: Flask):
    """Testing new user creation"""

    # given a user model

    # when user is created
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        # then the email, password, name and admin role are set correctly
        assert user.email == test_user_email
        assert user.password != 'password'
        assert check_password_hash(user.password, 'password')
        assert user.name == 'Tomas'
        assert not user.admin


def test_new_password_reset_token_creation(user: User, app: Flask):
    # given a user model

    with app.app_context():
        # when a new token is created
        user.create_token_for('password_reset')
        db.session.add(user)
        db.session.commit()

        # then the fields connected with token should be set correctly
        assert user.password_reset_token != ''
        assert _check_token(user.password_reset_hash, user.password_reset_token)
        assert user.password_reset_sent_at


def test_new_activation_account_token_creation(user: User, app: Flask):
    # given a user model

    with app.app_context():
        # when a token is created
        user.create_token_for('activation')
        db.session.add(user)
        db.session.commit()

        # then fields associated with token shoud be set
        assert user.activation_token != ''
        assert _check_token(user.activation_hash, user.activation_token)
        assert user.activation_sent_at


def test_activation_account_by_token(user: User, app: Flask):
    # given a user model

    with app.app_context():
        # when a token is created
        user.create_token_for('activation')
        db.session.add(user)
        db.session.commit()

        # then activation function should return true
        assert user.activate_user_account(user.activation_token)
        assert user.activated


def test_check_user_password(user: User, app: Flask):
    # given a user model

    actual_user_password = 'password'

    # when we create a user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        # we can should get a True from checking password function
        assert user.check_password(actual_user_password)


def test_user_repr(user: User, app: Flask):
    # given a user model

    # when we create a user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        # then the repr should be equal to this
        assert repr(user) == 'User(id=2, email=%s)' % test_user_email


def test_if_user_exist_with_valid_email(user: User, app: Flask):
    # given a user model

    # when we create a user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        # then the repr should be equal to this
        assert User.is_user_with_email_exist(user.email)


def test_if_user_not_exist_with_nonvalid_email(user: User, app: Flask):
    # given a user model

    # when we create a user
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        # then the repr should be equal to this
        assert not User.is_user_with_email_exist('non-existing-email-in-db@x.com')


def test_user_is_setting_a_new_password(user: User, app: Flask):
    # given a user model

    # when we create a user and setting a new password to existing one
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        new_password = 'Silly-password'
        user.set_password(new_password)

        # then the new password hash will be valid
        assert user.check_password(new_password)


def test_user_check_valid_password_reset_token(user: User, app: Flask):
    # given a user model

    # when we create a user and setting a new password to existing one
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        user.create_token_for('password_reset')
        db.session.commit()

        # then the new password hash will be valid
        assert user.check_password_reset_token(user.password_reset_token)


# Below CountdownResult class tests


def test_create_countdown_result(user: User, app: Flask, countdown_result: CountdownResult):
    # given a user model and countdown result model

    # when we create a countdown result entry
    with app.app_context():
        db.session.add(user)
        countdown_result.user_id = user.id
        db.session.add(countdown_result)
        db.session.commit()

        # all fields should be filled
        assert countdown_result.id
        assert countdown_result.start_date
        assert countdown_result.finish_date
        assert countdown_result.start_date < countdown_result.finish_date
        assert countdown_result.success
        assert countdown_result.user_id == user.id


def test_countdown_result_repr_function(countdown_result: CountdownResult, app: Flask, user: User):
    # given a model

    # when we call a repr function
    with app.app_context():
        db.session.add(user)
        countdown_result.user_id = user.id
        db.session.add(countdown_result)
        db.session.commit()

        # we will get a valid string
        assert repr(countdown_result) == 'CountdownResult(id=1, start_date=2021-01-01 00:00:00,' \
                                         ' finish_date=2021-01-02 00:00:00, success=True, user_id=2)'


def test_countdown_result_find_by_valid_query_parameters(countdown_result_filters: dict, user: User, app: Flask,
                                                         countdown_result: CountdownResult):
    # given a model

    # when we add some countdown results to db
    with app.app_context():
        db.session.add(user)
        countdown_result.user_id = user.id
        db.session.add(countdown_result)
        db.session.commit()

        # we can find them by user id
        countdown_results, number_of_elements = CountdownResult.find_by_query_parameter(countdown_result_filters,
                                                                                        user.id)
        assert number_of_elements == 1
        assert countdown_results


def test_countdown_result_delete_all_for_user(user: User, app: Flask, countdown_result: CountdownResult):
    # given a model

    # when we add some countdown results to db and then delete
    with app.app_context():
        db.session.add(user)
        countdown_result.user_id = user.id
        db.session.add(countdown_result)
        db.session.commit()
        number_of_records_before_removal = CountdownResult.query.count()
        CountdownResult.delete_all_by_user_id(user.id)
        db.session.commit()

        # there should be no records left
        assert CountdownResult.query.count() == 0
        assert number_of_records_before_removal != CountdownResult.query.count()


def test_countdown_results_find_db_column():
    # given a model

    # when we have some countdown results filter key
    filter_keys = ['startDate', 'finishDate', 'success']

    # they should be found
    for key in filter_keys:
        assert get_db_column(key)


def test_countdown_results_doesnt_find_db_column():
    # given a model

    # when we have some countdown results filter key which are non valid
    filter_keys = ['randomValue', 'DROP TABLE users;', 'SELECT * FROM USER']

    # they should raise an KeyError because we didn't define them
    for key in filter_keys:
        with pytest.raises(KeyError):
            get_db_column(key)


# Below Cite class tests


def test_cite_creation(cite: Cite, app: Flask):
    # given a model

    # when we create a cite and save in db
    with app.app_context():
        db.session.add(cite)
        db.session.commit()

        # all fields should be set
        assert cite.id
        assert cite
        assert cite.text == 'Some important and brilliant cite text.'


def test_cite_repr_format(cite: Cite, app: Flask):
    # given a model

    # when we create a cite and save in db
    with app.app_context():
        db.session.add(cite)
        db.session.commit()

        # all fields should be set
        number_of_cites = Cite.query.count()
        assert repr(cite) == 'Cite(id=%d, cite=Some important and brilliant cite text.)' % number_of_cites
