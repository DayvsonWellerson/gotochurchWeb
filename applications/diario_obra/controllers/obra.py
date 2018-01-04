def index():
	pesquisa = db(Obra.id >= 1).select()
	return locals()

@auth.requires_login()
def _novaObra():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		form = SQLFORM(Obra, _class='ui form')

		if form.accepts(request.vars):
			session.flash = 'Obra "%s" Cadastrada!' %request.vars.nome
			redirect(URL(a='diario_obra', c='obra', f='_listarObras'))
		elif form.errors:
			for input in form.elements('input'):
				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Salvar'

				if input['_id'] == 'obra_data_inicio':
						input['_class'] += 'datas'

				if input['_id'] == 'obra_data_final':
						input['_class'] += 'datas'
			return locals()
		else:
			for input in form.elements('input'):
				input['_class'] = ''

				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Salvar'


				if input['_id'] == 'obra_data_inicio':
						input['_class'] += 'datas'

				if input['_id'] == 'obra_data_final':
						input['_class'] += 'datas'

		return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))

@auth.requires_login()
def _editarObra():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		if request.args:
			
			arg = request.args(0)

			form = SQLFORM(Obra, arg, _class='ui form')

			if form.accepts(request.vars):
				session.flash = 'Obra "%s" alterada!' %request.vars.nome
				redirect(URL(a='diario_obra', c='obra', f='_listarObras'))
			elif form.errors:
				for input in form.elements('input'):
					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

					if input['_id'] == 'obra_data_inicio':
						input['_class'] += 'datas'

					if input['_id'] == 'obra_data_final':
						input['_class'] += 'datas'
				return locals()
			else:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_id'] == 'obra_data_inicio':
						input['_class'] += 'datas'

					if input['_id'] == 'obra_data_final':
						input['_class'] += 'datas'

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

			return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))


@auth.requires_login()
def _listarObras():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == adm:
		
		if request.vars:
			arg = request.vars.nome
			listaObras = db(Obra.nome.ilike('%'+arg+'%')).select()

			return locals()
		else:

			listaObras = db(Obra.id>0).select()

			return locals()
	elif tipo == 2:
		if request.vars:
			arg = request.vars.nome
			listaObras = db(Obra.nome.ilike('%'+arg+'%') and Obra.cliente == usuario_logado).select()

			return locals()
		else:

			listaObras = db(Obra.cliente == usuario_logado).select()

			return locals()
	elif tipo == funcionario:
		if request.vars:
			arg = request.vars.nome
			listaObras = db(Obra.nome.ilike('%'+arg+'%') and (Obra.responsavel == usuario_logado or Obra.created_by == usuario_logado)).select()

			return locals()
		else:

			listaObras = db(Obra.responsavel == usuario_logado or Obra.created_by == usuario_logado).select()

			return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))

@auth.requires_login()
def _excluirObra():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		if request.args:
			arg = request.args(0)
			try:
				db(Obra.id == arg).delete()
			except Exception as e:
				return locals()
			else:
				redirect(URL(a='diario_obra', c='obra', f='_listarObras'))
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))
