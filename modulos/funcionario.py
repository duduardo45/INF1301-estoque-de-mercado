import json
from datetime import date

_todos_funcionarios = {}

FUNCIONARIOS_JSON = 'dados/funcionarios.json'

__all__ = [
    "Funcionario",
    "adiciona_funcionario",
    "novo_funcionario",
    "consultar_funcionario",
    "consultar_funcionarios_por_nome",
    "listar_todos_funcionarios",
    "salvar_funcionarios",
    "carregar_funcionarios"
]


class Funcionario:
    def __init__(self, nome, codigo, cargo, data_contratacao, data_desligamento=None):
        """
        Inicializa um objeto Funcionario com os dados fornecidos.

        Args:
            nome (str): Nome completo do funcionário.
            codigo (int): Código identificador único.
            cargo (str): Cargo ocupado pelo funcionário.
            data_contratacao (str): Data de contratação no formato 'YYYY/MM/DD'.
            data_desligamento (str, opcional): Data de desligamento, se houver.

        Retorna:
            None
        """
        self.nome = nome
        self.codigo = codigo
        self.cargo = cargo
        self.data_contratacao = data_contratacao
        self.data_desligamento = data_desligamento


    def __str__(self, resumo_vendas: tuple[int, float] = None):
        """
        Retorna uma representação em string amigável do objeto Funcionario.

        Args:
            resumo_vendas (tuple, opcional): tupla contendo (número de vendas, total arrecadado)

        Retorna:
            str: descrição resumida do funcionário
        """
        partes = [
            f"Funcionário: {self.nome}",
            f"Código: {self.codigo}",
            f"Cargo: {self.cargo}",
            f"Data de contratação: {self.data_contratacao}",
        ]

        if self.data_desligamento:
            partes.append("Status: Desativado")
            partes.append(f"Data de desligamento: {self.data_desligamento}")
        else:
            partes.append("Status: Ativo")

        if resumo_vendas is not None:
            num_vendas, total_arrecadado = resumo_vendas
            partes.append(f"Vendas realizadas: {num_vendas}")
            partes.append(f"Total arrecadado: R$ {total_arrecadado:.2f}")

        return " | ".join(partes)
    
    def to_json(self):
        return {
            "nome": self.nome,
            "codigo": self.codigo,
            "cargo": self.cargo,
            "data_contratacao": self.data_contratacao,
            "data_desligamento": self.data_desligamento
        }

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            nome=data["nome"],
            codigo=data["codigo"],
            cargo=data["cargo"],
            data_contratacao=data["data_contratacao"],
            data_desligamento=data.get("data_desligamento")
        )

    def atualizar(self, atributo: str, valor):
        """
        Atualiza um atributo do funcionário.

        Args:
            atributo (str): Nome do atributo a ser alterado.
            valor: Novo valor a ser atribuído.

        Retorna:
            0 -> Sucesso
            1 -> Atributo inexistente
            2 -> Parâmetro nulo
            3 -> Parâmetro incorreto
        """
        if atributo is None or valor is None:
            return {'retorno': 2, 'mensagem': 'Parâmetro nulo'}
        if not isinstance(atributo, str):
            return {'retorno': 3, 'mensagem': 'Parâmetro atributo errado'}
        if not hasattr(self, atributo):
            return {'retorno': 1, 'mensagem': f"Atributo '{atributo}' não encontrado"}

        setattr(self, atributo, valor)
        return {'retorno': 0, 'mensagem': f"Atributo '{atributo}' atualizado com sucesso"}

    def desligar_funcionario(self, data: str = None):
        """
        Registra o desligamento do funcionário.

        Args:
            data (str, opcional): Data do desligamento. Se não informada, usa a data atual.

        Retorna:
            0 -> Funcionário desligado com sucesso
            1 -> Já desligado
        """
        if self.data_desligamento is not None:
            return {'retorno': 1, 'mensagem': 'Funcionário já desligado'}

        if data is None:
            data = date.today().strftime("%Y/%m/%d")

        self.data_desligamento = data
        return {'retorno': 0, 'mensagem': 'Funcionário desligado com sucesso'}

    def ativo(self):
        """
        Verifica se o funcionário está ativo (sem data de desligamento).

        Retorna:
            bool: True se o funcionário estiver ativo, False caso contrário.
        """
        return self.data_desligamento is None

