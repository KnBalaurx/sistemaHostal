"""
Definición de los modelos de la aplicación gestion.

Estos modelos representan las entidades principales del sistema,
como clientes, trabajadores, habitaciones, reservas y registros de
check-in/check-out.
"""
from django.db import models
from django.utils.timezone import now

class Cliente(models.Model):
    """
    Modelo que representa un cliente del hostal.

    Atributos:
        - rut: Identificador único del cliente.
        - nombre: Nombre del cliente.
        - apellido: Apellido del cliente.
        - correo: Correo electrónico del cliente.
        - telefono: Número de teléfono del cliente.
        - password_hash: Contraseña cifrada del cliente.
        - fecha_registro: Fecha de registro del cliente en el sistema.
    """
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    password_hash = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"


class Trabajador(models.Model):
    """
    Modelo que representa un trabajador del hostal.

    Atributos:
        - rut: Identificador único del trabajador.
        - nombre: Nombre del trabajador.
        - apellido: Apellido del trabajador.
    """
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"


class Habitacion(models.Model):
    """
    Modelo que representa una habitación del hostal.

    Atributos:
        - numero_habitacion: Número identificador de la habitación.
        - precio: Precio de la habitación.
        - estado: Estado actual de la habitación (disponible, reservada, etc.).
    """
    numero_habitacion = models.CharField(max_length=10, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ESTADO_CHOICES = [
        ("disponible", "Disponible"),
        ("reservada", "Reservada"),
        ("mantenimiento", "En Mantenimiento"),
    ]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="disponible")

    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.estado}"


class Reserva(models.Model):
    """
    Modelo que representa una reserva en el hostal.

    Atributos:
        - habitacion: Habitación asociada a la reserva.
        - trabajador: Trabajador encargado de la reserva.
        - cliente: Cliente asociado a la reserva.
        - numero_habitacion: Número de la habitación reservada.
        - origen: Origen de la reserva (manual o de otra plataforma).
        - estado: Estado actual de la reserva.
        - fecha: Fecha en la que se realizó la reserva.
    """
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.SET_NULL, null=True, blank=True
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, blank=True
    )
    numero_habitacion = models.CharField(max_length=10)
    ORIGEN_CHOICES = [
        ("manual", "Manual"),
        ("otra_plataforma", "Otra Plataforma"),
    ]
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default="manual")
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("finalizada", "Finalizada"),
    ]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="pendiente")
    fecha = models.DateTimeField(default=now)

    def __str__(self):
        return f"Reserva {self.id} - Habitación {self.numero_habitacion}"

    def actualizar_estado_habitacion(self):
        """
        Actualiza el estado de la habitación asociada según el estado de la reserva.
        """
        if self.habitacion:
            if self.estado == "finalizada":
                self.habitacion.estado = "reservada"
            else:
                self.habitacion.estado = "disponible"
            self.habitacion.save()


class CheckIn(models.Model):
    """
    Modelo que representa un registro de entrada (Check-In).

    Atributos:
        - reserva: Reserva asociada al Check-In.
        - fecha_hora: Fecha y hora del Check-In.
        - qr_escaneado: Indica si el QR fue escaneado.
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=now)
    QR_CHOICES = [
        ("sí", "Sí"),
        ("no", "No"),
    ]
    qr_escaneado = models.CharField(max_length=2, choices=QR_CHOICES, default="no")

    def __str__(self):
        return f"Check-In de Reserva {self.reserva.id}"


class CheckOut(models.Model):
    """
    Modelo que representa un registro de salida (Check-Out).

    Atributos:
        - reserva: Reserva asociada al Check-Out.
        - fecha_hora: Fecha y hora del Check-Out.
        - qr_escaneado: Indica si el QR fue escaneado.
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=now)
    QR_CHOICES = [
        ("sí", "Sí"),
        ("no", "No"),
    ]
    qr_escaneado = models.CharField(max_length=2, choices=QR_CHOICES, default="no")

    def __str__(self):
        return f"Check-Out de Reserva {self.reserva.id}"


