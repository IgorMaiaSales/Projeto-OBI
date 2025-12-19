from django.db import models
from django.contrib.auth.models import User

class Problema(models.Model):
    # Identificação
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) 
    
    # --- NOVA ESTRUTURA DE CLASSIFICAÇÃO ---
    ano = models.IntegerField(help_text="Ano da prova (ex: 2025)")
    fase = models.IntegerField(help_text="Fase da prova (1, 2, 3...)")
    
    # Opções fixas para evitar "Júnior" e "Junior" (padronização)
    NIVEL_CHOICES = [
        ('PJ', 'Iniciação (PJ)'),
        ('J', 'Júnior'),
        ('1', 'Nível 1'),
        ('2', 'Nível 2'),
        ('S', 'Sênior'),
    ]
    nivel = models.CharField(max_length=2, choices=NIVEL_CHOICES, default='J')
    # ---------------------------------------

    # Conteúdo Editorial
    enunciado = models.TextField()
    especificacao_entrada = models.TextField()
    especificacao_saida = models.TextField()
    restricoes = models.TextField()
    
    # Metadados Técnicos
    time_limit = models.IntegerField(default=1000)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} ({self.ano})"

class ExemploDeProblema(models.Model):
    """
    Representa os exemplos visíveis no enunciado (Vêm do info.json).
    Não são usados pelo juiz, apenas para o aluno ler.
    """
    problema = models.ForeignKey(Problema, related_name='exemplos', on_delete=models.CASCADE)
    entrada_texto = models.TextField()
    saida_texto = models.TextField()
    explicacao = models.TextField(blank=True, null=True, help_text="Texto explicativo didático")
    
    def __str__(self):
        return f"Exemplo de {self.problema.titulo}"

class CasoDeTeste(models.Model):
    """
    Representa os arquivos ocultos usados pelo Juiz (Vêm da varredura de pastas).
    """
    problema = models.ForeignKey(Problema, related_name='casos_teste', on_delete=models.CASCADE)
    
    # Organização por Subtarefas (Se for NULL, é um problema plano)
    subtarefa_id = models.IntegerField(null=True, blank=True)
    
    # Caminhos absolutos para os arquivos (Mais leve para o banco)
    caminho_entrada = models.CharField(max_length=500)
    caminho_saida = models.CharField(max_length=500)
    
    def __str__(self):
        tipo = f"Subtarefa {self.subtarefa_id}" if self.subtarefa_id else "Geral"
        return f"{self.problema.titulo} - {tipo}"

class Submissao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE)
    codigo = models.TextField()
    linguagem = models.CharField(max_length=50, default='python')
    status = models.CharField(max_length=50)
    tempo = models.FloatField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.problema.titulo} - {self.status}"