def salvar_funcionarios():
    json_funcionarios = {}

    for codigo, f in _todos_funcionarios.items():
        json_funcionarios[str(codigo)] = f.to_json()

    with open(FUNCIONARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(json_funcionarios, f, ensure_ascii=False, indent=4)

def carregar_funcionarios():
    try:
        with open(FUNCIONARIOS_JSON, "r", encoding="utf-8") as f:
            json_funcionarios = json.load(f)
    except FileNotFoundError:
        return

    for codigo, f_json in json_funcionarios.items():
        _todos_funcionarios[int(codigo)] = Funcionario.from_json(f_json)


def adiciona_funcionario(nome: str, codigo: int, cargo: str, data_contratacao: str):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: adiciona_funcionario()

    B) OBJETIVO:
    Adicionar um novo funcionário ao registro global, validando a integridade e unicidade dos dados fornecidos, incluindo uma data de contratação manual.

    C) ACOPLAMENTO:
    PARÂMETRO 1: nome (string)
    Nome completo do funcionário.
    PARÂMETRO 2: codigo (inteiro)
    Código identificador único do funcionário.
    PARÂMETRO 3: cargo (string)
    Cargo a ser ocupado pelo funcionário.
    PARÂMETRO 4: data_contratacao (string)
    Data em que o funcionário foi contratado, no formato "YYYY/MM/DD".

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}
    
    RETORNO 2: DICIONÁRIO DE ERRO POR NOME INVÁLIDO:
    {"retorno": 2, "mensagem": "Nome obrigatório"}

    RETORNO 3: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 4, "mensagem": "Parâmetro <nome_do_parametro> errado"}

    RETORNO 4: DICIONÁRIO DE ERRO POR CÓDIGO DUPLICADO:
    {"retorno": 1, "mensagem": "Código já cadastrado"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Funcionário adicionado com sucesso"}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Todos os parâmetros são fornecidos e com os tipos corretos.
    - `nome` é uma string não vazia.
    - `codigo` é um inteiro único que não existe no registro.

    Assertiva(s) de saída:
    - O retorno é um dicionário indicando o resultado da operação.
    - Se bem-sucedida, um novo objeto `Funcionario` é criado e armazenado no registro.

    E) DESCRIÇÃO:
    1. Verifica se algum dos parâmetros obrigatórios é nulo.
    2. Valida se o `nome` é uma string válida e não vazia.
    3. Valida se os tipos dos parâmetros `codigo`, `cargo` e `data_contratacao` estão corretos.
    4. Verifica no dicionário `_todos_funcionarios` se o `codigo` já existe para evitar duplicatas.
    5. Se todas as validações passarem, cria uma nova instância da classe `Funcionario`.
    6. Adiciona o novo funcionário ao dicionário `_todos_funcionarios`, usando o código como chave.
    7. Retorna um dicionário de sucesso.

    F) HIPÓTESES:
    - Existe um dicionário global chamado `_todos_funcionarios` para o armazenamento.
    - A classe `Funcionario` está definida e disponível.

    G) RESTRIÇÕES:
    - O armazenamento de dados é em memória e não persiste.
    - A função não valida o formato da string `data_contratacao`, apenas seu tipo.
    """
    if nome is None or codigo is None or cargo is None or data_contratacao is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(nome, str) or not nome.strip():
        return {'retorno': 2, 'mensagem': 'Nome obrigatório'}
    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}
    if not isinstance(cargo, str):
        return {'retorno': 4, 'mensagem': 'Parâmetro cargo errado'}
    if not isinstance(data_contratacao, str):
        return {'retorno': 4, 'mensagem': 'Parâmetro data_contratacao errado'}

    if codigo in _todos_funcionarios:
        return {'retorno': 1, 'mensagem': 'Código já cadastrado'}

    _todos_funcionarios[codigo] = Funcionario(nome, codigo, cargo, data_contratacao)
    return {'retorno': 0, 'mensagem': 'Funcionário adicionado com sucesso'}


def novo_funcionario(nome: str, codigo: int, cargo: str):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: novo_funcionario()

    B) OBJETIVO:
    Criar e registrar um novo funcionário, utilizando a data atual do sistema como data de contratação de forma automática.

    C) ACOPLAMENTO:
    PARÂMETRO 1: nome (string)
    Nome completo do funcionário.
    PARÂMETRO 2: codigo (inteiro)
    Código identificador único do funcionário.
    PARÂMETRO 3: cargo (string)
    Cargo a ser ocupado pelo funcionário.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}
    
    RETORNO 2: DICIONÁRIO DE ERRO POR NOME INVÁLIDO:
    {"retorno": 2, "mensagem": "Nome obrigatório"}

    RETORNO 3: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 4, "mensagem": "Parâmetro <nome_do_parametro> errado"}

    RETORNO 4: DICIONÁRIO DE ERRO POR CÓDIGO DUPLICADO:
    {"retorno": 1, "mensagem": "Código já cadastrado"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Funcionário registrado com sucesso"}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Os parâmetros `nome`, `codigo` e `cargo` são fornecidos e com os tipos corretos.
    - `codigo` é um inteiro único que não existe no registro.

    Assertiva(s) de saída:
    - O retorno é um dicionário indicando o resultado.
    - Se bem-sucedida, um novo `Funcionario` é adicionado ao registro com a data de contratação do dia.

    E) DESCRIÇÃO:
    1. Valida os parâmetros `nome`, `codigo` e `cargo` contra valores nulos e tipos incorretos.
    2. Verifica a unicidade do `codigo` no dicionário `_todos_funcionarios`.
    3. Obtém a data atual do sistema.
    4. Formata a data atual para o padrão "YYYY/MM/DD".
    5. Cria uma nova instância da classe `Funcionario`, passando a data formatada.
    6. Adiciona o novo funcionário ao dicionário `_todos_funcionarios`.
    7. Retorna um dicionário de sucesso.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_funcionarios`.
    - A classe `Funcionario` está definida.
    - O módulo `datetime` está disponível para obter a data atual.

    G) RESTRIÇÕES:
    - O armazenamento é em memória.
    - A data de contratação é sempre a data em que a função é executada.
    """
    if nome is None or codigo is None or cargo is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(nome, str) or not nome.strip():
        return {'retorno': 2, 'mensagem': 'Nome obrigatório'}
    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}
    if not isinstance(cargo, str):
        return {'retorno': 4, 'mensagem': 'Parâmetro cargo errado'}

    if codigo in _todos_funcionarios:
        return {'retorno': 1, 'mensagem': 'Código já cadastrado'}

    hoje = date.today().strftime("%Y/%m/%d")
    _todos_funcionarios[codigo] = Funcionario(nome, codigo, cargo, data_contratacao=hoje)

    return {'retorno': 0, 'mensagem': 'Funcionário registrado com sucesso'}


