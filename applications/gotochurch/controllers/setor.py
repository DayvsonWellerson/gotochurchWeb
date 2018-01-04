def novoSetor():
    if request.vars:
        numero = request.vars.numero
        idCoordenador = request.vars.idCoordenador
        if idCoordenador != '' and numero != '':
            try:
                Setor.insert(coordenador=idCoordenador, numero=numero)
            except Exception as e:
                db.rollback()
                return 0
            else:
                db.commit()
                return 1
        else:
            return 2
            
def editaSetor():
    if request.vars:
        if request.vars.id:
            idSetor = request.vars.id
            if idSetor != '':
                try:
                    numero = request.vars.numero
                    idCoordenador = request.vars.idCoordenador
                    db(Setor.id == idSetor).update(coordenador=idCoordenador, numero=numero)
                except Exception as e:
                    db.rollback()
                    return 0
                else:
                    db.commit()
                    return 1
            else:
                return 2
        else:
            return 2
    else:
        return 2

def excluiSetor():
    if request.vars:
        if request.vars.id:
            try:
                idSetor = request.vars.id
                db(Setor.id == idSetor).delete()
            except Exception as e:
                db.rollback()
                return 0
            else:
                db.commit()
                return 1
        else:
            return 2
    else:
        return 2

def listaSetores():
    #setores = db(Setor.id > 0).select()
    setores = db.executesql("SELECT s.id, s.numero, s.coordenador as idcoordenador, au.first_name as coordenador FROM setor as s INNER JOIN auth_user as au on au.id = s.coordenador", as_dict=True)
    from gluon.serializers import json
    return XML(json(setores))

def pesquisaSetorPorId():
    if request.vars:
        idSetor = request.vars.id
        #setor = db(Setor.id == idSetor).select()
        setor = db.executesql("SELECT s.id, s.numero, s.coordenador as idcoordenador, au.first_name as coordenador FROM setor as s INNER JOIN auth_user as au on au.id = s.coordenador WHERE s.id = %s" %idSetor, as_dict=True)
        from gluon.serializers import json
        return XML(json(setor))