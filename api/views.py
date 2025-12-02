import json
import requests
import time
import base64

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Problema, Submissao
from .serializers import ProblemaSerializer, SubmissaoSerializer, UserSerializer

# --- View de Teste (Pode manter para debug) ---
def hello_juiz(request):
    BASE_URL = "https://ce.judge0.com"
    codigo_fonte = "print('Ola OBI via Django')" 
    
    payload = {
        "source_code": codigo_fonte,
        "language_id": 71, 
        "stdin": "",       
        "expected_output": "Ola OBI via Django"
    }

    try:
        response = requests.post(f"{BASE_URL}/submissions/?base64_encoded=false&wait=false", json=payload)
        token = response.json().get("token")
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

    status_desc = "Processing"
    resultado_final = {}
    
    while status_desc in ["Processing", "In Queue"]:
        time.sleep(1)
        res = requests.get(f"{BASE_URL}/submissions/{token}?base64_encoded=false")
        resultado_final = res.json()
        status_desc = resultado_final["status"]["description"]

    return JsonResponse({
        "mensagem": "Teste realizado com sucesso!",
        "status_juiz": status_desc,
        "saida_codigo": resultado_final.get("stdout"),
        "tempo": resultado_final.get("time")
    })

# --- Listagem e Detalhes de Problemas ---
class ListaProblemas(generics.ListAPIView):
    queryset = Problema.objects.filter(ativo=True)
    serializer_class = ProblemaSerializer

class DetalheProblema(generics.RetrieveAPIView):
    queryset = Problema.objects.filter(ativo=True)
    serializer_class = ProblemaSerializer
    lookup_field = 'slug'

# --- A LÓGICA DE SUBMISSÃO (CORRIGIDA) ---
class SubmeterSolucao(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, slug):
        # 1. Achar o problema
        problema = get_object_or_404(Problema, slug=slug)
        codigo = request.data.get('codigo')
        
        # 2. Pegar o caso de teste
        caso_teste = problema.casos_teste.first()
        if not caso_teste:
            return Response({"erro": "Este problema não tem casos de teste cadastrados!"}, status=400)

        # 3. Preparar dados (Base64)
        try:
            source_b64 = base64.b64encode(codigo.encode('utf-8')).decode('utf-8')
            stdin_b64 = base64.b64encode((caso_teste.entrada or "").encode('utf-8')).decode('utf-8')
            expected_b64 = base64.b64encode((caso_teste.saida_esperada or "").encode('utf-8')).decode('utf-8')
        except Exception as e:
            return Response({"erro": "Erro ao codificar dados para envio."}, status=400)

        payload = {
            "source_code": source_b64,
            "language_id": 71, # Python (71)
            "stdin": stdin_b64,
            "expected_output": expected_b64
        }
        
        # URL do Judge0 (Certifique-se que esta URL está correta para seu plano)
        url = "https://ce.judge0.com/submissions/?base64_encoded=true&wait=true" 
        
        # 4. Enviar para o Juiz com TRATAMENTO DE ERRO ROBUSTO
        try:
            print(f"--- Submetendo {slug} para Judge0 ---")
            
            resposta_judge = requests.post(
                url, 
                json=payload, 
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status HTTP Judge0: {resposta_judge.status_code}") 

            # AQUI ESTA A CORREÇÃO PRINCIPAL:
            # Se der erro 520 (Cloudflare) ou 500/404, isso levanta exceção antes de quebrar o JSON
            resposta_judge.raise_for_status() 

            # Só tenta ler JSON se o status for OK (200/201)
            res = resposta_judge.json()

        except requests.exceptions.HTTPError as err:
            # Captura erros de servidor externo (ex: Cloudflare 520)
            print(f"ERRO API JUDGE0: {err}")
            print(f"Conteúdo HTML/Texto recebido: {resposta_judge.text[:200]}...") # Loga o erro real
            
            msg = "Erro na comunicação com o avaliador."
            if resposta_judge.status_code == 520:
                msg = "O sistema de avaliação está instável momentaneamente (Erro 520)."
            
            return Response({"erro": msg, "detalhes": str(err)}, status=502)

        except json.JSONDecodeError:
            # Captura caso a API retorne 200 OK mas mande HTML (erro comum de proxy)
            print("ERRO PARSE JSON: A API retornou HTML em vez de JSON.")
            return Response({"erro": "Resposta inválida do avaliador."}, status=500)

        except Exception as e:
            # Erro genérico (conexão, etc)
            print(f"ERRO GERAL BACKEND: {e}") 
            return Response({"erro": "Falha interna no servidor."}, status=500)

        # 5. Ler o veredito (Se chegou aqui, temos um JSON válido)
        status_juiz = res.get('status', {}).get('description', 'Unknown Error')
        tempo = res.get('time')

        # 6. Salvar no Banco de Dados
        submissao = Submissao.objects.create(
            usuario=request.user,
            problema=problema,
            codigo=codigo,
            status=status_juiz,
            tempo=tempo if tempo else 0.0
        )

        # 7. Retornar
        return Response(SubmissaoSerializer(submissao).data)

# --- Registro de Usuário ---
class RegistrarUsuario(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]