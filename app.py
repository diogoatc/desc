import os
from flask import Flask,session,flash, render_template,redirect, url_for, json, request,jsonify
import random
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
#from flask_debugtoolbar import DebugToolbarExtension




app = Flask(__name__,static_folder='static', static_url_path='/static')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT,'static/img/cats')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, origins='*')
mysql = MySQL(app)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'bfc1f7492709c0'
app.config['MYSQL_DATABASE_PASSWORD'] = '42121e97'
app.config['MYSQL_DATABASE_DB'] = 'ad_1fde3f7e20bc37f'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-03.cleardb.net'
mysql.init_app(app)

#FUNÇÃO PARA VERIFICAR SE O ARQUIVO É VALIDO
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#-------------------------------------------------------------------------------------------------------------
#FUNÇÃO PARA LISTAR TODAS AS CATEGORIAS
def lista_categorias():
	con=mysql.connect()
	cursor=con.cursor()
	cursor.execute("SELECT nome from categorias")
	categorias=cursor.fetchall()
	cursor.close()
	return categorias
#-------------------------------------------------------------------------------------------------------------
def lista_anuncios():
	con=mysql.connect()
	cursor=con.cursor()
	cursor.execute("SELECT categoria,expiracao,texto_tras,imagem_frente FROM anuncios order by expiracao ASC")
	anuncios=cursor.fetchall()
	cursor.close()
	con.close()
	return anuncios
#--------------------------------------------------------------------------------------------------------------
# Rota Index
@app.route('/')
def index():
	if session.get('logado') == True:
		return redirect(url_for("admin"))
	return render_template("login.html")
#-------------------------------------------------------------------------------------------------------------
# Rota Logout
@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------
# Rota Login
@app.route('/login',methods=['POST'])
def login():
	usr=str(request.form['user'])
	psw=str(request.form['password'])
	con=mysql.connect()
	cursor=con.cursor()
	cursor.execute("SELECT usuario,senha from usuarios WHERE usuario ='"+usr+"'")
	user=cursor.fetchall()
	con.close()

	if len(user) is 1:
		if (str(user[0][1])==psw):
			session['logado']=True #Setando a sessão
			return redirect(url_for("admin"))
		else:
			return "falhou"
	else:
		return "Usuario invalido"
#-------------------------------------------------------------------------------------------------------------
#Rota página Admin
@app.route('/admin')
def admin():
	if session.get('logado') != True:
		return redirect(url_for("index"))
	categorias = lista_categorias()
	return render_template("admin.html",categorias=categorias)
#-------------------------------------------------------------------------------------------------------------
#Rota lista anuncio
@app.route('/listar-anuncio')
def listanunc():
	if session.get('logado') != True:
		return redirect(url_for("index"))
	anuncios = lista_anuncios()
	return render_template("listar-anuncio.html",anuncios=anuncios)
#-------------------------------------------------------------------------------------------------------------
#Rota lista cliente
@app.route('/listar-cliente')
def listacliente():
	if session.get('logado') != True:
		return redirect(url_for("index"))
	return render_template("listar-cliente.html")
#-------------------------------------------------------------------------------------------------------------
#Rota lista categoria
@app.route('/listar-categoria')
def listacategoria():
	if session.get('logado') != True:
		return redirect(url_for("index"))
	categorias = lista_categorias()
	return render_template("listar-categoria.html", categorias=categorias)

#-------------------------------------------------------------------------------------------------------------
#Função cadastrar cliente
@app.route('/cadcliente',methods=['POST'])
def cadcliente():
	razao=str(request.form['razao'])
	cnpj=str(request.form['cnpj'])
	tel=str(request.form['telefone'])
	email=str(request.form['email'])
	resp=str(request.form['responsavel'])
	con=mysql.connect()
	cursor=con.cursor()
	try:
		cursor.callproc('cadcliente',(razao,cnpj,tel,email,resp))
		con.commit()
		flash('Cliente inserido com sucesso!')
	except:
		con.rollback()
		flash('Cliente não inserido!')
	cursor.close()
	con.close()

	return redirect(url_for("admin"))
