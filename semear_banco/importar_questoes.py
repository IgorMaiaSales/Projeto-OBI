import os
import sys
import glob
import json

# --- CONFIGURAÇÃO DE CAMINHOS ---
# 1. Pega o diretório onde este arquivo está (semear_banco)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Pega o diretório pai (raiz do projeto, onde está o 'manage.py' e a pasta 'setup')
project_root = os.path.dirname(current_dir)

# 3. Adiciona a raiz ao sys.path para o Python achar o 'setup.settings'
sys.path.append(project_root)

# --- SETUP DJANGO ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
import django
django.setup()

from api.models import Problema, ExemploDeProblema, CasoDeTeste

PASTA_PROBLEMAS = os.path.join(current_dir, 'problemas')

def processar_pasta_problema(nome_pasta):
    caminho_pasta = os.path.join(PASTA_PROBLEMAS, nome_pasta)
    arquivo_json = os.path.join(caminho_pasta, "info.json")

    # 1. Validação Básica
    if not os.path.exists(arquivo_json):
        print(f"⚠️ Pulei '{nome_pasta}': info.json não encontrado.")
        return

    print(f"🔹 Processando: {nome_pasta}...")

    # 2. Ler Metadados do JSON
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON de {nome_pasta}: {e}")
        return

# 3. Criar ou Atualizar o Problema (COM OS NOVOS CAMPOS)
    problema, _ = Problema.objects.update_or_create(
        slug=data.get('slug', nome_pasta),
        defaults={
            "titulo": data.get('titulo', 'Sem Título'),
            
            # NOVOS CAMPOS AQUI
            "ano": data.get('ano', 2024),
            "fase": data.get('fase', 1),
            "nivel": data.get('nivel', 'J'), # J, 1, 2, S...
            
            "time_limit": data.get('time_limit', 1000),
            "enunciado": data.get('enunciado', ''),
            "especificacao_entrada": data.get('entrada', ''),
            "especificacao_saida": data.get('saida', ''),
            "restricoes": data.get('restricoes', ''),
            "ativo": True
        }
    )

    # 4. Importar Exemplos (Visíveis/Didáticos)
    # Limpa exemplos antigos para garantir sincronia com o JSON
    problema.exemplos.all().delete()
    
    exemplos_json = data.get('exemplos', [])
    for ex in exemplos_json:
        ExemploDeProblema.objects.create(
            problema=problema,
            entrada_texto=ex.get('input', ''),
            saida_texto=ex.get('output', ''),
            explicacao=ex.get('explanation', None) # Pode ser null
        )
    print(f"   📝 {len(exemplos_json)} exemplos didáticos importados.")

    # 5. Importar Casos de Teste do Juiz (Varredura de Arquivos)
    # Limpa testes antigos
    problema.casos_teste.all().delete()
    
    testes_count = 0
    
    # Verifica estrutura: Subtarefas (pastas numéricas) ou Plana?
    itens = os.listdir(caminho_pasta)
    subpastas_numericas = [d for d in itens if os.path.isdir(os.path.join(caminho_pasta, d)) and d.isdigit()]
    
    if subpastas_numericas:
        # --- MODO SUBTAREFAS ---
        print("   📂 Estrutura detectada: SUBTAREFAS")
        for sub in subpastas_numericas:
            path_sub = os.path.join(caminho_pasta, sub)
            inputs = glob.glob(os.path.join(path_sub, "*.in"))
            
            for arq_in in inputs:
                arq_sol = arq_in.replace(".in", ".sol")
                if not os.path.exists(arq_sol): 
                    arq_sol = arq_in.replace(".in", ".out") # Tenta .out também
                
                if os.path.exists(arq_sol):
                    CasoDeTeste.objects.create(
                        problema=problema,
                        subtarefa_id=int(sub),
                        caminho_entrada=arq_in,
                        caminho_saida=arq_sol
                    )
                    testes_count += 1
    else:
        # --- MODO PLANO (Flat) ---
        print("   📂 Estrutura detectada: PLANA (Sem subtarefas)")
        inputs = glob.glob(os.path.join(caminho_pasta, "*.in"))
        for arq_in in inputs:
            # Ignora arquivos que comecem com 'sample' se quiser, mas agora a fonte da verdade é o JSON
            arq_sol = arq_in.replace(".in", ".sol")
            if not os.path.exists(arq_sol): 
                arq_sol = arq_in.replace(".in", ".out")
            
            if os.path.exists(arq_sol):
                CasoDeTeste.objects.create(
                    problema=problema,
                    subtarefa_id=None,
                    caminho_entrada=arq_in,
                    caminho_saida=arq_sol
                )
                testes_count += 1

    print(f"   ⚖️  {testes_count} arquivos de teste vinculados ao juiz.")

def main():
    if not os.path.exists(PASTA_PROBLEMAS):
        print(f"❌ Pasta '{PASTA_PROBLEMAS}' não encontrada.")
        return

    pastas = [f for f in os.listdir(PASTA_PROBLEMAS) if os.path.isdir(os.path.join(PASTA_PROBLEMAS, f))]
    
    print("🚀 Iniciando importação completa do sistema...")
    for p in pastas:
        processar_pasta_problema(p)
    print("\n✅ Processo finalizado.")

if __name__ == "__main__":
    main()