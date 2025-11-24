from django.http import JsonResponse
import requests
import time
import base64

def hello_juiz(request):
    # 1. Configuração (Igual ao seu script)
    BASE_URL = "https://ce.judge0.com"
    codigo_fonte = "print('Ola OBI via Django')" # Mudamos o texto para provar que é novo
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