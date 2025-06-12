

class Produto:
    def __init__(self, nome: str, marca: str, categoria: str, codigo: str,
                 peso: float, preco: float, preco_por_peso: float = None):
        self.nome = nome
        self.marca = marca
        self.categoria = categoria
        self.codigo = codigo
        self.peso = peso
        self.preco = preco
        self.preco_por_peso = preco_por_peso

    def calcula_preco(self, quantidade):
        if quantidade <= 0:
            return {"retorno": 1, "mensagem": "Quantidade deve ser maior que zero."}

        if self.preco_por_peso is None:
            preco_total = self.preco * quantidade
            return {"retorno": 0, "mensagem": "Preço calculado com sucesso.", "valor": preco_total}
        else:
            preco_total = self.preco * quantidade / self.preco_por_peso
            return {"retorno": 0, "mensagem": "Preço calculado com sucesso.", "valor": preco_total}

    def atualizar(self, atributo: str, valor):
        if not hasattr(self, atributo):
            return {"retorno": 1, "mensagem": f"Atributo '{atributo}' não encontrado no produto."}

        setattr(self, atributo, valor)
        return {"retorno": 0, "mensagem": f"Atributo '{atributo}' atualizado com sucesso."}


class Estoque:
    def __init__(self):
        self.estoque = {}
        self.exposicao = {}
        self.capacidades = {}

    def registrar_produto(self, produto, capacidade_estoque, capacidade_exposicao):
        codigo = produto.codigo
        if codigo in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto já está registrado."}

        self.estoque[codigo] = 0
        self.exposicao[codigo] = 0
        self.capacidades[codigo] = {
            "estoque": capacidade_estoque,
            "exposicao": capacidade_exposicao
        }
        return {"retorno": 0, "mensagem": "Produto registrado com sucesso."}
    
    def atualizar_capacidades(self, codigo, capacidade_estoque=None, capacidade_exposicao=None):
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado no estoque."}

        if capacidade_estoque is not None:
            self.capacidades[codigo]["estoque"] = capacidade_estoque

        if capacidade_exposicao is not None:
            self.capacidades[codigo]["exposicao"] = capacidade_exposicao

        return {"retorno": 0, "mensagem": "Capacidades atualizadas com sucesso."}

    def adicionar_produto(self, produto, quantidade, destino='estoque'):
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        if destino == 'estoque':
            atual = self.estoque[codigo]
            limite = self.capacidades[codigo]["estoque"]
            if atual + quantidade > limite:
                return {"retorno": 2, "mensagem": "Capacidade de estoque excedida para o produto."}
            self.estoque[codigo] += quantidade
            return {"retorno": 0, "mensagem": "Produto adicionado ao estoque interno."}

        elif destino == 'exposicao':
            atual = self.exposicao[codigo]
            limite = self.capacidades[codigo]["exposicao"]
            if atual + quantidade > limite:
                return {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}
            self.exposicao[codigo] += quantidade
            return {"retorno": 0, "mensagem": "Produto adicionado à exposição."}

        else:
            return {"retorno": 4, "mensagem": "Destino inválido. Use 'estoque' ou 'exposicao'."}

    def mover_para_exposicao(self, produto, quantidade):
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}
        if self.estoque[codigo] < quantidade:
            return {"retorno": 2, "mensagem": "Estoque insuficiente para movimentação."}
        if self.exposicao[codigo] + quantidade > self.capacidades[codigo]["exposicao"]:
            return {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}

        self.estoque[codigo] -= quantidade
        self.exposicao[codigo] += quantidade
        return {"retorno": 0, "mensagem": "Produto movido para a exposição."}

    def retirar_venda(self, produto, quantidade):
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}
        if self.exposicao[codigo] < quantidade:
            return {"retorno": 2, "mensagem": "Quantidade insuficiente na exposição para venda."}

        self.exposicao[codigo] -= quantidade
        return {"retorno": 0, "mensagem": "Venda registrada com sucesso."}

    def consultar_quantidade(self, produto):
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        return {
            "retorno": 0,
            "mensagem": "Consulta realizada com sucesso.",
            "valor":{
                    "estoque": self.estoque[codigo],
                    "exposicao": self.exposicao[codigo],
                    "capacidade_estoque": self.capacidades[codigo]["estoque"],
                    "capacidade_exposicao": self.capacidades[codigo]["exposicao"]
                }
        }



class Venda:
    def __init__(self, id: int, data_hora: str, itens:list[tuple]=[]):
        self.id = id
        self.data_hora = data_hora
        self.itens = itens  # lista de tuplas de (produto, quantidade)

class Funcionario:
    def __init__(self, nome, codigo, cargo, local_de_trabalho, data_contratacao, data_desligamento=None):
        self.nome = nome
        self.codigo = codigo
        self.cargo = cargo 
        self.local_de_trabalho = local_de_trabalho
        self.data_contratacao = data_contratacao
        self.data_desligamento = data_desligamento


class Localidade:
    def __init__(self, nome: str, codigo: int, estoque: Estoque, localizacao: tuple, funcionarios: list, vendas:list=[]) -> None:
        self.nome = nome
        self.codigo = codigo
        self.estoque = estoque
        self.localizacao = localizacao
        self.funcionarios = funcionarios
        self.vendas = vendas
