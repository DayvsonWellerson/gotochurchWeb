def novaInstituicao():
    response.app = 'Nova Instituição'
    form = SQLFORM(Instituicao, _id='form-instituicao', submit_button='Salvar')
    
    if form.process().accepted:
        return locals()
    elif form.errors:
        return locals()
    else:

        return locals()