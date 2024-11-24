"""
Definición de formularios utilizados en la aplicación gestion.

Estos formularios están basados en los modelos Cliente y Reserva.
Se utilizan para validar y procesar datos ingresados por el usuario
en las interfaces de la aplicación.
"""
from django import forms
from gestion.models import Cliente, Reserva

class ClienteForm(forms.ModelForm):
    """
    Formulario para manejar la creación y edición de clientes.

    Campos:
        - rut: Identificador único del cliente.
        - nombre: Nombre del cliente.
        - apellido: Apellido del cliente.
        - correo: Correo electrónico del cliente.
        - telefono: Teléfono de contacto del cliente.
    """
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'correo', 'telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReservaForm(forms.ModelForm):
    """
    Formulario para manejar la creación y edición de reservas.

    Campos:
        - habitacion: Habitación reservada.
        - cliente: Cliente asociado a la reserva.
        - estado: Estado actual de la reserva (pendiente, confirmada, etc.).
    """
    class Meta:
        model = Reserva
        fields = ['habitacion', 'cliente', 'estado']
        widgets = {
            'habitacion': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

