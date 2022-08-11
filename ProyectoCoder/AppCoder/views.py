from typing import List
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse
from AppCoder.models import Curso, Profesor, Avatar
from AppCoder.forms import CursoFormulario, ProfesorFormulario, UserRegisterForm, UserEditForm, AvatarFormulario
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

# Create your views here.
def curso(request):
      curso =  Curso(nombre="Desarrollo web", camada="19881")
      curso.save()
      documentoDeTexto = f"--->Curso: {curso.nombre}   Camada: {curso.camada}"
      return HttpResponse(documentoDeTexto)

@login_required
def inicio(request):
      return render(request, "AppCoder/inicio.html")

def estudiantes(request):
      return render(request, "AppCoder/estudiantes.html")

def entregables(request):
      return render(request, "AppCoder/entregables.html")


def cursos(request):
      if request.method == 'POST':
            miFormulario = CursoFormulario(request.POST) 
            print(miFormulario)
            if miFormulario.is_valid:   
                  informacion = miFormulario.cleaned_data
                  curso = Curso (nombre=informacion['curso'], camada=informacion['camada']) 
                  curso.save()
                  return render(request, "AppCoder/inicio.html") 
      else: 
            miFormulario= CursoFormulario() 
      return render(request, "AppCoder/cursos.html", {"miFormulario":miFormulario})

def profesores(request):
      if request.method == 'POST':
            miFormulario = ProfesorFormulario(request.POST) 
            print(miFormulario)
            if miFormulario.is_valid:   
                  informacion = miFormulario.cleaned_data
                  profesor = Profesor (nombre=informacion['nombre'], apellido=informacion['apellido'],
                  email=informacion['email'], profesion=informacion['profesion']) 
                  profesor.save()
                  return render(request, "AppCoder/inicio.html") 
      else: 
            miFormulario= ProfesorFormulario() 
      return render(request, "AppCoder/profesores.html", {"miFormulario":miFormulario})

def buscar(request):
      if  request.GET["camada"]: 
            camada = request.GET['camada'] 
            cursos = Curso.objects.filter(camada__icontains=camada)

            return render(request, "AppCoder/inicio.html", {"cursos":cursos, "camada":camada})
      else: 
        respuesta = "No enviaste datos"
      return HttpResponse(respuesta)

def leerProfesores(request):
      profesores = Profesor.objects.all()
      contexto= {"profesores":profesores} 
      return render(request, "AppCoder/leerProfesores.html",contexto)

def eliminarProfesor(request, profesor_nombre):
      profesor = Profesor.objects.get(nombre=profesor_nombre)
      profesor.delete()
      profesores = Profesor.objects.all() 
      contexto= {"profesores":profesores} 
      return render(request, "AppCoder/leerProfesores.html",contexto)

def editarProfesor(request, profesor_nombre):
      profesor = Profesor.objects.get(nombre=profesor_nombre)
      if request.method == 'POST':
            miFormulario = ProfesorFormulario(request.POST) 
            print(miFormulario)
            if miFormulario.is_valid:   
                  informacion = miFormulario.cleaned_data
                  profesor.nombre = informacion['nombre']
                  profesor.apellido = informacion['apellido']
                  profesor.email = informacion['email']
                  profesor.profesion = informacion['profesion']
                  profesor.save()
                  return render(request, "AppCoder/inicio.html")
      else: 
            miFormulario= ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido':profesor.apellido , 
            'email':profesor.email, 'profesion':profesor.profesion}) 
      return render(request, "AppCoder/editarProfesor.html", {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre})

class CursoList(ListView):
      model = Curso 
      template_name = "AppCoder/cursos_list.html"

class CursoDetalle(DetailView):
      model = Curso
      template_name = "AppCoder/curso_detalle.html"

class CursoCreacion(CreateView):
      model = Curso
      success_url = "/AppCoder/curso/list"
      fields = ['nombre', 'camada']

class CursoUpdate(UpdateView):
      model = Curso
      success_url = "/AppCoder/curso/list"
      fields  = ['nombre', 'camada']

class CursoDelete(DeleteView):
      model = Curso
      success_url = "/AppCoder/curso/list"

def logout_request(request):
      logout(request)
      messages.info(request, "No se generaron problemas")
      return redirect("inicio")
     
def login_request(request):
      if request.method == "POST":
            form = AuthenticationForm(request, data = request.POST)
            if form.is_valid():
                  usuario = form.cleaned_data.get('username')
                  contra = form.cleaned_data.get('password')
                  user = authenticate(username=usuario, password=contra)
                  if user is not None:
                        login(request, user)
                        return render(request,"AppCoder/inicio.html",  {"mensaje":f"Bienvenido {usuario}"} )
                  else: 
                        return render(request,"AppCoder/inicio.html", {"mensaje":"Error, datos incorrectos"} )
            else: 
                        return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Error, formulario erroneo"})
      form = AuthenticationForm()
      return render(request,"AppCoder/login.html", {'form':form} )

def register(request):
      if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Usuario Creado :)"})
      else:         
            form = UserRegisterForm()     
      return render(request,"AppCoder/registro.html" ,  {"form":form})

@login_required
def editarPerfil(request):
      usuario = request.user
      if request.method == 'POST':
            miFormulario = UserEditForm(request.POST) 
            if miFormulario.is_valid:  
                  informacion = miFormulario.cleaned_data
                  usuario.email = informacion['email']
                  usuario.password1 = informacion['password1']
                  usuario.password2 = informacion['password1']
                  usuario.save()
                  return render(request, "AppCoder/inicio.html") 
            else: 
                miFormulario= UserEditForm(initial={ 'email':usuario.email}) 
            return render(request, "AppCoder/editarPerfil.html", {"miFormulario":miFormulario, "usuario":usuario})

@login_required
def agregarAvatar(request):
      if request.method == 'POST':
            miFormulario = AvatarFormulario(request.POST, request.FILES) 
            if miFormulario.is_valid:   
                  u = User.objects.get(username=request.user)
                  avatar = Avatar (user=u, imagen=miFormulario.cleaned_data['imagen']) 
                  avatar.save()
                  return render(request, "AppCoder/inicio.html")
      else: 
            miFormulario= AvatarFormulario() 
      return render(request, "AppCoder/agregarAvatar.html", {"miFormulario":miFormulario})

def urlImagen():
      return "/media/avatares/imagenuno.png"

def sobreMi (request):
      return render (request, 'sobreMi.html')
