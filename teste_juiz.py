import requests
import time
import base64

# URL da API pública do Judge0
BASE_URL = "https://ce.judge0.com"

def testar_juiz():
    print("--- Iniciando Teste do Juiz (Judge0) ---")

    # 1. O código que queremos testar (Simulando um aluno enviando uma solução)
    # Vamos testar um código em Python (ID da linguagem 71)
    codigo_fonte = "print('Ola OBI')"
    
    # Codificando para base64 (padrão do Judge0)
    codigo_b64 = base64.b64encode(codigo_fonte.encode('utf-8')).decode('utf-8')

    # 2. Preparar a submissão
    payload = {
        "source_code": codigo_fonte,
        "language_id": 71, # 71 é Python 3.8.1 no Judge0
        "stdin": "",       # Entrada padrão
        "expected_output": "Ola OBI" # O que esperamos que saia
    }

    print("1. Enviando código para avaliação...")
    
    # Envia a requisição POST para criar a submissão
    try:
        response = requests.post(f"{BASE_URL}/submissions/?base64_encoded=false&wait=false", json=payload)
        response.raise_for_status() # Verifica se deu erro na requisição HTTP
        
        token = response.json().get("token")
        print(f"   Sucesso! Token da submissão: {token}")

    except Exception as e:
        print(f"   Erro ao enviar: {e}")
        return

    # 3. Esperar o resultado (Polling)
    print("2. Aguardando resultado...")
    
    status = "Processing"
    resultado_final = None

    while status in ["Processing", "In Queue"]:
        time.sleep(2) # Espera 2 segundos antes de perguntar de novo
        
        res = requests.get(f"{BASE_URL}/submissions/{token}?base64_encoded=false")
        resultado_final = res.json()
        status = resultado_final["status"]["description"]
        print(f"   Status atual: {status}")

    # 4. Mostrar o Veredito
    print("\n--- Veredito Final ---")
    print(f"Status: {status}")
    print(f"Saída do código (stdout): {resultado_final.get('stdout')}")
    print(f"Tempo de execução: {resultado_final.get('time')}s")
    
    if status == "Accepted":
        print("✅ SUCESSO! O Juiz está funcionando e aceitou o código.")
    else:
        print("❌ Ocorreu um erro ou resposta errada.")

if __name__ == "__main__":
    testar_juiz()