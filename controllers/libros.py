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
        libro.update_record(cantidad_prestados=int(form.vars.cantidad))
        
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
    
    form = SQLFORM.factory(
            Field('libro_id', default=movimiento.libro_id),
            Field('persona_id', default=movimiento.persona_id),
            Field('cantidad', default=movimiento.cantidad),
            Field('estado', default=movimiento.estado),
            )       
    if form.process().accepted:
        Movimientos.insert(libro_id=form.vars.libro_id,
                            persona_id=form.vars.persona_id,
                            cantidad=form.vars.cantidad,
                            estado=form.vars.estado)
        session.flash='registro insertado'

    return dict(form=form)
