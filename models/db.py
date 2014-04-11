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
				Field('nombre'),
				Field('descripcion', 'text'),
				Field('contenedor_superior', 'reference contenedor'),
				Field('es_contenedor', 'boolean'),
				auth.signature,
				format='%(nombre)s'
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
