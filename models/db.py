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
				common_filter=lambda q: db['contenedor'].is_active == True,
				format='%(nombre)s'
			)


Libro = db.define_table('libro',
			Field('titulo'),
			Field('descripcion', 'text'),
			Field('isbn'),
			Field('autor'),
			Field('editorial'),
			Field('fecha_publicacion', 'date'),
			Field('ubicacion', 'reference contenedor'),
			Field('codsearch', 
				   compute=lambda r: '%s %s %s %s' % (r['titulo'], 
				   								 	  r['autor'],
				   								   	  r['editorial'],
				   								   	  r['isbn'])
				),
			Field('cantidad_total', 'integer'),
			Field('cantidad_prestados', 'integer', default=0),
			Field('cantidad_disponible',
				  compute=lambda r: r['cantidad_total'] - r['cantidad_prestados']),
			auth.signature,
			common_filter=lambda q: db['libro'].is_active == True,
			format='%(titulo)s'
			)


Persona = db.define_table('persona',
			Field('nombre'),
			Field('apellido'),
			Field('dni', 'integer', unique=True),
			Field('domicilio'),
			Field('email'),
			Field('tipo', 'list:string'),
			Field('telefono', 'integer'),
			Field('curso'),
			Field('codsearch',
				   compute=lambda r: '%s %s %s' % (r['nombre'], 
				   								   r['apellido'],
				   								   r['dni'])
				),
			auth.signature,
			common_filter=lambda q: db['persona'].is_active == True,
			format='%(apellido)s, %(nombre)s'
			)


Movimientos = db.define_table('movimientos',
			Field('libro_id', 'reference libro'),
			Field('persona_id', 'reference persona'),
			Field('cantidad', 'integer'),
			Field('estado', 'list:string'),
			auth.signature,
			common_filter=lambda q: db['movimientos'].is_active == True,
			)