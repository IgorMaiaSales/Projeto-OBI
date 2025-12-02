from rest_framework import serializers
from .models import Problema, Submissao
from django.contrib.auth.models import User

class ProblemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problema
        # Escolhemos quais campos vamos entregar para o React
        fields = ['id', 'titulo', 'slug', 'enunciado', 'nivel']

class SubmissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissao
        fields = ['id', 'codigo', 'status', 'tempo', 'data']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Esta função garante que a senha seja criptografada
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user