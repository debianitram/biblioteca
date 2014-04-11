# Controlador que se encarga de manejar la lógica de los contenedores
# Tipo de contenedores: Contenedor/Sección

def administrar():
    # Grid para administrar los Contenedores/Secciones.

    tipo = request.vars.get('tipo', 'contenedor')

    if tipo == 'contenedor':
        query = Contenedor.es_contenedor == True
        query &= Contenedor.is_active != False
        
    
    elif tipo == 'seccion':
        query = Contenedor.es_contenedor == False
        query &= Contenedor.is_active != False


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