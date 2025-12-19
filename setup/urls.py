from django.contrib import admin
from django.urls import path, include
from api.views import ListaProblemas, DetalheProblema, SubmeterSolucao

# Importações necessárias para o Login Social
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# --- CORREÇÃO DO ERRO 'SCOPE_DELIMITER' ---
class GoogleClientFix(OAuth2Client):
    """
    Classe personalizada para corrigir o conflito de versões entre dj-rest-auth e allauth.
    Remove o argumento 'scope_delimiter' dos kwargs se ele já estiver sendo passado,
    evitando o erro 'multiple values for argument'.
    """
    def __init__(self, *args, **kwargs):
        if 'scope_delimiter' in kwargs:
            del kwargs['scope_delimiter']
        super().__init__(*args, **kwargs)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = GoogleClientFix  # <--- Usamos nossa classe corrigida aqui

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas da API de Problemas
    path('problemas/', ListaProblemas.as_view()),
    path('problemas/<slug:slug>/', DetalheProblema.as_view()),
    path('problemas/<slug:slug>/submeter/', SubmeterSolucao.as_view()),

    # Autenticação
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Rota do Google usando a View corrigida
    path('auth/google/', GoogleLogin.as_view(), name='google_login')
]