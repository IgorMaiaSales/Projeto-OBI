import os
import sys
import django

# --- CONFIGURAÇÃO DE AMBIENTE ---
# Garante que o Python ache a pasta 'setup' voltando um nível
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from api.models import Problema, CasoDeTeste

print("🚀 Iniciando importação forçada dos dados do PDF da OBI 2025 (Fase 1)...")

# --- DADOS EXTRAÍDOS MANUALMENTE DO PDF ---
DADOS_PROVA = [
    {
        "slug": "pizzaria", # Nome esperado na URL
        "titulo": "Pizzaria",
        "nivel": "Júnior - Fase 1 (2025)",
        "enunciado": """A mãe de Larissa decidiu comemorar o aniversário da filha em uma pizzaria. Nessa pizzaria, existem pizzas de dois tamanhos: uma pizza grande possui 8 fatias, enquanto que uma pizza pequena possui 4 fatias.

A mãe de Larissa já fez um pedido indicando quantas pizzas de cada tamanho ela vai comprar. Larissa gostaria de saber quantos amigos ela pode convidar de modo que todos os convidados (ela, sua mãe e seus amigos) recebam uma fatia de pizza.

Sua tarefa é: dadas a quantidade de pizzas grandes e a quantidade de pizzas pequenas que a mãe de Larissa pediu, calcule o número máximo de amigos que Larissa pode convidar para a festa, ou seja, o número de fatias que sobram após reservar uma fatia para Larissa e uma para sua mãe.""",
        "especificacao_entrada": "A entrada possui duas linhas. A primeira linha contém um inteiro G, indicando a quantidade de pizzas grandes. A segunda linha contém um inteiro P, indicando a quantidade de pizzas pequenas.",
        "especificacao_saida": "Seu programa deverá imprimir uma única linha contendo um único inteiro: o número máximo de amigos que Larissa pode convidar.",
        "restricoes": "1 <= G <= 10\n1 <= P <= 10",
        "exemplos": [ # Dados das páginas 4 e 5 do PDF
            {"in": "2\n3", "out": "26"},
            {"in": "7\n4", "out": "70"},
            {"in": "1\n2", "out": "14"}
        ]
    },
    {
        "slug": "leite",
        "titulo": "Café com Leite",
        "nivel": "Júnior - Fase 1 (2025)",
        "enunciado": """Felipe trabalha em uma cafeteria especializada em café com leite. Cada cliente possui uma xícara de um tamanho diferente e prefere quantidades diferentes de leite.

O cliente indica o volume mínimo A e o volume máximo B de leite que deseja. Indica também a capacidade C da xícara.
A máquina prepara D mililitros de café. Felipe completa a xícara com leite (Volume Leite = C - D).

Sua tarefa é determinar se o volume de leite na bebida atenderá às preferências do cliente (se está entre A e B, inclusive).""",
        "especificacao_entrada": "Quatro linhas, cada uma contendo um inteiro:\n1. Volume mínimo A\n2. Volume máximo B\n3. Capacidade C da xícara\n4. Volume D de café preparado",
        "especificacao_saida": "Imprima 'S' se Felipe conseguir satisfazer as preferências, ou 'N' caso contrário.",
        "restricoes": "100 <= C <= 500\n0 <= A <= B < C\n10 <= D <= 100",
        "exemplos": [ # Dados da página 6 do PDF
            {"in": "130\n150\n170\n30", "out": "S"},
            {"in": "220\n230\n240\n30", "out": "N"},
            {"in": "0\n200\n300\n45", "out": "N"},
            {"in": "120\n120\n200\n80", "out": "S"}
        ]
    },
    {
        "slug": "dieta",
        "titulo": "Dieta",
        "nivel": "Júnior - Fase 1 (2025)",
        "enunciado": """O gato Garfield comeu lasanhas demais e John decidiu colocá-lo em dieta. John definiu um limite M de calorias diárias.

Para calcular as calorias já consumidas, John usa a conversão:
- 1g Proteína = 4 calorias
- 1g Gordura = 9 calorias
- 1g Carboidrato = 4 calorias

Dada a lista de N refeições que Garfield já fez (com suas gramas de Proteína, Gordura e Carboidrato), ajude o gato a saber qual o máximo de calorias que ele AINDA pode consumir sem exceder o limite M.""",
        "especificacao_entrada": "A primeira linha contém N (refeições feitas) e M (limite total).\nCada uma das N linhas seguintes contém três inteiros: P, G e C (gramas de proteínas, gorduras e carboidratos).",
        "especificacao_saida": "Imprima um único inteiro: a quantidade máxima de calorias que Garfield ainda pode consumir.",
        "restricoes": "1 <= N <= 30\n1 <= M <= 300.000\n0 < P, G, C < 500",
        "exemplos": [ # Dados da página 8 do PDF
            {"in": "3 2000\n65 15 20\n40 20 25\n50 10 35", "out": "655"},
            {"in": "1 3700\n50 300 200", "out": "0"}
        ]
    }
]

def forcar_importacao():
    count_novos = 0
    count_atualizados = 0

    for dados in DADOS_PROVA:
        print(f"🔹 Processando: {dados['titulo']}...")
        
        # 1. Cria ou recupera o problema
        problema, created = Problema.objects.get_or_create(
            slug=dados["slug"],
            defaults={
                "titulo": dados["titulo"],
                "enunciado": dados["enunciado"],
                "especificacao_entrada": dados["especificacao_entrada"],
                "especificacao_saida": dados["especificacao_saida"],
                "restricoes": dados["restricoes"],
                "nivel": dados["nivel"],
                "ativo": True
            }
        )

        # 2. Se já existia, força a atualização dos textos para garantir que não esteja vazio
        if not created:
            problema.titulo = dados["titulo"]
            problema.enunciado = dados["enunciado"]
            problema.especificacao_entrada = dados["especificacao_entrada"]
            problema.especificacao_saida = dados["especificacao_saida"]
            problema.restricoes = dados["restricoes"]
            problema.ativo = True
            problema.save()
            count_atualizados += 1
        else:
            count_novos += 1

        # 3. Insere os Exemplos do PDF (Garante que tenha testes visíveis)
        # Primeiro, verificamos se esses exemplos já existem para não duplicar
        for ex in dados["exemplos"]:
            # Deleta se já existir igualzinho (para evitar duplicatas ao rodar várias vezes)
            CasoDeTeste.objects.filter(
                problema=problema, 
                entrada=ex["in"], 
                eh_exemplo=True
            ).delete()

            # Cria de novo
            CasoDeTeste.objects.create(
                problema=problema,
                entrada=ex["in"],
                saida_esperada=ex["out"],
                eh_exemplo=True
            )
        
        print(f"   ✅ {len(dados['exemplos'])} exemplos inseridos/atualizados.")

    print("\n" + "="*40)
    print(f"🏁 RESUMO: {count_novos} problemas criados, {count_atualizados} atualizados.")
    print("Agora acesse http://127.0.0.1:8000/problemas/ e verifique se eles aparecem!")

if __name__ == "__main__":
    forcar_importacao()