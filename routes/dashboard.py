from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models.transacao import Transacao
from models.categoria import Categoria
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db
from decimal import Decimal

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    
    # Rota para o dashboard do usuário.
    # Exibe um resumo das finanças.
    
    user_id = current_user.id

    # Exemplo: total de receitas e despesas do mês atual
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    receitas_mes_atual = db.session.query(func.sum(Transacao.valor)).filter(
        Transacao.user_id == user_id,
        Transacao.tipo == 'receita',
        Transacao.data >= start_of_month.date(),
        Transacao.data <= end_of_month.date()
    ).scalar() or 0.0

    despesas_mes_atual = db.session.query(func.sum(Transacao.valor)).filter(
        Transacao.user_id == user_id,
        Transacao.tipo == 'despesa',
        Transacao.data >= start_of_month.date(),
        Transacao.data <= end_of_month.date()
    ).scalar() or 0.0

    saldo_mes_atual = Decimal(receitas_mes_atual) - Decimal(despesas_mes_atual)


    # Transações recentes (últimas 5)
    transacoes_recentes = Transacao.query.filter_by(user_id=user_id).order_by(
        Transacao.data.desc(), Transacao.created_at.desc()
    ).limit(5).all()

    # Total por categoria (apenas despesas para simplificar o exemplo)
    despesas_por_categoria = db.session.query(
        Categoria.nome,
        func.sum(Transacao.valor)
    ).join(Transacao).filter(
        Transacao.user_id == user_id,
        Transacao.tipo == 'despesa',
        Transacao.data >= start_of_month.date(),
        Transacao.data <= end_of_month.date()
    ).group_by(Categoria.nome).all()

    return render_template(
        'dashboard/dashboard.html',
        receitas_mes_atual=receitas_mes_atual,
        despesas_mes_atual=despesas_mes_atual,
        saldo_mes_atual=saldo_mes_atual,
        transacoes_recentes=transacoes_recentes,
        despesas_por_categoria=despesas_por_categoria
    )
