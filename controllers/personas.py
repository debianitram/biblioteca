# Controlador que se encarga de manejar la lógica de las personas.
# Tipo de personas: Alumnos/Docentes/No Docentes

def index():
    return dict()


def administrar():
    # Grid para realizar el crud de las personas.
    query = Persona.is_active == True

    grid = SQLFORM.grid(query,
                        csv=False,
                        orderby=Persona.created_on,
                        )
    return dict()


