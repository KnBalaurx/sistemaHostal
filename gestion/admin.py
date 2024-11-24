from django.contrib import admin
from .models import Cliente, Trabajador, Habitacion, Reserva, CheckIn, CheckOut


@admin.register(Cliente)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'correo', 'telefono', 'fecha_registro')
    search_fields = ('rut', 'nombre', 'apellido', 'correo')
    list_filter = ('fecha_registro',)


@admin.register(Trabajador)
class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido')
    search_fields = ('rut', 'nombre', 'apellido')


@admin.register(Habitacion)
class HabitacionesAdmin(admin.ModelAdmin):
    list_display = ('numero_habitacion', 'precio', 'estado')
    search_fields = ('numero_habitacion',)
    list_filter = ('estado',)


@admin.register(Reserva)
class ReservasAdmin(admin.ModelAdmin):
    list_display = ('id', 'habitacion', 'trabajador', 'cliente', 'origen', 'estado', 'fecha')
    search_fields = ('id', 'habitacion__numero_habitacion', 'cliente__rut')
    list_filter = ('origen', 'estado', 'fecha')


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'fecha_hora', 'qr_escaneado')
    search_fields = ('reserva__id',)
    list_filter = ('fecha_hora', 'qr_escaneado')


@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'fecha_hora', 'qr_escaneado')
    search_fields = ('reserva__id',)
    list_filter = ('fecha_hora', 'qr_escaneado')

