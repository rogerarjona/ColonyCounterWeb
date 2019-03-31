from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from api import views

urlpatterns = [

	url(r'^post-crear-nuevo-proyecto/$', views.post_nuevo_proyecto, name="post_nuevo_proyecto"),
	url(r'^post-editar-proyecto/$', views.post_editar_proyecto, name="post_editar_proyecto"),
	url(r'^post-obtener-proyecto/$', views.post_obtener_proyectos, name="post_obtener_proyectos"),
	url(r'^post-eliminar-proyecto/$', views.post_eliminar_proyecto, name="post_eliminar_proyectos"),

	url(r'^post-obtener-imagenes-proyecto/$', views.post_obtener_imagenes_proyecto, name="post_obtener_imagenes_proyecto"),
	url(r'^post-obtener-imagen-cloudinary/$', views.get_image_from_post, name="post_eliminar_proyectos"),

	url(r'^post-actualizar-colony-elements/$', views.post_actualizar_colony_elements, name="post_actualizar_colony_elements"),
	url(r'^post-obtener-colony-elements/$', views.post_obtener_colony_elements, name="post_obtener_colony_elements"),
	
	#PARTE PAGINA WEB
	url(r'^dashboard/$', login_required(views.dashboard), name="dashboard"),
	url(r'^proyectos/$', login_required(views.lista_proyectos), name="lista_proyectos"),
	url(r'^imagenes-proyecto/([0-9]+)/$', login_required(views.lista_imagenes_proyecto), name="lista_imagenes_proyecto"),
	url(r'^imagen-elementos/([0-9]+)/$', login_required(views.datos_colony_elements), name="datos_colony_elements"),

	url(r'^crear-proyecto/$', login_required(views.crear_proyecto), name="crear_proyecto"),

]

