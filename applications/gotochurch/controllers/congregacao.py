def novaCongregacao():
    if request.vars:
        nome = request.vars.nome
        coordenador = request.vars.coordenador
        qtd_assentos = request.vars.qtd_assentos
        rua = request.vars.rua
        bairro = request.vars.bairro
        cidade = request.vars.cidade
        complemento = request.vars.complemento
        numero = request.vars.numero
        latitude = request.vars.latitude
        logitude = request.vars.longitude

        Congregacao.insert(nome=nome, coordenador=coordenador, qtd_assentos=qtd_assentos, rua=rua, bairro=bairro, cidade=cidade, complemento=complemento, numero=numero, latitude=latitude, logitude=logitude)

def excluirCongregacao():
    if request.vars:
        idCongregacao = request.vars.id
        db(Congregacao.id == idCongregacao).delete()

def editarCongregacao():
    if request.vars:
        idCongregacao = request.vars.id
        nome = request.vars.nome
        coordenador = request.vars.coordenador
        qtd_assentos = request.vars.qtd_assentos
        rua = request.vars.rua
        bairro = request.vars.bairro
        cidade = request.vars.cidade
        complemento = request.vars.complemento
        numero = request.vars.numero
        latitude = request.vars.latitude
        logitude = request.vars.longitude

        db(Congregacao.id == idCongregacao).update(nome=nome, coordenador=coordenador, qtd_assentos=qtd_assentos, rua=rua, bairro=bairro, cidade=cidade, complemento=complemento, numero=numero, latitude=latitude, logitude=logitude)

def listarCongregacao():
    congregacoes = db.executesql("SELECT c.nome, c.coordenador, c.qtd_assentos, c.rua, c.bairro, c.cidade, c.complemento, c.numero, c.latitude, c.logitude FROM congregacao as c", as_dict=True)
    from gluon.serializers import json
    return XML(json(congregacoes))

def pesquisarCongregacaoPorId():
    if request.vars:
        idCongregacao = request.vars.id
        congregacoe = db.executesql("SELECT c.nome, c.coordenador, c.qtd_assentos, c.rua, c.bairro, c.cidade, c.complemento, c.numero, c.latitude, c.logitude FROM congregacao as c WHERE c.id = %s" %idCongregacao, as_dict=True)
        from gluon.serializers import json
        return XML(json(congregacoe))