# Definición de objetos o funciones auxiliares.
# Settings de variables.

install = False

if not install:
    # Si el sistema no está instalado y no existen usuario, se crea uno.
    if not db(db.auth_user.id > 0).count():
        admin = db.auth_user.validate_and_insert(first_name='admin',
                                                 last_name='admin',
                                                 email='admin@admin.com',
                                                 password='colmenalabs_0')

    groups = [{'role': 'administrador',
               'description': 'Acceso a todos los controles del Sistema'},
              {'role': 'gestion_libros',
               'description': 'Permiso para la gestión de los libros'},
              {'role': 'gestion_personas',
               'description': 'Permiso para la gestión de las personas'},
              {'role': 'gestion_contenedores',
               'description': 'Permiso para la gestión de contenedores'}]

    if not db(db.auth_group.id > 0).count():
        groups_list = db.auth_group.bulk_insert(groups)

    if not db(db.auth_membership.id > 0).count():
        db.auth_membership.insert(user_id=admin,
                                  group_id=groups_list[0])


def getContainerUp(key):
    """ 
        Retornar el nombre del Contenedor Superior.
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

def devolver_libro(row):
    """ Se muestra el botón Devolver en SQLFORM.grid """

    btn = A(I(_class='icon-thumbs-up'), 
            ' Devolver',
            _href=URL(c='libros', f='devolver', vars=dict(id=row.id)),
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


