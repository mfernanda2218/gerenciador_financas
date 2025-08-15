import os

class Config:
    """
    Classe de configuração para o aplicativo Flask.
    Define a URI do banco de dados e a chave secreta.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura'
    # Configuração do SQLite3:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'financas_db.sqlite3')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desativa o rastreamento de modificações para economizar memória
    # Define o diretório para templates e static files (já são padrão, mas bom ter aqui)
    TEMPLATES_FOLDER = 'templates'
    STATIC_FOLDER = 'static'