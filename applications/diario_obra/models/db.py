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
    #db = DAL(myconf.get('db.uri'),
    db = DAL('mysql://root:senha123@localhost/diarioobra',
    #db = DAL('mysql://dayvsonnasciment:senha123@dayvsonnascimento.mysql.pythonanywhere-services.com/dayvsonnasciment$diarioobra',
        pool_size=myconf.get('db.pool_size'),
        migrate_enabled=myconf.get('db.migrate'),
        check_reserved=['all'])

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

auth.settings.extra_fields['auth_user']= [
  Field('cpf', 'string', label='CPF'),
  Field('cnpj', 'string', label='CNPJ'),
  Field('tipo', 'integer', label='Tipo de Usuario')
]


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

Obra = db.define_table('obra',
    Field('data_inicio', 'date', label='Data de Inicio'),
    Field('data_final', 'date', label='Data Final'),
    Field('responsavel', 'reference auth_user', label='Responsável'),
    Field('aditivo', 'string', label='Aditivo'),
    Field('orcamento', 'double', label='Orçamento'),
    Field('endereco', 'string', label='Endereço'),
    Field('cliente', 'reference auth_user', label='Cliente'),
    Field('nome', 'string', label='Nome da Obra'),
    auth.signature
)
#Obra.cliente.requires = IS_IN_DB(db(db.auth_user.id == db(db.auth_membership.group_id == 2).select(db.auth_membership.user_id)[0].user_id ), db.auth_user.id, '%(first_name)s'+' '+'%(last_name)s')
Obra.cliente.requires = IS_IN_DB(db(db.auth_user.tipo == 2), db.auth_user.id, '%(first_name)s'+' '+'%(last_name)s')
Obra.responsavel.requires = IS_IN_DB(db(db.auth_user.tipo == 3), db.auth_user.id, '%(first_name)s'+' '+'%(last_name)s')

DiarioObra = db.define_table('diario_obra',
    Field('obra', Obra, label='Obra'),
    Field('ser_executado', 'string', label='Serviço executado'),
    Field('observaceos', 'text', label='Observações'),
    Field('tempo', 'string', label='Tempo'),
    Field('validacao', 'boolean', label='Validação', default=False),
    Field('dia_semana', 'string', label='Dia da Semana'),
    Field('data_validacao', 'date', label='Data de validação'),
    Field('efetivo_servente', 'string', label='Efetivo Servente'),
    Field('ocorrencia_diaria', 'string', label='Ocorrência Diária'),
    Field('folha_relatorio', 'string', label='Relatorio'),
    Field('efetivo_profissional', 'string', label='Efetico profissional'),
    Field('imagem', 'upload', label='Imagem'),
    Field('cliente', 'reference auth_user', label='Cliente'),
    auth.signature
)

DiarioObra.obra.requires = IS_IN_DB(db, Obra.id, '%(nome)s', error_message='Defina a Obra')
DiarioObra.cliente.requires = IS_IN_DB(db(db.auth_user.tipo == 2), db.auth_user.id, '%(first_name)s'+' '+'%(last_name)s', error_message='Defina o cliente')

tipos = [(1,'Administrador'),(2,'Cliente'),(3,'Funcionario')]
db.auth_user.tipo.requires = IS_IN_SET(tipos)
db.auth_user.cpf.requires = IS_EMPTY_OR(IS_NOT_IN_DB(db, 'auth_user.cpf', error_message='CPF já cadastrado!'))
db.auth_user.cnpj.requires = IS_EMPTY_OR(IS_NOT_IN_DB(db, 'auth_user.cnpj', error_message='CNPJ já cadastrado!'))
db.auth_user.password.requires = IS_NOT_EMPTY(error_message='A senha deve ser preenchida!')



Ocorrencia = db.define_table('ocorrencia',
    Field('diarioObra', DiarioObra, label='Diario de Obra'),
    Field('descricao', 'string', label='Descrição'),
    Field('validacao','boolean', label='Validação'),
    Field('msg_recusa','text', label='Mensagem de Recusa'),
    Field('num_ocorrencia','integer', label='Número da Ocorrêmcia'),
    auth.signature
)


Imagens_Ocorrencia = db.define_table('imageens_ocorrencias',
    Field('ocorrencia', Ocorrencia, label='Ocorrência'),
    Field('imagem','upload', label='Imagem'),
    Field('diario_obra', DiarioObra, label='Diario de Obra'),
    auth.signature
)

