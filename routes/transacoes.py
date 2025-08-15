from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.transacao import Transacao
from models.categoria import Categoria
from datetime import datetime, date

transacoes_bp = Blueprint('transacoes', __name__)

@transacoes_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required

def adicionar_transacao():
    """
    Rota para adicionar uma nova transação (receita ou despesa).
    """
    user_id = current_user.id
    categorias = Categoria.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')
        tipo = request.form.get('tipo')
        categoria_id = request.form.get('categoria_id')

        # Converte valores e valida
        try:
            valor = float(valor)
        except (ValueError, TypeError):
            flash('O valor informado é inválido.', 'danger')
            return render_template('transacoes/adicionar.html', categorias=categorias, data_hoje=date.today().strftime("%Y-%m-%d"))

        # Converte a string de data para objeto date
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            flash('A data informada é inválida.', 'danger')
            return render_template('transacoes/adicionar.html', categorias=categorias, data_hoje=date.today().strftime("%Y-%m-%d"))

        # Validações básicas
        if not descricao or not valor or not data_str or not tipo:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('transacoes/adicionar.html', categorias=categorias, data_hoje=date.today().strftime("%Y-%m-%d"))

        # Se a categoria for "Nenhuma", defina categoria_id como None
        if categoria_id == 'none':
            categoria_id = None
        else:
            categoria_id = int(categoria_id)

        nova_transacao = Transacao(
            descricao=descricao,
            valor=valor,
            data=data,
            tipo=tipo,
            user_id=user_id,
            categoria_id=categoria_id
        )
        db.session.add(nova_transacao)
        db.session.commit()
        flash('Transação adicionada com sucesso!', 'success')
        return redirect(url_for('transacoes.listar_transacoes'))

    # Passa a data atual para o template
    return render_template(
        'transacoes/adicionar.html',
        categorias=categorias,
        data_hoje=date.today().strftime("%Y-%m-%d")
    )

@transacoes_bp.route('/listar')
@login_required
def listar_transacoes():
    """
    Rota para listar todas as transações do usuário.
    """
    user_id = current_user.id
    # Busca todas as transações, ordenadas por data e criação
    transacoes = Transacao.query.filter_by(user_id=user_id).order_by(
        Transacao.data.desc(), Transacao.created_at.desc()
    ).all()

    return render_template('transacoes/listar.html', transacoes=transacoes)

@transacoes_bp.route('/editar/<int:transacao_id>', methods=['GET', 'POST'])
@login_required
def editar_transacao(transacao_id):
    """
    Rota para editar uma transação existente.
    """
    transacao = Transacao.query.get_or_404(transacao_id)
    # Garante que apenas o proprietário da transação possa editá-la
    if transacao.user_id != current_user.id:
        flash('Você não tem permissão para editar esta transação.', 'danger')
        return redirect(url_for('transacoes.listar_transacoes'))

    categorias = Categoria.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        transacao.descricao = request.form.get('descricao')
        transacao.valor = float(request.form.get('valor'))
        transacao.data = datetime.strptime(request.form.get('data'), '%Y-%m-%d').date()
        transacao.tipo = request.form.get('tipo')
        categoria_id = request.form.get('categoria_id')
        transacao.categoria_id = int(categoria_id) if categoria_id != 'none' else None

        db.session.commit()
        flash('Transação atualizada com sucesso!', 'success')
        return redirect(url_for('transacoes.listar_transacoes'))

    return render_template('transacoes/editar.html', transacao=transacao, categorias=categorias)

@transacoes_bp.route('/excluir/<int:transacao_id>', methods=['POST'])
@login_required
def excluir_transacao(transacao_id):
    """
    Rota para excluir uma transação.
    """
    transacao = Transacao.query.get_or_404(transacao_id)
    # Garante que apenas o proprietário da transação possa excluí-la
    if transacao.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta transação.', 'danger')
        return redirect(url_for('transacoes.listar_transacoes'))

    db.session.delete(transacao)
    db.session.commit()
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('transacoes.listar_transacoes'))

# Rotas de Categoria (opcional, pode ser movido para um blueprint separado se ficar grande)
@transacoes_bp.route('/categorias/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_categoria():
    """
    Rota para adicionar uma nova categoria.
    """
    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo = request.form.get('tipo') # 'receita' ou 'despesa'

        if not nome or not tipo:
            flash('Nome e tipo da categoria são obrigatórios!', 'danger')
            return render_template('transacoes/adicionar_categoria.html')

        new_category = Categoria(nome=nome, tipo=tipo, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('transacoes.listar_categorias')) # Redireciona para listar categorias

    return render_template('transacoes/adicionar_categoria.html')

@transacoes_bp.route('/categorias/listar')
@login_required
def listar_categorias():
    """
    Rota para listar todas as categorias do usuário.
    """
    categorias = Categoria.query.filter_by(user_id=current_user.id).all()
    return render_template('transacoes/listar_categorias.html', categorias=categorias)
