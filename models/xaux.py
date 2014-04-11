# Definición de objetos o funciones auxiliares.
# Settings de variables.

etapa_desarrollo = True

if etapa_desarrollo:
    # Si estamos en la etapa de desarrollo y no existen usuario, se crea uno.
    if not db(db.auth_user.id > 0).count():
        db.auth_user.validate_and_insert(first_name='etapa',
                                         last_name='desarrollo',
                                         email='test@test.com',
                                         password='123qwe')