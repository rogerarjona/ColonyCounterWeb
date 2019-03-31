from django.contrib import admin
from .models import *
# Register your models here.

class ColonyProyectAdmin(admin.ModelAdmin):
    model=ColonyProyect
    search_fields = ('id','name', "user")
    list_display = ('id','name','created','user')
    raw_id_fields = ['user',]
    
admin.site.register(ColonyProyect, ColonyProyectAdmin)

class PhotoColonyAdmin(admin.ModelAdmin):
    model=PhotoColony
    search_fields = ('id',"user")
    list_display = ('id','created','user', 'proyecto')
    raw_id_fields = ['user','proyecto']
    
admin.site.register(PhotoColony, PhotoColonyAdmin)

class ColonyElementsAdmin(admin.ModelAdmin):
    model=ColonyElements
    search_fields = ('id',"proyect")
    list_display = ('id','proyect')
    raw_id_fields = ['photography','proyect']
    
admin.site.register(ColonyElements, ColonyElementsAdmin)