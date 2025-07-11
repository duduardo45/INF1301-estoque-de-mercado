import json
from datetime import date, datetime
from .funcionario import Funcionario
from .estoque import Estoque
from .carrinho import Carrinho


__all__ = [
    "Localidade",
    "adiciona_Unidade",
    "remove_Unidade",
    "consulta_Unidade",
    "listar_Unidades",
    "atualiza_Unidade",
    "relatorio_Unidade",
    "salvar_unidades",
    "carregar_unidades"
]


UNIDADES_JSON = 'dados/unidades.json'

_unidades = {}

class Localidade:
    def __init__(self, nome: str, codigo: int, estoque: Estoque, localizacao: tuple[float, float], funcionarios: list[Funcionario], vendas:list[Carrinho], ativo:bool=True):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __init__()

        B) OBJETIVO:
        Inicializar (construir) uma nova instância do objeto Localidade, atribuindo todos os valores e objetos relacionados aos seus respectivos atributos.

        C) ACOPLAMENTO:
        PARÂMETRO 1: nome (string)
        Nome descritivo da unidade.

        PARÂMETRO 2: codigo (inteiro)
        Código identificador único para a unidade.

        PARÂMETRO 3: estoque (Estoque)
        Instância da classe Estoque associada a esta unidade.

        PARÂMETRO 4: localizacao (tupla[float, float])
        Tupla contendo a latitude e longitude da unidade.

        PARÂMETRO 5: funcionarios (lista[Funcionario])
        Lista contendo instâncias da classe Funcionario que trabalham na unidade.

        PARÂMETRO 6: vendas (lista[Carrinho])
        Lista contendo instâncias da classe Carrinho que representam as vendas da unidade.

        PARÂMETRO 7: ativo (booleano, opcional)
        Indica se a unidade está ativa. O valor padrão é True.

        RETORNO: Nenhum. Este é um método construtor.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - Os parâmetros são fornecidos com os tipos de dados corretos.
        - As instâncias de `Estoque`, `Funcionario` e `Carrinho` são objetos válidos.

        Assertiva(s) de saída:
        - Uma nova instância da classe `Localidade` é criada e retornada com seus atributos devidamente populados.

        E) DESCRIÇÃO:
        1. Este método é o construtor da classe `Localidade`.
        2. Ele recebe todos os dados necessários para representar uma unidade.
        3. Atribui cada parâmetro recebido a um atributo correspondente na instância (`self`). Por exemplo, `self.nome` recebe o valor do parâmetro `nome`.
        4. Define o estado inicial do objeto no momento de sua criação.

        F) HIPÓTESES:
        - As classes `Estoque`, `Funcionario` e `Carrinho` estão definidas e importadas corretamente.
        - A lógica que chama este construtor (como a função `adiciona_Unidade`) já validou os dados de entrada.

        G) RESTRIÇÕES:
        - O construtor não executa nenhuma lógica de validação interna; ele assume que os dados recebidos são válidos.
        """    
        self.nome = nome
        self.codigo = codigo
        self.estoque = estoque
        self.localizacao = localizacao
        self.funcionarios = funcionarios
        self.vendas = vendas
        self.ativo = ativo

    def to_json(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: to_json()

        B) OBJETIVO:
        Converter (serializar) a instância atual do objeto `Localidade` em um dicionário Python, que pode ser facilmente convertido para o formato JSON.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: DICIONÁRIO SERIALIZÁVEL
        Retorna um dicionário que representa o estado completo do objeto, incluindo seus objetos aninhados.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida da classe `Localidade`.
        - Os objetos aninhados (em `self.estoque`, `self.funcionarios`, `self.vendas`) devem ter seus próprios métodos `to_json()`.

        Assertiva(s) de saída:
        - O dicionário retornado contém apenas tipos de dados primitivos (strings, números, booleanos, listas, dicionários), tornando-o compatível com JSON.

        E) DESCRIÇÃO:
        1. Cria um dicionário contendo os atributos de tipo primitivo da unidade: `nome`, `codigo`, `localizacao` e `ativo`.
        2. Invoca o método `to_json()` do objeto `estoque` e armazena o resultado na chave "estoque".
        3. Utiliza uma list comprehension para iterar sobre a lista de `funcionarios`, chamando o método `to_json()` para cada objeto `Funcionario` e criando uma lista de dicionários.
        4. Realiza o mesmo processo para a lista de `vendas`, convertendo cada objeto `Carrinho` em um dicionário.
        5. Retorna o dicionário completo e estruturado.

        F) HIPÓTESES:
        - As classes `Estoque`, `Funcionario` e `Carrinho` possuem um método `to_json()` implementado que serializa corretamente seus respectivos objetos.

        G) RESTRIÇÕES:
        - A estrutura do dicionário de saída é fixa. Se novos atributos forem adicionados à classe, este método precisará ser atualizado para incluí-los na serialização.
        """    
        return {
            "nome": self.nome,
            "codigo": self.codigo,
            "localizacao": self.localizacao,
            "estoque": self.estoque.to_json(),
            "funcionarios": [f.to_json() for f in self.funcionarios],
            "vendas": [v.to_json() for v in self.vendas],
            "ativo": self.ativo
        }

    @classmethod    
    def from_json(cls, data: dict):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: from_json()

        B) OBJETIVO:
        Criar uma nova instância da classe `Localidade` a partir de um dicionário (geralmente obtido pela desserialização de um JSON), reconstruindo o objeto e seus componentes.

        C) ACOPLAMENTO:
        PARÂMETRO 1: data (dicionário)
        Um dicionário contendo todos os dados necessários para recriar uma instância de `Localidade`.

        RETORNO 1: INSTÂNCIA DE LOCALIDADE
        Retorna uma nova instância da classe `Localidade` (`cls`), populada com os dados fornecidos.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `data` é um dicionário que contém as chaves necessárias ("nome", "codigo", "estoque", "funcionarios", "vendas", "localizacao").
        - Os valores associados às chaves de objetos aninhados ("estoque", "funcionarios", "vendas") são representações de dicionário válidas para esses objetos.

        Assertiva(s) de saída:
        - Uma instância completa e funcional da classe `Localidade` é retornada.

        E) DESCRIÇÃO:
        1. Sendo um método de classe (`@classmethod`), ele opera sobre a classe (`cls`) em si, e não sobre uma instância.
        2. Reconstrói o objeto `Estoque` chamando o método de classe `Estoque.from_json()`.
        3. Reconstrói a lista de funcionários iterando sobre os dados em `data["funcionarios"]` e chamando `Funcionario.from_json()` para cada item.
        4. Reconstrói a lista de vendas de forma análoga, usando `Carrinho.from_json()`.
        5. Invoca o construtor da própria classe (`cls(...)`), passando os dados primitivos extraídos do dicionário (`nome`, `codigo`) e os objetos complexos recém-criados (`estoque`, `funcionarios`, `vendas`).
        6. Garante que `localizacao` seja uma tupla.
        7. Usa `data.get("ativo", True)` para obter o status, mantendo a compatibilidade com arquivos JSON mais antigos que possam não ter essa chave.
        8. Retorna a nova instância criada.

        F) HIPÓTESES:
        - As classes `Estoque`, `Funcionario` e `Carrinho` possuem um método de classe `from_json()` capaz de recriar suas instâncias a partir de um dicionário.
        - A estrutura e as chaves do dicionário `data` correspondem exatamente ao que o método espera.

        G) RESTRIÇÕES:
        - O método levantará uma exceção `KeyError` se uma chave obrigatória (como "nome" ou "estoque") estiver faltando no dicionário `data`.
        - Não há validação interna sobre os tipos ou valores dos dados dentro do dicionário `data`.
        """
        estoque = Estoque.from_json(data["estoque"])
        funcionarios = [Funcionario.from_json(f) for f in data["funcionarios"]]
        vendas = [Carrinho.from_json(v) for v in data["vendas"]]

        return cls(
            nome=data["nome"],
            codigo=data["codigo"],
            localizacao=tuple(data["localizacao"]),
            estoque=estoque,
            funcionarios=funcionarios,
            vendas=vendas,
            ativo=data.get("ativo", True)
        )

    def atualizar(self, atributo:str, valor):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: atualizar()

        B) OBJETIVO:
        Modificar de forma segura um único atributo da instância do objeto `Localidade`, verificando previamente a existência do atributo antes da alteração.

        C) ACOPLAMENTO:
        PARÂMETRO 1: atributo (string)
        O nome do atributo da instância que deve ser atualizado (ex: "nome").

        PARÂMETRO 2: valor (variado)
        O novo valor a ser atribuído ao atributo especificado.

        RETORNO 1: DICIONÁRIO DE ERRO POR ATRIBUTO NÃO ENCONTRADO:
        {"retorno": 1, "mensagem": "Atributo '<atributo>' não encontrado no produto."}

        RETORNO 2: DICIONÁRIO DE SUCESSO NA ATUALIZAÇÃO:
        {"retorno": 0, "mensagem": "Atributo '<atributo>' atualizado com sucesso."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida da classe `Localidade`.
        - `atributo` é uma string com o nome de um possível atributo da classe.
        - `valor` possui um tipo de dado compatível com o atributo a ser alterado.

        Assertiva(s) de saída:
        - O retorno é um dicionário contendo as chaves "retorno" (int) e "mensagem" (str).
        - Se a operação for bem-sucedida, o atributo correspondente da instância `self` é modificado para o novo `valor`.

        E) DESCRIÇÃO:
        1. Utiliza a função `hasattr(self, atributo)` para verificar se a instância atual (`self`) possui um atributo com o nome passado na string `atributo`.
        2. Se `hasattr` retornar `False`, a função conclui que o atributo não existe e retorna imediatamente um dicionário de erro com `retorno: 1`.
        3. Se `hasattr` retornar `True`, a função utiliza `setattr(self, atributo, valor)` para definir o novo `valor` para o `atributo` especificado na instância `self`.
        4. Após a atualização bem-sucedida, retorna um dicionário de sucesso com `retorno: 0`.

        F) HIPÓTESES:
        - A função é executada no contexto de uma instância de `Localidade`.

        G) RESTRIÇÕES:
        - A validação do tipo de dado do `valor` não é realizada por este método; espera-se que o código chamador forneça um valor de tipo apropriado para o atributo.
        - O método pode alterar qualquer atributo existente, público ou privado (por convenção), desde que o nome corresponda.
        """
        if not hasattr(self, atributo):
            return {"retorno": 1, "mensagem": f"Atributo '{atributo}' não encontrado no produto."}

        setattr(self, atributo, valor)
        return {"retorno": 0, "mensagem": f"Atributo '{atributo}' atualizado com sucesso."}

