from app import db
from datetime import datetime

class Transacao(db.Model):
    """
    Modelo de dados para a tabela de Transações financeiras (receitas e despesas).
    """
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False) # Armazena valores monetários com 2 casas decimais
    data = db.Column(db.Date, nullable=False, default=datetime.now().date())
    tipo = db.Column(db.String(20), nullable=False) # 'receita' ou 'despesa'
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True) # Pode não ter categoria
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transacao {self.descricao} - {self.valor}>'
