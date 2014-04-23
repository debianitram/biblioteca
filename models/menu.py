# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('{ Biblioteca }'),
                  _class="brand",_href="http://colmenalabs.com.ar/")
response.title = 'Biblioteca'.title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Colmenalabs <soporte@colmenalabs.com.ar>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (SPAN(I(_class='icon-leaf icon-white'), B(' Movimientos')),
         False,
         URL(c='default', f='index'))
]

DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def menu():
    response.menu += [
        ### Btn Personas
        (SPAN(I(_class='icon-user icon-white'), B(' Personas')),
         False,
         URL(c='personas', f='administrar')),
        ### Btn Libros
        (SPAN(I(_class='icon-book icon-white'), B(' Libros')),
         False,
         URL(c='libros', f='administrar')),
        ### Btn Ubicación
        (SPAN(I(_class='icon-map-marker icon-white'), B(' Ubicación')),
         False,
         '',
         [(SPAN(I(_class='icon-inbox'), ' Contenedores'),
           False,
           URL(c='contenedores', f='administrar', vars=dict(tipo='contenedor'))),
          (SPAN(I(_class='icon-list'), ' Secciones'),
           False,
           URL(c='contenedores', f='administrar', vars=dict(tipo='seccion')))
          ]
        ),
        ### Btn Libros
        (SPAN(I(_class='icon-asterisk icon-white'),
              B(' Panel Admin'), _style='color:grey'),
         False,
         URL(c='default', f='admin')),
    ]

if auth.user_id:
    menu()

if "auth" in locals(): auth.wikimenu() 
