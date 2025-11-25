"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# Importamos a View lá da pasta 'api'
from api.views import ListaProblemas, DetalheProblema, SubmeterSolucao

urlpatterns = [
    path('admin/', admin.site.urls),

    # Quando acessar /problemas/, mostre a lista
    path('problemas/', ListaProblemas.as_view()),

    # Nova rota: O <slug:slug> é uma variável na URL
    # Exemplo: http://site.com/problemas/soma-simples/
    path('problemas/<slug:slug>/', DetalheProblema.as_view()),

    path('problemas/<slug:slug>/submeter/', SubmeterSolucao.as_view()),
]