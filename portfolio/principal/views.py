from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .utils.conectar import conectar_db
from bson.objectid import ObjectId
from django.core.mail import send_mail


# Create your views here.
def inicio(request):
    coleccion_trabajos = conectar_db()
    trabajos = list(coleccion_trabajos.find().sort("fecha", -1))
    categorias = coleccion_trabajos.find({}, {"_id": 0, "categoria": 1})
    categorias_unicas = {doc["categoria"] for doc in categorias if "categoria" in doc}
    categorias_unicas = sorted(categorias_unicas)

    return render(
        request,
        "principal/index.html",
        {"trabajos": trabajos, "categorias": categorias_unicas},
    )  # Aquí 'index.html' es tu archivo HTML


def portfolio(request):
    return render(request, "principal/portfolio-details.html")


def service(request):
    return render(request, "principal/service-details.html")


def starter(request):
    return render(request, "principal/starter-page.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def panel_admin(request):
    if request.method == "POST":
        # Aquí puedes manejar los datos del formulario si es necesario
        titulo = request.POST["titulo"]
        descripcion = request.POST["descripcion"]
        categoria = request.POST["categoria"]
        imagenes = request.FILES.getlist("imagenes")
        fecha = request.POST["fecha"]
        # Aquí puedes guardar los datos en la base de datos o realizar otras acciones necesarias

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        rutas_imagenes = []
        for imagen in imagenes:
            nombre_imagen = fs.save(imagen.name, imagen)
            ruta_completa = os.path.join(settings.MEDIA_URL, nombre_imagen)
            rutas_imagenes.append(ruta_completa)

        trabajo = {
            "titulo": titulo,
            "descripcion": descripcion,
            "categoria": categoria,
            "imagenes": rutas_imagenes,
            "fecha": fecha,
        }
        # Establecer conexion
        trabajos_coleccion = conectar_db()
        trabajos_coleccion.insert_one(trabajo)
        return redirect(
            "inicio"
        )  # Redirigir a la página de inicio después de guardar los datos

    return render(request, "principal/panel-administracion.html")


@login_required
def listar_posteos(request):
    coleccion = conectar_db()
    posteos = list(coleccion.find().sort("fecha", -1))

    # Convertir _id a string y moverlo a una clave visible
    for post in posteos:
        post["id"] = str(post["_id"])

    return render(request, "principal/listar-posteos.html", {"posteos": posteos})


@login_required
def eliminar_posteo(request, posteo_id):
    trabajos_coleccion = conectar_db()
    trabajos_coleccion.delete_one({"_id": ObjectId(posteo_id)})
    return redirect("listar_posteos")


@login_required
def editar_posteo(request, posteo_id):
    trabajos_coleccion = conectar_db()
    posteo = trabajos_coleccion.find_one({"_id": ObjectId(posteo_id)})

    if request.method == "POST":
        titulo = request.POST["titulo"]
        descripcion = request.POST["descripcion"]
        categoria = request.POST["categoria"]
        fecha = request.POST["fecha"]

        imagenes = request.FILES.getlist("imagenes")
        rutas_imagenes = posteo.get("imagenes", [])
        if imagenes:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            rutas_imagenes = []
            for imagen in imagenes:
                nombre_imagen = fs.save(imagen.name, imagen)
                ruta_completa = os.path.join(settings.MEDIA_URL, nombre_imagen)
                rutas_imagenes.append(ruta_completa)

        trabajos_coleccion.update_one(
            {"_id": ObjectId(posteo_id)},
            {
                "$set": {
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "categoria": categoria,
                    "imagenes": rutas_imagenes,
                    "fecha": fecha,
                }
            },
        )
        return redirect("listar_posteos")

    return render(request, "principal/editar-posteo.html", {"posteo": posteo})


def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("name")
        email = request.POST.get("email")
        asunto = request.POST.get("subject")
        mensaje = request.POST.get("message")

        cuerpo_mensaje = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"

        send_mail(
            asunto,
            f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}",
            email,  # Remitente
            ["nicoga.96@gmail.com"],  # Cambiá esto por tu correo real
            fail_silently=False,
        )

        # 2. Guardar en MongoDB
        coleccion = conectar_db()  # Usa tu función personalizada
        coleccion.insert_one(
            {
                "nombre": nombre,
                "email": email,
                "asunto": asunto,
                "mensaje": mensaje,
            }
        )
        return redirect("contacto_exito")  # opcional

    return redirect("inicio")  # o redirigir a donde quieras si entran por GET


def contacto_exito(request):
    return render(request, "contacto_exito.html")


def procesar_formulario(request):
    if request.method == "POST":
        # Aquí procesas los datos del formulario
        # ...
        return redirect("contacto_exito")  # Redirigir a la página de éxito
    return render(request, "contacto.html")  # Mostrar el formulario si no es POST
