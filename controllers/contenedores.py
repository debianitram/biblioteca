# Controlador que se encarga de manejar la lógica de los contenedores
# Tipo de contenedores: Contenedor/Sección

def administrar():
    """ Administración de los contenedores/secciones - CRUD """
    response.view = 'biblioteca/contenedores_administrar.html'
    tipo = request.vars.get('tipo', 'contenedor')

    # Armamos la consulta según sea: Contenedor o Sección.
    # Colocamos los Fields según sea: Contenedor o Sección.
    if tipo == 'contenedor':
        titulo = 'Contenedor'
        query = Contenedor.es_contenedor == True
        fields = [Contenedor.nombre, 
                  Contenedor.descripcion]

    elif tipo == 'seccion':
        titulo = 'Sección'
        query = Contenedor.es_contenedor == False
        fields = [Contenedor.nombre, 
                  Contenedor.descripcion,
                  Contenedor.contenedor_superior]
        Contenedor.contenedor_superior.readable = True
        Contenedor.contenedor_superior.writable = True
        Contenedor.contenedor_superior.represent = lambda v, r: getContainerUp(v)

    else:
        session.flash = 'No encontró la URL'
        redirect(URL(c='default', f='index'))
    # Fin de la Query

    # Reconfiguramos los Fields.
    if 'new' in request.args or 'edit' in request.args:
        if tipo == 'contenedor':
            Contenedor.es_contenedor.default = True

        elif tipo == 'seccion':
            Q = Contenedor.es_contenedor == True
            Contenedor.es_contenedor.default = False
            Contenedor.contenedor_superior.requires = IS_IN_DB(db(Q),
                                                               Contenedor.id,
                                                               '%(nombre)s')

    # fin de la configuración de Fields.

    grid = SQLFORM.grid(query, 
                        fields=fields,
                        csv=False,
                        orderby=Contenedor.created_on,
                        user_signature=True)

    return dict(titulo=titulo, grid=grid)



def generar_caratula():
    """ 
    Formato de las carátulas:
        [Image Book] Section Name
        [Image Library] Containers Name
    """
    return 'Return PDF'