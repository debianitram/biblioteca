# Controlador que se encarga de manejar la lógica de las personas.
# Tipo de personas: Alumnos/Docentes/No Docentes

def index():
    redirect(URL(c='personas', f='administrar'))


@auth.requires(auth.has_membership('gestion_personas') or \
               auth.has_membership('administrador'))
def administrar():
    """ Administración de las personas - CRUD """
    response.view = 'biblioteca/personas_administrar.html'
    query = Persona.is_active == True
    fields = [Persona.nombre, Persona.apellido, Persona.dni, Persona.tipo]

    grid = SQLFORM.grid(query,
                        fields=fields,
                        maxtextlength=45,
                        csv=False,
                        orderby=Persona.created_on,
                        ondelete=ondelete
                        )

    # Cambiando la clase para el botón submit.
    if grid.element('input', _type='submit'):
        grid.element('input', _type='submit')['_class'] = 'btn btn-primary'

    return dict(grid=grid)


