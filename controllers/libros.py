# Controlador que se encarga de manejar la lógica de los libros
def index():
    redirect(URL(c='libros', f='administrar'))
    


def administrar():
    """ Administración de los libros en la biblioteca - CRUD """
    query = Libro.is_active == True

    grid = SQLFORM.grid(query,
                        csv=False,
                        orderby=Libro.created_on,
                        user_signature=False)

    return dict(grid=grid)


def prestar():
    return 'Lógica para el prestamo de libros'


def devolver():
    return 'Lógica para devolver los libros'
