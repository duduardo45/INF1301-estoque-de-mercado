import json
from datetime import date
from .produto import Produto


__all__ = [
    "Carrinho",
    "cria_carrinho",
    "consultar_carrinho_por_id",
    "listar_todos_carrinhos",
    "salvar_carrinhos",
    "carregar_carrinhos"
]


CARRINHOS_JSON = 'dados/carrinhos.json'

_todos_carrinhos = {}


class Carrinho:
    def __init__(self, id:int, data_hora:str=None, itens:dict=None, total:float=None, funcionario: 'Funcionario'=None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __init__()

        B) OBJETIVO:
        Inicializar uma nova instância da classe Carrinho, que representa uma venda ou uma cesta de compras, configurando seus atributos iniciais.

        C) ACOPLAMENTO:
        PARÂMETRO 1: id (inteiro)
        Identificador único para o carrinho.
        PARÂMETRO 2: data_hora (string, opcional)
        Data e hora da transação, preenchida na finalização.
        PARÂMETRO 3: itens (dicionário, opcional)
        Dicionário no formato {objeto Produto: quantidade}.
        PARÂMETRO 4: total (float, opcional)
        Valor total da compra, preenchido após o cálculo.
        PARÂMETRO 5: funcionario (Funcionario, opcional)
        Objeto do funcionário que realizou a venda.

        RETORNO: Nenhum (é um método construtor).

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `id` é um número inteiro.
        - Os demais parâmetros, se fornecidos, têm os tipos corretos.

        Assertiva(s) de saída:
        - Uma nova instância da classe `Carrinho` é criada com seus atributos definidos, garantindo que `itens` seja sempre um dicionário.

        E) DESCRIÇÃO:
        1. Atribui os parâmetros `id`, `data_hora`, `total` e `funcionario` aos atributos correspondentes da instância.
        2. Verifica se o parâmetro `itens` foi fornecido.
        3. Se `itens` for `None`, inicializa `self.itens` como um dicionário vazio para evitar erros em operações futuras.
        4. Se `itens` for um dicionário, ele é atribuído diretamente.

        F) HIPÓTESES:
        - A validação da unicidade do `id` é feita pela função que chama este construtor (ex: `criar_carrinho`).

        G) RESTRIÇÕES:
        - Não realiza validações internas sobre os tipos ou valores dos parâmetros.
        """
        if itens is None:
            itens = {}

        self.id = id
        self.data_hora = data_hora
        self.itens = itens
        self.total = total
        self.funcionario = funcionario
    


    def to_json(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: to_json()

        B) OBJETIVO:
        Serializar a instância do Carrinho para um dicionário Python, convertendo os objetos `Produto` e `Funcionario` em seus respectivos códigos para compatibilidade com o formato JSON.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: DICIONÁRIO SERIALIZÁVEL
        Um dicionário contendo os dados do carrinho, pronto para ser salvo em JSON.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Carrinho`.
        - Os objetos `Produto` e `Funcionario` associados possuem um atributo `codigo`.

        Assertiva(s) de saída:
        - Retorna um dicionário onde todas as chaves e valores são tipos primitivos.

        E) DESCRIÇÃO:
        1. Cria um dicionário de resultado com os atributos `id`, `data_hora` e `total`.
        2. Usa "dictionary comprehension" para transformar o dicionário `self.itens`, utilizando o código do produto (`produto.codigo`) como a nova chave.
        3. Verifica se existe um funcionário associado (`self.funcionario`).
        4. Se existir, adiciona o código do funcionário à chave "funcionario"; caso contrário, adiciona `None`.
        5. Retorna o dicionário completo.

        F) HIPÓTESES:
        - A estrutura de dados interna está consistente.

        G) RESTRIÇÕES:
        - A estrutura do dicionário de saída é fixa e depende da implementação atual da classe.
        """
        return {
            "id": self.id,
            "data_hora": self.data_hora,
            "itens": {p.codigo: qtd for p, qtd in self.itens.items()},
            "total": self.total,
            "funcionario": self.funcionario.codigo if self.funcionario else None
        }

    @classmethod
    def from_json(cls, data: dict):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: from_json()

        B) OBJETIVO:
        Criar (desserializar) uma instância da classe `Carrinho` a partir de um dicionário, recriando a estrutura interna com objetos `Produto` e `Funcionario` reais.

        C) ACOPLAMENTO:
        PARÂMETRO 1: data (dicionário)
        Dicionário com os dados do carrinho, onde produtos e funcionários são representados por seus códigos.

        RETORNO 1: Uma nova instância da classe `Carrinho`.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `data` é um dicionário com a estrutura gerada por `to_json`.
        - Os códigos de produto e funcionário em `data` devem corresponder a entidades existentes no sistema.

        Assertiva(s) de saída:
        - Retorna uma instância de `Carrinho` cujos dicionários internos usam objetos como chaves/valores.

        E) DESCRIÇÃO:
        1. Realiza importações locais de `consultar_produto_por_codigo` e `consultar_funcionario` para evitar importações circulares.
        2. Inicia um dicionário `itens` vazio.
        3. Itera sobre os códigos de produto em `data["itens"]`, busca cada objeto `Produto` e popula o dicionário `itens`.
        4. Verifica se há um código de funcionário em `data`. Se houver, busca o objeto `Funcionario`.
        5. Se um produto ou funcionário não for encontrado durante a busca, lança uma exceção `ValueError`.
        6. Invoca o construtor da classe (`cls(...)`) com os dados e objetos recuperados.
        7. Retorna a instância de `Carrinho` completamente populada.

        F) HIPÓTESES:
        - Os módulos de produto e funcionário, juntamente com seus dados, já foram carregados no sistema.

        G) RESTRIÇÕES:
        - Lança uma exceção não tratada se um código de produto ou funcionário não existir, o que pode interromper o processo de carregamento do sistema.
        """    
        from modulos.produto import consultar_produto_por_codigo
        from modulos.funcionario import consultar_funcionario

        itens = {}
        for cod, qtd in data["itens"].items():
            res = consultar_produto_por_codigo(cod)
            if res["retorno"] != 0:
                raise ValueError(f"Produto {cod} não encontrado. Inicialize antes de carregar o carrinho.")
            itens[res["dados"]] = qtd

        funcionario = None
        if data.get("funcionario"):
            res = consultar_funcionario(data["funcionario"], incluir_inativos=True)
            if res["retorno"] != 0:
                raise ValueError(f"Funcionário {data['funcionario']} não encontrado.")
            funcionario = res["dados"]

        return cls(
            id=data["id"],
            data_hora=data.get("data_hora"),
            itens=itens,
            total=data.get("total"),
            funcionario=funcionario
        )



    def adiciona_no_carrinho(self, produto: Produto, qtd: float):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: adiciona_no_carrinho() (Método de Carrinho)

        B) OBJETIVO:
        Adicionar um produto ao carrinho. Se o produto já existir, a nova quantidade é somada à existente; caso contrário, o produto é adicionado como um novo item.

        C) ACOPLAMENTO:
        PARÂMETRO 1: produto (Produto)
        O objeto do produto a ser adicionado.
        PARÂMETRO 2: qtd (float)
        A quantidade do produto a ser adicionada.

        RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
        {"retorno": 3, "mensagem": "Parâmetro nulo"}

        RETORNO 2: DICIONÁRIO DE ERRO POR QUANTIDADE INVÁLIDA:
        {"retorno": 2, "mensagem": "Parâmetro quantidade inválido"}

        RETORNO 3: DICIONÁRIO DE SUCESSO AO ATUALIZAR QUANTIDADE:
        {"retorno": 1, "mensagem": "Produto já existia, quantidade atualizada"}

        RETORNO 4: DICIONÁRIO DE SUCESSO AO ADICIONAR NOVO PRODUTO:
        {"retorno": 0, "mensagem": "Produto adicionado com sucesso"}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `produto` é um objeto da classe `Produto`.
        - `qtd` é um número (inteiro ou float) maior que zero.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - O dicionário `self.itens` da instância é modificado para refletir a adição.

        E) DESCRIÇÃO:
        1. Valida se os parâmetros `produto` e `qtd` não são nulos.
        2. Valida se `qtd` é um número positivo.
        3. Verifica se o `produto` já existe como chave no dicionário `self.itens`.
        4. Se existir, soma a `qtd` ao valor existente.
        5. Se não existir, insere o `produto` como nova chave com o valor `qtd`.
        6. Retorna o dicionário de status apropriado.

        F) HIPÓTESES:
        - O dicionário `self.itens` utiliza objetos `Produto` como chaves e números como valores.
        - A classe `Produto` pode ser usada como chave de dicionário (é hasheável).

        G) RESTRIÇÕES:
        - Modifica o estado do objeto `Carrinho`.
        """
        if produto is None or qtd is None:
            return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}
        if not isinstance(qtd, (int, float)) or qtd <= 0:
            return {'retorno': 2, 'mensagem': 'Parâmetro quantidade inválido'}

        if produto in self.itens:
            self.itens[produto] += qtd
            return {'retorno': 1, 'mensagem': 'Produto já existia, quantidade atualizada'}

        self.itens[produto] = qtd
        return {'retorno': 0, 'mensagem': 'Produto adicionado com sucesso'}



    def remover_do_carrinho(self, produto: Produto, quantidade: float):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: remover_do_carrinho() (Método de Carrinho)

        B) OBJETIVO:
        Remover uma quantidade específica de um produto do carrinho. Se a quantidade a ser removida for maior ou igual à existente, o produto é removido por completo.

        C) ACOPLAMENTO:
        PARÂMETRO 1: produto (Produto)
        O objeto do produto a ser removido.
        PARÂMETRO 2: quantidade (float)
        A quantidade do produto a ser removida.

        RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
        {"retorno": 3, "mensagem": "Parâmetro nulo"}

        RETORNO 2: DICIONÁRIO DE ERRO POR QUANTIDADE INVÁLIDA:
        {"retorno": 2, "mensagem": "Quantidade inválida"}

        RETORNO 3: DICIONÁRIO DE ERRO POR PRODUTO NÃO ENCONTRADO:
        {"retorno": 1, "mensagem": "Produto não encontrado no carrinho"}

        RETORNO 4: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Produto removido do carrinho"}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `produto` é um objeto da classe `Produto`.
        - `quantidade` é um número positivo.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - O dicionário `self.itens` é modificado para refletir a remoção.

        E) DESCRIÇÃO:
        1. Valida os parâmetros `produto` e `quantidade` contra nulos e valores inválidos.
        2. Verifica se o `produto` existe no carrinho. Se não, retorna erro.
        3. Compara a quantidade existente do produto com a `quantidade` a ser removida.
        4. Se a quantidade a remover for maior ou igual, remove o item completamente do dicionário.
        5. Caso contrário, apenas subtrai a `quantidade` da quantidade existente.
        6. Retorna um dicionário de sucesso.

        F) HIPÓTESES:
        - O dicionário `self.itens` utiliza objetos `Produto` como chaves.

        G) RESTRIÇÕES:
        - A ação de remoção é irreversível para o estado atual do carrinho.
        """
        if produto is None or quantidade is None:
            return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}
        if not isinstance(quantidade, (int, float)) or quantidade <= 0:
            return {'retorno': 2, 'mensagem': 'Quantidade inválida'}

        if produto not in self.itens:
            return {'retorno': 1, 'mensagem': 'Produto não encontrado no carrinho'}

        if self.itens[produto] <= quantidade:
            del self.itens[produto]
        else:
            self.itens[produto] -= quantidade

        return {'retorno': 0, 'mensagem': 'Produto removido do carrinho'}



    def calcula_total(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: calcula_total() (Método de Carrinho)

        B) OBJETIVO:
        Calcular o preço total de todos os itens presentes no carrinho, atualizando o atributo `total` da instância.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: VALOR TOTAL (float)
        A soma dos preços de todos os itens no carrinho.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - O dicionário `self.itens` contém objetos `Produto` como chaves e suas quantidades como valores.
        - Cada objeto `Produto` possui um método `calcula_preco(quantidade)` que retorna um dicionário com o preço na chave 'dados'.

        Assertiva(s) de saída:
        - Retorna um float com o valor total.
        - O atributo `self.total` da instância é atualizado com o valor calculado.

        E) DESCRIÇÃO:
        1. Inicializa uma variável de total local como 0.
        2. Itera sobre cada par de produto-quantidade no dicionário `self.itens`.
        3. Para cada item, chama o método `calcula_preco` do objeto produto, passando a quantidade.
        4. Extrai o valor do preço do dicionário de retorno do método e o soma ao total local.
        5. Ao final do loop, atribui o total calculado ao atributo `self.total`.
        6. Retorna o valor total.

        F) HIPÓTESES:
        - O método `calcula_preco` de um `Produto` retorna um dicionário no formato `{'retorno': 0, 'dados': <preco>}` em caso de sucesso.

        G) RESTRIÇÕES:
        - A precisão do cálculo depende da implementação do método `calcula_preco` na classe `Produto`.
        """
        total = 0
        for produto, quantidade in self.itens.items():
            resultado_preco = produto.calcula_preco(quantidade)
            if resultado_preco['retorno'] == 0:
                total += resultado_preco['dados']
        self.total = total
        return total



    def listar_itens(self, verbose: bool = False):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: listar_itens() (Método de Carrinho)

        B) OBJETIVO:
        Fornecer uma lista de todos os itens no carrinho, seja de forma resumida (código e quantidade) ou detalhada (descrição completa).

        C) ACOPLAMENTO:
        PARÂMETRO 1: verbose (booleano, opcional)
        Se `True`, a lista contém descrições detalhadas dos itens. Se `False` (padrão), contém tuplas `(codigo, quantidade)`.

        RETORNO 1: DICIONÁRIO SE O CARRINHO ESTIVER VAZIO:
        {"retorno": 1, "mensagem": "Carrinho vazio", "dados": []}

        RETORNO 2: DICIONÁRIO DE SUCESSO COM OS ITENS:
        {"retorno": 0, "mensagem": "Itens listados com sucesso", "dados": [<lista de itens>]}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `verbose` é um valor booleano.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status, cuja chave 'dados' contém uma lista dos itens no formato solicitado.

        E) DESCRIÇÃO:
        1. Verifica se o dicionário `self.itens` está vazio. Se estiver, retorna um erro indicando carrinho vazio.
        2. Se `verbose` for `False`, cria uma lista de tuplas, cada uma contendo o código e a quantidade do produto.
        3. Se `verbose` for `True`, cria uma lista de strings, cada uma sendo a representação textual do produto com sua quantidade.
        4. Retorna um dicionário de sucesso com a lista criada.

        F) HIPÓTESES:
        - Os objetos `Produto` possuem um atributo `codigo` e um método `__str__(quantidade)` que retorna uma descrição formatada.

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        if not self.itens:
            return {'retorno': 1, 'mensagem': 'Carrinho vazio', 'dados': []}

        if not verbose:
            dados = [(produto.codigo, quantidade) for produto, quantidade in self.itens.items()]
        else:
            dados = [produto.__str__(quantidade) for produto, quantidade in self.itens.items()]

        return {'retorno': 0, 'mensagem': 'Itens listados com sucesso', 'dados': dados}



    def limpar_carrinho(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: limpar_carrinho() (Método de Carrinho)

        B) OBJETIVO:
        Remover todos os itens do carrinho, deixando-o em um estado vazio.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Carrinho esvaziado com sucesso"}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - Nenhuma.

        Assertiva(s) de saída:
        - O dicionário `self.itens` da instância se torna um dicionário vazio.

        E) DESCRIÇÃO:
        1. Chama o método `.clear()` no dicionário `self.itens` para remover todos os seus elementos.
        2. Retorna um dicionário de sucesso.

        F) HIPÓTESES:
        - `self.itens` é um dicionário.

        G) RESTRIÇÕES:
        - A operação é irreversível para o estado atual dos itens no carrinho.
        """
        self.itens.clear()
        return {'retorno': 0, 'mensagem': 'Carrinho esvaziado com sucesso'}



    def finaliza_carrinho(self, funcionario: 'Funcionario'=None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: finaliza_carrinho() (Método de Carrinho)

        B) OBJETIVO:
        Marcar o carrinho como finalizado, registrando a data da transação e o funcionário responsável pela venda.

        C) ACOPLAMENTO:
        PARÂMETRO 1: funcionario (Funcionario)
        O objeto do funcionário que finalizou a venda.

        RETORNO 1: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Carrinho finalizado"}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `funcionario` é um objeto da classe `Funcionario`.

        Assertiva(s) de saída:
        - Os atributos `self.data_hora` e `self.funcionario` da instância são preenchidos.

        E) DESCRIÇÃO:
        1. Obtém a data atual do sistema.
        2. Formata a data para o padrão "YYYY/MM/DD" e a atribui a `self.data_hora`.
        3. Atribui o objeto `funcionario` recebido a `self.funcionario`.
        4. Retorna um dicionário de sucesso.

        F) HIPÓTESES:
        - O módulo `datetime` está disponível para obter a data.

        G) RESTRIÇÕES:
        - Esta função apenas marca o carrinho como finalizado. Ela não realiza a baixa no estoque ou processamento de pagamento.
        """
        self.data_hora = date.today().strftime("%Y/%m/%d")
        self.funcionario = funcionario
        return {'retorno': 0, 'mensagem': 'Carrinho finalizado'}
    


