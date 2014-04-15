# Controlador que se encarga de manejar la lógica de los libros
def index():
    redirect(URL(c='libros', f='administrar'))
    

def administrar():
    """ Administración de los libros en la biblioteca - CRUD """
    response.view = 'biblioteca/libros_administrar.html'  # File view
    query = Libro.is_active == True

    # Fields a mostrar en la grilla.
    fields = [Libro.titulo, 
              Libro.autor,
              Libro.ubicacion,
              Libro.cantidad_disponible]



    grid = SQLFORM.grid(query,
                        csv=False,
                        fields=fields,
                        maxtextlength=45,
                        orderby=Libro.created_on,
                        ondelete=ondelete,
                        links=[lambda r: prestar_libro(r)],
                        user_signature=False)

    return dict(grid=grid)


def prestar():
    # from modal_FieldsReference import modalFieldsReference as modal
    libro = Libro(request.vars.libro_id) or redirect(URL(c='libros', f='administrar'))
    response.view = 'biblioteca/libros_prestar.html'
    
    form = SQLFORM.factory(
            Field('persona',
                  'reference persona',
                  requires=IS_IN_DB(db(Persona.id > 0), Persona.id)
                  ),
            Field('cantidad', 
                  'list:string',
                  requires=IS_IN_SET(range(1, libro.cantidad_disponible + 1)))
            )

    if form.accepts(request.vars, session):
        # Lógica valores en la Base de datos
        cantidad_prestados=int(libro.cantidad_prestados)+int(form.vars.cantidad)
        libro.update_record(cantidad_prestados=cantidad_prestados)
        
        Movimientos.insert(libro_id=libro.id,
                           persona_id=form.vars.persona,
                           cantidad=int(form.vars.cantidad),
                           estado='1')
        db.commit()
        redirect(URL('default', 'index'))

    elif form.errors:
        response.flash = 'Controle el formulario'

    return dict(form=form, libro=libro)


def devolver():

    movimiento = Movimientos(request.vars.id)
    libro = Libro(movimiento.libro_id)

    form = SQLFORM.factory(
            Field('libro_id', default=movimiento.libro_id),
            Field('persona_id', default=movimiento.persona_id),
            Field('cantidad',
                    'list:string',
                    requires=IS_IN_SET(range(1, movimiento.cantidad + 1)),
                    label='Cantidad a Devolver'),
            )

    if form.process().accepted:
        if int(movimiento.cantidad) == int(form.vars.cantidad):
            # Devolucion Total.
            #Aqui hace el update en la tabla libros mas la sumatoria de cantidad_prestados
            cantidad_prestados=int(libro.cantidad_prestados)-int(form.vars.cantidad)
            libro.update_record(cantidad_prestados=cantidad_prestados)
            movimiento.update_record(cantidad=0, estado=2)
            db.commit()
            session.flash='Se devolvió con exito el total de los libros prestados.'
            redirect(URL('default', 'index'))
        else:
            # Devolucion Parcial
            cantidad_prestados=int(libro.cantidad_prestados)-int(form.vars.cantidad)
            libro.update_record(cantidad_prestados=cantidad_prestados)
            # Hace el update de la tabla movimiento.
            cantidad=int(movimiento.cantidad)-int(form.vars.cantidad)
            movimiento.update_record(cantidad=cantidad)
            db.commit()
            session.flash='Se devolvió el libro con exito.'
            redirect(URL('default', 'index'))

    return dict(form=form)
