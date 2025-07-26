from warnings import WarningMessage
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
from flask_wtf import FlaskForm, form
from wtforms import PasswordField, StringField, TextAreaField, FloatField, IntegerField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from bancodedados import Categoria, db, Produto, configurar_banco, Login 
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets, os
from uuid import uuid4
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(64)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = configurar_banco(app)

def resgatar_categorias():
    categorias = Categoria.query.all()
    lista = []
    for categoria in categorias:
        lista.append((categoria.id, categoria.nome))
    return lista

def resgatar_produtos():
    produtos = Produto.query.all()
    lista = []
    for produto in produtos:
        lista.append((produto.id, produto.nome))
    return lista
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    remember_me = SubmitField('Remember Me')
    submit = SubmitField('Login') 

# Trazendo as informações digitadas pelo usuario na página de adicionar
class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=255)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco = FloatField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    categoria = SelectField('Categoria', coerce=str, validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg','png','svg','jpeg','gif'], 'Apenas imagens são permitidas!')])
    data_criacao = DateField('Data de Criação', validators=[DataRequired()])
    estoque = IntegerField('Estoque', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Salvar')

class CategoriaForm(FlaskForm):
    produto = SelectField('Produto', coerce=str, validators=[DataRequired()])
    categoria = SelectField('Categoria', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Salvar')




@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(user_id)

@app.route('/busca',endpoint='busca')
def busca():
    termo = request.args.get('termo')
    if not termo:
         return render_template("busca.html", produtos=[])
    produtos = Produto.query.filter(Produto.nome.contains(termo)).all()
    return render_template("busca.html", produtos=produtos)

@app.route('/gore')
def gore():
    return render_template("gore.html")


@app.route('/categoria', methods=['GET', 'POST'])
def categoria():
    form = CategoriaForm()
    form.produto.choices = resgatar_produtos()
    form.categoria.choices = resgatar_categorias()
    if form.validate_on_submit():
        produto = Produto.query.get(form.produto.data)
        categoria = Categoria.query.get(form.categoria.data)
        if produto and categoria:
            produto.categorias.append(categoria)
            db.session.commit()
        return redirect('/')
    return render_template('categoria.html', form=form)

@app.route('/categoria_editar/<string:id>', methods=['GET', 'POST'])
def categoria_editar(id):
    produto = Produto.query.get_or_404(id)
    form = CategoriaForm(obj=produto)
    form.produto.choices = resgatar_produtos()
    form.categoria.choices = resgatar_categorias()
    if form.validate_on_submit():
        produto = Produto.query.get(form.produto.data)
        categoria = Categoria.query.get(form.categoria.data)
    return render_template('categoria_editar.html', form=form, produto=produto)

@app.route('/categoria_deletar/<string:produto_id>/<string:categoria_id>', methods=['GET', 'POST'])
def categoria_deletar(produto_id, categoria_id):
    produto = Produto.query.get(produto_id)
    categoria = Categoria.query.get(categoria_id)
    if produto and categoria:
        produto.categorias.remove(categoria)
        db.session.commit()
    return redirect('/')

@app.route('/categoria_edicao/<string:produto_id>/<string:categoria_id>', methods=['GET', 'POST'])
def categoria_edicao(produto_id, categoria_id):
    form = CategoriaForm()
    if request.method == 'GET':
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            form.categoria.data = categoria.id
    produto = Produto.query.get(produto_id)
    categoria = Categoria.query.get(categoria_id)
    categorias = resgatar_categorias()
    if produto and categoria:
        form.produto.choices = [(produto.id, produto.nome)]
        form.categoria.choices = categorias
        if form.validate_on_submit():
            produto = Produto.query.get(form.produto.data)
            novaCategoria = Categoria.query.get(form.categoria.data)
            if produto and categoria:
                produto.categorias.remove(categoria)
                produto.categorias.append(novaCategoria)
                db.session.commit()
            return redirect('/')
    return render_template('categoria_edicao.html', form=form)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    form = ProdutoForm()
    form.categoria.choices = resgatar_categorias()
    if form.validate_on_submit():
        arquivo = form.imagem.data
        nomedoarquivo = secure_filename(arquivo.filename)
        id = f'{uuid4().hex}_{nomedoarquivo}'
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], id)
        arquivo.save(caminho)

        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            #categoria=form.categoria.data,
            imagem=id,
            data_criacao=form.data_criacao.data,
            estoque=form.estoque.data
        )
        categoria_id = form.categoria.data
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            produto.categorias.append(categoria)
        db.session.add(produto)
        db.session.commit()
        return redirect('/')
    return render_template('adicionar.html', form=form)

@app.route('/')
def index():
    produtos = Produto.query.all()

    return render_template("index.html", produtos=produtos, load_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/perfil')
@login_required
def perfil():
    return render_template("perfil.html", load_user=current_user)

@app.route('/sobre')
def sobre():
    return render_template("sobre.html")





@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/')
        else:
               return render_template('login.html', form=form, error='Usuário ou senha inválido')
    return render_template('login.html', form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = Login.query.filter_by(username=form.username.data).first()
        existing_email = Login.query.filter_by(email=form.email.data).first()
        if existing_user and existing_email:
            return render_template('cadastro.html', form=form, error='Nome de usuário já existe')
        
        senha_hash = generate_password_hash(form.password.data)
        novo_login = Login(
            username=form.username.data,
            email=form.email.data,
            password=senha_hash
        )
        db.session.add(novo_login)
        db.session.commit()
        return redirect('/login')
    return render_template('cadastro.html', form=form)



@app.route('/produto/<string:id>')
def produto(id):
    produto = Produto.query.get_or_404(id)
    return render_template("produto.html", produto=produto)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.categoria = form.categoria.data
        produto.data_criacao = form.data_criacao.data
        produto.estoque = form.estoque.data

        try:
            arquivo = form.imagem.data
            nomedoarquivo = secure_filename(arquivo.filename)
            id = f'{uuid4().hex}_{nomedoarquivo}'
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], id)
            arquivo.save(caminho)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], produto.imagem))
            produto.imagem = id
        except Exception as e:
            if "[Errno 2]" in str(e):
                 arquivo = form.imagem.data
                 nomedoarquivo = secure_filename(arquivo.filename)
                 id = f'{uuid4().hex}_{nomedoarquivo}'
                 caminho = os.path.join(app.config['UPLOAD_FOLDER'], id)
                 arquivo.save(caminho)
                 produto.imagem = id
        db.session.commit()
        return redirect('/')
    return render_template("editar.html", form=form, produto=produto)

@app.route('/deletar/<string:id>', methods=['GET', 'POST'])
def deletar(id):
    produto = Produto.query.get_or_404(id)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], produto.imagem))
    db.session.delete(produto)
    db.session.commit()
    return redirect('/')

@app.route('/uploads/<arquivo>')#arquivocarregado', arquivo
def arquivocarregado(arquivo):
    return send_from_directory(app.config['UPLOAD_FOLDER'], arquivo)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)







