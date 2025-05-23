"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from principal import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("portfolio-details/", views.portfolio, name="portfolio"),
    path("service-details/", views.service, name="service-details"),
    path("starter-page/", views.starter, name="starter-page"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("panel-admin/", views.panel_admin, name="panel-admin"),
    path("posteos/", views.listar_posteos, name="listar_posteos"),
    path("posteos/editar/<str:posteo_id>/", views.editar_posteo, name="editar_posteo"),
    path(
        "posteos/eliminar/<str:posteo_id>/",
        views.eliminar_posteo,
        name="eliminar_posteo",
    ),
    path("contacto/", views.contacto, name="contacto"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
