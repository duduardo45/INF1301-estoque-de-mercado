import json
from datetime import date

_todos_funcionarios = {}

FUNCIONARIOS_JSON = 'dados/funcionarios.json'

__all__ = [
    "Funcionario",
    "adiciona_funcionario",
    "novo_funcionario",
    "consultar_funcionario",
    "consultar_funcionario_por_nome",
    "listar_todos_funcionarios",
    "salvar_funcionarios",
    "carregar_funcionarios"
]


class Funcionario:
    def __init__(self, nome, codigo, cargo, data_contratacao, data_desligamento=None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __init__()

        B) OBJETIVO:
        Inicializar uma nova instância da classe Funcionario, configurando seus atributos básicos com os dados fornecidos.

        C) ACOPLAMENTO:
        PARÂMETRO 1: nome (string)
        Nome completo do funcionário.
        PARÂMETRO 2: codigo (inteiro)
        Código identificador único do funcionário.
        PARÂMETRO 3: cargo (string)
        Cargo ocupado pelo funcionário.
        PARÂMETRO 4: data_contratacao (string)
        Data de contratação no formato 'YYYY/MM/DD'.
        PARÂMETRO 5: data_desligamento (string, opcional)
        Data de desligamento no formato 'YYYY/MM/DD'. Padrão é None.

        RETORNO: Nenhum (é um método construtor).

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - Os parâmetros são fornecidos com os tipos de dados corretos.

        Assertiva(s) de saída:
        - Uma nova instância da classe `Funcionario` é criada com seus atributos definidos.

        E) DESCRIÇÃO:
        1. Este método é o construtor da classe.
        2. Ele atribui cada parâmetro recebido a um atributo correspondente na instância (`self`), como `self.nome`, `self.codigo`, etc.
        3. Define o estado inicial do objeto no momento de sua criação.

        F) HIPÓTESES:
        - A validação da integridade e do formato dos dados (como o formato da data) é realizada antes da chamada a este construtor.

        G) RESTRIÇÕES:
        - O construtor não realiza nenhuma validação interna dos dados; ele assume que os valores recebidos são válidos.
        """
        self.nome = nome
        self.codigo = codigo
        self.cargo = cargo
        self.data_contratacao = data_contratacao
        self.data_desligamento = data_desligamento


    def __str__(self, resumo_vendas: tuple[int, float] = None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __str__()

        B) OBJETIVO:
        Fornecer uma representação textual e legível de um funcionário, incluindo seu status (ativo/inativo) e, opcionalmente, um resumo de seu desempenho de vendas.

        C) ACOPLAMENTO:
        PARÂMETRO 1: resumo_vendas (tupla, opcional)
        Tupla contendo o número de vendas e o valor total arrecadado (ex: (10, 1500.50)).

        RETORNO 1: Uma string formatada descrevendo o funcionário.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Funcionario`.
        - `resumo_vendas`, se fornecido, é uma tupla com um inteiro e um float.

        Assertiva(s) de saída:
        - Retorna uma string única com os detalhes do funcionário concatenados.

        E) DESCRIÇÃO:
        1. Inicia uma lista de strings com informações básicas do funcionário: nome, código, cargo e data de contratação.
        2. Verifica se o atributo `data_desligamento` possui um valor.
        3. Se sim, adiciona o status "Desativado" e a data de desligamento à lista.
        4. Se não, adiciona o status "Ativo".
        5. Verifica se o parâmetro `resumo_vendas` foi fornecido. Se sim, adiciona os dados de vendas e total arrecadado à lista.
        6. Concatena todos os itens da lista em uma única string, separados por " | ", e a retorna.

        F) HIPÓTESES:
        - Nenhuma.

        G) RESTRIÇÕES:
        - A formatação do valor monetário está fixa em duas casas decimais.
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
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: to_json()

        B) OBJETIVO:
        Converter (serializar) a instância do objeto `Funcionario` em um dicionário Python, para que possa ser facilmente salvo em formato JSON.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: DICIONÁRIO SERIALIZÁVEL
        Um dicionário contendo os atributos da instância como pares de chave-valor.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Funcionario`.

        Assertiva(s) de saída:
        - O dicionário retornado contém apenas tipos de dados primitivos, compatíveis com a serialização JSON.

        E) DESCRIÇÃO:
        1. Cria e retorna um dicionário.
        2. Mapeia cada atributo da instância (`self.nome`, `self.codigo`, etc.) para uma chave de mesmo nome no dicionário.

        F) HIPÓTESES:
        - Todos os atributos do objeto são de tipos diretamente serializáveis para JSON.

        G) RESTRIÇÕES:
        - Se novos atributos forem adicionados à classe, este método precisará ser atualizado para incluí-los na serialização.
        """        
        return {
            "nome": self.nome,
            "codigo": self.codigo,
            "cargo": self.cargo,
            "data_contratacao": self.data_contratacao,
            "data_desligamento": self.data_desligamento
        }

    @classmethod
    def from_json(cls, data: dict):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: from_json()

        B) OBJETIVO:
        Criar uma nova instância da classe `Funcionario` a partir de um dicionário (geralmente desserializado de um arquivo JSON).

        C) ACOPLAMENTO:
        PARÂMETRO 1: data (dicionário)
        Um dicionário contendo os dados do funcionário.

        RETORNO 1: Uma nova instância da classe `Funcionario`.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `data` é um dicionário que contém as chaves obrigatórias ("nome", "codigo", "cargo", "data_contratacao").

        Assertiva(s) de saída:
        - Uma instância completa e funcional da classe `Funcionario` é retornada.

        E) DESCRIÇÃO:
        1. Sendo um método de classe, opera sobre a classe (`cls`) em si.
        2. Extrai os valores para os atributos obrigatórios diretamente do dicionário `data`.
        3. Utiliza `data.get("data_desligamento", None)` para obter a data de desligamento, tratando o caso em que a chave pode não existir.
        4. Invoca o construtor da classe (`cls(...)`) com todos os valores extraídos para criar a nova instância.
        5. Retorna a instância criada.

        F) HIPÓTESES:
        - A estrutura do dicionário `data` é consistente com a esperada, contendo as chaves necessárias.

        G) RESTRIÇÕES:
        - Se uma chave obrigatória (ex: "nome") estiver ausente no dicionário, uma exceção `KeyError` será levantada.
        """    
        return cls(
            nome=data["nome"],
            codigo=data["codigo"],
            cargo=data["cargo"],
            data_contratacao=data["data_contratacao"],
            data_desligamento=data.get("data_desligamento", None)
        )

    def atualizar(self, atributo: str, valor):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: atualizar()

        B) OBJETIVO:
        Atualizar de forma segura um atributo específico de uma instância de funcionário, validando a existência do atributo antes da modificação.

        C) ACOPLAMENTO:
        PARÂMETRO 1: atributo (string)
        Nome do atributo a ser alterado.
        PARÂMETRO 2: valor (variado)
        Novo valor a ser atribuído ao atributo.

        RETORNO 1: DICIONÁRIO DE ERRO POR ATRIBUTO INEXISTENTE:
        {"retorno": 1, "mensagem": "Atributo '<atributo>' não encontrado"}
        RETORNO 2: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
        {"retorno": 2, "mensagem": "Parâmetro nulo"}
        RETORNO 3: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
        {"retorno": 3, "mensagem": "Parâmetro atributo errado"}
        RETORNO 4: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Atributo '<atributo>' atualizado com sucesso"}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Funcionario`.
        - `atributo` é uma string, e `valor` não é nulo.

        Assertiva(s) de saída:
        - O retorno é um dicionário indicando o resultado da operação.
        - Se bem-sucedida, o atributo da instância é modificado.

        E) DESCRIÇÃO:
        1. Valida se os parâmetros `atributo` e `valor` não são nulos.
        2. Valida se o `atributo` é do tipo string.
        3. Utiliza a função `hasattr(self, atributo)` para verificar se a instância possui o atributo especificado. Se não, retorna erro.
        4. Se o atributo existir, utiliza `setattr(self, atributo, valor)` para definir o novo valor.
        5. Retorna um dicionário de sucesso.

        F) HIPÓTESES:
        - A validação do tipo e do valor de `valor` é de responsabilidade do código que chama a função.

        G) RESTRIÇÕES:
        - Permite a modificação de qualquer atributo existente na classe, sem uma lista de permissão.
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
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: desligar_funcionario()

        B) OBJETIVO:
        Registrar a data de desligamento de um funcionário, efetivamente marcando-o como inativo no sistema.

        C) ACOPLAMENTO:
        PARÂMETRO 1: data (string, opcional)
        Data do desligamento no formato 'YYYY/MM/DD'. Se não informada, utiliza a data atual do sistema.

        RETORNO 1: DICIONÁRIO DE ERRO POR FUNCIONÁRIO JÁ DESLIGADO:
        {"retorno": 1, "mensagem": "Funcionário já desligado"}
        RETORNO 2: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Funcionário desligado com sucesso"}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância de um funcionário atualmente ativo (`data_desligamento` é `None`).
        - `data`, se fornecida, é uma string.

        Assertiva(s) de saída:
        - O atributo `data_desligamento` da instância é preenchido com uma string de data.

        E) DESCRIÇÃO:
        1. Verifica se o atributo `data_desligamento` já possui um valor. Se sim, retorna um erro informando que o funcionário já está desligado.
        2. Se o parâmetro `data` não for fornecido (`None`), a função obtém a data atual do sistema.
        3. Formata a data para uma string no padrão "YYYY/MM/DD".
        4. Atribui a string de data ao atributo `self.data_desligamento`.
        5. Retorna um dicionário de sucesso.

        F) HIPÓTESES:
        - O módulo `datetime` e sua classe `date` estão disponíveis para obter a data atual.

        G) RESTRIÇÕES:
        - A função não valida o formato da string de data recebida como parâmetro.
        """
        if self.data_desligamento is not None:
            return {'retorno': 1, 'mensagem': 'Funcionário já desligado'}

        if data is None:
            data = date.today().strftime("%Y/%m/%d")

        self.data_desligamento = data
        return {'retorno': 0, 'mensagem': 'Funcionário desligado com sucesso'}

    def ativo(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: ativo()

        B) OBJETIVO:
        Verificar de forma simples e direta se um funcionário está ativo no sistema.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: Booleano (`True` se o funcionário estiver ativo, `False` caso contrário).

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Funcionario`.

        Assertiva(s) de saída:
        - O retorno é estritamente `True` ou `False`.

        E) DESCRIÇÃO:
        1. A função avalia a condição `self.data_desligamento is None`.
        2. Um funcionário é considerado ativo se não possuir uma data de desligamento.
        3. Retorna o resultado booleano dessa avaliação.

        F) HIPÓTESES:
        - O atributo `data_desligamento` é rigorosamente mantido como `None` para funcionários ativos.

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        return self.data_desligamento is None

def salvar_funcionarios():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: salvar_funcionarios()

    B) OBJETIVO:
    Persistir em um arquivo JSON o estado atual de todos os funcionários armazenados na memória.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito. A função realiza uma operação de escrita em arquivo.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O dicionário global `_todos_funcionarios` contém instâncias da classe `Funcionario`.

    Assertiva(s) de saída:
    - O arquivo definido em `FUNCIONARIOS_JSON` é criado ou sobrescrito com os dados dos funcionários.

    E) DESCRIÇÃO:
    1. Inicializa um dicionário vazio `json_funcionarios`.
    2. Itera sobre cada par de código-funcionário no dicionário global `_todos_funcionarios`.
    3. Para cada objeto, invoca seu método `to_json()` e armazena o resultado no `json_funcionarios`, usando o código (convertido para string) como chave.
    4. Abre o arquivo de destino em modo de escrita ("w").
    5. Utiliza `json.dump()` para escrever o dicionário `json_funcionarios` no arquivo, com formatação indentada.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_funcionarios`.
    - A constante `FUNCIONARIOS_JSON` aponta para um caminho de arquivo válido e com permissão de escrita.
    - A classe `Funcionario` possui um método `to_json()`.

    G) RESTRIÇÕES:
    - A função sobrescreve o arquivo de destino sem aviso.
    - Possíveis erros de I/O não são tratados internamente.
    """
    json_funcionarios = {}

    for codigo, f in _todos_funcionarios.items():
        json_funcionarios[str(codigo)] = f.to_json()

    with open(FUNCIONARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(json_funcionarios, f, ensure_ascii=False, indent=4)

def carregar_funcionarios():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: carregar_funcionarios()

    B) OBJETIVO:
    Ler os dados de funcionários de um arquivo JSON e carregá-los para a memória, populando o dicionário global.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito. A função modifica o estado do dicionário global `_todos_funcionarios`.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O arquivo especificado pela constante `FUNCIONARIOS_JSON` deve existir e ser um JSON válido.

    Assertiva(s) de saída:
    - O dicionário global `_todos_funcionarios` é preenchido com instâncias de `Funcionario` recriadas a partir do arquivo.

    E) DESCRIÇÃO:
    1. Utiliza um bloco `try-except` para tratar o caso de o arquivo não existir (`FileNotFoundError`), retornando silenciosamente.
    2. Se o arquivo existir, ele é aberto e seu conteúdo JSON é carregado usando `json.load()`.
    3. Itera sobre cada par de código-dados no dicionário carregado.
    4. Para cada item, invoca o método de classe `Funcionario.from_json()` para criar uma nova instância.
    5. Armazena a instância no dicionário global `_todos_funcionarios`, convertendo a chave de string para inteiro.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_funcionarios`.
    - A constante `FUNCIONARIOS_JSON` aponta para o caminho correto.
    - A classe `Funcionario` implementa um método de classe `from_json()` funcional.

    G) RESTRIÇÕES:
    - A função não trata erros de formatação no JSON (`JSONDecodeError`) ou de chaves ausentes (`KeyError`).
    """
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