def salvar_carrinhos():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: salvar_carrinhos()

    B) OBJETIVO:
    Persistir em um arquivo JSON o estado atual de todos os carrinhos (vendas) registrados no sistema.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito. A função realiza uma operação de escrita em arquivo.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O dicionário global `_todos_carrinhos` contém instâncias da classe `Carrinho`.

    Assertiva(s) de saída:
    - O arquivo definido pela constante `CARRINHOS_JSON` é criado ou sobrescrito com os dados de todos os carrinhos.

    E) DESCRIÇÃO:
    1. Inicializa um dicionário vazio `json_carrinhos`.
    2. Itera sobre cada par de id-carrinho no dicionário global `_todos_carrinhos`.
    3. Para cada objeto, invoca seu método `to_json()` para obter sua representação em dicionário serializável.
    4. Adiciona este dicionário ao `json_carrinhos`, usando o ID do carrinho como chave.
    5. Abre o arquivo de destino em modo de escrita ("w") com codificação "utf-8".
    6. Utiliza `json.dump()` para escrever o conteúdo do `json_carrinhos` no arquivo, com formatação indentada.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_carrinhos`.
    - A constante `CARRINHOS_JSON` aponta para um caminho de arquivo válido e com permissão de escrita.
    - A classe `Carrinho` possui um método `to_json()` funcional.

    G) RESTRIÇÕES:
    - A função sobrescreve o arquivo de destino sem aviso ou backup.
    - Possíveis erros de I/O não são tratados internamente.
    """
    json_carrinhos = {}

    for id, c in _todos_carrinhos.items():
        json_carrinhos[id] = c.to_json()

    with open(CARRINHOS_JSON, "w", encoding="utf-8") as f:
        json.dump(json_carrinhos, f, ensure_ascii=False, indent=4)

def carregar_carrinhos():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: carregar_carrinhos()

    B) OBJETIVO:
    Ler os dados de carrinhos de um arquivo JSON e carregá-los para a memória, populando o dicionário global `_todos_carrinhos`.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito. Modifica o estado do dicionário global `_todos_carrinhos`.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O arquivo `CARRINHOS_JSON` existe e é um JSON válido.
    - Todos os produtos e funcionários referenciados nos dados já devem ter sido carregados no sistema.

    Assertiva(s) de saída:
    - O dicionário `_todos_carrinhos` é preenchido com instâncias de `Carrinho` recriadas a partir do arquivo.

    E) DESCRIÇÃO:
    1. Utiliza um bloco `try-except` para tratar o caso de o arquivo não existir (`FileNotFoundError`), retornando silenciosamente.
    2. Se o arquivo existir, seu conteúdo JSON é carregado para um dicionário `json_carrinhos`.
    3. Itera sobre cada par de id-dados no dicionário carregado.
    4. Invoca o método de classe `Carrinho.from_json()` para criar uma nova instância de `Carrinho`.
    5. Armazena a instância no dicionário global `_todos_carrinhos`.

    F) HIPÓTESES:
    - As funções `carregar_produtos()` e `carregar_funcionarios()` foram executadas previamente.

    G) RESTRIÇÕES:
    - Não trata exceções que podem ser levantadas por `Carrinho.from_json` (como `ValueError` ou `KeyError`), o que pode interromper o processo de carregamento.
    """
    try:
        with open(CARRINHOS_JSON, "r", encoding="utf-8") as f:
            json_carrinhos = json.load(f)
    except FileNotFoundError:
        return  # Arquivo ainda não existe, nada para carregar

    for id, c_json in json_carrinhos.items():
        _todos_carrinhos[id] = Carrinho.from_json(c_json)

def criar_carrinho():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: criar_carrinho()

    B) OBJETIVO:
    Criar uma nova instância de `Carrinho` com um ID único sequencial e registrá-la no dicionário global do sistema.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO 1: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Carrinho criado com sucesso", "dados": <objeto Carrinho>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Nenhuma.

    Assertiva(s) de saída:
    - Um novo objeto `Carrinho` é criado e adicionado ao dicionário `_todos_carrinhos`.
    - O retorno é um dicionário contendo o objeto recém-criado.

    E) DESCRIÇÃO:
    1. Determina um novo ID para o carrinho, utilizando o tamanho atual do dicionário `_todos_carrinhos` e somando 1.
    2. Importa a classe `Carrinho` localmente para evitar possíveis problemas de referência.
    3. Cria uma nova instância da classe `Carrinho`, passando o novo ID.
    4. Adiciona o novo carrinho ao dicionário global `_todos_carrinhos`, usando o ID como chave.
    5. Retorna um dicionário de sucesso com uma mensagem e o objeto carrinho criado.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_carrinhos` para o armazenamento.

    G) RESTRIÇÕES:
    - O método de geração de ID é simples (tamanho + 1) e pode não ser robusto para casos de remoção de carrinhos ou ambientes concorrentes.
    """
    novo_id = len(_todos_carrinhos) + 1
    from modulos.carrinho import Carrinho

    carrinho = Carrinho(id=novo_id)
    _todos_carrinhos[novo_id] = carrinho
    return {"retorno": 0, "mensagem": "Carrinho criado com sucesso", "dados": carrinho}


def consultar_carrinho_por_id(id: int):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: consultar_carrinho_por_id()

    B) OBJETIVO:
    Buscar e retornar um carrinho específico registrado no sistema, utilizando seu ID como chave de busca.

    C) ACOPLAMENTO:
    PARÂMETRO 1: id (inteiro)
    O ID do carrinho a ser consultado.

    RETORNO 1: DICIONÁRIO DE ERRO POR ID INVÁLIDO:
    {"retorno": 2, "mensagem": "Parâmetro inválido: id deve ser um inteiro"}

    RETORNO 2: DICIONÁRIO DE ERRO POR CARRINHO NÃO ENCONTRADO:
    {"retorno": 1, "mensagem": "Carrinho não encontrado"}

    RETORNO 3: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Carrinho encontrado", "dados": <objeto Carrinho>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `id` é um número inteiro.

    Assertiva(s) de saída:
    - O retorno é um dicionário de status que, em caso de sucesso, contém o objeto `Carrinho` na chave 'dados'.

    E) DESCRIÇÃO:
    1. Valida se o `id` fornecido é do tipo inteiro. Se não for, retorna um erro.
    2. Utiliza o método `.get()` para buscar o `id` no dicionário global `_todos_carrinhos`.
    3. Se o método `.get()` retornar `None` (carrinho não encontrado), retorna um dicionário de erro.
    4. Se o carrinho for encontrado, retorna um dicionário de sucesso com o objeto correspondente.

    F) HIPÓTESES:
    - `_todos_carrinhos` é o dicionário global que armazena todas as instâncias de `Carrinho`.

    G) RESTRIÇÕES:
    - Nenhuma.
    """
    if not isinstance(id, int):
        return {"retorno": 2, "mensagem": "Parâmetro inválido: id deve ser um inteiro"}

    carrinho = _todos_carrinhos.get(id)
    if not carrinho:
        return {"retorno": 1, "mensagem": "Carrinho não encontrado"}

    return {"retorno": 0, "mensagem": "Carrinho encontrado", "dados": carrinho}


