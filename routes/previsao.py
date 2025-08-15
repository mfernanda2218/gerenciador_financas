from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from services.previsao_service import PrevisaoService
from models.transacao import Transacao
from models.categoria import Categoria
from datetime import datetime, timedelta
from sqlalchemy import func

previsao_bp = Blueprint('previsao', __name__)

@previsao_bp.route('/gastos_futuros', methods=['GET'])
@login_required
def gastos_futuros():
    """
    Rota para exibir a previsão de gastos futuros.
    Calcula a média de gastos dos últimos X meses por categoria
    e projeta para o próximo mês.
    """
    user_id = current_user.id
    # Obtém todas as transações de despesa do usuário
    transacoes = Transacao.query.filter_by(user_id=user_id, tipo='despesa').all()
    categorias = Categoria.query.filter_by(user_id=user_id).all()

    previsao_service = PrevisaoService(transacoes, categorias)
    previsao_por_categoria = previsao_service.prever_gastos_proximo_mes()

    return render_template('previsao/gastos_futuros.html', previsao=previsao_por_categoria)
