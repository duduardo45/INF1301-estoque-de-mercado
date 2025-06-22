import json

PRODUTOS_JSON = 'dados/produtos.json'

_todos_produtos = {}

__all__ = [
    "Produto",
    "consultar_produto_por_codigo",
    "registrar_produto",
    "atualizar_produto",
    "pesquisar_produto",
    "listar_todos_produtos",
    "salvar_produtos",
    "carregar_produtos"
]




class Produto:
    def __init__(self, nome: str, marca: str, categoria: str, codigo: str, peso: float, preco: float, preco_por_peso: float = None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __init__()

        B) OBJETIVO:
        Inicializar uma nova instância da classe Produto, atribuindo todos os dados essenciais que caracterizam um produto.

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
        Peso do produto na unidade correspondente.
        PARÂMETRO 6: preco (float)
        Preço por unidade do produto.
        PARÂMETRO 7: preco_por_peso (float, opcional)
        Preço por unidade de peso (ex: preço/kg), se aplicável.

        RETORNO: Nenhum (é um método construtor).

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - Os parâmetros são fornecidos com os tipos de dados corretos.

        Assertiva(s) de saída:
        - Uma nova instância da classe `Produto` é criada com todos os seus atributos definidos.

        E) DESCRIÇÃO:
        1. Este método é o construtor da classe `Produto`.
        2. Ele recebe todos os dados necessários para representar um produto.
        3. Atribui cada parâmetro recebido a um atributo correspondente na instância (`self`), definindo o estado inicial do objeto.

        F) HIPÓTESES:
        - A validação da integridade e formato dos dados (como a validação do código de barras) é realizada antes da invocação deste construtor.

        G) RESTRIÇÕES:
        - O construtor não realiza nenhuma validação interna dos dados; ele confia que os valores recebidos são corretos e válidos.
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
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __str__()

        B) OBJETIVO:
        Fornecer uma representação textual legível de uma instância do produto, adaptando os detalhes exibidos com base na presença de uma quantidade.

        C) ACOPLAMENTO:
        PARÂMETRO 1: quantidade (float, opcional)
        Se fornecido, a string de retorno incluirá a quantidade e o subtotal. Caso contrário, exibirá o preço padrão.

        RETORNO 1: Uma string formatada descrevendo o produto.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Produto`.
        - `quantidade`, se fornecida, é um valor numérico.

        Assertiva(s) de saída:
        - Retorna uma string única com os detalhes do produto concatenados.

        E) DESCRIÇÃO:
        1. Inicia uma lista de strings com as informações básicas: nome, marca, categoria e código.
        2. Verifica se o parâmetro `quantidade` foi fornecido.
        3. Se `quantidade` for nulo, a lista é preenchida com o peso e o preço (unitário ou por peso, conforme aplicável).
        4. Se `quantidade` for um número, a lista é preenchida com a quantidade e o subtotal, calculado através do método `calcula_preco`.
        5. Concatena todos os itens da lista em uma única string, separados por " | ", e a retorna.

        F) HIPÓTESES:
        - O método `calcula_preco` está implementado e retorna um dicionário com o preço calculado na chave "dados".

        G) RESTRIÇÕES:
        - A formatação do preço e do subtotal está fixa para duas casas decimais.
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
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: to_json()

        B) OBJETIVO:
        Converter (serializar) a instância do objeto `Produto` em um dicionário Python, adequado para a persistência em formato JSON.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: DICIONÁRIO SERIALIZÁVEL
        Um dicionário contendo os atributos da instância como pares de chave-valor.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Produto`.

        Assertiva(s) de saída:
        - O dicionário retornado contém apenas tipos de dados primitivos, compatíveis com a serialização JSON.

        E) DESCRIÇÃO:
        1. Cria um dicionário.
        2. Mapeia cada atributo da instância (`self.nome`, `self.marca`, etc.) para uma chave correspondente no dicionário.
        3. Retorna o dicionário populado com todos os dados do produto.

        F) HIPÓTESES:
        - Todos os atributos do objeto são de tipos diretamente serializáveis para JSON (string, número, booleano, None).

        G) RESTRIÇÕES:
        - Se novos atributos forem adicionados à classe `Produto`, este método precisará ser atualizado para incluí-los na serialização.
        """        
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
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: from_json()

        B) OBJETIVO:
        Criar uma nova instância da classe `Produto` a partir de um dicionário (geralmente desserializado de um arquivo JSON).

        C) ACOPLAMENTO:
        PARÂMETRO 1: json_dict (dicionário)
        Um dicionário contendo os dados do produto.

        RETORNO 1: Uma nova instância da classe `Produto`.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `json_dict` é um dicionário que contém as chaves obrigatórias ("nome", "marca", "categoria", "codigo", "peso", "preco").

        Assertiva(s) de saída:
        - Uma instância completa e funcional da classe `Produto` é retornada.

        E) DESCRIÇÃO:
        1. É um método de classe, operando sobre a classe (`cls`) em vez de uma instância.
        2. Extrai os valores para `nome`, `marca`, `categoria`, `codigo`, `peso` e `preco` diretamente do dicionário.
        3. Utiliza `json_dict.get("preco_por_peso", None)` para obter o preço por peso, tratando o caso em que a chave pode não existir.
        4. Invoca o construtor da classe (`cls(...)`) com todos os valores extraídos.
        5. Retorna a nova instância criada.

        F) HIPÓTESES:
        - A estrutura do dicionário `json_dict` é consistente com a esperada, contendo as chaves necessárias.

        G) RESTRIÇÕES:
        - Se uma chave obrigatória (ex: "nome") estiver ausente no dicionário, uma exceção `KeyError` será levantada.
        - Não há validação interna dos tipos de dados dos valores no dicionário.
        """        
        nome = json_dict["nome"]
        marca = json_dict["marca"]
        categoria = json_dict["categoria"]
        codigo = json_dict["codigo"]
        peso = json_dict["peso"]
        preco = json_dict["preco"]
        preco_por_peso = json_dict.get("preco_por_peso", None)
        return cls(nome, marca, categoria, codigo, peso, preco, preco_por_peso)



    def calcula_preco(self, quantidade):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: calcula_preco()

        B) OBJETIVO:
        Calcular o preço total para uma quantidade específica de um produto, tratando corretamente produtos com preço unitário e produtos com preço por peso.

        C) ACOPLAMENTO:
        PARÂMETRO 1: quantidade (float)
        A quantidade do produto para a qual o preço total será calculado.

        RETORNO 1: DICIONÁRIO DE ERRO POR QUANTIDADE INVÁLIDA:
        {"retorno": 1, "mensagem": "Quantidade deve ser maior que zero."}

        RETORNO 2: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Preço calculado com sucesso.", "dados": <preco_total>}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Produto`.
        - `quantidade` é um valor numérico.

        Assertiva(s) de saída:
        - O retorno é um dicionário com as chaves "retorno", "mensagem" e, em caso de sucesso, "dados" contendo o preço total.

        E) DESCRIÇÃO:
        1. Valida se a `quantidade` fornecida é maior que zero. Se não for, retorna um dicionário de erro.
        2. Verifica se o atributo `preco_por_peso` da instância é nulo.
        3. Se for nulo, o cálculo é feito multiplicando o preço unitário (`self.preco`) pela `quantidade`.
        4. Se `preco_por_peso` tiver um valor, o cálculo é feito multiplicando este valor pela `quantidade`.
        5. Retorna um dicionário de sucesso com o preço total calculado no campo "dados".

        F) HIPÓTESES:
        - Os atributos `preco` e `preco_por_peso` da instância são valores numéricos válidos para cálculo.

        G) RESTRIÇÕES:
        - A função assume que a `quantidade` está na unidade correta para o tipo de preço (unidades para preço unitário, peso para preço por peso).
        """
        if quantidade <= 0:
            return {"retorno": 1, "mensagem": "Quantidade deve ser maior que zero."}

        if self.preco_por_peso is None:
            preco_total = self.preco * quantidade
        else:
            preco_total = self.preco_por_peso * quantidade

        return {"retorno": 0, "mensagem": "Preço calculado com sucesso.", "dados": preco_total}



def salvar_produtos():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: salvar_produtos()

    B) OBJETIVO:
    Persistir o estado atual de todos os produtos, que estão armazenados na memória, em um arquivo no formato JSON.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito é retornado. A função realiza uma operação de I/O, escrevendo em um arquivo.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O dicionário global `_todos_produtos` está inicializado e contém instâncias da classe `Produto`.

    Assertiva(s) de saída:
    - Um arquivo JSON, localizado no caminho definido pela constante `PRODUTOS_JSON`, é criado ou sobrescrito com os dados dos produtos.

    E) DESCRIÇÃO:
    1. Inicializa um dicionário vazio `json_produtos`.
    2. Itera sobre cada par de código-produto no dicionário global `_todos_produtos`.
    3. Para cada objeto de produto, invoca seu método `to_json()` para obter sua representação em dicionário.
    4. Adiciona este dicionário ao `json_produtos`, usando o código do produto como chave.
    5. Abre o arquivo de destino em modo de escrita ("w") e com codificação "utf-8".
    6. Utiliza a função `json.dump()` para escrever o conteúdo do dicionário `json_produtos` no arquivo, com formatação indentada.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos` para armazenamento em memória.
    - A constante `PRODUTOS_JSON` contém um caminho de arquivo válido.
    - Cada objeto em `_todos_produtos` possui um método `to_json()` funcional.
    - O programa tem permissão de escrita no diretório de destino.

    G) RESTRIÇÕES:
    - A função sobrescreve o arquivo de destino sem aviso ou backup.
    - Possíveis erros de I/O (ex: disco cheio) não são tratados e podem interromper o programa.
    """
    json_produtos = {}

    for codigo, p in _todos_produtos.items():
        json_produtos[codigo] = p.to_json()

    with open(PRODUTOS_JSON, "w", encoding="utf-8") as f:
        json.dump(json_produtos, f, ensure_ascii=False, indent=4)

