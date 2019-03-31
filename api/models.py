from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
# Create your models here.

class PhotoColony(models.Model):
    
    public_id = models.CharField(max_length=50)
    url_thumbnail = models.URLField(blank=True, null=True)
    url_imagen = models.URLField(blank=True, null=True)
    url_contado = models.URLField(blank=True, null=True)
    url_contado_thumbnail = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    user = models.ForeignKey(User, related_name='photo_colony_user', verbose_name="Creado Por", on_delete=models.SET_NULL, null=True, blank=True)
    proyecto = models.ForeignKey("api.ColonyProyect", related_name="photo_colony_proyecto", on_delete=models.SET_NULL, null=True)

class ColonyElements(models.Model):

    #Forma que tiene la colonia a simple vista
    PUNTIFORME = 1
    CIRCULAR = 2
    IRREGULAR = 3
    RIZOIDE = 4
    FUSIFORME = 5 
    COLONY_FORM = ((PUNTIFORME, "Puntiforme"), (CIRCULAR, "Circular"), (IRREGULAR, "Irregular"), (RIZOIDE, "Rizoide"), (FUSIFORME, "Fusiforme"),)

    #Superficie de las colonias
    LISA = 1
    RUGOSA = 2
    PLEGADA = 3
    COLONY_SURFACE = ((LISA, "Lisa"),(RUGOSA, "Rugosa"),(PLEGADA, "Plegada"),)

    #Borde de las colonias
    REDONDEADO = 1
    ONDULADO = 2
    LOBULADO = 3
    FILAMENTOSO = 4
    COLONY_EDGE = ((REDONDEADO, "Redondeado"),(ONDULADO, "Ondulado"),(LOBULADO, "Lobulado"),(FILAMENTOSO, "Filamentoso"))

    #Elevacion de la colonia respecto a la placa de petri
    PLANO = 1
    CONVEXA = 2
    ELEVADA = 3
    COLONY_ELEVATION = ((PLANO, "Plana"),(CONVEXA, "Convexa"),(ELEVADA, "Elevada"))

    #Crecimiento de la colonia
    SIN_CRECIMIENTO = 1
    REGULAR = 2
    ABUNDANTE = 3
    COLONY_GROWTH = ((SIN_CRECIMIENTO, "Sin Crecimiento"),(REGULAR, "Crecimiento Regular"),(ABUNDANTE, "Crecimient Abundante"))

    temperature = models.SmallIntegerField(default=0)
    form = models.PositiveSmallIntegerField(choices=COLONY_FORM, default=PUNTIFORME,)
    surface = models.PositiveSmallIntegerField(choices=COLONY_SURFACE, default=LISA,)
    edge = models.PositiveSmallIntegerField(choices=COLONY_EDGE, default=REDONDEADO,)
    elevation = models.PositiveSmallIntegerField(choices=COLONY_ELEVATION, default=PLANO,)
    color = models.CharField(max_length=50, default="")
    size = models.SmallIntegerField(default=0)
    growth = models.PositiveSmallIntegerField(choices=COLONY_GROWTH, default=SIN_CRECIMIENTO,)
    observation = models.TextField(blank=True)

    photography = models.ForeignKey("PhotoColony", related_name="photo_colony_elements", on_delete=models.SET_NULL, null=True)
    proyect = models.ForeignKey("api.ColonyProyect", related_name="colony_elements_proyect", on_delete=models.SET_NULL, null=True)

class ColonyProyect(models.Model):
    
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    descripcion = models.TextField(default="", blank=True)
    url_imagen = models.URLField(default="https://res.cloudinary.com/rogerarjona/image/upload/c_thumb,w_200,g_face/v1553401632/colony_default.png", null=True)
    url_thumbnail = models.URLField(default="https://res.cloudinary.com/rogerarjona/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1553404423/colony_300_default.png", blank=True, null=True)
    #colony_elements = models.ForeignKey("ColonyElements", related_name="colony_elements_proyect", on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, related_name='colony_proyect_user', verbose_name="Creado Por", on_delete=models.SET_NULL, null=True, blank=True)

class PerfilUsuario(models.Model):

    avatar = StdImageField(upload_to='usuarios/%Y/%m/',
                          variations={'perfil': {"width": 240, "height": 240, "crop": True}, 'thumbnail': {"width": 45, "height": 45, "crop": True} }, default="usuarios/avatar.png") 
    
    #Foreign Keys
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return u'Perfil de: %s' % self.user.username