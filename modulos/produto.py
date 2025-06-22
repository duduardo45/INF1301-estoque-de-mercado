_todos_produtos = {}

__all__ = [
    "Produto",
    "consultar_produto_por_codigo",
    "registrar_produto",
    "atualizar_produto",
    "pesquisar_produto",
    "listar_todos_produtos",
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



    def to_json(self):
        return {
            "nome": self.nome,
            "marca": self.marca,
            "categoria": self.categoria,
            "codigo": self.codigo,
            "peso": self.peso,
            "preco": self.preco,
            "preco_por_peso": self.preco_por_peso
        }
    


    @classmethod
    def from_json(cls, json_dict):
        nome = json_dict["nome"]
        marca = json_dict["marca"]
        categoria = json_dict["categoria"]
        codigo = json_dict["codigo"]
        peso = json_dict["peso"]
        preco = json_dict["preco"]
        preco_por_peso = json_dict["preco_por_peso"]
        return cls(nome, marca, categoria, codigo, peso, preco, preco_por_peso)



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

    if len(codigo) != 13 or not codigo.isdigit():
        return False

    numeros = [int(d) for d in codigo]
    soma_impares = sum(numeros[i] for i in range(0, 12, 2))
    soma_pares = sum(numeros[i] for i in range(1, 12, 2)) * 3
    total = soma_impares + soma_pares
    digito_verificador = (10 - (total % 10)) % 10

    return digito_verificador == numeros[-1]



def consultar_produto_por_codigo(codigo: str):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: consultar_produto_por_codigo()

    B) OBJETIVO:
    Buscar e retornar um objeto de produto específico na base de dados, utilizando seu código de barras como identificador único.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (string)
    Código de barras (EAN-13) do produto a ser consultado.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 4, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 3, "mensagem": "Parâmetro 'codigo' errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR PRODUTO NÃO ENCONTRADO:
    {"retorno": 2, "mensagem": "Produto não encontrado"}

    RETORNO 4: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Produto encontrado com sucesso", "dados": <objeto Produto>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é uma string.

    Assertiva(s) de saída:
    - O retorno é um dicionário com as chaves "retorno" (inteiro), "mensagem" (string) e, em caso de sucesso, "dados" contendo o objeto `Produto`.

    E) DESCRIÇÃO:
    1. Valida se o parâmetro `codigo` não é nulo.
    2. Valida se o `codigo` é do tipo string.
    3. Procura pelo `codigo` como chave no dicionário `_todos_produtos`.
    4. Se o produto não for encontrado, retorna um dicionário de erro.
    5. Se o produto for encontrado, retorna um dicionário de sucesso com o objeto `Produto` correspondente.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos` que armazena todos os produtos cadastrados, usando o código como chave.

    G) RESTRIÇÕES:
    - O armazenamento de dados é em memória e não persiste após o término da execução do programa.
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
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: registrar_produto()

    B) OBJETIVO:
    Cadastrar um novo produto na base de dados, validando todos os parâmetros fornecidos, a validade do código de barras e a sua unicidade.

    C) ACOPLAMENTO:
    PARÂMETRO 1: nome (string)
    Nome do produto.
    PARÂMETRO 2: marca (string)
    Marca do produto.
    PARÂMETRO 3: categoria (string)
    Categoria à qual o produto pertence.
    PARÂMETRO 4: codigo (string)
    Código de barras EAN-13 do produto.
    PARÂMETRO 5: peso (float)
    Peso do produto.
    PARÂMETRO 6: preco (float)
    Preço unitário do produto.
    PARÂMETRO 7: preco_por_peso (float, opcional)
    Preço por unidade de peso (ex: preço por quilo).

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 4, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 3, "mensagem": "Parâmetro 'codigo' errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR CÓDIGO DE BARRAS INVÁLIDO:
    {"retorno": 3, "mensagem": "Código de barras inválido"}

    RETORNO 4: DICIONÁRIO DE ERRO POR PRODUTO JÁ CADASTRADO:
    {"retorno": 5, "mensagem": "Produto já cadastrado com este código"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Produto registrado com sucesso", "dados": <objeto Produto>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Todos os parâmetros obrigatórios são fornecidos e com os tipos corretos.
    - `codigo` é uma string que representa um código de barras EAN-13 válido.

    Assertiva(s) de saída:
    - O retorno é um dicionário com "retorno", "mensagem" e, em caso de sucesso, "dados".
    - Se bem-sucedida, um novo produto é adicionado ao dicionário `_todos_produtos`.

    E) DESCRIÇÃO:
    1. Verifica se algum dos parâmetros obrigatórios é nulo.
    2. Valida se o `codigo` é do tipo string.
    3. Utiliza a função auxiliar `_valida_codigo_barras` para verificar a validade do código.
    4. Verifica se o `codigo` já existe no dicionário `_todos_produtos` para evitar duplicatas.
    5. Se todas as validações passarem, cria uma nova instância da classe `Produto`.
    6. Adiciona o novo produto ao dicionário `_todos_produtos`.
    7. Retorna um dicionário de sucesso com o objeto recém-criado.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos` para armazenamento.
    - A função auxiliar `_valida_codigo_barras()` está disponível para validação.
    - A classe `Produto` está definida.

    G) RESTRIÇÕES:
    - O armazenamento de dados é em memória.
    - A validação do código de barras se limita ao padrão EAN-13.
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
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: atualizar_produto()

    B) OBJETIVO:
    Atualizar um ou mais atributos de um produto já existente na base de dados.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (string)
    Código do produto a ser atualizado.
    PARÂMETRO 2: dados (dicionário)
    Dicionário contendo os campos a serem atualizados como chaves e os novos valores.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 4, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 3, "mensagem": "Parâmetro 'codigo' errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR PRODUTO NÃO ENCONTRADO:
    {"retorno": 2, "mensagem": "Produto não encontrado"}

    RETORNO 4: DICIONÁRIO DE ERRO POR CAMPO INVÁLIDO:
    {"retorno": 3, "mensagem": "Campo inválido para atualização: <nome_do_campo>"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Produto atualizado com sucesso", "dados": <objeto Produto>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é uma string que corresponde a um produto existente.
    - `dados` é um dicionário onde as chaves são nomes válidos de atributos da classe `Produto`.

    Assertiva(s) de saída:
    - O retorno é um dicionário de status.
    - Se bem-sucedida, os atributos do objeto `Produto` correspondente são modificados.

    E) DESCRIÇÃO:
    1. Verifica se os parâmetros `codigo` e `dados` são nulos.
    2. Valida se o `codigo` é do tipo string.
    3. Busca o produto no dicionário `_todos_produtos`. Se não encontrar, retorna erro.
    4. Define uma lista de campos que são permitidos para atualização.
    5. Itera sobre o dicionário `dados`.
    6. Para cada campo, verifica se ele pertence à lista de campos permitidos. Se não, retorna erro.
    7. Se o campo for válido, utiliza a função `setattr` para atualizar o valor no objeto `Produto`.
    8. Após iterar por todos os campos, retorna um dicionário de sucesso com o objeto atualizado.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos`.
    - Os objetos da classe `Produto` são mutáveis.

    G) RESTRIÇÕES:
    - Não é possível atualizar o código de um produto com esta função.
    - Apenas um conjunto pré-definido de atributos pode ser alterado.
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
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: pesquisar_produto()

    B) OBJETIVO:
    Realizar uma busca flexível por produtos, combinando uma pesquisa por texto (em nome, marca e categoria) com filtros exatos em outros atributos.

    C) ACOPLAMENTO:
    PARÂMETRO 1: texto (string)
    Termo de busca a ser procurado nos campos `nome`, `marca` e `categoria`. A busca é insensível a maiúsculas/minúsculas.
    PARÂMETRO 2: filtros (dicionário, opcional)
    Dicionário para aplicar filtros de correspondência exata. Ex: `{"marca": "Marca Exemplo"}`.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 4, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "<N> produto(s) encontrado(s)", "dados": [<lista de objetos Produto>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `texto` é uma string.
    - `filtros` é um dicionário onde as chaves são nomes de atributos válidos.

    Assertiva(s) de saída:
    - O retorno é um dicionário contendo o status e uma lista de objetos `Produto` que satisfazem os critérios de busca. A lista pode estar vazia.

    E) DESCRIÇÃO:
    1. Verifica se o parâmetro `texto` é nulo.
    2. Converte o `texto` de busca para minúsculas para uma comparação case-insensitive.
    3. Inicializa uma lista vazia para armazenar os resultados.
    4. Itera sobre todos os produtos no dicionário `_todos_produtos`.
    5. Para cada produto, verifica se o texto de busca está contido em seu nome, marca ou categoria (também convertidos para minúsculas).
    6. Se o texto for encontrado, a função então verifica se o produto atende a todos os filtros definidos no dicionário `filtros`.
    7. A verificação de filtros compara o valor do atributo no produto com o valor no dicionário de filtros. Se algum filtro não corresponder, o produto é descartado.
    8. Se o produto passar tanto na busca por texto quanto nos filtros, ele é adicionado à lista de resultados.
    9. Ao final, retorna um dicionário de sucesso com a contagem de resultados e a lista de produtos encontrados.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos`.
    - Os produtos possuem os atributos `nome`, `marca` e `categoria` como strings para a busca por texto.

    G) RESTRIÇÕES:
    - A busca por texto é sempre case-insensitive, enquanto os filtros exigem correspondência exata.
    - A performance pode ser impactada em bases de dados muito grandes, pois a busca é sequencial.
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

