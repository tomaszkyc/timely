import logging
import os

import flask_migrate
import yaml
from flask import Flask, render_template, current_app
from flask_migrate import Migrate
from flask_restful import Api

from app.api import initialize_routes
from app.api.schemas import ma
from app.auth.views import auth
from app.config import app_config
from app.main.views import main
from app.models import db, CountdownResult, Cite, User
from app.tools.mail import mail

migrate = Migrate()
api = Api()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def _initial_app_setup(app_instance):
    try:
        with app_instance.app_context():
            app_instance.logger.info('Trying to do initial app setup.')
            add_initial_cites(app_instance)
            _add_test_user(app_instance)
            db.session.commit()
            app_instance.logger.info('Initial app setup finished successfully.')
    except Exception as e:
        app_instance.logger.error('There was an exception '
                          'during app initialization: %s', e)


def _add_test_user(app_instance):
    """Adds a sample test user to application."""
    number_of_users = User.query.count()
    user_email = app_instance.config['TEST_USER_EMAIL']
    user_name = app_instance.config['TEST_USER_NAME']
    user_password = app_instance.config['TEST_USER_PASSWORD']
    if number_of_users == 0:
        app_instance.logger.info('Adding a sample user.')
        user = User(user_email, user_password, user_name, True)
        user.activated = True
        db.session.add(user)
        app_instance.logger.info('Sample user added successfully.')


def add_initial_cites(app_instance):
    """Add initial cites when there is no cites in db."""
    number_of_cites = Cite.query.count()
    if number_of_cites == 0:
        app_instance.logger.info('There is no cites in db. Trying to add sample cites.')
        sample_cites_filepath = os.path.join(app_directory, 'sample_cites.yaml')
        app_instance.logger.info('Sample cites filepath: %s', sample_cites_filepath)
        with open(sample_cites_filepath, encoding='utf8') as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content:
                cites = yaml_content.get('cites')
            else:
                cites = []
        import app.models
        for cite in [app.models.Cite(cite_text) for cite_text in cites]:
            db.session.add(cite)
            db.session.commit()
        app_instance.logger.info('Sample cites added correctly.')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    _register_extensions(app)
    _register_blueprints(app)

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': db}

    @app.errorhandler(Exception)
    def handle_exception(e):
        current_app.logger.error(e)
        return render_template('_error_page.html')

    # init db
    _upgrade_db(app)

    # do some initial app setup
    _initial_app_setup(app)
    return app


def _register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    api = Api(app)
    initialize_routes(api)
    ma.init_app(app)
    mail.init_app(app)


def _register_blueprints(app: Flask):
    app.register_blueprint(main)
    app.register_blueprint(auth)


def _upgrade_db(app: Flask):
    with app.app_context():

        is_app_testing = app.config['TESTING']
        if is_app_testing:
            print('App in testing mod. Will drop and create all tables')
            db.session.remove()
            db.drop_all()
            db.session.commit()
            db.create_all()
            db.session.commit()

        print('Trying to upgrade the database')
        print('Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])
        try:
            flask_migrate.upgrade(directory=(os.path.join(app_directory, 'migrations')))
        except Exception as e:
            print('There was an error during migration:', e)
        print('Database upgraded successfully')
