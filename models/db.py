# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])

response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


# Definicion de tablas

Contenedor = db.define_table('contenedor',
<<<<<<< HEAD
			Field('nombre'),
			Field('descripcion', 'text'),
			Field('contenedor_superior', 'reference contenedor'),
			Field('es_contenedor', 'boolean'),
			auth.signature,
			format='%(nombre)s'
=======
				Field('nombre'),
				Field('descripcion', 'text'),
				Field('contenedor_superior', 'reference contenedor'),
				Field('es_contenedor', 'boolean'),
				auth.signature,
				format='%(nombre)s'
>>>>>>> 677807e06e49bb0fa081ab49d01a159e55132f4e
			)

Libro = db.define_table('libro',
			Field('titulo'),
			Field('descripcion'),
			Field('isbn'),
			Field('autor'),
			Field('editorial'),
			Field('fecha_publicacion', 'date'),
			Field('ubicacion', 'reference contenedor'),
			Field('cantidad_total', 'integer'),
			Field('cantidad_prestados', 'integer'),
			Field('cantidad_disponible'),
			auth.signature,
			format='%(titulo)s'
			)

tipos = ['Alumno', 'Docente', 'No Docente']
Persona = db.define_table('persona',
			Field('nombre'),
			Field('apellido'),
			Field('dni', 'integer'),
			Field('domicilio'),
			Field('email'),
			Field('tipo', 'list:string', requires=IS_IN_SET(tipos)),
			Field('telefono', 'integer'),
			Field('curso'),
			auth.signature,
			format='%(nombre)s'
			)

estados = ['Estado1', 'Estado2', 'Estado3']
Movimientos = db.define_table('movimientos',
			Field('libro_id', 'reference libro'),
			Field('persona_id', 'reference persona'),
			Field('cantidad', 'integer'),
			Field('estado', 'list:string', requires=IS_IN_SET(estados)),
			auth.signature,
			)
