from rest_framework import serializers
from .models import Problema, Submissao, ExemploDeProblema
from django.contrib.auth.models import User

# 1. Serializer dos Exemplos Didáticos
class ExemploSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemploDeProblema
        fields = ['id', 'entrada_texto', 'saida_texto', 'explicacao']

# --- NOVO: Serializer Leve para a Home (Listagem) ---
class ProblemaSummarySerializer(serializers.ModelSerializer):
    # Cria o campo 'nivel_extenso' usando o método get_nivel_display do Model
    nivel_extenso = serializers.CharField(source='get_nivel_display', read_only=True)

    class Meta:
        model = Problema
        # Apenas os dados necessários para o card na tela
        fields = ['id', 'titulo', 'slug', 'nivel', 'nivel_extenso', 'ano', 'fase']

# 2. Serializer Completo para o Resolver (Detalhes)
class ProblemaDetailSerializer(serializers.ModelSerializer):
    entrada = serializers.CharField(source='especificacao_entrada', read_only=True)
    saida = serializers.CharField(source='especificacao_saida', read_only=True)
    nivel_extenso = serializers.CharField(source='get_nivel_display', read_only=True)
    exemplos = ExemploSerializer(many=True, read_only=True)

    class Meta:
        model = Problema
        fields = [
            'id', 'titulo', 'slug', 'nivel', 'nivel_extenso', 
            'ano', 'fase', # <--- ADICIONADO AQUI
            'enunciado', 'entrada', 'saida', 'restricoes', 'time_limit',
            'exemplos'
        ]

class SubmissaoSerializer(serializers.ModelSerializer):
    problema_slug = serializers.ReadOnlyField(source='problema.slug')

    class Meta:
        model = Submissao
        fields = ['id', 'problema_slug', 'codigo', 'status', 'tempo', 'data']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user