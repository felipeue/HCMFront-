from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import six
from django.core.exceptions import PermissionDenied
from forms import *
from django.db.models import Q

# Create your views here.


def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group

        if user.groups.filter(name__in=groups).exists():
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)


def index(request):
    return render(request, 'index.html', {})


def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index_admin/')
            else:
                return render_to_response('login_error.html', {})
        else:
            return HttpResponseRedirect('/login_admin/')
    else:
        return render(request, 'login_admin.html', {})


@login_required
@group_required('Administrador')
def dashboard_admin(request):
    salas = Sala.objects.all()
    return render(request, 'index_admin.html', {'salas': salas})


@login_required
@group_required('Administrador')
def agregar_sala(request):
    if request.method == 'POST':
        sala_form = SalaForm(data=request.POST)
        if sala_form.is_valid():
            sala_form.save()
            return HttpResponseRedirect('/index_admin/')
    else:
        sala_form = SalaForm()
    return render(request, 'agregar_sala.html', {'sala_form': sala_form})


@login_required
@group_required('Administrador')
def agregar_insumo(request, sala_id):
    s = Sala.objects.get(id=sala_id)
    insumos = Insumo.objects.filter(sala_origen=s)
    if request.method == 'POST':
        insumo_form = InsumoForm(data=request.POST)
        if insumo_form.is_valid():
            i = insumo_form.save(commit=False)
            i.sala_origen = s
            i.save()
            return HttpResponseRedirect('/agregar_insumo/%s/' % sala_id)
    else:
        insumo_form = InsumoForm()
    return render(request, 'agregar_insumo.html', {'insumo_form': insumo_form, 'insumos': insumos, 's': s})


def login_empleado(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index_empleado/')
            else:
                return render_to_response('login_error.html', {})
        else:
            return HttpResponseRedirect('/login_empleado/')
    else:
        return render(request, 'login_empleado.html', {})


@login_required
@group_required('Empleado')
def dashboard_empleado(request):
    return render(request, 'index_empleado.html', {})


@login_required
@group_required('Empleado')
def agregar_reserva(request):
    current = request.user
    if request.method == 'POST':
        reserva_form = ReservaForm(data=request.POST)
        if reserva_form.is_valid():
            r = reserva_form.save(commit=False)
            r.empleado = current
            r.save()
            return HttpResponseRedirect('/agregar_insumo_reserva/%s/' % r.id)
    else:
        reserva_form = ReservaForm()
    return render(request, 'agregar_reserva.html', {'reserva_form': reserva_form})


@login_required
@group_required('Empleado')
def agregar_insumo_reserva(request, reserva_id):
    r = Reserva.objects.get(id=reserva_id)
    if request.method == 'POST':
        insumo_form = InsumoForm(data=request.POST)
        if insumo_form.is_valid():
            i = insumo_form.save()
            r.insumos.add(i)
            r.save()
            return HttpResponseRedirect('/agregar_insumo_reserva/%s/' % r.id)
    else:
        insumo_form = InsumoForm()
    return render(request, 'agregar_insumo_reserva.html', {'insumo_form': insumo_form, 'r': r})


@login_required
@group_required('Empleado')
def salas_recomendadas(request, reserva_id):
    r = Reserva.objects.get(id=reserva_id)
    salas = Sala.objects.filter(hora_inicio__lte=r.hora_inicio, hora_fin__gte=r.hora_fin, capacidad__gte=r.cantidad).exclude(Q(estado='ND') | Q(estado='C'))
    return render(request, 'salas_recomendadas.html', {'salas': salas, 'r': r})


@login_required
@group_required('Empleado')
def reservar_sala(request, sala_id, reserva_id):
    s = Sala.objects.get(id=sala_id)
    r = Reserva.objects.get(id=reserva_id)
    r.sala = s
    r.save()
    s.estado = 'R'
    s.save()
    return HttpResponseRedirect('/salas_recomendadas/%s/' % r.id)


@login_required
@group_required('Empleado')
def enviar_solicitud(request, reserva_id):
    r = Reserva.objects.get(id=reserva_id)
    if request.method == 'POST':
        solicitud_form = SolicitudForm(data=request.POST)
        if solicitud_form.is_valid():
            s = solicitud_form.save(commit=False)
            s.reserva = r
            s.save()
            return HttpResponseRedirect('/confirmacion/')
    else:
        solicitud_form = SolicitudForm()
    return render(request, 'agregar_solicitud.html', {'solicitud_form': solicitud_form, 'r': r})


@login_required
@group_required('Empleado')
def envio_exitoso(request):
    return render(request, 'confirmacion.html', {})