def salvar_unidades():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: salvar_unidades()

    B) OBJETIVO:
    Serializar e salvar o estado atual de todas as unidades cadastradas na memória para um arquivo de texto no formato JSON, garantindo a persistência dos dados entre as execuções do programa.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito é retornado. A função realiza uma operação de I/O, escrevendo em um arquivo.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O dicionário global `_unidades` está inicializado e contém instâncias de objetos da classe `Localidade`.

    Assertiva(s) de saída:
    - Um arquivo JSON, localizado no caminho definido pela constante `UNIDADES_JSON`, é criado ou sobrescrito.
    - O arquivo contém a representação JSON de todas as unidades presentes no dicionário `_unidades`.

    E) DESCRIÇÃO:
    1. Inicializa um dicionário temporário `json_unidades` para armazenar a versão serializável das unidades.
    2. Itera sobre cada par chave-valor (código, objeto unidade) no dicionário global `_unidades`.
    3. Para cada objeto de unidade, invoca o seu método `to_json()` para obter um dicionário que representa o estado do objeto.
    4. Adiciona este dicionário ao `json_unidades`, usando o código original da unidade como chave.
    5. Abre o arquivo de destino (definido em `UNIDADES_JSON`) em modo de escrita ("w") com codificação "utf-8".
    6. Utiliza a função `json.dump()` para escrever o dicionário `json_unidades` no arquivo, formatando-o com indentação para melhor legibilidade.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades` que serve como repositório em memória para os objetos `Localidade`.
    - A constante `UNIDADES_JSON` contém o caminho relativo válido para o arquivo de destino (ex: 'dados/unidades.json').
    - Cada objeto no dicionário `_unidades` possui um método `to_json()` que o serializa para um dicionário Python.
    - O diretório que conterá o arquivo JSON (`dados/`) existe e o programa tem permissão de escrita no local.

    G) RESTRIÇÕES:
    - A função sobrescreve completamente o arquivo `unidades.json` a cada chamada, sem criar backups.
    - Erros de I/O (ex: disco cheio, permissão negada) não são tratados internamente e podem interromper o programa.
    """
    json_unidades = {}

    for codigo, unidade in _unidades.items():
        json_unidades[codigo] = unidade.to_json()

    with open(UNIDADES_JSON, "w", encoding="utf-8") as f:
        json.dump(json_unidades, f, ensure_ascii=False, indent=4)

def carregar_unidades():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: carregar_unidades()

    B) OBJETIVO:
    Ler os dados de unidades de um arquivo JSON e carregá-los para a memória, populando o dicionário global `_unidades` com instâncias da classe `Localidade`.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito é retornado. A função modifica o estado do dicionário global `_unidades`.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O arquivo especificado pela constante `UNIDADES_JSON` deve existir no caminho esperado.
    - O conteúdo do arquivo deve ser um JSON válido que represente um dicionário de unidades.

    Assertiva(s) de saída:
    - O dicionário global `_unidades` é preenchido com as instâncias de `Localidade` recriadas a partir dos dados do arquivo JSON.
    - Se o arquivo não for encontrado, o dicionário `_unidades` permanece inalterado.

    E) DESCRIÇÃO:
    1. Utiliza um bloco `try-except` para lidar com a ausência do arquivo.
    2. Tenta abrir o arquivo definido em `UNIDADES_JSON` em modo de leitura ("r").
    3. Se o arquivo for aberto com sucesso, utiliza `json.load()` para desserializar seu conteúdo em um dicionário `json_unidades`.
    4. Caso o arquivo não exista (`FileNotFoundError`), a função termina sua execução silenciosamente.
    5. Itera sobre cada par chave-valor (código, dados da unidade) no dicionário `json_unidades` lido do arquivo.
    6. Para cada unidade, invoca o método de classe `Localidade.from_json()`, passando os dados da unidade para criar uma nova instância do objeto.
    7. Armazena a instância recém-criada no dicionário global `_unidades`, usando seu código (convertido para inteiro) como chave.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades` destinado a armazenar os objetos `Localidade`.
    - A constante `UNIDADES_JSON` aponta para o caminho correto do arquivo de dados.
    - A classe `Localidade` implementa um método de classe `from_json(data)` capaz de reconstruir uma instância a partir de um dicionário.
    - A estrutura de dados dentro do arquivo JSON é consistente com a esperada pelo método `Localidade.from_json()`.

    G) RESTRIÇÕES:
    - A função não realiza validação da integridade ou do esquema dos dados lidos do JSON.
    - Erros de formatação no JSON ou inconsistências de dados (ex: chaves faltando) podem levantar exceções (`JSONDecodeError`, `KeyError`) não tratadas, interrompendo o carregamento.
    """
    try:
        with open(UNIDADES_JSON, "r", encoding="utf-8") as f:
            json_unidades = json.load(f)
    except FileNotFoundError:
        return

    for codigo, unidade_json in json_unidades.items():
        _unidades[int(codigo)] = Localidade.from_json(unidade_json)


def adiciona_Unidade(codigo:int, nome:str, localizacao:tuple[float,float], estoque:Estoque=None, funcionarios:list[Funcionario]=None, vendas: list[Carrinho]=None):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: adiciona_Unidade()

    B) OBJETIVO:
    Cadastrar uma nova unidade no sistema, validando a integridade e unicidade dos dados fornecidos antes de efetuar o cadastro.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (inteiro)
    Identificador único da unidade.

    PARÂMETRO 2: nome (string)
    Nome da unidade.

    PARÂMETRO 3: localizacao (tupla)
    Tupla contendo a latitude e a longitude da unidade (ex: (-22.9068, -43.1729)).

    PARÂMETRO 4: estoque (Estoque, opcional)
    Objeto do tipo Estoque associado à unidade. Se não fornecido, um novo estoque vazio é criado.

    PARÂMETRO 5: funcionarios (lista[Funcionario], opcional)
    Lista de funcionários da unidade. Se não fornecida, uma lista vazia é criada.

    PARÂMETRO 6: vendas (lista[Carrinho], opcional)
    Lista de vendas da unidade. Se não fornecida, uma lista vazia é criada.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 4, "mensagem": "Parâmetro <nome_do_parametro> errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR CÓDIGO DUPLICADO:
    {"retorno": 1, "mensagem": "Código duplicado"}

    RETORNO 4: DICIONÁRIO DE ERRO POR NOME VAZIO:
    {"retorno": 2, "mensagem": "Nome obrigatório"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Unidade adicionada com sucesso"}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é um número inteiro.
    - `nome` é uma string não vazia.
    - `localizacao` é uma tupla com dois floats.

    Assertiva(s) de saída:
    - O retorno é um dicionário com as chaves "retorno" (inteiro) e "mensagem" (string), indicando o resultado da operação.

    E) DESCRIÇÃO:
    1. Valida se os parâmetros obrigatórios (`codigo`, `nome`, `localizacao`) não são nulos.
    2. Valida se os tipos de dados dos parâmetros estão corretos.
    3. Verifica no dicionário `_unidades` se o `codigo` fornecido já existe para evitar duplicatas.
    4. Garante que a string `nome` não está vazia.
    5. Se os parâmetros opcionais (`estoque`, `funcionarios`, `vendas`) não forem fornecidos, inicializa-os com valores padrão (vazios).
    6. Cria uma nova instância do objeto `Localidade` com os dados validados.
    7. Adiciona a nova unidade ao dicionário global `_unidades`, usando o `codigo` como chave.
    8. Retorna um dicionário indicando o sucesso da operação.

    F) HIPÓTESES:
    - Existe um dicionário global chamado `_unidades` que armazena as instâncias de `Localidade`.
    - As classes `Localidade`, `Estoque`, `Funcionario` e `Carrinho` estão definidas e disponíveis no escopo.

    G) RESTRIÇÕES:
    - O armazenamento das unidades é feito em memória no dicionário `_unidades` e não persiste após o término da execução do programa.
    """
    if codigo is None or nome is None or localizacao is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}
    if not isinstance(nome, str):
        return {'retorno': 4, 'mensagem': 'Parâmetro nome errado'}
    if not isinstance(localizacao, tuple) or len(localizacao) != 2 or not all(isinstance(p, float) for p in localizacao):
        return {'retorno': 4, 'mensagem': 'Parâmetro localizacao errado'}

    if codigo in _unidades:
        return {'retorno': 1, 'mensagem': 'Código duplicado'}

    if not nome:
        return {'retorno': 2, 'mensagem': 'Nome obrigatório'}

    if estoque is None:
        estoque = Estoque(codigo=f"EST{codigo}")
    if funcionarios is None:
        funcionarios = []
    if vendas is None:
        vendas = []

    nova_unidade = Localidade(
        nome=nome,
        codigo=codigo,
        estoque=estoque,
        localizacao=localizacao,
        funcionarios=funcionarios,
        vendas=vendas
    )

    _unidades[codigo] = nova_unidade
    return {'retorno': 0, 'mensagem': 'Unidade adicionada com sucesso'}

