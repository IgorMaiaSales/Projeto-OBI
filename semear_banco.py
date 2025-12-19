import os
import django

# Configura o Django para rodar fora do manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings') # Verifique se sua pasta principal chama 'setup' ou o nome do projeto
django.setup()

from api.models import Problema, CasoDeTeste

dados_problemas = [
    {
        "titulo": "Antecessor e Sucessor",
        "slug": "antecessor-sucessor",
        "nivel": "Iniciante",
        "enunciado": "Faça um programa que leia um número inteiro N e imprima o seu antecessor (N-1) e o seu sucessor (N+1) na mesma linha, separados por um espaço.",
        "especificacao_entrada": "A entrada consiste de um único número inteiro N.",
        "especificacao_saida": "Imprima dois números inteiros: o antecessor e o sucessor de N.",
        "restricoes": "-1000 <= N <= 1000",
        "testes": [
            {"entrada": "10", "saida": "9 11", "exemplo": True},
            {"entrada": "0", "saida": "-1 1", "exemplo": False},
            {"entrada": "-5", "saida": "-6 -4", "exemplo": False}
        ]
    },
    {
        "titulo": "Área do Quadrado",
        "slug": "area-quadrado",
        "nivel": "Iniciante",
        "enunciado": "João quer calcular a área de quadrados. Escreva um programa que receba o valor do lado L de um quadrado e imprima sua área.",
        "especificacao_entrada": "A entrada contém um único inteiro L, representando o lado do quadrado.",
        "especificacao_saida": "Imprima um inteiro representando a área.",
        "restricoes": "1 <= L <= 100",
        "testes": [
            {"entrada": "3", "saida": "9", "exemplo": True},
            {"entrada": "5", "saida": "25", "exemplo": True},
            {"entrada": "10", "saida": "100", "exemplo": False}
        ]
    },
    {
        "titulo": "Positivo, Negativo ou Nulo",
        "slug": "positivo-negativo",
        "nivel": "Júnior",
        "enunciado": "Escreva um programa que leia um número inteiro X e imprima 'positivo' se X for maior que zero, 'negativo' se for menor que zero, ou 'nulo' se for igual a zero.",
        "especificacao_entrada": "Um número inteiro X.",
        "especificacao_saida": "Uma string: 'positivo', 'negativo' ou 'nulo'.",
        "restricoes": "-100 <= X <= 100",
        "testes": [
            {"entrada": "5", "saida": "positivo", "exemplo": True},
            {"entrada": "-2", "saida": "negativo", "exemplo": True},
            {"entrada": "0", "saida": "nulo", "exemplo": True},
            {"entrada": "100", "saida": "positivo", "exemplo": False}
        ]
    },
    {
        "titulo": "Tabuada",
        "slug": "tabuada",
        "nivel": "Júnior",
        "enunciado": "Faça um programa que leia um número inteiro N e imprima a tabuada de multiplicação de 1 a 10, no formato '1 x N = RESULTADO'.",
        "especificacao_entrada": "Um inteiro N.",
        "especificacao_saida": "10 linhas contendo a tabuada.",
        "restricoes": "1 <= N <= 100",
        "testes": [
            {
                "entrada": "5", 
                "saida": "1 x 5 = 5\n2 x 5 = 10\n3 x 5 = 15\n4 x 5 = 20\n5 x 5 = 25\n6 x 5 = 30\n7 x 5 = 35\n8 x 5 = 40\n9 x 5 = 45\n10 x 5 = 50", 
                "exemplo": True
            },
            {
                "entrada": "2", 
                "saida": "1 x 2 = 2\n2 x 2 = 4\n3 x 2 = 6\n4 x 2 = 8\n5 x 2 = 10\n6 x 2 = 12\n7 x 2 = 14\n8 x 2 = 16\n9 x 2 = 18\n10 x 2 = 20", 
                "exemplo": False
            }
        ]
    }
]

print("Iniciando importação...")

for p_data in dados_problemas:
    prob, created = Problema.objects.get_or_create(
        slug=p_data["slug"],
        defaults={
            "titulo": p_data["titulo"],
            "enunciado": p_data["enunciado"],
            "especificacao_entrada": p_data["especificacao_entrada"],
            "especificacao_saida": p_data["especificacao_saida"],
            "restricoes": p_data["restricoes"],
            "nivel": p_data["nivel"],
            "ativo": True
        }
    )
    
    if created:
        print(f"[+] Criado problema: {prob.titulo}")
    else:
        print(f"[.] Atualizando testes de: {prob.titulo}")
        prob.casos_teste.all().delete()

    for t_data in p_data["testes"]:
        CasoDeTeste.objects.create(
            problema=prob,
            entrada=t_data["entrada"],
            saida_esperada=t_data["saida"],
            eh_exemplo=t_data["exemplo"]
        )

print("--- Concluído com sucesso! ---")