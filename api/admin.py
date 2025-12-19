from django.contrib import admin
from .models import Problema, ExemploDeProblema, CasoDeTeste

class ExemploInline(admin.StackedInline):
    """Permite editar os exemplos didáticos (com explicação)"""
    model = ExemploDeProblema
    extra = 0
    verbose_name = "Exemplo do Enunciado"
    verbose_name_plural = "Exemplos do Enunciado (Visíveis)"

class CasoDeTesteInline(admin.TabularInline):
    """Lista os arquivos de teste usados pelo Juiz (apenas leitura recomendada)"""
    model = CasoDeTeste
    extra = 0
    verbose_name = "Arquivo de Teste (Juiz)"
    verbose_name_plural = "Arquivos de Teste (Ocultos)"
    
    # Exibe os caminhos, mas evita que editem manualmente sem saber o que fazem
    readonly_fields = ('caminho_entrada', 'caminho_saida') 
    can_delete = True

class ProblemaAdmin(admin.ModelAdmin):
    inlines = [ExemploInline, CasoDeTesteInline]
    list_display = ('titulo', 'slug', 'nivel', 'ativo')
    search_fields = ('titulo', 'slug')
    prepopulated_fields = {"slug": ("titulo",)}

admin.site.register(Problema, ProblemaAdmin)