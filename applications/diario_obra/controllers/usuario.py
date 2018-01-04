@auth.requires_login()
def _novoUsuario():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		form = SQLFORM(db.auth_user, _class='ui form')

		if form.accepts(request.vars):
			session.flash = 'Usuário %s Cadastrado!' %request.vars.first_name
			redirect(URL(a='diario_obra', c='usuario', f='_listarUsuario'))
		elif form.errors:
			for input in form.elements('input'):
				input['_class'] = ''

				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Salvar'

				if input['_name'] == 'first_name':
					input['_placeholder'] = 'Nome'

				if input ['_name'] == 'last_name':
					input['_placeholder'] = 'Sobrenome'
				
				if input['_name'] == 'cpf':
					input['_class'] = 'cpfs'
				
				if input['_name'] == 'cnpj':
    					input['_class'] = 'cnpj'
			return locals()
		else:
			for input in form.elements('input'):
				input['_class'] = ''

				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Salvar'

				if input['_name'] == 'first_name':
					input['_placeholder'] = 'Nome'

				if input ['_name'] == 'last_name':
					input['_placeholder'] = 'Sobrenome'

				if input['_name'] == 'cpf':
    					input['_class'] = 'cpfs'
				
				if input['_name'] == 'cnpj':
					input['_class'] = 'cnpj'
		return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))

@auth.requires_login()
def _editarUsuario():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	if request.args:
		arg = request.args(0)
		if tipo == funcionario or tipo == adm:
			if int(usuario_logado) == int(arg):
				editarTudo = False
			else:
				editarTudo = True

			form = SQLFORM(db.auth_user, arg, _class='ui form')

			if form.accepts(request.vars):
				session.flash = 'Informaçõe do Usuário %s alteradas!' %request.vars.first_name
				redirect(URL(a='diario_obra', c='usuario', f='_listarUsuario'))
			elif form.errors:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

					if input['_name'] == 'first_name':
						input['_placeholder'] = 'Nome'

					if input ['_name'] == 'last_name':
						input['_placeholder'] = 'Sobrenome'
					
					if input['_name'] == 'cpf':
						input['_class'] = 'cpfs'
				
					if input['_name'] == 'cnpj':
							input['_class'] = 'cnpj'
				return locals()
			else:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'
					
					if input['_name'] == 'cpf':
    						input['_class'] = 'cpfs'
				
					if input['_name'] == 'cnpj':
							input['_class'] = 'cnpj'
			return locals()
		elif int(usuario_logado) == int(arg):
			
			editarTudo = False
			form = SQLFORM(db.auth_user, arg, _class='ui form')
			
			tipo_u = db(db.auth_user.id == arg).select(db.auth_user.tipo)[0].tipo

			if form.accepts(request.vars):
				session.flash = 'Informações alteradas com sucesso!'
				redirect(URL(a='diario_obra', c='inicio', f='index'))
			elif form.errors:
				response.flash = 'Erro %s var tipo = %s' %(form.errors, request.vars.tipo)
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

					if input['_name'] == 'first_name':
						input['_placeholder'] = 'Nome'

					if input ['_name'] == 'last_name':
						input['_placeholder'] = 'Sobrenome'
					
					if input['_name'] == 'cpf':
    						input['_class'] = 'cpfs'
				
					if input['_name'] == 'cnpj':
							input['_class'] = 'cnpj'
				return locals()
			else:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'
					
					if input['_name'] == 'cpf':
    						input['_class'] = 'cpfs'
				
					if input['_name'] == 'cnpj':
							input['_class'] = 'cnpj'
			return locals()
		else:
			redirect(URL(a='diario_obra', c='inicio', f='index'))

@auth.requires_login()
def _excluirUsuario():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		if request.args:
			arg = request.args(0)
			if arg != usuario_logado:
				try:
					db(db.auth_user.id == arg).delete()
				except Exception as e:
					return locals()
				else:
					session.flash = 'Usuário Excluído com sucesso!'
					redirect(URL(a='diario_obra', c='usuario', f='_listarUsuario'))
			else:
				session.flash = 'POR MOTIVOS DE SEGURANÇA VOCÊ NÃO PODE EXCLUIR O SEU USUÁRIO!'
				redirect(URL(a='diario_obra', c='usuario', f='_listarUsuario'))
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))


@auth.requires_login()
def _listarUsuario():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		if request.vars:
			arg = request.vars.nome
			
			listaUsuario = db(db.auth_user.first_name.ilike('%'+arg+'%')).select()
			if len(listaUsuario) == 0:
				listaUsuario = db(db.auth_user.last_name.ilike('%'+arg+'%')).select()

				if len(listaUsuario) == 0:
					listaUsuario = db(db.auth_user.email.ilike('%'+arg+'%')).select()

					if len(listaUsuario) == 0:
						listaUsuario = db(db.auth_user.cpf.ilike('%'+arg+'%')).select()

			return locals()
		else:
			listaUsuario = db(db.auth_user.id>0).select()

			return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))
