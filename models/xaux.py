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


def prestar_libro(row):
    """ Se muestra el botón Prestar en SQLFORM.grid
        si el libro se encuentra disponible """

    if not row.cantidad_disponible:
        btn = A('No Disponible', _class='btn disabled')
    else:
        btn = A(I(_class='icon-thumbs-up'), 
                ' Prestar',
                _href=URL(c='libros', f='prestar', vars=dict(libro_id=row.id)),
                _class='btn')
    return btn

def oncreate(table, id):
    response.flash = (table, id)
    return


def ondelete(table, id):
    db[table](id).update_record(is_active=False) # Desactivamos el registro
    db.commit() # Commit
    session.flash = 'Se eliminó el registro con id: %s' % id # Mensaje
    redirect(URL())


