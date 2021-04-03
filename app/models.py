from datetime import datetime

import pytz
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, and_
from werkzeug.security import generate_password_hash, check_password_hash

from app.tools.auth import generate_token, generate_hash, _check_token

db = SQLAlchemy(app=None, session_options={
    'expire_on_commit': False
})


class Cite(db.Model):
    """Model represents sample cite which is shown
    on the main app page."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Cite(id={self.id}, cite={self.text})"


class User(db.Model):
    """User model which is used application-wide."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_success_login = db.Column(db.DateTime, nullable=True)
    last_failure_login = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password_reset_token = db.Column(db.String(255), nullable=True)
    password_reset_hash = db.Column(db.String(255), nullable=True)
    password_reset_sent_at = db.Column(db.DateTime, nullable=True)
    activation_token = db.Column(db.String(255), nullable=True)
    activation_hash = db.Column(db.String(255), nullable=True)
    activation_sent_at = db.Column(db.DateTime, nullable=True)
    activated = db.Column(db.Boolean(), default=False)
    countdown_activities = db.relationship('CountdownResult', backref='user', lazy=True)

    def __init__(self, email='', password='', name='', admin=False):
        self.email = email
        self.password = generate_password_hash(password)
        self.name = name
        self.registered_on = datetime.utcnow()
        self.admin = admin

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"

    def create_token_for(self, token_type):
        """Creates a token for given attribute name."""
        if token_type not in ['password_reset', 'activation']:
            raise ValueError('Cannot create a token for given token type: %s' % token_type)

        setattr(self, token_type + "_token", generate_token())
        setattr(self, token_type + "_hash", generate_hash(getattr(self, token_type + "_token")))
        setattr(self, token_type + "_sent_at", datetime.utcnow())
        db.session.add(self)

    def activate_user_account(self, token):
        """Checks whether the given token is valid and and
           was generated earlier than 2 days ago."""
        days_from_sending_activation = (datetime.utcnow() - self.activation_sent_at).total_seconds() / 60 / 60 / 24
        if _check_token(self.activation_hash, token) and days_from_sending_activation < 2:
            self.activated = True
            self.activation_hash = ''
            db.session.add(self)
            return True
        return False

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_anonymous(self):
        """Checks if user is anonymous (not authenticated)."""
        return '' == self.email

    def is_authenticated(self):
        """Checks if user is authenticated."""
        return not self.is_anonymous()

    def check_password_reset_token(self, token):
        """Checks whether the given password token is valid and and
           was generated earlier than 30 minutes ago."""
        minutes_from_sending_reset = (datetime.utcnow() - self.password_reset_sent_at).total_seconds() / 60
        if _check_token(self.password_reset_hash, token) and minutes_from_sending_reset < 30:
            return True
        return False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @staticmethod
    def is_user_with_email_exist(email):
        """Checks in db user by specified email.

        Returns True if user with given mail exists. False otherwise.
        """
        return User.query.filter_by(email=email).count() != 0


class CountdownResult(db.Model):
    """Class contains countdown result - a main object of an app."""
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime, nullable=False)
    finish_date = db.Column(db.DateTime, nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, start_date, finish_date, success, user_id):
        self.start_date = as_utc_date(start_date)
        self.finish_date = as_utc_date(finish_date)
        self.success = success
        self.user_id = user_id

    def __repr__(self):
        return f"CountdownResult(id={self.id}, start_date={self.start_date}, finish_date={self.finish_date}," \
               f" success={self.success}, user_id={self.user_id})"

    @staticmethod
    def find_by_query_parameter(filters, current_user_id):
        """Finds a countdown results by given filters and current user id."""
        query = CountdownResult.query

        # adding WHERE clause
        where_clauses = list()
        where_clauses.append(CountdownResult.user_id == current_user_id)
        if filters['filter']['countdown_status'] != 'all':
            where_clauses.append(
                CountdownResult.success == (True if filters['filter']['countdown_status'] == 'success' else False))
        if filters['filter']['start_date']:
            where_clauses.append(CountdownResult.start_date >= filters['filter']['start_date'])
        if filters['filter']['finish_date']:
            where_clauses.append(CountdownResult.finish_date <= filters['filter']['finish_date'])
        query = query.filter(and_(*where_clauses))

        # adding ORDER BY
        if filters['sorters']:
            order_by_clauses = ''
            for sorter in filters['sorters']:
                key = sorter['property_name']
                order = sorter['order']
                db_column = get_db_column(key)
                order_by_clause = f"{db_column} {order},"
                order_by_clauses += order_by_clause
            order_by_clauses = order_by_clauses[:-1]
            query = query.order_by(text(order_by_clauses))

        # adding pagination
        query = query.paginate(filters['page'], filters['page_size'], False)

        # here we're returning data for current page
        # and total number of items matching query
        return query.items, query.total

    @staticmethod
    def delete_all_by_user_id(user_id):
        """Deletes all countdown results which belong to given user id."""
        CountdownResult.query.filter(CountdownResult.user_id == user_id).delete()


def get_db_column(key):
    """Returns a db column associated with sorter."""
    return {
        'startDate': 'start_date',
        'finishDate': 'finish_date',
        'success': 'success'
    }[key]


def as_utc_date(date: datetime):
    print(date)
    return date