def carregar_produtos():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: carregar_produtos()

    B) OBJETIVO:
    Ler os dados de produtos de um arquivo JSON e carregá-los para a memória, populando o dicionário global `_todos_produtos`.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito é retornado. A função modifica o estado do dicionário global `_todos_produtos`.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O arquivo especificado pela constante `PRODUTOS_JSON` deve existir.
    - O conteúdo do arquivo deve ser um JSON válido que represente um dicionário de produtos.

    Assertiva(s) de saída:
    - O dicionário global `_todos_produtos` é preenchido com as instâncias de `Produto` recriadas a partir dos dados do arquivo.

    E) DESCRIÇÃO:
    1. Utiliza um bloco `try-except` para lidar com a possível ausência do arquivo.
    2. Tenta abrir o arquivo definido em `PRODUTOS_JSON` em modo de leitura ("r").
    3. Caso o arquivo não exista (`FileNotFoundError`), a função termina sua execução silenciosamente.
    4. Se o arquivo for aberto com sucesso, utiliza `json.load()` para desserializar seu conteúdo.
    5. Itera sobre cada par de código-produto no dicionário lido do arquivo.
    6. Para cada item, invoca o método de classe `Produto.from_json()` para criar uma nova instância do objeto.
    7. Armazena a instância recém-criada no dicionário global `_todos_produtos`, usando o código como chave.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_produtos` para ser populado.
    - A constante `PRODUTOS_JSON` aponta para o caminho correto do arquivo.
    - A classe `Produto` implementa um método de classe `from_json()` funcional.

    G) RESTRIÇÕES:
    - A função não trata erros de formatação no JSON (`JSONDecodeError`) ou de chaves ausentes (`KeyError`), que podem interromper o carregamento.
    """
    try:
        with open(PRODUTOS_JSON, "r", encoding="utf-8") as f:
            json_produtos = json.load(f)
    except FileNotFoundError:
        return

    for codigo, p_json in json_produtos.items():
        _todos_produtos[codigo] = Produto.from_json(p_json)



def _valida_codigo_barras(codigo: str):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: _valida_codigo_barras()

    B) OBJETIVO:
    Validar a integridade de um código de barras no padrão EAN-13, verificando seu formato e o dígito verificador.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (string)
    A string de 13 dígitos do código de barras a ser validado.

    RETORNO 1: Booleano (`True` se o código for válido, `False` caso contrário).

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O parâmetro `codigo` é do tipo string.

    Assertiva(s) de saída:
    - O retorno é estritamente `True` ou `False`.

    E) DESCRIÇÃO:
    1. Verifica se o `codigo` é uma string, se tem o comprimento de 13 caracteres e se contém apenas dígitos. Se qualquer uma dessas condições falhar, retorna `False`.
    2. Converte a string do código em uma lista de inteiros.
    3. Aplica o algoritmo de soma do EAN-13:
        a. Soma os dígitos nas posições 0, 2, 4, 6, 8, 10.
        b. Soma os dígitos nas posições 1, 3, 5, 7, 9, 11 e multiplica o resultado por 3.
    4. Soma os dois totais obtidos.
    5. Calcula o dígito verificador: `(10 - (soma_total % 10)) % 10`.
    6. Compara o dígito verificador calculado com o último dígito do código de barras original (`numeros[-1]`).
    7. Retorna `True` se forem iguais, e `False` caso contrário.

    F) HIPÓTESES:
    - O algoritmo de cálculo do dígito verificador está corretamente implementado para o padrão EAN-13.

    G) RESTRIÇÕES:
    - Esta função valida exclusivamente o formato EAN-13 e não serve para outros tipos de códigos de barras.
    - Sendo uma função "privada" (prefixo `_`), seu uso é destinado apenas a este módulo.
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
