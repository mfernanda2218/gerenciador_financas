from app import db
from datetime import datetime

class Categoria(db.Model):
    """
    Modelo de dados para a tabela de Categorias de transações (Ex: Alimentação, Transporte).
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(20), nullable=False) # 'receita' ou 'despesa'
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com Transacao (uma categoria pode ter muitas transações)
    transacoes = db.relationship('Transacao', backref='category', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nome} ({self.tipo})>'