def listar_todos_carrinhos():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: listar_todos_carrinhos()

    B) OBJETIVO:
    Retornar uma lista contendo todos os objetos de carrinho (vendas) registrados no sistema.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO 1: DICIONÁRIO SE NÃO HOUVER CARRINHOS:
    {"retorno": 1, "mensagem": "Nenhum carrinho registrado", "dados": []}

    RETORNO 2: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Listagem realizada com sucesso", "dados": [<lista de objetos Carrinho>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Nenhuma.

    Assertiva(s) de saída:
    - O retorno é um dicionário com uma chave "dados" contendo uma lista de objetos `Carrinho`. A lista pode estar vazia.

    E) DESCRIÇÃO:
    1. Verifica se o dicionário global `_todos_carrinhos` está vazio.
    2. Se estiver vazio, retorna um dicionário informando que não há carrinhos registrados.
    3. Se houver carrinhos, converte os valores do dicionário em uma lista (`list(_todos_carrinhos.values())`).
    4. Retorna um dicionário de sucesso com a lista de todos os carrinhos.

    F) HIPÓTESES:
    - `_todos_carrinhos` é o dicionário que centraliza todos os carrinhos.

    G) RESTRIÇÕES:
    - A função retorna uma lista com todos os objetos, o que pode consumir uma quantidade significativa de memória se o número de carrinhos for muito grande.
    """
    if not _todos_carrinhos:
        return {"retorno": 1, "mensagem": "Nenhum carrinho registrado", "dados": []}

    return {"retorno": 0, "mensagem": "Listagem realizada com sucesso", "dados": list(_todos_carrinhos.values())}
