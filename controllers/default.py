# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#pagina de listagem das pautas
def index():
    if request.vars:
        if request.vars.lista == 'mais-novas':
            lista = db(db.pauta.id > 0).select(orderby=~db.pauta.id)
        elif request.vars.lista == 'mais-comentadas':
            lista = db(db.pauta.id > 0).select(orderby=~db.pauta.comentarios)
        elif request.vars.lista == 'suas-pautas':
            lista = db(db.pauta.id_usuario == auth.user.id).select()
        elif request.vars.lista == 'tags':
            lista = db(db.pauta.tags.contains(request.vars.tag, all=True)).select()
        elif request.vars.lista == 'veiculo':
            lista = db(db.pauta.veiculo == request.vars.veiculo).select()
    else:
        lista = db(db.pauta.id > 0).select(orderby=~db.pauta.votos)

    return locals()

def webservice():
    
    lista = db(db.pauta.id > 0).select(orderby=~db.pauta.votos)

    return dict(lista=lista)

#formulario de sugestão de pautas.
#requer usuário logado
@auth.requires_login()
def sugerir_pauta():
    form = crud.create(db.pauta, message="Sugestão de pauta cadastrada com sucesso.")
    return locals()

#visualiza pauta 
def ver_pauta():
    id_pauta = request.args(0) or redirect(URL(c='default', f='index'))
    pauta = db(db.pauta.id == id_pauta).select()
    form = SQLFORM(db.comentario)
    comentario = db(db.comentario.id_pauta == id_pauta).select()
    
    if form.process().accepted:
        db(db.pauta.id == id_pauta).update(comentarios = db.pauta.comentarios+1)
        session.flash = "Comentário publicado com sucesso"
        redirect(URL(c='default', f='ver_pauta', args=id_pauta))
    elif form.errors:
        response.flash = "Houve um erro na sua requisição"

    return locals()

@auth.requires_login()
def votar():
    id_pauta = request.args(0) or redirect(URL(c='default', f='index'))
    verifica_voto = db((db.voto.id_usuario == auth.user.id)&(db.voto.id_pauta == id_pauta)).select()

    if not verifica_voto:
        db.voto.insert(
            id_usuario = auth.user.id,
            id_pauta = id_pauta
            )
        db(db.pauta.id == id_pauta).update(votos = db.pauta.votos + 1)
        session.flash = "Obrigado pelo seu voto. Aproveite e compartilhe sua sugestão de pauta nas redes sociais."
        redirect(URL(c='default', f='ver_pauta', args=id_pauta))
    else:
        session.flash = "Você já votou nesse pauta. Aproveite e compartilhe essa sugestão de pauta nas redes sociais."
        redirect(URL(c='default', f='ver_pauta', args=id_pauta))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
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


