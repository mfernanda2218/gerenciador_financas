from database import db  # Importe 'db' do novo arquivo extensions.py
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    # O restante do seu modelo de dados permanece o mesmo
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    categorias = db.relationship('Categoria', backref='owner', lazy=True)
    transacoes = db.relationship('Transacao', backref='user', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False