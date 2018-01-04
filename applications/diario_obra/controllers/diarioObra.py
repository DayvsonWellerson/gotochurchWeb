@auth.requires_login()
def _novoDiario():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == funcionario or tipo == adm:
		numRdo = (len(db(DiarioObra.id>0).select()) + 1)
		if numRdo > 999:
			numRdo = '0'+str(numRdo)
		elif numRdo > 99:
			numRdo = '00'+str(numRdo)
		elif numRdo > 9:
			numRdo = '000'+str(numRdo)
		else:
			numRdo = '0000'+str(numRdo)

		form = SQLFORM(DiarioObra, _class='ui form', _id='formDiarioObra')

		if form.accepts(request.vars):
			import json
			
			listaDeOcorrencias = json.loads(request.vars.todasOcorrencias)
			
			x=0

			idDiarioObra = db().select(DiarioObra.id, orderby=~DiarioObra.id, limitby=(0, 1))[0].id

			while x < len(listaDeOcorrencias):
				
				descricao = listaDeOcorrencias[x]

				Ocorrencia.insert(diarioObra=int(idDiarioObra), descricao=descricao)

				x = x + 1

			redirect(URL(a='diario_obra', c='diarioObra', f='_listarDiariosObra'))

		elif form.errors:
			for input in form.elements('input'):
    				input['_class'] = ''

				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Salvar'
			return locals()
		else:
			for input in form.elements('input'):
				input['_class'] = ''

				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Salvar'
		return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))



@auth.requires_login()
def _editarDiario():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	if request.args:
		if tipo == funcionario or tipo == adm:
			
			arg = request.args(0)

			numRdo = arg
			if numRdo > 999:
				numRdo = '0'+str(numRdo)
			elif numRdo > 99:
				numRdo = '00'+str(numRdo)
			elif numRdo > 9:
				numRdo = '000'+str(numRdo)
			else:
				numRdo = '0000'+str(numRdo)

			form = SQLFORM(DiarioObra, arg, _class='ui form', _id='formDiarioObra')

			if form.accepts(request.vars):
				import json
				
				listaDeOcorrencias = json.loads(request.vars.todasOcorrencias)
				
				x=0

				idDiarioObra = db().select(DiarioObra.id, orderby=~DiarioObra.id, limitby=(0, 1))[0].id

				while x < len(listaDeOcorrencias):
					id_ocorrencia = listaDeOcorrencias[x]['id']
					descricao = listaDeOcorrencias[x]['valor']

					db(Ocorrencia.id == int(id_ocorrencia)).update(descricao=descricao)

					x = x + 1

				redirect(URL(a='diario_obra', c='diarioObra', f='_listarDiariosObra'))

			elif form.errors:
				for input in form.elements('input'):
					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

				ocorrencias = db(Ocorrencia.diarioObra==arg).select()
				return locals()
			else:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

				ocorrencias = db(Ocorrencia.diarioObra==arg).select()
				return locals()
		else:
			redirect(URL(a='diario_obra', c='inicio', f='index'))

@auth.requires_login()
def _verDiarioObra():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	if request.args:
		if tipo == funcionario or tipo == adm or tipo == 2:
			
			arg = request.args(0)

			numRdo = arg
			if numRdo > 999:
				numRdo = '0'+str(numRdo)
			elif numRdo > 99:
				numRdo = '00'+str(numRdo)
			elif numRdo > 9:
				numRdo = '000'+str(numRdo)
			else:
				numRdo = '0000'+str(numRdo)

			form = SQLFORM(DiarioObra, arg, _class='ui form', _id='formDiarioObra')

			if form.accepts(request.vars):
				import json
				
				listaDeOcorrencias = json.loads(request.vars.todasOcorrencias)
				
				x=0

				idDiarioObra = db().select(DiarioObra.id, orderby=~DiarioObra.id, limitby=(0, 1))[0].id

				while x < len(listaDeOcorrencias):
					
					descricao = listaDeOcorrencias[x]

					Ocorrencia.insert(diarioObra=int(idDiarioObra), descricao=descricao, num_ocorrencia=x+1)

					x = x + 1

				redirect(URL(a='diario_obra', c='inicio', f='index'))

			elif form.errors:
				for input in form.elements('input'):
					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

				ocorrencias = db(Ocorrencia.diarioObra==arg).select()
				return locals()
			else:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

				ocorrencias = db(Ocorrencia.diarioObra==arg).select()
				return locals()
		else:
			redirect(URL(a='diario_obra', c='inicio', f='index'))



