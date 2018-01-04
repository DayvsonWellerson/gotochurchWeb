# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('mysql://root:senha123@localhost/gestor',
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# ---------------------------------------------
#               Tabela Instituição
# ---------------------------------------------
Instituicao = db.define_table('instituicao',
    Field('titulo','string',label='Título'),
    Field('industria','string',label='Industria'),
    Field('site','string',label='WebSite'),
    Field('palavraschave','string',label='Palavras Chave'),
    Field('telefonePrincipal','string',label='Telefone Principal', default='Não Informado'),
    Field('endereco', 'string',label='Endereço'),

    #Field('semContatos','boolean',default=True)
)
#Instituicao.industria.requires = IS_IN_DB(db(ListaSuspensa.classe=='Setor Industrial'), ListaSuspensa.id, '%(descricao)s' )


# ---------------------------------------------
#               Tabela Notas
# ---------------------------------------------
EtiquetaNotas = db.define_table('etiquetaNotas',
    Field('titulo', 'string', label='Titulo da etiqueta'),
    Field('publico','boolean', label='Público', default=False),
    auth.signature,

)


Notas = db.define_table('notas',
    Field('etiqueta',EtiquetaNotas, label='Etiqueta'),#default=30
    Field('nota','text', label='Nota'),
    Field('ativo','boolean',label='Ativo', default=True),
    #Field('publico','boolean',label='Tornar público', default=False),
    Field('publico','boolean', label='Público', default=False),
    auth.signature,

)

#Condição para mostrar apenas etiquetas criadas pelo usuário ou as públicas
if auth.user == None:
    Notas.etiqueta.requires = IS_IN_DB(db(), EtiquetaNotas.id, '%(titulo)s') # Caso não existir usuario logado (OBS: Deve acontecer apenas na parte administrativa da aplicação)
else:
    Notas.etiqueta.requires = IS_EMPTY_OR(IS_IN_DB(db(EtiquetaNotas.created_by==int(auth.user.id) or EtiquetaNotas.publico==True), EtiquetaNotas.id, '%(titulo)s')) # Lista apenas etiquetas criadas pelo usuário logado ou as públicas
    

#Notas = db.define_table('notas',
#    Field('etiqueta',EtiquetaNotas, label='Etiqueta', default='Comum'),
#    Field('nota','text', label='Nota'),
#    Field('ativo','boolean',label='Ativo', default=True),
#    Field('publico','boolean',label='Tornar público', default=False),
#    Field('cor', 'string', label='Cor da etiqueta', default='#ffffff'),
#    auth.signature
#)
#Notas.etiqueta.requires = IS_IN_DB(db(), EtiquetaNotas.id, '%(titulo)s')





# ---------------------------------------------
#               Tabela Contatos
# ---------------------------------------------

AgendaTelefonica = db.define_table('agendaTelefonica',
    Field('instituicao',Instituicao, label='Instituição'),
    Field('setor', 'string' , label='Setor da organização'),
    Field('pessoaContato','string', label='Pessoa para contato'),
    Field('telefone','string', label='Telefone'),
    Field('email','string',label="E-mail"),
    Field('ativo','boolean',label='Ativo',default=True),
    Field('publico','boolean', label='Público', default=False),
    auth.signature,

)

#AgendaTelefonica.setor.requires = IS_IN_DB(db(ListaSuspensa.classe=='Departamento interno'), ListaSuspensa.id, '%(descricao)s' )
AgendaTelefonica.instituicao.requires = IS_IN_DB(db(), Instituicao.id, '%(titulo)s')

#Telefones = db.define_table('telefones',
    #Field('agenda', AgendaTelefonica)
    #Field('numero', 'string')
#)

# ---------------------------------------------
#               Tabela Favoritos
# ---------------------------------------------

EtiquetaFavoritos = db.define_table('etiquetaFavoritos',
    Field('titulo', 'string', label='Titulo da etiqueta'),
    Field('publico','boolean', label='Público', default=False),
    auth.signature,

)


Favoritos = db.define_table('favoritos',
    Field('etiqueta',EtiquetaFavoritos, label='Etiqueta', default=1),
    Field('url','string', label='URL'),
    Field('descricao', 'string', label='Descrição'),
    Field('publico','boolean', label='Público', default=False),
    auth.signature,

)
Favoritos.etiqueta.requires = IS_IN_DB(db(), EtiquetaFavoritos.id, '%(titulo)s')





Arquivador = db.define_table('arquivador',
    Field('descricao', 'string', label='Descrição'),
    Field('arquivo', 'upload'),
    auth.signature,
)


#Eletron = db.define_table('eletron',
    #Field('cliente', 'string', label='Cliente'),
    #Field('tempo', 'datetime', label='Tempo'),
#)
