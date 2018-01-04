@auth.requires_login()
def index():
    response.title = 'DA - Agenta Telefonica'
    response.app = 'Agenda Telefônica'
    return locals()

@auth.requires_login()
def novoContato():
    """

    Retorna: Formulário para cadastro de um novo contato

    """
    response.title = 'DA - Agenta Telefonica'
    response.app = 'Novo Contato'
    form = SQLFORM(AgendaTelefonica, _id='form-contato', submit_button='Salvar')
    for element in form.elements('select'):
        element['_class'] = 'mdb-select colorful-select dropdown-primary'
        
    if form.process().accepted:
        return locals()
    elif form.errors:
        return locals()
    else:

        return locals()


def novaInstituicao():
    response.title = 'DA - Agenta Telefonica'
    response.app = 'Nova Instituição'
    form = SQLFORM(Instituicao, _id='form-instituicao', submit_button='Salvar')
    
    if form.process().accepted:
        return locals()
    elif form.errors:
        return locals()
    else:

        return locals()


def FXHR_pesquisaContatos():
    """
        Pesquisa Contatos no banco de dados

    """
    if request.args(0) and len(request.args(0)) > 1:
        arg0 = request.args(0)

        if arg0[0] == ' ':

            contato = db.executesql("select distinct a.id, a.instituicao, i.titulo, i.site, i.telefoneprincipal, i.endereco, a.setor as descricao, a.pessoacontato, a.email, a.telefone from instituicao as i left join agendatelefonica as a on i.id = a.instituicao where i.titulo ilike('"+arg0[1]+"%%') and a.ativo='T' order by i.titulo, a.pessoacontato; " , as_dict=True)
            
            novaPesquisa = db.executesql("select distinct i.id, i.titulo, i.site, i.telefoneprincipal, i.endereco from instituicao as i left join agendatelefonica as a on i.id = a.instituicao where i.titulo ilike('"+arg0[1]+"%%') and a.instituicao is null order by i.titulo", as_dict=True)          

            
            contato += novaPesquisa
            #Pesquisa instituição caso todos os contatos estiverem na lixeira
            if len(contato) == 0:
                contato = db.executesql("select distinct i.id, i.titulo, i.site, i.telefoneprincipal, i.endereco from instituicao as i left join agendatelefonica as a on i.id = a.instituicao where i.titulo ilike('"+arg0[1]+"%%') and a.ativo='F' order by i.titulo; " , as_dict=True)

        else:    

            contato = db.executesql("select distinct a.id, a.instituicao, i.titulo, i.site, i.telefoneprincipal, i.endereco, a.setor as descricao, a.pessoacontato, a.email, a.telefone from instituicao as i inner join agendatelefonica as a on i.id = a.instituicao where a.ativo='T' order by i.titulo, a.pessoacontato; " , as_dict=True)

            if len(contato) == 0:
                contato = db.executesql("select distinct a.id, a.instituicao, i.titulo, i.site, i.telefoneprincipal, i.endereco, a.setor as descricao, a.pessoacontato, a.email, a.telefone from instituicao as i inner join agendatelefonica as a on i.id = a.instituicao where a.pessoacontato ilike('%%"+arg0+"%%') and a.ativo='T' order by i.titulo, a.pessoacontato;", as_dict=True)

                if len(contato) == 0:
                    contato = db.executesql("select distinct a.id, a.instituicao, i.titulo, i.site, i.telefoneprincipal, i.endereco, a.setor as descricao, a.pessoacontato, a.email, a.telefone from instituicao as i inner join agendatelefonica as a on i.id = a.instituicao where a.email ilike('%%"+arg0+"%%') and a.ativo='T' order by i.titulo, a.pessoacontato;", as_dict=True)
                    if len(contato) == 0:
                        contato = db.executesql("select distinct a.id, a.instituicao, i.titulo, i.site, i.telefoneprincipal, i.endereco, a.setor as descricao, a.pessoacontato, a.email, a.telefone from instituicao as i inner join agendatelefonica as a on i.id = a.instituicao where a.setor ilike('%%"+arg0+"%%') and a.ativo='T' order by i.titulo, a.pessoacontato;", as_dict=True)
                        if len(contato) == 0:
                            contato = db.executesql("select distinct a.id, a.instituicao, i.titulo, i.site, i.telefoneprincipal, i.endereco, a.setor as descricao, a.pessoacontato, a.email, a.telefone from instituicao as i inner join agendatelefonica as a on i.id = a.instituicao where i.palavraschave ilike('%%"+arg0+"%%') and a.ativo='T' order by i.titulo, a.pessoacontato;", as_dict=True)
                            if len(contato) == 0:
                                
                                contato = db.executesql("select distinct i.id, i.titulo, i.site, i.telefoneprincipal, i.endereco from instituicao as i where i.titulo ilike('%%"+arg0+"%%') order by i.titulo", as_dict=True)
                                #contato = db(db.instituicao.titulo.ilike('%fo%')).select().as_dict()
        # --------------------------------------------------------
        #   Pesquisa de instituições sem contatos cadastrados
        # --------------------------------------------------------


        
            novaPesquisa = db.executesql("select distinct i.id, i.titulo, i.site, i.telefoneprincipal, i.endereco from instituicao as i left join agendatelefonica as a on i.id = a.instituicao where i.titulo ilike('%%"+arg0+"%%') and a.instituicao is null order by i.titulo", as_dict=True)          
            
            if len(contato) == 0:
                contato = novaPesquisa
            else:
                contato += novaPesquisa


            #novaPesquisa = db.executesql("select i.id, i.titulo, i.site, i.telefoneprincipal, i.endereco from instituicao as i left join agendatelefonica as a on i.id = a.instituicao where i.titulo ilike('%%"+arg0+"%%') and a.instituicao is null order by i.titulo", as_dict=True)
            
            #if len(novaPesquisa) == 0:
                #novaPesquisa = db.executesql("select i.id, i.titulo, i.site, i.telefoneprincipal, i.endereco from instituicao as i left join agendatelefonica as a on i.id = a.instituicao where i.palavraschave ilike('%%"+arg0+"%%') and a.instituicao is null order by i.titulo", as_dict=True)
            
            #contato += novaPesquisa

    else:
        contato = '[]'
    from gluon.serializers import json
    return XML(json(contato))