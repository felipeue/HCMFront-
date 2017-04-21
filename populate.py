import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hcmfront.settings')
import django
django.setup()
from app.models import *
from django.contrib.auth.models import Group


def add_user(nombre, apellido, username):
    u = User.objects.get_or_create(username=username, first_name=nombre, last_name=apellido)[0]
    u.set_password('hcmfront2017')
    u.save()
    return u


def add_sala(nombre, ubicacion, capacidad, hora_inicio, hora_fin, estado):
    s = Sala.objects.get_or_create(nombre=nombre, ubicacion=ubicacion, capacidad=capacidad, hora_inicio=hora_inicio, hora_fin=hora_fin, estado=estado)[0]
    s.save()
    return s


def add_insumo(nombre, cantidad, sala):
    i = Insumo.objects.get_or_create(nombre=nombre, cantidad=cantidad, sala_origen=sala)[0]
    i.save()
    return i


def populate():

    x = add_user('Nicolas', 'Hanckes', 'administrador' )
    y = add_user('Felipe', 'Rios', 'empleado')
    z = add_user('Juan', 'Perez', 'empleado2')
    Group.objects.get_or_create(name='Administrador')
    Group.objects.get_or_create(name='Empleado')
    g = Group.objects.get(name='Administrador')
    gr = Group.objects.get(name='Empleado')
    x.groups.add(g)
    y.groups.add(gr)
    z.groups.add(gr)
    a = add_sala('Sala nueva', 'Valparaiso', 12, '13:00:00', '14:00:00', 'D')
    b = add_sala('Sala vieja', 'Santiago', 12, '14:00:00', '15:00:00', 'D')
    c = add_sala('Sala normal', 'Providencia', 12, '15:00:00', '16:00:00', 'D')

    add_insumo('Pizarron', 1, a)
    add_insumo('Pizarron', 1, b)
    add_insumo('Pizarron', 1, c)
    add_insumo('Proyector', 1, a)
    add_insumo('Proyector', 1, b)
    add_insumo('Proyector', 1, c)
    add_insumo('Plumon', 12, c)
    add_insumo('Borrador', 1, c)
    add_insumo('Cuaderno', 5, a)
    add_insumo('Pc', 5, b)


if __name__ == '__main__':

    print "Iniciando..."
    populate()

