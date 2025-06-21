'''
├── produto.py
│   ├── class Produto
│   │   ├── calcular_preco(quantidade)
│   ├── registrar_produto(nome: str, marca: str, categoria: str, codigo: str, peso: float, preco: float, preco_por_peso: float = None)
│   ├── atualizar_produto(codigo: int, dados: dict)
│   ├── consultar_produto_por_codigo(codigo: int)
│   ├── pesquisar_produto(texto, filtros={})
'''


_todos_produtos = {}

__all__ = [
    "Produto",
    "consultar_produto_por_codigo",
    "registrar_produto",
    "atualizar_produto",
    "pesquisar_produto",
]



class Produto:
    def __init__(self, nome: str, marca: str, categoria: str, codigo: str, peso: float, preco: float, preco_por_peso: float = None):
        """
        Inicializa um objeto Produto.

        Args:
            nome (str): nome do produto
            marca (str): marca do produto
            categoria (str): categoria do produto
            codigo (str): código de barras do produto (EAN-13)
            peso (float): peso do produto em unidades apropriadas
            preco (float): preço unitário do produto
            preco_por_peso (float, opcional): preço por unidade de peso, se aplicável

        Returns:
            None
        """
        self.nome = nome
        self.marca = marca
        self.categoria = categoria
        self.codigo = codigo
        self.peso = peso
        self.preco = preco
        self.preco_por_peso = preco_por_peso

    def __str__(self, quantidade:float=None):
        """
        Retorna uma representação em string amigável do objeto Produto.

        Returns:
            str: descrição resumida do produto
        """
        partes = [
            f"Produto: {self.nome}",
            f"Marca: {self.marca}",
            f"Categoria: {self.categoria}",
            f"Código: {self.codigo}",
        ]

        if quantidade is None:

            partes.append(f"Peso: {self.peso}")
            if self.preco_por_peso is not None:
                partes.append(f"Preço por peso: R$ {self.preco_por_peso:.2f}")
            else:
                partes.append(f"Preço unitário: R$ {self.preco:.2f}")
        else:
            partes.append(f"Quantidade: {quantidade}")

            partes.append(f"Subtotal: {self.calcula_preco(quantidade)}")
        return " | ".join(partes)

    def calcula_preco(self, quantidade):
        """
        Calcula o preço total para uma dada quantidade do produto.

        Args:
            quantidade (float): quantidade desejada para cálculo do preço

        Retorna:
            0 -> preço calculado com sucesso, valor disponível em 'dados'
            1 -> quantidade inválida (menor ou igual a zero)
        """
        if quantidade <= 0:
            return {"retorno": 1, "mensagem": "Quantidade deve ser maior que zero."}

        if self.preco_por_peso is None:
            preco_total = self.preco * quantidade
        else:
            preco_total = self.preco_por_peso * quantidade

        return {"retorno": 0, "mensagem": "Preço calculado com sucesso.", "dados": preco_total}



def _valida_codigo_barras(codigo: str):
    """
    Valida um código de barras EAN-13 representado como string.

    Args:
        codigo (str): código de barras com 13 dígitos

    Returns:
        bool: True se válido, False se inválido
    """
    if not isinstance(codigo, str):
        return False

    codigo_str = codigo.zfill(13)  # garante 13 dígitos com zeros à esquerda

    if len(codigo_str) != 13 or not codigo_str.isdigit():
        return False

    numeros = [int(d) for d in codigo_str]
    soma_impares = sum(numeros[i] for i in range(0, 12, 2))
    soma_pares = sum(numeros[i] for i in range(1, 12, 2)) * 3
    total = soma_impares + soma_pares
    digito_verificador = (10 - (total % 10)) % 10

    return digito_verificador == numeros[-1]



def consultar_produto_por_codigo(codigo: str):
    """
    Procura pelo objeto que representa o produto com o código especificado.

    Args:
        codigo (str): código referente ao produto desejado

    Retorna:
        0 -> produto encontrado com sucesso (objeto disponível em 'dados')
        2 -> produto não encontrado
        3 -> parâmetro 'codigo' incorreto
        4 -> parâmetro nulo
    """
    if codigo is None:
        return {"retorno": 4, "mensagem": "Parâmetro nulo"}

    if not isinstance(codigo, str):
        return {"retorno": 3, "mensagem": "Parâmetro 'codigo' errado"}

    produto = _todos_produtos.get(codigo)

    if not produto:
        return {"retorno": 2, "mensagem": "Produto não encontrado"}

    return {"retorno": 0, "mensagem": "Produto encontrado com sucesso", "dados": produto}