def consultar_funcionario(codigo: int, incluir_inativos: bool = False):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: consultar_funcionario()

    B) OBJETIVO:
    Consultar e retornar os dados de um funcionário específico pelo seu código, com a opção de incluir funcionários inativos na busca.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (inteiro)
    Código do funcionário a ser consultado.
    PARÂMETRO 2: incluir_inativos (booleano, opcional)
    Se `True`, a busca retornará o funcionário mesmo que ele esteja desligado. Padrão é `False`.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}
    
    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 2, "mensagem": "Parâmetro código inválido"}

    RETORNO 3: DICIONÁRIO DE ERRO POR FUNCIONÁRIO NÃO ENCONTRADO:
    {"retorno": 1, "mensagem": "Funcionário não encontrado"}

    RETORNO 4: DICIONÁRIO DE ERRO POR FUNCIONÁRIO INATIVO:
    {"retorno": 1, "mensagem": "Funcionário inativo"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Funcionário encontrado", "dados": <objeto Funcionario>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é um número inteiro.
    - `incluir_inativos` é um booleano.

    Assertiva(s) de saída:
    - O retorno é um dicionário de status, contendo os dados do funcionário na chave "dados" em caso de sucesso.

    E) DESCRIÇÃO:
    1. Valida se o `codigo` é nulo ou se não é um inteiro.
    2. Busca o funcionário no dicionário `_todos_funcionarios` usando o `codigo`.
    3. Se não for encontrado, retorna erro.
    4. Se o parâmetro `incluir_inativos` for `False` e o funcionário encontrado possuir uma data de desligamento, retorna um erro indicando que o funcionário está inativo.
    5. Se as condições acima não forem atendidas, retorna sucesso com os dados do funcionário.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_funcionarios`.
    - Os objetos `Funcionario` possuem o atributo `data_desligamento`.

    G) RESTRIÇÕES:
    - Os casos de "não encontrado" e "encontrado mas inativo" retornam o mesmo código de erro (1), diferenciando-se apenas pela mensagem.
    """
    if codigo is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}
    if not isinstance(codigo, int):
        return {'retorno': 2, 'mensagem': 'Parâmetro código inválido'}

    funcionario = _todos_funcionarios.get(codigo)
    if not funcionario:
        return {'retorno': 1, 'mensagem': 'Funcionário não encontrado'}
    if not incluir_inativos and funcionario.data_desligamento is not None:
        return {'retorno': 1, 'mensagem': 'Funcionário inativo'}
    
    return {'retorno': 0, 'mensagem': 'Funcionário encontrado', 'dados': funcionario}


def consultar_funcionario_por_nome(nome: str, incluir_inativos: bool = False):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: consultar_funcionario_por_nome()

    B) OBJETIVO:
    Buscar e retornar uma lista de funcionários cujo nome contenha uma substring fornecida, de forma insensível a maiúsculas/minúsculas.

    C) ACOPLAMENTO:
    PARÂMETRO 1: nome (string)
    Nome ou parte do nome a ser buscado.
    PARÂMETRO 2: incluir_inativos (booleano, opcional)
    Se `True`, inclui funcionários desligados nos resultados. Padrão é `False`.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 2, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR NOME INVÁLIDO:
    {"retorno": 3, "mensagem": "Parâmetro nome inválido"}

    RETORNO 3: DICIONÁRIO SE NENHUM FUNCIONÁRIO FOR ENCONTRADO:
    {"retorno": 1, "mensagem": "Nenhum funcionário encontrado", "dados": []}

    RETORNO 4: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Funcionários encontrados", "dados": [<lista de objetos Funcionario>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `nome` é uma string não vazia.
    - `incluir_inativos` é um booleano.

    Assertiva(s) de saída:
    - O retorno é um dicionário contendo o status e uma lista de objetos `Funcionario` que satisfazem a busca.

    E) DESCRIÇÃO:
    1. Valida se o parâmetro `nome` é nulo ou inválido (vazio/espaços).
    2. Normaliza o texto de busca (remove espaços das pontas e converte para minúsculas).
    3. Itera sobre todos os funcionários no registro.
    4. Para cada funcionário, verifica se o texto de busca está contido em seu nome (também normalizado) e se seu status (ativo/inativo) corresponde ao filtro `incluir_inativos`.
    5. Adiciona os funcionários que correspondem aos critérios a uma lista de resultados.
    6. Se a lista de resultados estiver vazia, retorna um dicionário indicando que ninguém foi encontrado.
    7. Caso contrário, retorna um dicionário de sucesso com a lista de funcionários.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_funcionarios`.
    - Objetos `Funcionario` possuem um atributo `nome` e um método `ativo()`.

    G) RESTRIÇÕES:
    - A busca é sequencial e pode ter a performance degradada em bases de dados muito grandes.
    """
    if nome is None:
        return {'retorno': 2, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(nome, str) or not nome.strip():
        return {'retorno': 3, 'mensagem': 'Parâmetro nome inválido'}

    nome = nome.strip().lower()
    resultados = [
        f for f in _todos_funcionarios.values()
        if nome in f.nome.lower() and (incluir_inativos or f.ativo())
    ]

    if not resultados:
        return {'retorno': 1, 'mensagem': 'Nenhum funcionário encontrado', 'dados': []}

    return {'retorno': 0, 'mensagem': 'Funcionários encontrados', 'dados': resultados}

def listar_todos_funcionarios(incluir_inativos: bool = False):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: listar_todos_funcionarios()

    B) OBJETIVO:
    Retornar uma lista de todos os funcionários registrados no sistema, com a opção de filtrar por status (ativo/inativo).

    C) ACOPLAMENTO:
    PARÂMETRO 1: incluir_inativos (booleano, opcional)
    Se `True`, a lista retornada incluirá todos os funcionários. Se `False` (padrão), retornará apenas os ativos.

    RETORNO 1: DICIONÁRIO SE NÃO HOUVER FUNCIONÁRIOS:
    {"retorno": 1, "mensagem": "Nenhum funcionário registrado", "dados": []}

    RETORNO 2: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Funcionários listados com sucesso", "dados": [<lista de objetos Funcionario>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `incluir_inativos` é um valor booleano.

    Assertiva(s) de saída:
    - O retorno é um dicionário com uma chave "dados" contendo uma lista de objetos `Funcionario`. A lista pode estar vazia.

    E) DESCRIÇÃO:
    1. Filtra a lista de todos os funcionários (`_todos_funcionarios.values()`).
    2. O critério de filtro mantém um funcionário se `incluir_inativos` for `True` ou se o funcionário estiver ativo (verificado pelo método `ativo()`).
    3. Se a lista resultante do filtro estiver vazia, retorna um dicionário indicando que não há funcionários registrados que atendam ao critério.
    4. Caso contrário, retorna um dicionário de sucesso com a lista filtrada de funcionários.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_funcionarios`.
    - Objetos `Funcionario` possuem um método `ativo()` que retorna seu status.

    G) RESTRIÇÕES:
    - A função retorna uma lista completa de objetos, o que pode consumir memória se o número de funcionários for muito grande.
    """
    funcionarios = [
        f for f in _todos_funcionarios.values()
        if incluir_inativos or f.ativo()
    ]

    if not funcionarios:
        return {'retorno': 1, 'mensagem': 'Nenhum funcionário registrado', 'dados': []}

    return {'retorno': 0, 'mensagem': 'Funcionários listados com sucesso', 'dados': funcionarios}