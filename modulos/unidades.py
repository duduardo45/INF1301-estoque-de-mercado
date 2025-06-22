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
        self.nome = nome
        self.codigo = codigo
        self.estoque = estoque
        self.localizacao = localizacao
        self.funcionarios = funcionarios
        self.vendas = vendas
        self.ativo = ativo

    def to_json(self):
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
        if not hasattr(self, atributo):
            return {"retorno": 1, "mensagem": f"Atributo '{atributo}' não encontrado no produto."}

        setattr(self, atributo, valor)
        return {"retorno": 0, "mensagem": f"Atributo '{atributo}' atualizado com sucesso."}

def salvar_unidades():
    json_unidades = {}

    for codigo, unidade in _unidades.items():
        json_unidades[codigo] = unidade.to_json()

    with open(UNIDADES_JSON, "w", encoding="utf-8") as f:
        json.dump(json_unidades, f, ensure_ascii=False, indent=4)

def carregar_unidades():
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