def listar_todos_produtos():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: listar_todos_produtos()

    B) OBJETIVO:
    Retornar uma lista de todos os produtos registrados no sistema.

    C) ACOPLAMENTO:
    Sem parâmetros de entrada.

    RETORNO 1: DICIONÁRIO SE NÃO HOUVER PRODUTOS:
    {"retorno": 1, "mensagem": "Nenhum produto registrado", "dados": []}

    RETORNO 2: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Produtos listados com sucesso", "dados": [<lista de objetos Produto>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Nenhuma.

    Assertiva(s) de saída:
    - O retorno é um dicionário com a chave "dados" contendo uma lista de objetos Produto. Pode estar vazia.

    E) DESCRIÇÃO:
    1. Obtém todos os produtos registrados em `_todos_produtos`.
    2. Retorna um dicionário com a lista ou uma mensagem informando que não há produtos registrados.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos`.

    G) RESTRIÇÕES:
    - A função retorna todos os objetos, o que pode consumir memória em bases grandes.
    """
    produtos = [
        p for p in _todos_produtos.values()
    ]

    if not produtos:
        return {'retorno': 1, 'mensagem': 'Nenhum produto registrado', 'dados': []}

    return {'retorno': 0, 'mensagem': 'Produtos listados com sucesso', 'dados': produtos}
