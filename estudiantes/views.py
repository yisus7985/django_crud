from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from .models import Estudiante

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all().order_by('nombre')
    return render(request, 'estudiantes/lista.html', {'estudiantes': estudiantes})

def agregar_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        edad = request.POST['edad']
        correo = request.POST['correo']
        
        # Validar que el correo no esté ya registrado
        if Estudiante.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'estudiantes/agregar.html', {
                'error': 'El correo electrónico ya está registrado.',
                'datos': {'nombre': nombre, 'edad': edad, 'correo': correo}
            })
        
        # Crear el nuevo estudiante
        Estudiante.objects.create(nombre=nombre, edad=edad, correo=correo)
        
        # Redireccionar con mensaje de éxito
        success_msg = 'Estudiante agregado exitosamente'
        base_url = reverse('lista_estudiantes')
        query_params = urlencode({'success': success_msg})
        url = f'{base_url}?{query_params}'
        return HttpResponseRedirect(url)
    
    return render(request, 'estudiantes/agregar.html')

def editar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        edad = request.POST['edad']
        correo = request.POST['correo']
        
        # Validar que el correo no esté ya registrado (excepto el correo actual)
        if Estudiante.objects.filter(correo=correo).exclude(id=id).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'estudiantes/editar.html', {
                'error': 'El correo electrónico ya está registrado.',
                'estudiante': estudiante
            })
        
        # Actualizar el estudiante
        estudiante.nombre = nombre
        estudiante.edad = edad
        estudiante.correo = correo
        estudiante.save()
        
        # Redireccionar con mensaje de éxito
        success_msg = 'Estudiante actualizado exitosamente'
        base_url = reverse('lista_estudiantes')
        query_params = urlencode({'success': success_msg})
        url = f'{base_url}?{query_params}'
        return HttpResponseRedirect(url)
    
    return render(request, 'estudiantes/editar.html', {'estudiante': estudiante})

def eliminar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    nombre_estudiante = estudiante.nombre
    estudiante.delete()
    
    # Redireccionar con mensaje de éxito
    success_msg = f'Estudiante "{nombre_estudiante}" eliminado exitosamente'
    base_url = reverse('lista_estudiantes')
    query_params = urlencode({'success': success_msg})
    url = f'{base_url}?{query_params}'
    return HttpResponseRedirect(url)