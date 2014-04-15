### Requires.
# Contenedor:
Contenedor.nombre.requires = IS_NOT_EMPTY()

# Libro
Libro.titulo.requires = [IS_NOT_EMPTY(), IS_UPPER()]
Libro.cantidad_total.requires = IS_NOT_EMPTY()
Libro.ubicacion.requires = IS_IN_DB(db(Contenedor.es_contenedor == False),
                                    Contenedor.id,
                                    '%(nombre)s')
# Libro.isbn.requires = IS_EMPTY_OR(IS_NOT_IN_DB(db, Libro))

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
### End Requires


### Readable And Writables
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
### End Readable And Writables


### Represent
# Libro
Libro.ubicacion.represent = lambda id, reg: str_libro_ubicacion(id)
Libro.cantidad_disponible.represent = lambda v, r: SPAN(v, _class='badge')
