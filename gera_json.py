from random import randint, choice, uniform, random, sample
from datetime import datetime, timedelta
import json

# Geradores utilitários para dados simulados

def gerar_codigo_ean13():
    """Gera um código EAN-13 válido."""
    base = [randint(0, 9) for _ in range(12)]
    soma = sum((3 if i % 2 else 1) * n for i, n in enumerate(base))
    digito = (10 - (soma % 10)) % 10
    return ''.join(map(str, base + [digito]))

def gerar_nome_produto():
    nomes = ["Arroz", "Feijão", "Óleo", "Sabonete", "Detergente", "Macarrão", "Açúcar", "Café", "Leite", "Farinha",
             "Molho", "Creme dental", "Shampoo", "Desinfetante", "Esponja", "Papel toalha", "Achocolatado", "Manteiga", "Suco", "Refrigerante"]
    marcas = ["Tio João", "Camil", "Liza", "Dove", "Ypê", "Barilla", "União", "Pilão", "Parmalat", "Dona Benta",
              "Heinz", "Colgate", "Seda", "Veja", "Scotch-Brite", "Snob", "Toddy", "Aviação", "Del Valle", "Coca-Cola"]
    categorias = ["Alimentos", "Higiene", "Limpeza", "Bebidas"]
    return choice(nomes), choice(marcas), choice(categorias)

