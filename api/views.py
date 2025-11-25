from django.http import JsonResponse
import requests
import time
import base64

from rest_framework import generics
from .models import Problema
from .serializers import ProblemaSerializer

def hello_juiz(request):
    # 1. Configuração
    BASE_URL = "https://ce.judge0.com"
    codigo_fonte = "print('Ola OBI via Django')" 
    codigo_b64 = base64.b64encode(codigo_fonte.encode('utf-8')).decode('utf-8')
    
    payload = {
        "source_code": codigo_fonte,
        "language_id": 71, 
        "stdin": "",       
        "expected_output": "Ola OBI via Django"
    }

    # 2. Envia para o Juiz
    try:
        response = requests.post(f"{BASE_URL}/submissions/?base64_encoded=false&wait=false", json=payload)
        token = response.json().get("token")
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

    # 3. Espera o resultado (Polling simples)
    status = "Processing"
    resultado_final = {}
    
    while status in ["Processing", "In Queue"]:
        time.sleep(1) # Espera 1 seg
        res = requests.get(f"{BASE_URL}/submissions/{token}?base64_encoded=false")
        resultado_final = res.json()
        status = resultado_final["status"]["description"]

    # 4. Retorna o JSON para o navegador
    return JsonResponse({
        "mensagem": "Teste realizado com sucesso!",
        "status_juiz": status,
        "saida_codigo": resultado_final.get("stdout"),
        "tempo": resultado_final.get("time")
    })

# Busca os problemas e lista na página
class ListaProblemas(generics.ListAPIView):
    queryset = Problema.objects.filter(ativo=True)
    serializer_class = ProblemaSerializer

# Busca apenas um problema usando o 'slug'
class DetalheProblema(generics.RetrieveAPIView):
    queryset = Problema.objects.filter(ativo=True)
    serializer_class = ProblemaSerializer
    lookup_field = 'slug' # Vamos buscar pelo slug (ex: soma-simples)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Problema, Submissao
from .serializers import SubmissaoSerializer
import requests
import base64
import time

class SubmeterSolucao(APIView):
    def post(self, request, slug):
        # 1. Achar o problema que o aluno quer resolver
        problema = get_object_or_404(Problema, slug=slug)
        codigo = request.data.get('codigo')
        
        # 2. Pegar o PRIMEIRO caso de teste (Para o MVP, vamos testar só 1 por enquanto)
        # No futuro, faremos um loop por todos os casos
        caso_teste = problema.casos_teste.first()
        
        if not caso_teste:
            return Response({"erro": "Este problema não tem casos de teste cadastrados!"}, status=400)

        # 3. Preparar dados para o Judge0
        # Codifica tudo em base64 para evitar erros com quebras de linha
        source_b64 = base64.b64encode(codigo.encode('utf-8')).decode('utf-8')
        stdin_b64 = base64.b64encode(caso_teste.entrada.encode('utf-8')).decode('utf-8')
        expected_b64 = base64.b64encode(caso_teste.saida_esperada.encode('utf-8')).decode('utf-8')

        payload = {
            "source_code": source_b64,
            "language_id": 71, # Python (Judge0 ID)
            "stdin": stdin_b64,
            "expected_output": expected_b64
        }
        
        # 4. Enviar para o Juiz
        url = "https://ce.judge0.com/submissions/?base64_encoded=true&wait=true" 
        # Nota: usaremos 'wait=true' para o Django esperar a resposta na mesma hora (mais simples pro MVP)
        
        try:
            print(f"Enviando para Judge0: {payload}") # Debug 1
            resposta_judge = requests.post(url, json=payload)
            print(f"Status HTTP Judge0: {resposta_judge.status_code}") # Debug 2
            print(f"Resposta bruta Judge0: {resposta_judge.text}") # Debug 3
            
            res = resposta_judge.json()
        except Exception as e:
            print(f"ERRO CRÍTICO NO BACKEND: {e}") # Vai mostrar o erro no terminal
            return Response({"erro": f"Falha interna: {str(e)}"}, status=500)

        # 5. Ler o veredito
        status_juiz = res.get('status', {}).get('description', 'Erro')
        tempo = res.get('time')

        # 6. Salvar no Banco de Dados (Histórico)
        submissao = Submissao.objects.create(
            problema=problema,
            codigo=codigo,
            status=status_juiz,
            tempo=tempo if tempo else 0.0
        )

        # 7. Retornar para o React
        return Response(SubmissaoSerializer(submissao).data)