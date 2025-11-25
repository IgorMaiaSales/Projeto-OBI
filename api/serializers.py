from rest_framework import serializers
from .models import Problema, Submissao

class ProblemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problema
        # Escolhemos quais campos vamos entregar para o React
        fields = ['id', 'titulo', 'slug', 'enunciado', 'nivel']

class SubmissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissao
        fields = ['id', 'codigo', 'status', 'tempo', 'data']