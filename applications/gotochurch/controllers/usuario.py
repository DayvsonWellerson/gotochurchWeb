def login():
    if request.vars:
        email = request.vars.email
        senha = request.vars.senha
        usuarios = db(db.auth_user.id > 0).select()
        tam = len(usuarios)
        login = False
        usuarioLogin = None
        for usuario in usuarios:
            
            if email == usuario.email:
                
                if senha == usuario.senha:
                    login = True
                    usuarioLogin = usuario

        if login:
            
            resultado = [{'resultado':1, 'dados':[usuarioLogin]}]

            from gluon.serializers import json
            return XML(json(resultado))
        else:
            resultado = [{'resultado':0}]
            from gluon.serializers import json
            return XML(json(resultado))
    #return locals() 

def novoUsuario():
    if request.vars:
        nome = request.vars.nome
        sobrenome = request.vars.sobrenome
        email = request.vars.email
        senha = request.vars.senha

        if request.vars.tipo:
            tipo = request.vars.tipo
        else:
            tipo = 2
        
        from gluon.serializers import json
        
        try:
            db.auth_user.insert(first_name=nome, last_name=sobrenome, email=email, password=senha, senha=senha)
        except Exception as e:
            error = [{'code':0,'error':e}]
            return XML(json(error))    
        else:
            return XML(json([{'code':1}]))

def editarUsuario():
    if request.vars:
        idusuario = request.vars.id
        nome = request.vars.nome
        sobrenome = request.vars.sobrenome
        email = request.vars.email
        senha = request.vars.senha

        if request.vars.tipo:
            tipo = request.vars.tipo
        else:
            tipo = 2
        
        from gluon.serializers import json
        
        try:
            db(db.auth_user.id == idusuario).update(first_name=nome, last_name=sobrenome, email=email, password=senha, senha=senha)
        except Exception as e:
            error = [{'code':0,'error':e}]
            return XML(json(error))    
        else:
            return XML(json([{'code':1}]))

def listaUsuarios():
    
    usuarios = db(db.auth_user.id > 0).select()
    
    from gluon.serializers import json
    return XML(json(usuarios))