#-------------------------------------------------------------------------------------------------------------
#FUNÇÃO CADASTRAR ANUNCIOS
@app.route('/cadanuncio',methods=['POST'])
def cadanuncio():
	categoria=str(request.form['categoria'])
	expiracao=request.form['expiracao']
	descricao = str(request.form['descricao'])
	img=request.files['imagem']
	name=str(random.randrange(1,1000000))+".png"
	img.save(os.path.join(app.config['UPLOAD_FOLDER'],name))
	con=mysql.connect()
	cursor=con.cursor()
	try:
		cursor.callproc('cadanuncio',(categoria,expiracao,descricao,name))
		con.commit()
		flash('Anuncio inserido com sucesso!')
	except:
		con.rollback()
		flash('Anuncio não inserido!')
	cursor.close()
	con.close()

	return redirect(url_for("admin"))

	
#------------------------------------------------------------------------------------------------------------
#Função cadastrar categoria
@app.route('/cadcat',methods=['POST'])
def cadcat():
	cate=request.form['cat']
	con=mysql.connect()
	cursor=con.cursor()
	try:
		cursor.callproc('cadcat',[cate,])
		con.commit()
		flash('Categoria inserida com sucesso!')
	except (ValueError, KeyError, TypeError) as error:  
	    con.rollback()
	    flash(error)
	cursor.close()
	con.close()

	return redirect(url_for("admin"))
#-------------------------------------------------------------------------------------------------------------
@app.route('/tst')
def viewteste():
	return render_template("teste2.html")
#-------------------------------------------------------------------------------------------------------------
@app.route('/teste',methods=['POST'])
def testeimg():
	img=request.files['imagem']
	name=str(random.randrange(1,1000000))+".png"
	img.save(os.path.join(app.config['UPLOAD_FOLDER'],name))
	teste = print(img)
	return "blablabla"
#-------------------------------------------------------------------------------------------------------------
#API retorna os anuncios da HOME
@app.route('/api/home')
def home():
	tipo=request.args.get("tipo")
	con=mysql.connect()
	cursor=con.cursor()
	cursor.callproc('ListaIndex',(tipo,))
	ret = cursor.fetchall()
	anuncios=[]
	for anuncio in ret:
		i={
			'id':anuncio[0],
			'imagem':anuncio[1],
			'texto':anuncio[2],
			'categoria':anuncio[3]
		}
		anuncios.append(i)
	return jsonify(anuncios)
#-------------------------------------------------------------------------------------------------------------
# API Retorna os anuncios da categoria
@app.route('/api/list', methods=['GET'])
def list():
	
	cat = request.args.get("categoria")
	con=mysql.connect()
	cursor=con.cursor()
	cursor.callproc('ListaAnuncios',(cat,))
	categorias = cursor.fetchall()
	anuncios=[]
	for anuncio in categorias:
		i={
			'id':anuncio[0],
			'imagem':anuncio[1],
			'texto':anuncio[2],
			'categoria':anuncio[3]
		}
		anuncios.append(i)
	return jsonify(anuncios)
#-------------------------------------------------------------------------------------------------------------
# API Retorna todas as categorias
@app.route('/api/categorias',methods=['POST'])
def list_cats():
	con=mysql.connect()
	cursor=con.cursor()
	cursor.callproc('ListaCategorias')
	list_categorias = cursor.fetchall()
	cat=[]
	for nome in list_categorias:
		i={
			'nome':nome[0]
		}
		cat.append(i)
	return jsonify(cat)
#-------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app.config['SECRET_KEY'] = "koakoakoqews"
	port = int(os.environ.get('PORT', 5000))
	#app.debug= True
	#toolbar = DebugToolbarExtension(app)
	app.run(host='127.0.0.1', port=port)  #usar se for testar localmente
	#app.run(host='0.0.0.0', port=port)	#usar no herokuc