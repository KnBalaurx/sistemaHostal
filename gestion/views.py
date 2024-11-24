from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from gestion.models import Trabajador, Reserva, Cliente, Habitacion
from gestion.forms import ClienteForm, ReservaForm
from django.shortcuts import get_object_or_404

# Vista para manejar el inicio de sesión de los trabajadores.
def login_trabajador(request):
    """
    Procesa el inicio de sesión para trabajadores.
    Si el método es POST, se intenta autenticar al trabajador usando su RUT y una contraseña creada de su nombre y apellido.
    """
    if request.method == "POST":
        # Recupera los datos enviados desde el formulario
        rut = request.POST.get("rut")
        password = request.POST.get("password")
        try:
            # Busca al trabajador en la base de datos por su RUT
            trabajador = Trabajador.objects.get(rut=rut)
            # Genera la contraseña esperada basada en las primeras tres letras del apellido y nombre
            expected_password = trabajador.apellido[:3].lower() + trabajador.nombre[:3].lower()

            if password.lower() == expected_password:
                # Si la contraseña es correcta, guarda los datos del trabajador en la sesión
                request.session['trabajador_id'] = trabajador.id
                request.session['trabajador_nombre'] = f"{trabajador.nombre} {trabajador.apellido}"
                return redirect('home')  # Redirige a la página principal
            else:
                # Si la contraseña es incorrecta, muestra un mensaje de error
                messages.error(request, "Contraseña incorrecta.")
        except Trabajador.DoesNotExist:
            # Si el trabajador no existe, muestra un mensaje de error
            messages.error(request, "Trabajador no encontrado.")
    
    # Renderiza la página de inicio de sesión si no se envía un formulario válido
    return render(request, 'gestion/login.html')



# Vista para cerrar la sesión de un trabajador.
def logout_trabajador(request):
    """
    Finaliza la sesión del trabajador actual y lo redirige a la página de inicio de sesión.
    """
    logout(request)  # Cierra la sesión
    return redirect('login')  # Redirige al login

# Vista para agregar un nuevo cliente.
def agregar_cliente(request):
    """
    Procesa un formulario para agregar un nuevo cliente a la base de datos.
    Si el formulario es válido, guarda al cliente; si no, redirige a la página principal.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)  # Instancia el formulario con los datos enviados
        if form.is_valid():
            form.save()  # Guarda el cliente en la base de datos
            return redirect('home')  # Redirige a la página principal
        else:
            # Muestra errores del formulario en consola (solo para depuración)
            print(form.errors)
    return redirect('home')

# Vista para agregar una nueva reserva.
def agregar_reserva(request):
    """
    Procesa un formulario para crear una nueva reserva y actualiza el estado de la habitación asociada.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)  # Instancia el formulario con los datos enviados
        if form.is_valid():
            reserva = form.save()  # Guarda la reserva en la base de datos
            reserva.actualizar_estado_habitacion()  # Cambia el estado de la habitación asociada
            return redirect('home')  # Redirige a la página principal
    return redirect('home')

# Vista para la página principal del sistema.
def home(request):
    """
    Renderiza la página principal, que muestra:
    - Datos del trabajador autenticado.
    - Reservas activas.
    - Formularios para agregar clientes y reservas.
    """
    if 'trabajador_id' not in request.session:
        # Si no hay un trabajador autenticado, redirige al login
        return redirect('login')
    
    # Obtiene el trabajador autenticado usando su ID almacenado en la sesión
    trabajador = Trabajador.objects.get(id=request.session['trabajador_id'])
    # Obtiene todas las reservas
    reservas = Reserva.objects.all()
    # Instancia formularios vacíos para agregar clientes y reservas
    cliente_form = ClienteForm()
    reserva_form = ReservaForm()

    # Datos que se enviarán a la plantilla
    data = {
        'trabajador': trabajador,
        'reservas': reservas,
        'cliente_form': cliente_form,
        'reserva_form': reserva_form,
    }
    # Renderiza la plantilla con los datos proporcionados
    return render(request, 'gestion/home.html', data)

# Vista para mostrar la tabla de clientes.
def tabla_clientes(request):
    """
    Renderiza una tabla con los datos de todos los clientes registrados en el sistema.
    Solo se puede acceder si hay un trabajador autenticado.
    """
    if 'trabajador_id' not in request.session:
        # Si no hay un trabajador autenticado, redirige al login
        return redirect('login')
    
    # Obtiene todos los clientes
    clientes = Cliente.objects.all()
    # Recupera el nombre del trabajador desde la sesión
    trabajador = request.session['trabajador_nombre']
    # Datos que se enviarán a la plantilla
    data = {
        'clientes': clientes,
        'trabajador': trabajador,
    }
    # Renderiza la plantilla con la lista de clientes
    return render(request, 'gestion/clientes.html', data)

# Vista para mostrar la tabla de habitaciones.
def tabla_habitaciones(request):
    """
    Renderiza una tabla con los datos de todas las habitaciones disponibles.
    Solo se puede acceder si hay un trabajador autenticado.
    """
    if 'trabajador_id' not in request.session:
        # Si no hay un trabajador autenticado, redirige al login
        return redirect('login')
    
    # Obtiene todas las habitaciones
    habitaciones = Habitacion.objects.all()
    # Recupera el nombre del trabajador desde la sesión
    trabajador = request.session['trabajador_nombre']
    # Datos que se enviarán a la plantilla
    data = {
        'habitaciones': habitaciones,
        'trabajador': trabajador,
    }
    # Renderiza la plantilla con la lista de habitaciones
    return render(request, 'gestion/habitaciones.html', data)
