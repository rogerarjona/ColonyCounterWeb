from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core import files
from django.urls import reverse
from django.contrib import messages
import json, requests, cv2
from io import BytesIO
import numpy as np
from .models import *
from .forms import *
# Create your views here.

url_webhook = "https://6594f809.ngrok.io"

#Proyectos
@csrf_exempt
def post_nuevo_proyecto(request):

    mensaje = "Proyecto No Creado"
    error = "000" 
    
    #Obtener el json posteado
    _request = request.body
    python_dict = json.loads(_request)
    
    #Como es un post para crear un proyecto obtenemos los datos a guardar
    nombre = python_dict.get("nombre")
    descripcion = python_dict.get("descripcion")
    usuario = python_dict.get("usuario")

    response = None
    if nombre and usuario:
        try:
            _usuario = User.objects.get(username=usuario)
        except Exception as e:
            _usuario = None

        if _usuario:
            proyecto = crear_nuevo_proyecto(_usuario, nombre, descripcion)
            if proyecto:
                mensaje = "Proyecto Creado Correctamente"
                error = False
        else:
            mensaje = "El usuario no Existe"
            error = "003"

    response = {"Mensaje":mensaje, "ErrorCode": error}
    response = json.dumps(response) 
    
    return HttpResponse(response, content_type='aplication/json')

@csrf_exempt
def post_editar_proyecto(request):

    mensaje = "Proyecto No Actualizado"
    error = "001" 
    
    #Obtener el json posteado
    _request = request.body
    python_dict = json.loads(_request)
    
    #Como es un post para crear un proyecto obtenemos los datos a guardar
    nombre_nuevo = python_dict.get("nombre")
    #usuario = python_dict.get("usuario")
    id_proyect = python_dict.get("id")

    response = None
    if (nombre and usuario):
        try:
            #_usuario = User.objects.get(username=usuario)
            _proyecto = ColonyProyect.objects.get(id=id_proyect)
        except Exce_proyectoption as e:
            _proyecto = None

        if _proyecto:
            proyecto = actualizar_proyecto(_proyecto, nombre_nuevo)
            if proyecto:
                mensaje = "Proyecto Actualizado Correctamente"
                error = False
        else:
            mensaje = "El Proyecto No Existe"
            error = "002"

    response = {"Mensaje":mensaje, "ErrorCode": error}
    response = json.dumps(response)

    return HttpResponse(response, content_type='aplication/json')

@csrf_exempt
def post_eliminar_proyecto(request):

    mensaje = "El Proyecto No Existe"
    error = "002" 
    
    #Obtener el json posteado
    _request = request.body
    python_dict = json.loads(_request)
    
    #Como es un post para crear un proyecto obtenemos los datos a guardar
    id_proyect = python_dict.get("id")
    proyecto_eliminado = eliminar_proyecto(id_proyect)

    if proyecto_eliminado:
        mensaje = "Proyecto Eliminado Correctamente"
        error = False

    response = {"Mensaje":mensaje, "ErrorCode": error}
    response = json.dumps(response)
    
    return HttpResponse(response, content_type='aplication/json')

@csrf_exempt
def post_obtener_proyectos(request):
    mensaje = "Proyecto No Creado"
    error = "000" 
    
    #Obtener el json posteado
    _request = request.body
    python_dict = json.loads(_request)

    id_proyect = python_dict.get("id_proyect")
    username = python_dict.get("usuario")

    proyectos_map = []
    if (username):
        if not id_proyect:
            user = User.objects.get(username=username)
            proyectos = ColonyProyect.objects.select_related("user").filter(user=user)
        else:
            user = User.objects.get(username=username)
            proyectos = ColonyProyect.objects.select_related("user").filter(user=user, id=id_proyect)
        
        for proyecto in proyectos:

            id_proyecto = proyecto.id
            nombre = proyecto.name
            descripcion = proyecto.descripcion
            url_imagen = proyecto.url_imagen
            usuario = proyecto.user.username
            proyectos_map.append({"id":id_proyecto,"nombre":nombre, "descripcion":descripcion, "url":url_imagen,"usuario":usuario})
        
    response = json.dumps({"proyectos":proyectos_map})

    return HttpResponse(response, content_type='aplication/json')

