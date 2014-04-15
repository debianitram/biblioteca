# Controlador que se encarga de manejar la lógica de los libros
def index():
    redirect(URL(c='libros', f='administrar'))
    

def administrar():
    """ Administración de los libros en la biblioteca - CRUD """
    response.view = 'biblioteca/libros_administrar.html'  # File view
    query = Libro.is_active == True

    #prestar.add_button('Volver', URL('otra_pagina'))

    # Fields a mostrar en la grilla.
    fields = [Libro.titulo, Libro.autor, Libro.ubicacion, Libro.cantidad_disponible]

    grid = SQLFORM.grid(query,
                        csv=False,
                        fields=fields,
                        maxtextlength=45,
                        orderby=Libro.created_on,
                        ondelete=ondelete,
                        user_signature=False)

    # Cambiando la clase para el botón submit.
    if grid.element('input', _type='submit'):
        grid.element('input', _type='submit')['_class'] = 'btn btn-primary'
        
    return dict(grid=grid)


def prestar():
    return 'Lógica para el prestamo de libros'


def devolver():
    return 'Lógica para devolver los libros'
