## Gerenciador de Finanças Pessoais
### 📋 Descrição do Projeto
Este é um aplicativo web para gerenciamento de finanças pessoais desenvolvido com Python, o framework web Flask e SQLite3 como banco de dados. Ele permite que usuários registrem receitas e despesas, categorizem suas transações e visualizem um resumo financeiro, incluindo uma previsão básica de gastos futuros.

O objetivo principal é oferecer uma ferramenta simples e eficiente para que indivíduos acompanhem suas finanças, entendam seus padrões de gastos e planejem melhor o futuro.

### ✨ Funcionalidades
Autenticação de Usuário: Registro e login seguros de usuários.

Gerenciamento de Transações:

Adicionar novas receitas e despesas.

Visualizar todas as transações de forma organizada.

Editar e excluir transações existentes.

Categorização:

Criar e gerenciar categorias personalizadas para receitas e despesas (ex: "Alimentação", "Salário", "Transporte").

Dashboard Interativo:

Visão geral das finanças do mês atual (receitas, despesas, saldo).

Listagem das últimas transações.

Resumo de despesas por categoria.

Previsão de Gastos:

Uma funcionalidade de previsão básica que estima gastos futuros com base no histórico de despesas por categoria.

### 🚀 Tecnologias Utilizadas
Backend:

Python (versão 3.9+)

Flask - Micro-framework web

Flask-SQLAlchemy - ORM para interação com o banco de dados

SQLAlchemy - Toolkit Python SQL e ORM

Flask-Login - Gerenciamento de sessões de usuário

Werkzeug - Utilitários para hashing de senhas

Python-Dotenv - Para carregar variáveis de ambiente

Banco de Dados:

SQLite3 - Banco de dados leve baseado em arquivo

Frontend:

HTML5

CSS3

Tailwind CSS - Framework CSS utilitário para estilização rápida

Jinja2 - Motor de templates do Flask

JavaScript (básico)

### ⚙️ Configuração e Instalação
Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

Pré-requisitos
Python 3.9+ instalado.

pip (gerenciador de pacotes do Python) instalado.

Passos
Clone o Repositório:
Abra seu terminal ou prompt de comando e clone o projeto:

    git clone https://github.com/seu-usuario/gerenciador-financas.git
    cd gerenciador-financas


Crie um Ambiente Virtual (Recomendado):
É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

    python -m venv venv

Ative o Ambiente Virtual:

Windows:

    .\venv\Scripts\activate

macOS/Linux:

    source venv/bin/activate

Instale as Dependências:
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no requirements.txt:

    pip install -r requirements.txt

Configuração do Banco de Dados (SQLite3):
O SQLite3 é um banco de dados baseado em arquivo, o que significa que ele não precisa de um servidor separado rodando. O arquivo do banco de dados (app.db por padrão) será criado automaticamente na raiz do projeto quando você rodar o aplicativo pela primeira vez, graças à linha db.create_all() no app.py.

Verifique config.py:
Certifique-se de que a linha SQLALCHEMY_DATABASE_URI no seu arquivo config.py está apontando para o SQLite3. Deverá ser algo como:

    config.py
    import os

    class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura'
        # Configuração para SQLite3
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        TEMPLATES_FOLDER = 'templates'
        STATIC_FOLDER = 'static'

(A SECRET_KEY é importante para a segurança das sessões. É recomendável que você a defina como uma variável de ambiente em produção ou em um arquivo .env para desenvolvimento).

### ▶️ Como Executar o Aplicativo
Com todas as dependências instaladas e o ambiente virtual ativado:

Defina a variável de ambiente FLASK_APP:

    export FLASK_APP=app.py  # No Windows, use 'set FLASK_APP=app.py'

Execute o aplicativo Flask:

    flask run

Ou, como no seu app.py, você pode simplesmente:

    python app.py

Acesse no Navegador:
Abra seu navegador web e acesse o endereço fornecido no terminal (geralmente http://127.0.0.1:5000/).