@csrf_exempt
def post_obtener_imagenes_proyecto(request):

    _request = request.body
    python_dict = json.loads(_request)

    id_proyecto = python_dict.get("id_proyecto")
    username = python_dict.get("usuario")

    imagenes_proyecto_map = []
    if id_proyecto and username:
        try:
            user = User.objects.get(username=username)
            proyecto = ColonyProyect.objects.get(id=id_proyecto)
            imagenes_proyectos = PhotoColony.objects.select_related("proyecto").filter(user=user, proyecto=proyecto)
        except Exception as e:
            imagenes_proyectos = None

        if imagenes_proyectos:
            
            for imagen in imagenes_proyectos:
                id_imagen = imagen.id
                url_thumbnail = imagen.url_thumbnail
                created = imagen.created.isoformat()
                imagenes_proyecto_map.append({"id_imagen":id_imagen, "url_thumbnail":url_thumbnail, "created":created})
    response = json.dumps({"imagenes_proyectos":imagenes_proyecto_map})

    return HttpResponse(response, content_type='aplication/json')

def crear_nuevo_proyecto(usuario, nombre_proyecto, descripcion):
    try:
        proyecto = ColonyProyect()
        proyecto.name = nombre_proyecto
        proyecto.user = usuario
        proyecto.descripcion = descripcion
        proyecto.save()
    except Exception as e:
        proyecto = None
    
    return proyecto

def actualizar_proyecto(proyecto, nombre_nuevo):
    try:
        proyecto.name = nombre_nuevo
        proyecto.save()
    except Exception as e:
        proyecto = None

    return proyecto

def eliminar_proyecto(id_proyect):
    proyecto_eliminado = True
    try:
        proyecto = ColonyProyect.objects.get(id=id_proyect)
        proyecto.delete()
    except Exception as e:
        proyecto_eliminado = False

    return proyecto_eliminado


###### IMAGENES ######
@csrf_exempt
def get_image_from_post(request):

    mensaje = "Imagen no Obtenida"
    error = "010" 

    _request = request.body
    python_dict = json.loads(_request)

    
    public_id = python_dict.get("public_id")
    url_image = python_dict.get("url")
    imagen_repetida = PhotoColony.objects.filter(public_id=public_id)

    if not imagen_repetida:
        tags = python_dict.get("tags")[0].split("##")
        url_contado_thumbnail = url_image.replace("upload/", "upload/c_thumb,w_200,g_face/")
        
        if tags[0] == "contado":
            id_photo_colony = tags[1]
            print("Entre a contado")
            try:
                photo = PhotoColony.objects.get(id=id_photo_colony)
            except Exception as e:
                photo = None
            print(photo)
            if photo:
                photo.url_contado = url_image
                photo.url_contado_thumbnail = url_contado_thumbnail
                photo.save()

                error = False
                Mensaje = "Imagen obtenida Correctamente"

        elif tags[0] == "imagen":
            print("ENTRO A IMAGEN")
            url_thumbnail = url_image.replace("upload/", "upload/c_thumb,w_200,g_face/")
            
            username = tags[1]
            id_proyecto = tags[2]

            try:
                user = User.objects.get(username=username)
                proyecto = ColonyProyect.objects.get(user=user, id=id_proyecto)
            except Exception as e:
                user =  None
                proyecto = None
            #nombre_imagen, file_imagen = get_image_from_url(url_image)

            path, file_name = get_image_from_url(url_image)
            total, new_path = count_colony_in_image(path, file_name)
            
            photo = PhotoColony()
            photo.public_id = public_id
            photo.url_imagen = url_image
            photo.url_thumbnail = url_thumbnail
            photo.total = total
            photo.user = user
            photo.proyecto = proyecto
            photo.save()

            colony_elements = ColonyElements()
            colony_elements.photography = photo
            colony_elements.proyect = proyecto
            colony_elements.save()
            
            error = False
            mensaje = "Imagen obtenida Correctamente"

            post = subir_imagen_cloudinary(new_path, photo.id)

    response = {"Mensaje":mensaje, "ErrorCode": error}
    response = json.dumps(response) 

    return HttpResponse(response, content_type='aplication/json')