def remove_Unidade(codigo: int):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: remove_Unidade()

    B) OBJETIVO:
    Desativar uma unidade existente no sistema, marcando-a como inativa em vez de excluí-la fisicamente para preservar o histórico.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (inteiro)
    Identificador da unidade a ser desativada.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 4, "mensagem": "Parâmetro codigo errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR UNIDADE NÃO ENCONTRADA:
    {"retorno": 1, "mensagem": "Unidade não encontrada"}

    RETORNO 4: DICIONÁRIO DE ERRO POR UNIDADE JÁ REMOVIDA:
    {"retorno": 2, "mensagem": "Unidade já removida"}

    RETORNO 5: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Unidade marcada como removida"}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é um número inteiro.

    Assertiva(s) de saída:
    - O retorno é um dicionário com as chaves "retorno" (inteiro) e "mensagem" (string).
    - Se a operação for bem-sucedida, o atributo `ativo` do objeto `Localidade` correspondente é definido como `False`.

    E) DESCRIÇÃO:
    1. Valida se o parâmetro `codigo` não é nulo.
    2. Valida se o tipo do parâmetro `codigo` é inteiro.
    3. Busca a unidade no dicionário `_unidades` usando o `codigo`. Se não encontrar, retorna erro.
    4. Verifica se a unidade encontrada já está inativa (atributo `ativo` é `False`). Se estiver, retorna erro informando que já foi removida.
    5. Altera o atributo `ativo` da unidade para `False`.
    6. Retorna um dicionário indicando o sucesso da operação.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades` que armazena as instâncias de `Localidade`.
    - Os objetos `Localidade` possuem um atributo booleano chamado `ativo`.

    G) RESTRIÇÕES:
    - A função realiza uma "remoção lógica" (soft delete), não uma exclusão física dos dados. A unidade permanece no dicionário `_unidades`.
    """
    if codigo is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}

    unidade_obj = _unidades.get(codigo)
    if not unidade_obj:
        return {'retorno': 1, 'mensagem': 'Unidade não encontrada'}

    if not unidade_obj.ativo:
        return {'retorno': 2, 'mensagem': 'Unidade já removida'}

    unidade_obj.ativo = False
    return {'retorno': 0, 'mensagem': 'Unidade marcada como removida'}

def consulta_Unidade(codigo:int):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: consulta_Unidade()

    B) OBJETIVO:
    Buscar e retornar todas as informações de uma unidade específica, seja ela ativa ou inativa.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (inteiro)
    O código da unidade a ser consultada.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 4, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 3, "mensagem": "Parâmetro codigo errado"}

    RETORNO 3: DICIONÁRIO SE A UNIDADE NÃO EXISTIR:
    {"retorno": 2, "mensagem": "Unidade não encontrada", "dados": None}

    RETORNO 4: DICIONÁRIO SE A UNIDADE ENCONTRADA ESTIVER DESATIVADA:
    {"retorno": 1, "mensagem": "Unidade desativada", "dados": <objeto Localidade>}

    RETORNO 5: DICIONÁRIO SE A UNIDADE ATIVA FOR ENCONTRADA:
    {"retorno": 0, "mensagem": "Unidade encontrada com sucesso", "dados": <objeto Localidade>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é um número inteiro.

    Assertiva(s) de saída:
    - O retorno é um dicionário com "retorno" (int), "mensagem" (str) e, em caso de sucesso ou encontro de unidade inativa, a chave "dados" contendo o objeto `Localidade` ou `None`.

    E) DESCRIÇÃO:
    1. Valida se o parâmetro `codigo` não é nulo.
    2. Valida se o tipo do parâmetro `codigo` é inteiro.
    3. Busca a unidade no dicionário `_unidades` pelo `codigo`.
    4. Se a unidade não for encontrada, retorna um dicionário de erro correspondente.
    5. Se a unidade for encontrada, verifica seu status através do atributo `ativo`.
    6. Se a unidade estiver inativa, retorna um dicionário com status específico para desativada, mas ainda fornece os dados da unidade.
    7. Se a unidade estiver ativa, retorna um dicionário de sucesso com os dados da unidade.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades`.
    - Objetos no dicionário `_unidades` são da classe `Localidade` e possuem um atributo `ativo`.

    G) RESTRIÇÕES:
    - A função é apenas de leitura, não modifica o estado da unidade consultada.
    """
    if codigo is None:
        return {'retorno': 4, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(codigo, int):
        return {'retorno': 3, 'mensagem': 'Parâmetro codigo errado'}

    unidade = _unidades.get(codigo)

    if not unidade:
        return {'retorno': 2, 'mensagem': 'Unidade não encontrada', 'dados': None}

    if not unidade.ativo:
        return {'retorno': 1, 'mensagem': 'Unidade desativada', 'dados': unidade}

    return {'retorno': 0, 'mensagem': 'Unidade encontrada com sucesso', 'dados': unidade}

def listar_Unidades(incluir_inativas:bool=False):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: listar_Unidades()

    B) OBJETIVO:
    Fornecer uma lista com todas as unidades cadastradas, com a opção de incluir ou não as unidades inativas.

    C) ACOPLAMENTO:
    PARÂMETRO 1: incluir_inativas (booleano, opcional)
    Se `True`, a lista retornada incluirá unidades ativas e inativas. O padrão é `False`.

    RETORNO 1: DICIONÁRIO COM A LISTA DE UNIDADES (INCLUINDO INATIVAS):
    {"retorno": 0, "dados": [<lista de todos os objetos Localidade>]}

    RETORNO 2: DICIONÁRIO COM BASE DE DADOS VAZIA (SOMENTE ATIVAS):
    {"retorno": 1, "dados": []}

    RETORNO 3: DICIONÁRIO COM A LISTA DE UNIDADES ATIVAS:
    {"retorno": 0, "dados": [<lista de objetos Localidade ativos>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `incluir_inativas` é um valor booleano.

    Assertiva(s) de saída:
    - O retorno é um dicionário com as chaves "retorno" (int) e "dados" (lista de objetos `Localidade`).

    E) DESCRIÇÃO:
    1. Verifica o valor do parâmetro `incluir_inativas`.
    2. Se `True`, retorna uma lista com todos os valores do dicionário `_unidades`.
    3. Se `False` (padrão), filtra o dicionário `_unidades`, criando uma lista que contém apenas as unidades com o atributo `ativo` igual a `True`.
    4. Se a lista de unidades ativas resultante estiver vazia, retorna com o status 1.
    5. Retorna a lista de unidades (completa ou filtrada) dentro de um dicionário.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades`.
    - Os objetos no dicionário `_unidades` possuem um atributo booleano `ativo`.

    G) RESTRIÇÕES:
    - A função retorna uma cópia da lista de valores, portanto, modificações na lista retornada não afetam o dicionário `_unidades` original.
    """
    if incluir_inativas:
        return {'retorno': 0, 'dados': list(_unidades.values())}

    ativas = [unidade for unidade in _unidades.values() if getattr(unidade, 'ativo', False)]

    if not ativas:
        return {'retorno': 1, 'dados': []}

    return {'retorno': 0, 'dados': ativas}

