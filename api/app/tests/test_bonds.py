from api.app.models.core import db
from api.app.app_factory import create_app
from api.app.config import TestConfig
from api.app.models.user import Users
from api.app.models.bonds import Bonds
from flask import current_app
from psycopg2.errors import UniqueViolation

def populate_test_db(db):
    user_1 = Users(
        id=1,
        email="test_1@test.com"
    )
    user_1.set_hashed_password('testtest')
    user_2 = Users(
        id=2,
        email="test_2@test.com"
    )
    user_2.set_hashed_password('testtest')
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    bond_1 = Bonds(
        user_id = 1,
        isin="TEST1",
        size=100,
        currency="EUR",
        maturity="1970-01-01",
        legal_name="TEST_LEI_1"
    )
    bond_2 = Bonds(
        user_id = 2,
        isin="TEST2",
        size=1000,
        currency="EUR",
        maturity="1970-01-02",
        legal_name="TEST_LEI_2"
    )
    db.session.add(bond_1)
    db.session.commit()
    db.session.add(bond_2)
    db.session.commit()


class TestClass:
    def setup_class(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        try:
            populate_test_db(db)
        except UniqueViolation:
            db.session.remove()
            db.drop_all()
            db.session.commit()

        print ('\nsetup_class()')

    @classmethod
    def teardown_class(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        print ('teardown_class()')

    # def setup_method(self, method):
    #     print ('\nsetup_method()')
    #
    # def teardown_method(self, method):
    #     print ('\nteardown_method()')

    def generate_jwt(self, user):
        with current_app.test_client() as c:
            if user == 1:
                jwt = c.post('/api/login',
                              content_type='application/json',
                              json={'email': 'test_1@test.com', 'password': 'testtest'},
                              ).json.get('jwt_token')
            if user == 2:
                jwt = c.post('/api/login',
                             content_type='application/json',
                             json={'email': 'test_2@test.com', 'password': 'testtest'},
                             ).json.get('jwt_token')
            return jwt

    def test_get_user_1_bonds(self):
        """ tests bonds api with user 1 """
        with current_app.test_client() as c:
            user_1_jwt = self.generate_jwt(1)
            response = c.get('/api/bonds', query_string=dict(api_key=user_1_jwt))
            assert response.json.get('data') == [{'id': 1,
                                                  'isin':'TEST1',
                                                  'size': 100,
                                                  'currency': 'EUR',
                                                  'maturity': '1970-01-01',
                                                  'legal_name': 'TEST_LEI_1'}]
    def test_get_user_2_bonds(self):
        """ tests bonds api with user 2 """
        with current_app.test_client() as c:
            user_2_jwt = self.generate_jwt(2)
            response = c.get('/api/bonds', query_string=dict(api_key=user_2_jwt))
            assert response.json.get('data') == [{'id': 2,
                                                  'isin': 'TEST2',
                                                  'size': 1000,
                                                  'currency': 'EUR',
                                                  'maturity': '1970-01-02',
                                                  'legal_name': 'TEST_LEI_2'}]

    def test_get_user_2_bonds_w_filter(self):
        """ tests bonds api with user 2 with matching filter """
        with current_app.test_client() as c:
            user_2_jwt = self.generate_jwt(2)
            response = c.get('/api/bonds', query_string=dict(api_key=user_2_jwt,
                                                             legal_name='TEST_LEI_2'))
            assert response.json.get('data') == [{'id': 2,
                                                  'isin': 'TEST2',
                                                  'size': 1000,
                                                  'currency': 'EUR',
                                                  'maturity': '1970-01-02',
                                                  'legal_name': 'TEST_LEI_2'}]

    def test_get_user_2_bonds_w_fail_filter(self):
        """ tests bonds api with user 2 with non-matching filter """
        with current_app.test_client() as c:
            user_2_jwt = self.generate_jwt(2)
            response = c.get('/api/bonds', query_string=dict(api_key=user_2_jwt,
                                                             legal_name='DOESNT_CORRESPOND_TO_ANYTHING'))
            print(response.json.get('data'))
            assert response.json.get('data') == []


