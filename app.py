from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from flask_moment import Moment # Já está importado!
from database import db

def create_app():
    # Inicializa o Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Isso injeta a variável 'moment' nos seus templates Jinja.
    moment = Moment(app)
    
    # Inicializa o SQLAlchemy e o Flask-Login com o app
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Importa e registra os Blueprints (rotas)
    # Essas importações precisam ocorrer DEPOIS que 'app' e 'db' são inicializados
    # para evitar problemas de importação circular.
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transacoes import transacoes_bp
    from routes.previsao import previsao_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transacoes_bp, url_prefix='/transacoes')
    app.register_blueprint(previsao_bp, url_prefix='/previsao')

    @login_manager.user_loader
    def load_user(user_id):
        # Importação local para evitar o ciclo, garantindo que 'Usuario'
        # seja carregado após 'db' ser inicializado.
        from models.usuario import Usuario 
        return Usuario.query.get(int(user_id))

    # Importa os modelos aqui para que o Flask-SQLAlchemy possa encontrá-los
    # (importação para garantir que os modelos sejam registrados antes de db.create_all())
    from models import usuario, categoria, transacao

    # Rota padrão para redirecionar para o dashboard ou login
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('auth.login'))
        
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Cria as tabelas do banco de dados (se não existirem)
        # Isso deve ser feito DENTRO do contexto da aplicação.
        db.create_all() 
    app.run(debug=True)