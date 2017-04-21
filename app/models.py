from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Sala(models.Model):
    ESTADOS = (
        ('R', 'Reservado'),
        ('D', 'Disponible'),
        ('ND', 'No disponible'),
        ('C', 'Confirmado'),
    )
    nombre = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=2, choices=ESTADOS, default='D')

    def __unicode__(self):
        return str(self.id)


class Insumo(models.Model):
    nombre = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    sala_origen = models.ForeignKey(Sala, unique=False, blank=True, null=True)

    def __unicode__(self):
        return str(self.nombre)


class Reserva(models.Model):

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cantidad = models.IntegerField()
    insumos = models.ManyToManyField(Insumo)
    empleado = models.ForeignKey(User)
    sala = models.ForeignKey(Sala, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)


class Solicitud(models.Model):
    mensaje = models.TextField(max_length=100)
    reserva = models.ForeignKey(Reserva)
    estado = models.NullBooleanField(blank=True, default=None)
    sala = models.ForeignKey(Sala)

    def __unicode__(self):
        return str(self.id)