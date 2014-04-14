# Definición de objetos o funciones auxiliares.
# Settings de variables.

etapa_desarrollo = True

if etapa_desarrollo:
    # Si estamos en la etapa de desarrollo y no existen usuario, se crea uno.
    if not db(db.auth_user.id > 0).count():
        db.auth_user.validate_and_insert(first_name='etapa',
                                         last_name='desarrollo',
                                         email='test@test.com',
                                         password='123qwe')


def getContainerUp(key):
    """ Retornar el nombre del Contenedor Superior.
        key = id del contenedor superior 
    """
    name = Contenedor(key)['nombre']
    return name


def str_libro_ubicacion(contenedor_id):
    r = Contenedor(contenedor_id)
    if r.es_contenedor:
        msg = SPAN('%s' % r.nombre, _class='label label-inverse')
    else:
        msg = TAG[''](SPAN('%s' % r.nombre, _class='label label-info'), ' ',
                      SPAN('%s' % r.contenedor_superior.nombre, 
                           _class='label label-inverse'))
    return msg


def oncreate(table, id):
    response.flash = (table, id)
    return


def ondelete(table, id):
    pass

