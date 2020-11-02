from .core import db

class Bonds(db.Model):
    __tablename__ = 'bonds'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isin = db.Column(db.String(64), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(16), nullable=False)
    maturity = db.Column(db.DateTime(True), nullable=False)
    legal_name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)