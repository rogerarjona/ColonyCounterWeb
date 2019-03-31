from django import forms
from .forms import *
from .models import *

class ActualizarColonyElementsForm(forms.ModelForm):
	class Meta:
		model = ColonyElements
		exclude = ('proyect', 'photography')
		widgets = {
			'observation': forms.Textarea(attrs={'rows':4,}),
		}

class CrearProyectoForm(forms.ModelForm):
	class Meta:
		model = ColonyProyect
		exclude = ("created", "user", "url_imagen", "url_thumbnail")
		widgets = {
			'descripcion': forms.Textarea(attrs={'rows':4,}),
		}	