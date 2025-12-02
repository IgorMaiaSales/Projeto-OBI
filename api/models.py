from django.db import models
from django.contrib.auth.models import User

class Problema(models.Model):
    # Identificação
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) # Ex: soma-simples (usado na URL)
    
    # O conteúdo que o aluno lê 
    enunciado = models.TextField()
    especificacao_entrada = models.TextField(help_text="Explicação do formato de entrada")
    especificacao_saida = models.TextField(help_text="Explicação do formato de saída")
    restricoes = models.TextField(help_text="Ex: 1 <= N <= 100")
    
    # Organização
    nivel = models.CharField(max_length=50, default='Júnior')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class CasoDeTeste(models.Model):
    # Relacionamento: Um problema tem vários testes
    problema = models.ForeignKey(Problema, related_name='casos_teste', on_delete=models.CASCADE)
    
    # O Gabarito do Juiz
    entrada = models.TextField(help_text="O dado que o sistema joga no código do aluno")
    saida_esperada = models.TextField(help_text="A resposta exata que o código deve dar")
    
    # Se for True, aparece como exemplo no enunciado [cite: 36]
    eh_exemplo = models.BooleanField(default=False)

    def __str__(self):
        return f"Teste para {self.problema.titulo}"
    
class Submissao(models.Model):
    # Quem e O Que
    # Usuário
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Mas vamos deixar preparado.
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE)
    codigo = models.TextField()
    linguagem = models.CharField(max_length=50, default='python') # 'c' ou 'python'
    
    # O Resultado do Juiz
    status = models.CharField(max_length=50) # Ex: Accepted, Wrong Answer
    tempo = models.FloatField(null=True, blank=True) # Tempo que demorou
    data = models.DateTimeField(auto_now_add=True) # Data de hoje automática

    def __str__(self):
        return f"{self.problema.titulo} - {self.status}"
