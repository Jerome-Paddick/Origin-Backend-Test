from api.app.app_factory import create_app
from api.app.config import DefaultConfig
from api.app.models.core import db

class TestClass:
    @classmethod
    def setup_class(cls):
        cls.app = create_app(DefaultConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def teardown_class(cls):
        db.session.remove()
        cls.app_context.pop()

    def test_main_postgres_connection(self):
        try:
            # to check database we will execute raw query
            db.session.execute('SELECT 1')
            return True
        except Exception as e:
            return False

