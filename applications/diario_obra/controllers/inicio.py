@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    usuario = auth.user
    usuario_logado = auth.user_id
    
    tipo = db(db.auth_user.id == usuario_logado).select(db.auth_user.tipo)[0].tipo 
    funcionario = 3
    adm = 1
    
    if tipo == adm:
    
        diariosPendentes = db(DiarioObra.validacao == False).select()

        return locals()
    elif tipo == 2:
        diariosPendentes = db(DiarioObra.validacao == False and DiarioObra.cliente==usuario_logado).select()

        return locals()
    elif tipo == funcionario:
        diariosPendentes = db(DiarioObra.validacao == False and DiarioObra.created_by==usuario_logado).select()

        return locals()
    else:
        redirect(URL(a='diario_obra', c='inicio', f='index'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()