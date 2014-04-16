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

    # Cambiando la clase para el botón submit.
    if grid.element('input', _type='submit'):
        grid.element('input', _type='submit')['_class'] = 'btn btn-primary'
    return dict(grid=grid)


def prestar():
    from modal_FieldsReference import modalFieldReference as mf

    libro = Libro(request.vars.libro_id)
    response.view = 'biblioteca/libros_prestar.html'
    
    form = SQLFORM.factory(
            Field('persona',
                  'reference persona',
                  requires=IS_IN_DB(db(Persona.id > 0), Persona.id),
                  widget=SQLFORM.widgets.autocomplete(request,
                                                      Persona.codsearch,
                                                      id_field=Persona.id,
                                                      db=db(Persona.id > 0))
                  ),
            Field('cantidad', 
                  'list:string',
                  requires=IS_IN_SET(range(1, libro.cantidad_disponible + 1)))
            )

    if form.accepts(request.vars, session):
        # Lógica valores en la Base de datos
        cantidad_prestados = libro.cantidad_prestados + int(form.vars.cantidad)
        cantidad_disponible = libro.cantidad_total - cantidad_prestados

        libro.update_record(cantidad_prestados=cantidad_prestados,
                            cantidad_disponible=cantidad_disponible)
        
        Movimientos.insert(libro_id=libro.id,
                           persona_id=form.vars.persona,
                           cantidad=int(form.vars.cantidad),
                           estado='1')
        db.commit()
        session.flash = 'Se prestaron %s libro/s %s' % (form.vars.cantidad, libro.titulo)
        redirect(URL('default', 'index'))

    elif form.errors:
        response.flash = 'Controle el formulario'

    return dict(form=form, libro=libro)


def devolver():

    movimiento = Movimientos(request.vars.id) or redirect(URL(c='default', f='index'))
    libro = Libro(movimiento.libro_id)
    response.view = 'biblioteca/libros_devolver.html'

    form = SQLFORM.factory(
            Field('cantidad',
                  'list:string',
                  requires=IS_IN_SET(range(1, movimiento.cantidad + 1)),
                  label='Cantidad a devolver'),
            )

    if form.accepts(request.vars, session):

        if movimiento.cantidad == int(form.vars.cantidad):
            # Devolución Total.
            # Aqui hace el update en la tabla libros 
            # mas la sumatoria de cantidad_prestados
            cantidad_prestados = libro.cantidad_prestados - int(form.vars.cantidad)
            libro.update_record(cantidad_prestados=cantidad_prestados)
            movimiento.update_record(cantidad=0, estado=2)
            session.flash='Se devolvió el total de los libros prestados.'
            
        else:
            # Devolucion Parcial
            cantidad_prestados = libro.cantidad_prestados - int(form.vars.cantidad)
            cantidad_disponible = libro.cantidad_total - cantidad_prestados
            libro.update_record(cantidad_prestados=cantidad_prestados,
                                cantidad_disponible=cantidad_disponible)
            # Hace el update de la tabla movimiento.
            cantidad = movimiento.cantidad - int(form.vars.cantidad)
            movimiento.update_record(cantidad=cantidad)
            session.flash='Se devolvió el libro con exito.'

        db.commit()
        redirect(URL('default', 'index'))

    elif form.errors:
        response.flash = 'Controle el formulario'

    return dict(form=form, datos=movimiento)