@auth.requires_login()
def _listarDiariosObra():
	usuario_logado = auth.user_id
	
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if tipo == adm:
		if request.vars.listaP:
			if int(request.vars.listaP) == 1:
				diarios = db(DiarioObra.id > 0).select(DiarioObra.ALL, orderby=~DiarioObra.obra)
			elif int(request.vars.listaP) == 2:
				diarios = db(DiarioObra.id > 0).select(DiarioObra.ALL, orderby=~DiarioObra.created_by)
			else:
				diarios = db(DiarioObra.id > 0).select()
		else:
			diarios = db(DiarioObra.id>0).select()

		diariosPendentes = db(DiarioObra.validacao == False).select()

		return locals()
	elif tipo == 2:
		if request.vars.listaP:
			if int(request.vars.listaP) == 1:
				diarios = db(DiarioObra.cliente == usuario_logado).select(DiarioObra.ALL, orderby=~DiarioObra.obra)
			elif int(request.vars.listaP) == 2:
				diarios = db(DiarioObra.cliente == usuario_logado).select(DiarioObra.ALL, orderby=~DiarioObra.created_by)
			else:
				diarios = db(DiarioObra.cliente == usuario_logado).select()
		else:
			diarios = db(DiarioObra.cliente==usuario_logado).select()
		diariosPendentes = db(DiarioObra.validacao == False and DiarioObra.cliente==usuario_logado).select()

		return locals()
	elif tipo == funcionario:
		if request.vars.listaP:
			if int(request.vars.listaP) == 1:
				diarios = db(DiarioObra.created_by == usuario_logado).select(DiarioObra.ALL, orderby=~DiarioObra.obra)
			elif int(request.vars.listaP) == 2:
				diarios = db(DiarioObra.created_by == usuario_logado).select(DiarioObra.ALL, orderby=~DiarioObra.created_by)
			else:
				diarios = db(DiarioObra.created_by == usuario_logado).select()
		else:
			diarios = db(DiarioObra.created_by==usuario_logado).select()
		diariosPendentes = db(DiarioObra.validacao == False and DiarioObra.created_by==usuario_logado).select()

		return locals()
	else:
		redirect(URL(a='diario_obra', c='inicio', f='index'))

def _adicionarFotosOcorrencia():
	if request.args:
		oco = request.args(0) #id Ocorrencia
		diario = request.args(1) #id diario de obra
		formFoto = SQLFORM(Imagens_Ocorrencia, _class='ui form', _id='formFotoOcorrencia')
		fotos = db(Imagens_Ocorrencia.ocorrencia == int(oco)).select()
		if formFoto.accepts(request.vars):
			img = db().select(Imagens_Ocorrencia.id, orderby=~Imagens_Ocorrencia.id, limitby=(0, 1))[0].id
			db(Imagens_Ocorrencia.id == img).update(ocorrencia=oco, diario_obra=diario)
			fotos = db(Imagens_Ocorrencia.ocorrencia == int(oco)).select()
			response.flash = 'Foto Adicionada!'
			for input in formFoto.elements('input'):
				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Adicionar'
			return locals()
		elif formFoto.errors:
			for input in formFoto.elements('input'):
				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Adicionar'

			return locals()
		else:
			for input in formFoto.elements('input'):
				if input['_type'] == 'submit':
					input['_class'] = 'ui button primary'
					input['_value'] = 'Adicionar'

			return locals()





