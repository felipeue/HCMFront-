from django import forms
from models import *


class SalaForm(forms.ModelForm):

    class Meta:
        model = Sala
        fields = ('nombre', 'ubicacion', 'capacidad', 'hora_inicio', 'hora_fin')


class InsumoForm(forms.ModelForm):

    class Meta:
        model = Insumo
        fields = ('nombre', 'cantidad')


class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ('fecha', 'hora_inicio', 'hora_fin', 'cantidad')


class SolicitudForm(forms.ModelForm):

    class Meta:
        model = Solicitud
        fields = ('mensaje',)