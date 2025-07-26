from flask_login.login_manager import LoginManager
from flask_login.utils import login_fresh, login_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
from flask_login import UserMixin
from wtforms.validators import email


# Instância do Banco de Dados
db = SQLAlchemy()





  

# Faz a verificação do banco de dados e cria, caso não exista
def configurar_banco(app):
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancodedados.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  # Cria o banco de dados se ele não existir
  with app.app_context():
      db.create_all()
      # Verifica se a tabela 'categoria' esta vazia
      if not db.session.query(Categoria).first():
          # Se estiver vazia, adiciona as categorias padrão
          categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Brinquedos', 'Livros', 'Outros']
          for nome in categorias:
              db.session.add(Categoria(nome=nome))
          db.session.commit()

      return db


def gerar_uuid():
  return uuid4().hex

produto_categoria = db.Table('produto_categoria',
  db.Column('produto_id', db.String(32), db.ForeignKey('produtos.id'), primary_key=True),
  db.Column('categoria_id', db.String(32), db.ForeignKey('categorias.id'), primary_key=True)
)

  

class Login(UserMixin, db.Model):
  __tablename__ = 'login'
  id = db.Column(db.String(32), primary_key=True, default=gerar_uuid)
  username = db.Column(db.String(50), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False,)
  password = db.Column(db.String(255), nullable=False)
  
  def __init__(self, username, email , password):
    self.username = username
    self.password = password
    self.email = email
    
      
class Categoria(db.Model):
  __tablename__ = 'categorias'
  id = db.Column(db.String(32), primary_key=True, default=gerar_uuid)
  nome = db.Column(db.String(255), nullable=False)
  produtos = db.relationship('Produto', secondary=produto_categoria, back_populates='categorias')
  def __init__(self, nome):
    self.nome = nome

  def __str__(self):
    return self.nome

class Produto(db.Model):
  # Modelo que representa os produtos do banco de dados
  __tablename__ = 'produtos'
  id = db.Column(db.String(32), primary_key=True, default=gerar_uuid)
  nome = db.Column(db.String(255), nullable=False)
  descricao = db.Column(db.Text, nullable=False)
  preco = db.Column(db.Float, nullable=False)
  categorias = db.relationship('Categoria', secondary=produto_categoria, back_populates='produtos')
  imagem = db.Column(db.String(255), nullable=False)
  data_criacao = db.Column(db.DateTime, default=datetime.now)
  estoque = db.Column(db.Integer, nullable=False)

  def __init__(self, nome, descricao, preco, imagem, data_criacao, estoque):
    self.nome = nome
    self.descricao = descricao
    self.preco = preco
    self.imagem = imagem
    self.data_criacao = data_criacao
    self.estoque = estoque