@auth.requires_login()
def imprimir():
	usuario_logado = auth.user_id
	tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
	funcionario = 3
	adm = 1
	
	if request.args:
		response.title = 'Impressão - RDO 0'+request.args(0)+' - \nImpresso por '+db(db.auth_user.id == usuario_logado).select(db.auth_user.first_name)[0].first_name
		if tipo == funcionario or tipo == adm or tipo == 2:
			
			arg = request.args(0)

			numRdo = arg
			if numRdo > 999:
				numRdo = '0'+str(numRdo)
			elif numRdo > 99:
				numRdo = '00'+str(numRdo)
			elif numRdo > 9:
				numRdo = '000'+str(numRdo)
			else:
				numRdo = '0000'+str(numRdo)

			form = SQLFORM(DiarioObra, arg, _class='ui form', _id='formDiarioObra')

			if form.accepts(request.vars):
				import json
				
				listaDeOcorrencias = json.loads(request.vars.todasOcorrencias)
				
				x=0

				idDiarioObra = db().select(DiarioObra.id, orderby=~DiarioObra.id, limitby=(0, 1))[0].id

				while x < len(listaDeOcorrencias):
					
					descricao = listaDeOcorrencias[x]

					Ocorrencia.insert(diarioObra=int(idDiarioObra), descricao=descricao, num_ocorrencia=x+1)

					x = x + 1

				redirect(URL(a='diario_obra', c='inicio', f='index'))

			elif form.errors:
				for input in form.elements('input'):
					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

				ocorrencias = db(Ocorrencia.diarioObra==arg).select()
				return locals()
			else:
				for input in form.elements('input'):
					input['_class'] = ''

					if input['_type'] == 'submit':
						input['_class'] = 'ui button primary'
						input['_value'] = 'Salvar'

				ocorrencias = db(Ocorrencia.diarioObra==arg).select()
				return locals()
		else:
			redirect(URL(a='diario_obra', c='inicio', f='index'))







def _verFotosOcorrencia():
	if request.args:
		oco = request.args(0) #id Ocorrencia
		fotos = db(Imagens_Ocorrencia.ocorrencia == int(oco)).select()

		return locals()

def _validaOcorrencia():
    if request.args:
		idOcorrencia = request.args(0)		
		db(Ocorrencia.id == idOcorrencia).update(validacao=True)
		idDiario = db(Ocorrencia.id == idOcorrencia).select(Ocorrencia.diarioObra)[0].diarioObra
		ocorrencias = db.executesql("select * from ocorrencia as o where o.validacao is null and o.diarioobra ="+str(idDiario), as_dict=True)
		if len(ocorrencias) < 1:
			
			db(DiarioObra.id == idDiario).update(validacao=True)


def _recusaOcorrencia():
    if request.vars:
		idOcorrencia = request.vars.id
		msg = request.vars.mensagem
		db(Ocorrencia.id == idOcorrencia).update(validacao=False, msg_recusa=msg)
		idDiario = db(Ocorrencia.id == idOcorrencia).select(Ocorrencia.diarioObra)[0].diarioObra
		ocorrencias = db.executesql("select * from ocorrencia as o where o.validacao is null and o.diarioobra ="+str(idDiario), as_dict=True)
		if len(ocorrencias) < 1:
			
			db(DiarioObra.id == idDiario).update(validacao=True)
		
		return locals()

def teste():
	#idDiarioObra = db().select(Obra.id, orderby=~Obra.id, limitby=(0, 1))
	#x = int(idDiarioObra[0].id)

	#img = db().select(Imagens_Ocorrencia.id, orderby=~Imagens_Ocorrencia.id, limitby=(0, 1))#[0].id

	import json

	#y = request.vars.t

	#d = json.loads(y)

	#t = len(d)
	idDiario = db(Ocorrencia.id == 4).select(Ocorrencia.diarioObra)[0].diarioObra
	ocorrencias = db.executesql("select * from ocorrencia as o where o.validacao is null and o.diarioobra ="+str(idDiario), as_dict=True)#db(Ocorrencia.validacao == None and Ocorrencia.diarioObra == idDiario).select()
	x = len(ocorrencias)
	usuario_logado = auth.user_id
	
	
	d = db.executesql("select * from diario_obra as da where da.validacao = 'F' and da.cliente ="+str(usuario_logado), as_dict=True)
	if len(d) > 0:
		y = obj(d[0])
	else:
		y = d
	#idd = y.id
	#pp = d.items()
	
	#diarioUpdate = ocorrencias[0]['diarioObra']
	#a = db(DiarioObra.id == diarioUpdate).select()
	#dd = d[0]['id']
	return locals()


	