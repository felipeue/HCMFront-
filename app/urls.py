from django.conf.urls import include, url
from app import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_admin/$', views.login_admin),
    url(r'^index_admin/$', views.dashboard_admin),
    url(r'^agregar_sala/$', views.agregar_sala),
    url(r'^agregar_insumo/(?P<sala_id>[\w\-]+)/$', views.agregar_insumo),
    url(r'^login_empleado/$', views.login_empleado),
    url(r'^index_empleado/$', views.dashboard_empleado),
    url(r'^agregar_reserva/$', views.agregar_reserva),
    url(r'^agregar_insumo_reserva/(?P<reserva_id>[\w\-]+)/$', views.agregar_insumo_reserva),
    url(r'^salas_recomendadas/(?P<reserva_id>[\w\-]+)/$', views.salas_recomendadas),
    url(r'^reservar_sala/(?P<sala_id>[\w\-]+)/(?P<reserva_id>[\w\-]+)/$', views.reservar_sala),
    url(r'^agregar_solicitud/(?P<reserva_id>[\w\-]+)/$', views.enviar_solicitud),
    url(r'^confirmacion/$', views.envio_exitoso),
]