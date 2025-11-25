from django.contrib import admin
from .models import Problema, CasoDeTeste

# Configuração para editar os testes DENTRO da página do problema
class CasoDeTesteInline(admin.TabularInline):
    model = CasoDeTeste
    extra = 1 # Começa com 1 campo vazio extra

class ProblemaAdmin(admin.ModelAdmin):
    inlines = [CasoDeTesteInline] # Adiciona os testes aqui
    list_display = ('titulo', 'nivel', 'ativo') # O que aparece na lista
    prepopulated_fields = {"slug": ("titulo",)} # Preenche o slug automático

# Registra no painel
admin.site.register(Problema, ProblemaAdmin)