def atualiza_Unidade(codigo: int, atributo: str, valor):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: atualiza_Unidade()

    B) OBJETIVO:
    Atualizar um atributo específico de uma unidade cadastrada, como nome ou localização.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (inteiro)
    Código da unidade a ser atualizada.

    PARÂMETRO 2: atributo (string)
    Nome do atributo do objeto Localidade a ser modificado (ex: "nome", "localizacao").

    PARÂMETRO 3: valor (variado)
    Novo valor a ser atribuído ao atributo.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 4, "mensagem": "Parâmetro <nome_do_parametro> errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR UNIDADE NÃO ENCONTRADA:
    {"retorno": 1, "mensagem": "Unidade não encontrada"}

    RETORNO 4: DICIONÁRIO DE ERRO POR UNIDADE DESATIVADA:
    {"retorno": 2, "mensagem": "Unidade desativada"}

    RETORNO 5: DICIONÁRIO DE ERRO POR ATRIBUTO INEXISTENTE:
    {"retorno": 5, "mensagem": "Atributo '<atributo>' não encontrado no produto."}

    RETORNO 6: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Atributo '<atributo>' atualizado com sucesso."}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é um inteiro.
    - `atributo` é uma string correspondente a um atributo da classe `Localidade`.
    - `valor` possui o tipo adequado para o `atributo` que será modificado.

    Assertiva(s) de saída:
    - O retorno é um dicionário informando o resultado da operação.
    - Se bem-sucedida, o atributo do objeto `Localidade` correspondente é alterado.

    E) DESCRIÇÃO:
    1. Valida se os parâmetros `codigo`, `atributo` e `valor` não são nulos.
    2. Valida os tipos dos parâmetros `codigo` e `atributo`.
    3. Busca a unidade no dicionário `_unidades` pelo `codigo`. Se não encontrar, retorna erro.
    4. Verifica se a unidade está ativa. Se estiver desativada, retorna erro.
    5. Chama o método `atualizar()` do objeto `Localidade`, passando o atributo e o valor.
    6. O método `atualizar()` verifica se o atributo existe antes de modificá-lo.
    7. Retorna o dicionário de resultado (sucesso ou erro de atributo não encontrado) fornecido pelo método `atualizar()`.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades`.
    - A classe `Localidade` possui um método `atualizar(atributo, valor)` que lida com a modificação de seus próprios atributos de forma segura.

    G) RESTRIÇÕES:
    - A função não permite a atualização de unidades marcadas como inativas.
    - A validação do tipo do `valor` é delegada ao código que usa a função ou à própria classe `Localidade`.
    """
    if codigo is None or atributo is None or valor is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}

    if not isinstance(atributo, str):
        return {'retorno': 4, 'mensagem': 'Parâmetro atributo errado'}

    unidade = _unidades.get(codigo)

    if not unidade:
        return {'retorno': 1, 'mensagem': 'Unidade não encontrada'}

    if not unidade.ativo:
        return {'retorno': 2, 'mensagem': 'Unidade desativada'}

    resultado = unidade.atualizar(atributo, valor)

    if resultado['retorno'] == 1:
        return {'retorno': 5, 'mensagem': resultado['mensagem']}

    return {'retorno': 0, 'mensagem': resultado['mensagem']}


def relatorio_Unidade(codigo:int, periodo:tuple[str,str], incluir_inativas:bool=False):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: relatorio_Unidade()

    B) OBJETIVO:
    Gerar um relatório detalhado de vendas e movimentações de funcionários para uma unidade específica dentro de um período de tempo.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (inteiro)
    O código da unidade para a qual o relatório será gerado.

    PARÂMETRO 2: periodo (tupla[string, string])
    Tupla com duas strings de data ("AAAA/MM/DD"), representando o início e o fim do período do relatório.

    PARÂMETRO 3: incluir_inativas (booleano, opcional)
    Se `True`, permite gerar relatório para uma unidade inativa. Padrão é `False`.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 4, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR TIPO DE PARÂMETRO INCORRETO:
    {"retorno": 5, "mensagem": "Parâmetro <nome_do_parametro> errado"}

    RETORNO 3: DICIONÁRIO DE ERRO POR FORMATO DE DATA INVÁLIDO:
    {"retorno": 5, "mensagem": "Formato de data inválido. Use AAAA/MM/DD."}

    RETORNO 4: DICIONÁRIO DE ERRO POR UNIDADE NÃO ENCONTRADA:
    {"retorno": 2, "mensagem": "Unidade não encontrada"}
    
    RETORNO 5: DICIONÁRIO DE ERRO POR UNIDADE DESATIVADA:
    {"retorno": 3, "mensagem": "Unidade desativada"}

    RETORNO 6: DICIONÁRIO DE ERRO POR PERÍODO INVÁLIDO:
    {"retorno": 3, "mensagem": "Período inválido"}

    RETORNO 7: DICIONÁRIO SEM DADOS NO PERÍODO:
    {"retorno": 1, "mensagem": "Sem dados"}

    RETORNO 8: DICIONÁRIO DE SUCESSO COM RELATÓRIO COMPLETO:
    {
        "retorno": 0,
        "mensagem": "Relatório completo gerado",
        "dados": {
            "codigo": <codigo>,
            "nome": <nome_unidade>,
            "movimentacoes_funcionarios": [<lista_movimentacoes>],
            "vendas_no_periodo": [<lista_vendas>]
        }
    }

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é um inteiro.
    - `periodo` é uma tupla de duas strings no formato "AAAA/MM/DD".
    - A data de início no período não é posterior à data de fim.

    Assertiva(s) de saída:
    - O retorno é um dicionário contendo o status da operação e, em caso de sucesso, os dados do relatório.

    E) DESCRIÇÃO:
    1. Valida se os parâmetros `codigo` e `periodo` não são nulos.
    2. Valida os tipos dos parâmetros.
    3. Busca a unidade pelo `codigo`. Se não existir, retorna erro.
    4. Se `incluir_inativas` for `False`, verifica se a unidade está ativa. Se não estiver, retorna erro.
    5. Tenta converter as strings de data do `periodo` para objetos `date`. Se o formato for inválido, retorna erro.
    6. Valida se a data de início não é futura e não é posterior à data de fim.
    7. Itera sobre as vendas da unidade, filtrando aquelas cuja data está dentro do período especificado.
    8. Itera sobre os funcionários, filtrando eventos de contratação e desligamento que ocorreram no período.
    9. Se nenhuma movimentação (vendas ou funcionários) for encontrada, retorna um relatório vazio com a mensagem "Sem dados".
    10. Monta o dicionário de relatório com os dados coletados e retorna-o.

    F) HIPÓTESES:
    - Existe um dicionário global `_unidades`.
    - Os objetos de unidade possuem listas `vendas` (com objetos `Carrinho`) e `funcionarios` (com objetos `Funcionario`).
    - Os objetos `Carrinho` e `Funcionario` possuem atributos de data ("data_hora", "data_contratacao", "data_desligamento") como strings no formato "AAAA/MM/DD".

    G) RESTRIÇÕES:
    - A precisão do relatório depende da consistência e do formato correto das strings de data armazenadas nos objetos.
    - O formato de data esperado é "AAAA/MM/DD".
    """
    if codigo is None or periodo is None:
        return {'retorno': 4, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(codigo, int):
        return {'retorno': 5, 'mensagem': 'Parâmetro codigo errado'}
    if not isinstance(periodo, tuple) or len(periodo) != 2 or not all(isinstance(p, str) for p in periodo):
        return {'retorno': 5, 'mensagem': 'Parâmetro periodo errado'}

    if codigo not in _unidades:
        return {'retorno': 2, 'mensagem': 'Unidade não encontrada'}

    unidade_obj = _unidades.get(codigo)

    if not incluir_inativas and not unidade_obj.ativo:
        return {'retorno': 3, 'mensagem': 'Unidade desativada'}

    try:
        data_inicio = datetime.strptime(periodo[0], "%Y/%m/%d").date()
        data_fim = datetime.strptime(periodo[1], "%Y/%m/%d").date()
    except ValueError:
        return {'retorno': 5, 'mensagem': 'Formato de data inválido. Use YYYY/MM/DD.'}

    if data_inicio > date.today() or data_inicio > data_fim:
        return {'retorno': 3, 'mensagem': 'Período inválido'}

    vendas_no_periodo = []
    renda_no_periodo = 0
    for venda in unidade_obj.vendas:
        if venda.data_hora is None:
            continue
        data_venda = datetime.strptime(venda.data_hora, "%Y/%m/%d").date()
        if data_inicio <= data_venda <= data_fim:
            if venda.total is not None:
                total = venda.total
            else:
                total = venda.calcula_total()
            vendas_no_periodo.append({
                'id_venda': venda.id,
                'data': venda.data_hora,
                'itens': [(item.nome, qtd) for item, qtd in venda.itens.items()],
                'total': total
            })
            renda_no_periodo += total

    movimentacoes_funcionarios = []
    for func in unidade_obj.funcionarios:
        eventos = []
        data_contrat = datetime.strptime(func.data_contratacao, "%Y/%m/%d").date()
        if data_inicio <= data_contrat <= data_fim:
            eventos.append({
                'evento': 'Contratação',
                'nome': func.nome,
                'codigo': func.codigo,
                'data': func.data_contratacao
            })
        if func.data_desligamento:
            data_deslig = datetime.strptime(func.data_desligamento, "%Y/%m/%d").date()
            if data_inicio <= data_deslig <= data_fim:
                eventos.append({
                    'evento': 'Desligamento',
                    'nome': func.nome,
                    'codigo': func.codigo,
                    'data': func.data_desligamento
                })
        movimentacoes_funcionarios.extend(eventos)

    if not vendas_no_periodo and not movimentacoes_funcionarios:
        return {'retorno': 1, 'mensagem': 'Sem dados'}

    resultado = {
        'retorno': 0,
        'mensagem':'Relatório completo gerado',
        'dados': {
            'codigo': codigo,
            'nome': unidade_obj.nome,
            'movimentacoes_funcionarios': movimentacoes_funcionarios,
            'vendas_no_periodo': vendas_no_periodo
        }
    }
    if incluir_inativas:
        resultado['ativo'] = unidade_obj.ativo
    return resultado