def registrar_produto(nome: str, marca: str, categoria: str, codigo: str, peso: float, preco: float, preco_por_peso: float = None):
    """
    Registra um novo produto na base de dados.

    Args:
        nome (str): nome do produto
        marca (str): marca do produto
        categoria (str): categoria do produto
        codigo (str): código de barras do produto (EAN-13)
        peso (float): peso do produto
        preco (float): preço unitário
        preco_por_peso (float, opcional): preço por unidade de peso

    Retorna:
        0 -> produto registrado com sucesso (objeto disponível em 'dados')
        3 -> parâmetro incorreto (ex: código inválido)
        4 -> parâmetro nulo
        5 -> produto já cadastrado com este código
    """
    if None in [nome, marca, categoria, codigo, peso, preco]:
        return {"retorno": 4, "mensagem": "Parâmetro nulo"}

    if not isinstance(codigo, str):
        return {"retorno": 3, "mensagem": "Parâmetro 'codigo' errado"}

    if not _valida_codigo_barras(codigo):
        return {"retorno": 3, "mensagem": "Código de barras inválido"}

    if codigo in _todos_produtos:
        return {"retorno": 5, "mensagem": "Produto já cadastrado com este código"}

    produto = Produto(nome, marca, categoria, codigo, peso, preco, preco_por_peso)
    _todos_produtos[codigo] = produto

    return {"retorno": 0, "mensagem": "Produto registrado com sucesso", "dados": produto}



def atualizar_produto(codigo: str, dados: dict):
    """
    Atualiza atributos do produto identificado pelo código.

    Args:
        codigo (str): código do produto a ser atualizado
        dados (dict): dicionário com os campos e novos valores a atualizar

    Retorna:
        0 -> produto atualizado com sucesso (objeto disponível em 'dados')
        2 -> produto não encontrado
        3 -> campo inválido para atualização ou parâmetro incorreto
        4 -> parâmetro nulo
    """
    if codigo is None or dados is None:
        return {"retorno": 4, "mensagem": "Parâmetro nulo"}

    if not isinstance(codigo, str):
        return {"retorno": 3, "mensagem": "Parâmetro 'codigo' errado"}

    produto = _todos_produtos.get(codigo)
    if not produto:
        return {"retorno": 2, "mensagem": "Produto não encontrado"}

    campos_validos = {"nome", "marca", "categoria", "peso", "preco", "preco_por_peso"}

    for chave, valor in dados.items():
        if chave not in campos_validos:
            return {"retorno": 3, "mensagem": f"Campo inválido para atualização: {chave}"}
        setattr(produto, chave, valor)

    return {"retorno": 0, "mensagem": "Produto atualizado com sucesso", "dados": produto}



def pesquisar_produto(texto: str, filtros: dict = {}):
    """
    Pesquisa produtos que contenham o texto em nome, marca ou categoria e que satisfaçam os filtros.

    Args:
        texto (str): texto para pesquisa (case insensitive)
        filtros (dict): filtros opcionais com chaves de atributos do Produto e valores esperados

    Retorna:
        0 -> sucesso (lista de produtos disponíveis em 'dados')
        4 -> parâmetro nulo
    """
    if texto is None:
        return {"retorno": 4, "mensagem": "Parâmetro nulo"}

    texto_lower = texto.lower()
    resultados = []

    for produto in _todos_produtos.values():
        if (texto_lower in produto.nome.lower() or
            texto_lower in produto.marca.lower() or
            texto_lower in produto.categoria.lower()):

            atende_filtros = True
            for chave, valor in filtros.items():
                if not hasattr(produto, chave) or getattr(produto, chave) != valor:
                    atende_filtros = False
                    break

            if atende_filtros:
                resultados.append(produto)

    return {"retorno": 0, "mensagem": f"{len(resultados)} produto(s) encontrado(s)", "dados": resultados}
