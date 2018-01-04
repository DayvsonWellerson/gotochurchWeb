def novaArea():
    if request.vars:
        setor = request.vars.setor
        idCoordenador = request.vars.idCoordenador
        if idCoordenador != '' and setor != '':
            try:
                Area.insert(coordenador=idCoordenador, setor=setor)
            except Exception as e:
                db.rollback()
                return 0
            else:
                db.commit()
                return 1
        else:
            return 2
            
def editaArea():
    if request.vars:
        if request.vars.id:
            idArea = request.vars.id
            if idArea != '':
                try:
                    setor = request.vars.setor
                    idCoordenador = request.vars.idCoordenador
                    db(Area.id == idArea).update(coordenador=idCoordenador, setor=setor)
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

def excluiArea():
    if request.vars:
        if request.vars.id:
            try:
                idArea = request.vars.id
                db(Area.id == idArea).delete()
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

def listaSAreas():
    
    areas = db.executesql("SELECT a.id, a.setor as idsetor, s.numero as setor, a.coordenador as idcoordenador, au.first_name as coordenador FROM area as a INNER JOIN auth_user as au on au.id = a.coordenador INNER JOIN setor as s on s.id=a.setor", as_dict=True)
    from gluon.serializers import json
    return XML(json(areas))

def pesquisaAreaPorId():
    if request.vars:
        idArea = request.vars.id
        #setor = db(Setor.id == idSetor).select()
        area = db.executesql("SELECT a.id, a.setor as idsetor, s.numero as setor, a.coordenador as idcoordenador, au.first_name as coordenador FROM area as s INNER JOIN auth_user as au on au.id = s.coordenador INNER JOIN setor as s on s.id=a.setor WHERE s.id = %s" %idSetor, as_dict=True)
        from gluon.serializers import json
        return XML(json(setor))