from estruturas import Carrinho

class Estoque:
    def __init__(self, codigo: str, estoque: dict = None, exposicao: dict = None, capacidades: dict = None):
        """
        Inicializa um objeto Estoque com dicionários para controle de quantidade e capacidade.

        Args:
            codigo (str): identificador único do estoque

        Returns:
            None
        """
        self.codigo = codigo
        self.estoque = {}
        self.exposicao = {}
        self.capacidades = {}

    def __str__(self):
        """
        Retorna uma representação legível do estoque.

        Returns:
            str: descrição do estoque
        """
        total_estoque = sum(self.estoque.values())
        total_exposicao = sum(self.exposicao.values())

        faltas_estoque = [codigo for codigo, qtd in self.estoque.items() if qtd == 0]
        faltas_exposicao = [codigo for codigo, qtd in self.exposicao.items() if qtd == 0]

        descricao = f"Estoque: '{self.codigo}'\n"
        descricao += f"Produtos registrados: {len(self.capacidades)}\n"
        descricao += f"Total no estoque interno: {total_estoque}\n"
        descricao += f"Total na exposição: {total_exposicao}\n"

        if faltas_estoque:
            descricao += "Faltando no estoque interno: " + ", ".join(faltas_estoque) + "\n"
        if faltas_exposicao:
            descricao += "Faltando na exposição: " + ", ".join(faltas_exposicao) + "\n"

        return descricao.strip()

    def registrar_produto(self, produto, capacidade_estoque, capacidade_exposicao):
        """
        Registra um novo produto no estoque com suas capacidades.

        Args:
            produto (Produto): objeto Produto a ser registrado
            capacidade_estoque (int): capacidade máxima no estoque interno
            capacidade_exposicao (int): capacidade máxima na exposição

        Returns:
            0 -> produto registrado com sucesso
            1 -> produto já está registrado
        """
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
        """
        Atualiza as capacidades máximas de estoque e exposição para um produto.

        Args:
            codigo (str): código do produto a atualizar
            capacidade_estoque (int, opcional): nova capacidade do estoque interno
            capacidade_exposicao (int, opcional): nova capacidade da exposição

        Returns:
            0 -> capacidades atualizadas com sucesso
            1 -> produto não cadastrado no estoque
            2 -> nenhuma capacidade foi especificada
        """
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado no estoque."}
        
        if capacidade_estoque is None and capacidade_exposicao is None:
            return {"retorno": 2, "mensagem": "Por favor especifique alguma capacidade a atualizar."}

        if capacidade_estoque is not None:
            self.capacidades[codigo]["estoque"] = capacidade_estoque

        if capacidade_exposicao is not None:
            self.capacidades[codigo]["exposicao"] = capacidade_exposicao

        return {"retorno": 0, "mensagem": "Capacidades atualizadas com sucesso."}

    def adicionar_produto(self, produto, quantidade, destino='estoque'):
        """
        Adiciona uma quantidade de produto no estoque ou exposição.

        Args:
            produto (Produto): objeto Produto a adicionar
            quantidade (int): quantidade a adicionar
            destino (str): 'estoque' ou 'exposicao' indicando onde adicionar

        Returns:
            0 -> produto adicionado com sucesso
            1 -> produto não cadastrado
            2 -> capacidade de estoque excedida
            3 -> capacidade de exposição excedida
            4 -> destino inválido
        """
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
        """
        Move uma quantidade do produto do estoque interno para a exposição.

        Args:
            produto (Produto): objeto Produto a mover
            quantidade (int): quantidade a mover

        Returns:
            0 -> produto movido com sucesso
            1 -> produto não cadastrado
            2 -> estoque insuficiente para movimentação
            3 -> capacidade de exposição excedida
        """
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

    def retirar_venda(self, venda: Carrinho):
        """
        Remove os produtos vendidos da exposição conforme os itens da venda.

        Args:
            venda (Carrinho): objeto que contém os itens vendidos (lista de tuplas Produto, quantidade)

        Returns:
            0 -> produtos removidos com sucesso
            1 -> produto não cadastrado
            2 -> quantidade insuficiente na exposição
        """
        for item in venda.itens:
            codigo = item[0].codigo
            quantidade = item[1]
            if codigo not in self.capacidades:
                return {"retorno": 1, "mensagem": "Produto não cadastrado."}
            if self.exposicao[codigo] < quantidade:
                return {"retorno": 2, "mensagem": "Quantidade insuficiente na exposição para venda."}

            self.exposicao[codigo] -= quantidade
        return {"retorno": 0, "mensagem": "Produtos removidos com sucesso."}

    def consultar_quantidade(self, produto):
        """
        Consulta as quantidades e capacidades do produto no estoque.

        Args:
            produto (Produto): produto a ser consultado

        Returns:
            0 -> consulta realizada com sucesso
            1 -> produto não cadastrado
        """
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        return {
            "retorno": 0,
            "mensagem": "Consulta realizada com sucesso.",
            "dados": {
                "estoque": self.estoque[codigo],
                "exposicao": self.exposicao[codigo],
                "capacidade_estoque": self.capacidades[codigo]["estoque"],
                "capacidade_exposicao": self.capacidades[codigo]["exposicao"]
            }
        }


_todos_estoques = {}

def registrar_estoque(codigo: str):
    """
    Cria e registra um novo objeto Estoque no sistema com o código especificado.

    Args:
        codigo (str): identificador único do estoque

    Returns:
        0 -> estoque registrado com sucesso
        1 -> estoque já registrado com este código
        2 -> parâmetro 'codigo' incorreto
        3 -> parâmetro nulo
    """
    if codigo is None:
        return {"retorno": 3, "mensagem": "Parâmetro nulo"}

    if not isinstance(codigo, str) or not codigo.strip():
        return {"retorno": 2, "mensagem": "Parâmetro 'codigo' incorreto"}

    if codigo in _todos_estoques:
        return {"retorno": 1, "mensagem": "Estoque já registrado com este código"}

    _todos_estoques[codigo] = Estoque(codigo=codigo)
    return {"retorno": 0, "mensagem": "Estoque registrado com sucesso"}