def get_image_from_url(URL):
    image = None
    r = requests.get(URL)
    if r.status_code == 200:
        fp = BytesIO()
        fp.write(r.content)
        file_name = URL.split("/")[-1] 
        
        path = "imagenes-petri/"
        with open(path+file_name, 'wb') as image:
            image.write(r.content)
            #photo.url_imagen.save(nombre_imagen, file_imagen)

    return path, file_name

def count_colony_in_image(path, file_name):

    total = 0

    import cv2
    import numpy as np

    # Cargar la imagen a ser analizada y ajustando tamaño.
    img = cv2.imread(path+file_name)
    #cv2.imshow('original', img)
    #cv2.waitKey(0)
    # Convertimos la imagen a escala de grises.
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('grises', img_gris)
    #cv2.waitKey(0)
    # Quitamos el ruido de la imagen por medio de un filtro Gaussiano
    img_gaussiana =  cv2.GaussianBlur(img_gris, (5,5), 0)
    #cv2.imshow('gaussiana', img_gaussiana)
    #cv2.waitKey(0)
    # Realizamos la deteccion de bordes por medio del algoritmo Canny
    img_canny = cv2.Canny(img_gaussiana, 50, 100)
    #cv2.imshow('canny', img_canny)
    #cv2.waitKey(0)
    # Deteccion de contornos
    (contornos, _) = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contornos)
    # print(_)
    #cv2.waitKey(0)
    new_path = "imagenes-contadas/"+file_name
    img_contornos = img.copy()
    cv2.drawContours(img_contornos,contornos,-1,(0,255,0), 2)
    cv2.imwrite(new_path,img_contornos) 
    #cv2.imshow("contornos", img_contornos)

    # Realizar los rectangulos para delimitar la region de interes (ROI)
    objetos = 0
    img_roi = img.copy()
    for c in contornos:
        (x,y,w,h) = cv2.boundingRect(c)
        color = (0,255,0)
        cv2.rectangle(img_roi, (x,y),(x+w,y+h), color, 2)
        objetos += 1
    # cv2.imshow("ROI", img_roi)

    print("Se encontraron {} objetos".format(objetos))

    total = objetos
    # Esperar presion de alguna tecla para finalizar
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return total, new_path

def subir_imagen_cloudinary(path, id_photo_colony):
    
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api

    print("Entre a cloudinary")
    cloudinary.config( 
      cloud_name = "rogerarjona", 
      api_key = "577752173664429", 
      api_secret = "Uk0ZBbLFwPS1l5ZUbNbD3qYqONY" 
    )

    notification_url = url_webhook+"post-obtener-imagen-cloudinary/"
    tags = "contado##{id_photo_colony}".format(id_photo_colony=id_photo_colony)
    
    try:
        cloudinary.uploader.upload(path,tags=tags)
        print("Imagen Subida")
    except Exception as e:
        print(e)
    
####### COLONY ELEMENTS ############
@csrf_exempt
def post_actualizar_colony_elements(request):

    mensaje = "Elementos no guardados"
    error = "123" 

    _request = request.body
    python_dict = json.loads(_request)

    id_photo_colony = python_dict.get("id_photo_colony")
    username = python_dict.get("username")
    temperature = python_dict.get("temperatura")
    form = python_dict.get("colony_form")
    surface = python_dict.get("colony_surface") 
    edge = python_dict.get("colony_edge")
    elevation = python_dict.get("colony_elevation") 
    color = python_dict.get("color") 
    size = 0 
    growth = python_dict.get("colony_growth") 
    observation = python_dict.get("observaciones")

    colony_elements = agregar_colony_elements_a_photo(id_photo_colony, temperature, form, surface, edge, elevation, color, size, growth, observation)
    if colony_elements:
        mensaje = "Elementos Guardados Correctamente"
        error = False

    response = {"Mensaje":mensaje, "ErrorCode": error}
    
    return HttpResponse(response, content_type='aplication/json')