def gerar_funcionario_nome():
    nomes = ["Ana", "Carlos", "Beatriz", "João", "Marina", "Rafael", "Camila", "Paulo", "Fernanda", "Luciano",
             "Patrícia", "Mateus", "Juliana", "André", "Larissa", "Vinícius", "Bruna", "Tiago", "Natália", "Diego"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Costa", "Ferreira", "Almeida", "Ribeiro", "Barbosa"]
    return f"{choice(nomes)} {choice(sobrenomes)}"

# Vamos gerar os dados para cada classe de acordo com as constraints

def gera_dados_teste():
    produtos = {}
    for _ in range(20):
        nome, marca, categoria = gerar_nome_produto()
        codigo = gerar_codigo_ean13()
        peso = round(uniform(0.1, 5.0), 2)
        preco = round(uniform(2.0, 50.0), 2)

        if random() < 0.4:  # ~40% dos produtos vendidos por peso
            preco_por_peso = round(preco / peso, 2)
            produto = {
                "nome": nome,
                "marca": marca,
                "categoria": categoria,
                "codigo": codigo,
                "peso": peso,
                "preco": preco,
                "preco_por_peso": preco_por_peso
            }
        else:
            produto = {
                "nome": nome,
                "marca": marca,
                "categoria": categoria,
                "codigo": codigo,
                "peso": peso,
                "preco": preco
            }

        produtos[codigo] = produto


    # funcionários


    funcionarios = {}
    cod_disp = 1000
    indices_desligados = set(sample(range(15), 3))  # Seleciona 3 índices aleatórios

    for i in range(15):
        nome = gerar_funcionario_nome()
        codigo = cod_disp
        cargo = choice(["Caixa", "Repositor", "Gerente"])
        ano_contrat = randint(2020, 2023)
        mes_contrat = randint(1, 12)
        dia_contrat = randint(1, 28)
        data_contratacao = f"{ano_contrat}/{mes_contrat:02}/{dia_contrat:02}"

        if i in indices_desligados:
            # Garante que a data de desligamento seja posterior à de contratação
            ano_deslig = randint(ano_contrat, 2024)
            mes_deslig = randint(1, 12)
            dia_deslig = randint(1, 28)
            data_desligamento = f"{ano_deslig}/{mes_deslig:02}/{dia_deslig:02}"
        else:
            data_desligamento = None

        funcionarios[codigo] = {
            "nome": nome,
            "codigo": codigo,
            "cargo": cargo,
            "data_contratacao": data_contratacao,
            "data_desligamento": data_desligamento
        }

        cod_disp += 1


    # Gerar estoques


    estoques = {}
    for i in range(3):
        estoque_codigo = f"EST{i+1:02}"
        produtos_unidade = list(produtos.values())[i*7:(i+1)*7]

        estoque = {
            "codigo": estoque_codigo,
            "estoque": {p["codigo"]: randint(10, 50) for p in produtos_unidade},
            "exposicao": {p["codigo"]: randint(1, 20) for p in produtos_unidade},
            "capacidades": {
                p["codigo"]: {
                    "estoque": randint(50, 150),
                    "exposicao": randint(20, 70)
                }
                for p in produtos_unidade
            }
        }
        estoques[estoque_codigo] = estoque


    # Gerar carrinhos

    funcionarios_divididos = [
        list(funcionarios.values())[:3],
        list(funcionarios.values())[3:8],
        list(funcionarios.values())[8:]
    ]

    # Gera dois índices aleatórios para divisão desigual dos 30 carrinhos
    i1, i2 = sorted([randint(1, 28), randint(2, 29)])
    quantidades = [i1, i2 - i1, 30 - i2]  # Soma dá 30

    carrinhos = {}
    id_counter = 1

    for unidade_id in range(3):
        funcionarios_unidade = funcionarios_divididos[unidade_id]

        for _ in range(quantidades[unidade_id]):
            if randint(1, 100) <= 20:  # Self-checkout
                funcionario = None
                data_base = datetime.strptime("2023/01/01", "%Y/%m/%d")
                data_limite = datetime.strptime("2025/06/21", "%Y/%m/%d")
            else:
                funcionario_obj = choice(funcionarios_unidade)
                funcionario = funcionario_obj["codigo"]
                data_base = datetime.strptime(funcionario_obj["data_contratacao"], "%Y/%m/%d")
                if funcionario_obj.get("data_desligamento"):
                    data_limite = datetime.strptime(funcionario_obj["data_desligamento"], "%Y/%m/%d")
                else:
                    data_limite = datetime.strptime("2025/06/21", "%Y/%m/%d")

            dias_range = max((data_limite - data_base).days, 1)
            data_venda = data_base + timedelta(days=randint(0, dias_range))
            data_str = data_venda.strftime("%Y/%m/%d")

            itens = {
                choice(list(produtos.values()))["codigo"]: randint(1, 5)
                for _ in range(randint(1, 4))
            }

            total = round(sum(
                prod["preco"] * qtd
                for cod, qtd in itens.items()
                for prod in list(produtos.values()) if prod["codigo"] == cod
            ), 2)

            carrinhos[id_counter] = {
                "id": id_counter,
                "data_hora": data_str,
                "itens": itens,
                "total": total,
                "funcionario": funcionario
            }

            id_counter += 1


    # Gerar unidades


    unidades = {}

    inicio = 0
    for i in range(3):
        fim = inicio + quantidades[i]  # quantidades calculadas antes
        codigo = 100 + i

        unidades[codigo] = {
            "nome": f"Unidade {i+1}",
            "codigo": codigo,
            "localizacao": [-23.5 + i * 0.01, -46.6 + i * 0.01],
            "estoque": list(estoques.values())[i],            # dicionário completo já gerado antes
            "funcionarios": funcionarios_divididos[i],  # lista de dicts completos
            "vendas": list(carrinhos.values())[inicio:fim],  # fatia variável conforme i1, i2
            "ativo": False if i == 2 else True
        }

        inicio = fim

    # Preparar os resultados

    jsons = {
        "produtos": produtos,
        "funcionarios": funcionarios,
        "estoques": estoques,
        "carrinhos": carrinhos,
        "unidades": unidades
    }

    # Salvar para visualização futura
    for nome, conteudo in jsons.items():
        with open(f"dados/{nome}.json", "w", encoding="utf-8") as f:
            json.dump(conteudo, f, indent=4, ensure_ascii=False)

    jsons.keys()
