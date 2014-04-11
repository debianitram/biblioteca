# Controlador que se encarga de manejar la lógica de los contenedores
# Tipo de contenedores: Contenedor/Sección

def administrar():
    # Grid para administrar los Contenedores/Secciones.

    tipo = request.vars.get('tipo', 'contenedor')

    # Armamos la consulta según sea un Contenedor o una Sección.
    query = Contenedor.is_active != False
    if tipo == 'contenedor':
        query &= Contenedor.es_contenedor == True

    elif tipo == 'seccion':
        query &= Contenedor.es_contenedor == False
    else:
        session.flash = 'No encontró la URL'
        redirect(URL(c='default', f='index'))
    # Fin de la Query

    # Reconfiguramos los Fields.
    if 'new' in request.args or 'edit' in request.args:
        if tipo == 'contenedor':
            Contenedor.contenedor_superior.readable = False
            Contenedor.contenedor_superior.writable = False
            Contenedor.es_contenedor.default = True
            Contenedor.es_contenedor.readable = False
            Contenedor.es_contenedor.writable = False

        elif tipo == 'seccion':
            Contenedor.es_contenedor.default = False
            Contenedor.es_contenedor.readable = False
            Contenedor.es_contenedor.writable = False


    grid = SQLFORM.grid(query, 
                        csv=False,
                        orderby=Contenedor.created_on)

    return dict(grid=grid)



def generar_caratula():
    """ 
    Formato de las carátulas:
        [Image Book] Section Name
        [Image Library] Containers Name
    """
    return 'Return PDF'