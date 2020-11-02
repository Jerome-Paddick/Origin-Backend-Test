from .core import db
import bcrypt

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_hashed_password(self, plain_text_password):
        # password hash is actually the cost, salt, and cipher text concatenated,
        # all have known lengths and can be retrieved easily
        self.password_hash = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

    def check_password(self, plain_text_password):
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), self.password_hash.encode('utf-8'))

