import os
import sys
import django
import glob

# --- CONFIGURAÇÃO DE AMBIENTE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from api.models import Problema, CasoDeTeste

# Caminho da pasta onde você descompactou os arquivos
PASTA_PROBLEMAS = os.path.join(current_dir, 'problemas')

def importar_casos_teste():
    if not os.path.exists(PASTA_PROBLEMAS):
        print(f"❌ Pasta não encontrada: {PASTA_PROBLEMAS}")
        return

    print(f"📂 Lendo testes de: {PASTA_PROBLEMAS}")
    pastas = [f for f in os.listdir(PASTA_PROBLEMAS) if os.path.isdir(os.path.join(PASTA_PROBLEMAS, f))]

    if not pastas:
        print("⚠️ Nenhuma pasta de problema encontrada.")
        return

    total_geral = 0

    for nome_pasta in pastas:
        # Extrai o slug (ex: '2025f1pj_pizzaria' -> 'pizzaria')
        slug = nome_pasta.split('_')[-1] if '_' in nome_pasta else nome_pasta
        
        print(f"\n🔹 Processando: {slug}...")

        # Busca o problema. Se não existir, não adianta importar teste.
        try:
            problema = Problema.objects.get(slug=slug)
        except Problema.DoesNotExist:
            print(f"   ⚠️ Problema '{slug}' não encontrado no banco. Rode o 'importar_dados.py' primeiro.")
            continue

        # LIMPEZA: Remove testes antigos para evitar duplicatas e corrigir o erro de visibilidade
        print(f"   [!] Limpando testes antigos de {slug}...")
        problema.casos_teste.all().delete()
        
        caminho_completo = os.path.join(PASTA_PROBLEMAS, nome_pasta)
        
        # Procura pastas numéricas (1, 2, 3...)
        itens = os.listdir(caminho_completo)
        subpastas = [i for i in itens if os.path.isdir(os.path.join(caminho_completo, i)) and i.isdigit()]
        
        # Se não houver subpastas (tudo na raiz), assumimos que NÃO é exemplo (segurança)
        if not subpastas:
            locais_de_busca = [("root", caminho_completo)] 
        else:
            locais_de_busca = [(sub, os.path.join(caminho_completo, sub)) for sub in sorted(subpastas)]

        count_problem = 0
        count_exemplos = 0
        
        for nome_sub, path_sub in locais_de_busca:
            # --- A MÁGICA ACONTECE AQUI ---
            # Só marcamos como exemplo se a pasta for estritamente "1"
            eh_exemplo = (nome_sub == "1")

            arquivos_in = glob.glob(os.path.join(path_sub, "*.in"))

            for arq_in in arquivos_in:
                # Busca o par .sol ou .out
                base = os.path.splitext(arq_in)[0]
                arq_sol = base + ".sol"
                if not os.path.exists(arq_sol):
                    arq_sol = base + ".out"
                
                if os.path.exists(arq_sol):
                    try:
                        with open(arq_in, 'r', encoding='utf-8', errors='ignore') as f:
                            dado_in = f.read().strip()
                        with open(arq_sol, 'r', encoding='utf-8', errors='ignore') as f:
                            dado_out = f.read().strip()

                        CasoDeTeste.objects.create(
                            problema=problema,
                            entrada=dado_in,
                            saida_esperada=dado_out,
                            eh_exemplo=eh_exemplo  # Salva True apenas se veio da pasta 1
                        )
                        count_problem += 1
                        if eh_exemplo: count_exemplos += 1

                    except Exception as e:
                        print(f"   ❌ Erro ao ler {os.path.basename(arq_in)}: {e}")

        print(f"   ✅ Total importado: {count_problem} (Visíveis no site: {count_exemplos})")
        total_geral += count_problem

    print(f"\n🚀 Concluído! Total de {total_geral} casos de teste inseridos.")

if __name__ == "__main__":
    importar_casos_teste()