@csrf_exempt
def post_obtener_colony_elements(request):

    _request = request.body
    python_dict = json.loads(_request)

    id_photo_colony = python_dict.get("id_photo_colony")
    colony_elements = obtener_colony_elements(id_photo_colony)

    colony_elements_map = []
    if colony_elements:
        temperature = colony_elements.temperature
        form = colony_elements.get_form_display()
        surface = colony_elements.get_surface_display()
        edge = colony_elements.get_edge_display()
        elevation = colony_elements.get_elevation_display()
        color = colony_elements.color
        size = colony_elements.size
        growth = colony_elements.get_growth_display()
        observation = colony_elements.observation
        photography_url = colony_elements.photography.url_thumbnail
        photography_counted_url = colony_elements.photography.url_contado_thumbnail

        colony_elements_map.append({"temperatura":temperature, "colony_form":form, "colony_surface":surface, "colony_edge":edge,
        "colony_elevation":elevation, "color":color, "size":size, "colony_growth":growth, "observacion":observation,
        "photography_url_thumbnail":photography_url, "photography_counted_url_thumbnail":photography_counted_url
        })

        response = json.dumps({"colony_elements":colony_elements_map})

    return HttpResponse(response, content_type='aplication/json')

def agregar_colony_elements_a_photo(id_photo_colony, temperature, form, surface, edge, elevation, color, size, growth, observation):

    try:
        colony_elements = ColonyElements.objects.get(photography__id=id_photo_colony)
        colony_elements.temperature = temperature
        colony_elements.form = form
        colony_elements.surface = surface
        colony_elements.edge = edge
        colony_elements.elevation = elevation
        colony_elements.color = color
        colony_elements.size = size
        colony_elements.growth = growth 
        colony_elements.observation = observation
        colony_elements.save()
    except Exception as e:
        colony_elements = None

    return colony_elements

def obtener_colony_elements(id_photo_colony):
    
    try:
        colony_elements = ColonyElements.objects.select_related("photography").get(photography__id=id_photo_colony)
    except Exception as e:
        colony_elements = None

    return colony_elements


######### PAGINA WEB #############
def dashboard(request):
    usuario = request.user

    return render(request, 'dashboard.html', {})

def lista_proyectos(request):
    
    usuario = request.user

    try:
        proyectos = ColonyProyect.objects.filter(user=usuario)
    except ColonyProyect.DoesNotExist:
        proyectos = None

    return render(request, 'lista_proyectos.html', {'proyectos':proyectos})

def lista_imagenes_proyecto(request, id_proyecto):

    usuario = request.user
    nombre_proyecto = ""
    try:
        project = ColonyProyect.objects.get(id=id_proyecto)
        imagenes_proyecto = PhotoColony.objects.select_related("proyecto").filter(user=usuario, proyecto=project)
    except ColonyProyect.DoesNotExist:
        imagenes_proyecto = None

    return render(request, 'lista_imagenes_proyecto.html', {'lista_imagenes':imagenes_proyecto, "nombre_proyecto":nombre_proyecto})


def datos_colony_elements(request, id_photo_colony):
    usuario = request.user

    try:
        instance_colony_elements = ColonyElements.objects.select_related("photography", "proyect").get(photography__id=id_photo_colony)
    except Exception as e:
        instance_colony_elements = None
    
    url_regreso = reverse('lista_imagenes_proyecto', args=[instance_colony_elements.proyect.id])

    if request.method == "POST":
        form = ActualizarColonyElementsForm(request.POST, instance=instance_colony_elements)
        if form.is_valid():
            form.save()
            
            messages.success(request, "Se actualizaron correctamente los datos de la Fotografia")
            return HttpResponseRedirect(url_regreso)
    else:
        form = ActualizarColonyElementsForm(instance=instance_colony_elements)
        
    return render(request, 'datos_colony_elements.html',{'url_regreso':url_regreso, 'form':form, 'instance_colony_elements':instance_colony_elements})

def crear_proyecto(request):
    usuario = request.user

    if request.method == "POST":
        form = CrearProyectoForm(request.POST)
        if form.is_valid():
            _form = form.save(commit=False)
            _form.user = usuario
            _form.save()

            messages.success(request, "Se actualizaron correctamente los datos de la Fotografia")
            return HttpResponseRedirect(reverse('lista_proyectos'))
    else:
        form = CrearProyectoForm()

    return render(request, 'crear_proyecto.html', {"form":form})