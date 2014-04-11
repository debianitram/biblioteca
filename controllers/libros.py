# Controlador que se encarga de manejar la lógica de los libros
def index():
    return dict()


def administrar():
    """ Administración de los libros en la biblioteca - CRUD """
    query = Libro.is_active == True

    grid = SQLFORM.grid(query,
                        csv=False,
                        orderby=Libro.create_on)

    return dict(grid=grid)


def prestar():
    return 'Lógica para el prestamo de libros'
