from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from .models.core import db
from .cli.commands import populate_database, clear_database
from flask_restful_swagger import swagger
import click
from .config import DefaultConfig

migrate = Migrate()

def create_app(config=DefaultConfig):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    # app.config.from_pyfile(config)

    db.init_app(app)
    app.db = db     # so we can call current_app.db from any resource

    migrate.init_app(app, db)

    # api = Api(app)

    @app.cli.command()
    def populate_db():
        """ Initialize the database. """
        populate_database()
        click.echo('Successfully Populated DB')

    @app.cli.command()
    def clear_db():
        """ Clear the database. """
        clear_database()
        click.echo('Successfully Cleared DB')

    # Swagger flask restful API:
    # https://github.com/rantav/flask-restful-swagger
    api = swagger.docs(
        Api(app),
        apiVersion='1.0',
        api_spec_url='/api/api_documentation',
        swaggerVersion='3.0',
        description='API'
    )

    from flask_restful import reqparse, Resource
    class StatusResource(Resource):
        def get(self):
            """ Check API Running """
            return {'status': 'OK', 'message': 'Connected to API'}, 200

    api.add_resource(StatusResource, '/api/status')

    from .resources.users import Login
    api.add_resource(Login, '/api/login')

    from .resources.users import Register
    api.add_resource(Register, '/api/register')

    from .resources.bonds import BondsResource
    api.add_resource(BondsResource, '/api/bonds')


    return app
