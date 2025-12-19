import json
import requests
import base64
import time
import os

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Problema, Submissao
from .serializers import (
    ProblemaSummarySerializer, 
    ProblemaDetailSerializer, 
    SubmissaoSerializer, 
    UserSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

def hello_juiz(request):
    return JsonResponse({"mensagem": "API Online v2.0 - File System Mode"})

class ListaProblemas(generics.ListAPIView):
    queryset = Problema.objects.filter(ativo=True)
    # AQUI ESTÁ A MUDANÇA: Usamos o serializer leve
    serializer_class = ProblemaSummarySerializer 
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ano', 'nivel', 'fase']
    search_fields = ['titulo', 'slug']
    ordering_fields = ['ano', 'titulo']
    ordering = ['-ano', 'titulo']

class DetalheProblema(generics.RetrieveAPIView):
    queryset = Problema.objects.filter(ativo=True)
    # AQUI ESTÁ A MUDANÇA: Usamos o serializer completo
    serializer_class = ProblemaDetailSerializer
    lookup_field = 'slug'

class SubmeterSolucao(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, slug):
        problema = get_object_or_404(Problema, slug=slug)
        codigo = request.data.get('codigo')
        
        if not codigo:
             return Response({"erro": "Código não fornecido."}, status=400)

        # 1. Buscar os caminhos dos arquivos de teste
        casos_teste = problema.casos_teste.all()
        if not casos_teste.exists():
            return Response({"erro": "Erro de configuração: Problema sem arquivos de teste."}, status=500)

        batch_submissions = []
        
        # 2. Ler os arquivos do disco
        try:
            source_b64 = base64.b64encode(codigo.encode('utf-8')).decode('utf-8')
            limite_tempo = problema.time_limit / 1000.0 # Converte ms para segundos

            for caso in casos_teste:
                if not os.path.exists(caso.caminho_entrada) or not os.path.exists(caso.caminho_saida):
                    print(f"ERRO: Arquivo faltando para o teste {caso.id}")
                    continue
                    
                with open(caso.caminho_entrada, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo_in = f.read()

                with open(caso.caminho_saida, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo_out = f.read()

                stdin_b64 = base64.b64encode(conteudo_in.encode('utf-8')).decode('utf-8')
                expected_b64 = base64.b64encode(conteudo_out.encode('utf-8')).decode('utf-8')
                
                batch_submissions.append({
                    "source_code": source_b64,
                    "language_id": 71, # Python 3
                    "stdin": stdin_b64,
                    "expected_output": expected_b64,
                    "cpu_time_limit": limite_tempo
                })
        except Exception as e:
            return Response({"erro": f"Erro interno ao ler arquivos: {str(e)}"}, status=500)

        if not batch_submissions:
            return Response({"erro": "Nenhum caso de teste válido encontrado."}, status=500)

        # --- NOVA LÓGICA DE LOTES (CHUNKING) ---
        url_base = "https://ce.judge0.com"
        # batch=true indica submissão em lote, wait=true tenta esperar a resposta
        url_post = f"{url_base}/submissions/batch?base64_encoded=true&wait=true"
        
        resultados_finais = []
        CHUNK_SIZE = 20 # Limite do Judge0 Free

        try:
            # Divide a lista gigante em pedaços de 20
            for i in range(0, len(batch_submissions), CHUNK_SIZE):
                chunk = batch_submissions[i:i + CHUNK_SIZE]
                print(f"--- Enviando lote {i//CHUNK_SIZE + 1} ({len(chunk)} testes) ---")

                payload = { "submissions": chunk }
                resp = requests.post(url_post, json=payload, headers={'Content-Type': 'application/json'})
                
                if resp.status_code != 200 and resp.status_code != 201:
                    print(f"ERRO DO JUIZ ({resp.status_code}): {resp.text}")
                    return Response({"erro": f"O Juiz rejeitou o lote {i//CHUNK_SIZE + 1}."}, status=502)

                resultados_lote = resp.json()

                # Lógica de Polling para este lote específico
                if isinstance(resultados_lote, list) and len(resultados_lote) > 0:
                    primeiro = resultados_lote[0]
                    # Se veio token mas não veio status, precisa esperar
                    if 'token' in primeiro and 'status' not in primeiro:
                        tokens = [r['token'] for r in resultados_lote]
                        tokens_str = ",".join(tokens)
                        url_check = f"{url_base}/submissions/batch?tokens={tokens_str}&base64_encoded=true&fields=status,stdout,stderr,compile_output,time"
                        
                        # Tenta 3 vezes esperar por este lote
                        for _ in range(3):
                            time.sleep(2)
                            resp_check = requests.get(url_check)
                            if resp_check.status_code == 200:
                                data_check = resp_check.json()
                                submissions_check = data_check.get('submissions', [])
                                if submissions_check and submissions_check[0].get('status', {}).get('id') >= 3:
                                    resultados_lote = submissions_check
                                    break
                
                # Acumula os resultados deste lote na lista final
                resultados_finais.extend(resultados_lote)

            # 4. Processar Resultados Finais (Agregados)
            status_final = "Accepted"
            tempo_total = 0.0
            
            for res in resultados_finais:
                desc = res.get('status', {}).get('description', 'Erro')
                tempo = float(res.get('time') or 0)
                tempo_total = max(tempo_total, tempo)
                
                # Se encontrar qualquer erro, esse passa a ser o status da submissão
                if desc != "Accepted":
                    status_final = desc
                    break
            
        except requests.exceptions.RequestException as err:
            print(f"Erro Conexão Judge0: {err}")
            return Response({"erro": "O Juiz Online está instável."}, status=502)

        # 5. Salvar Submissão
        submissao = Submissao.objects.create(
            usuario=request.user,
            problema=problema,
            codigo=codigo,
            status=status_final,
            tempo=tempo_total
        )

        return Response(SubmissaoSerializer(submissao).data)

class RegistrarUsuario(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]