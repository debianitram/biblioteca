################## Labels

# Movimientos
Movimientos.created_on.label = 'Fecha de prestamo'
Movimientos.libro_id.label = 'Libro'
Movimientos.persona_id.label = 'Persona'

################## End Labels 


################## Requires

# Contenedor:
Contenedor.nombre.requires = IS_NOT_EMPTY()

# Libro
Libro.titulo.requires = [IS_NOT_EMPTY(), IS_UPPER()]
Libro.cantidad_total.requires = IS_NOT_EMPTY()
Libro.ubicacion.requires = IS_IN_DB(db(Contenedor.es_contenedor == False),
                                    Contenedor.id,
                                    '%(nombre)s')

# Persona
tipos = ['Alumno', 'Docente', 'No Docente']
Persona.nombre.requires = IS_NOT_EMPTY()
Persona.apellido.requires = IS_NOT_EMPTY()
Persona.dni.requires = IS_NOT_IN_DB(db, Persona.dni)
Persona.tipo.requires = IS_IN_SET(tipos)
Persona.curso.requires = IS_NOT_EMPTY()

# Movimientos
estado_movimiento = {'1': 'Prestado', '2': 'Devuelto'}
Movimientos.estado.requires = IS_IN_SET(estado_movimiento)

################## End Requires


################## Readable And Writable

# Contenedor
Contenedor.es_contenedor.readable = False
Contenedor.es_contenedor.writable = False
Contenedor.contenedor_superior.readable = False
Contenedor.contenedor_superior.writable = False

# Libro
Libro.cantidad_prestados.readable = False
Libro.cantidad_prestados.writable = False
Libro.codsearch.readable = False

# Persona
Persona.codsearch.readable = False
Persona.codsearch.writable = False

# Movimientos
Movimientos.created_on.readable = True

################## End Readable And Writable


################## Represent

# Libro
Libro.ubicacion.represent = lambda v, r: str_libro_ubicacion(v)
Libro.cantidad_disponible.represent = lambda v, r: SPAN(v, _class='badge')

# Movimientos
Movimientos.estado.represent = lambda v, r: SPAN(estado_movimiento.get(v[0]), \
                                                 _class='badge badge-important')
Movimientos.cantidad.represent = lambda v, r: SPAN(v, _class='badge badge-info')
Movimientos.created_on.represent = lambda v, r: SPAN(prettydate(v), \
                                                    _class='badge badge-inverse',
                                                    _title=v)

################## End Represent
