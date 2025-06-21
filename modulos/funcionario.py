from datetime import date

_todos_funcionarios = {}

__all__ = [
    "Funcionario",
    "adiciona_funcionario",
    "novo_funcionario",
    "consulta_funcionario",
    "consultar_funcionario_por_nome",
    "listar_todos_funcionarios",
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



def adiciona_funcionario(nome: str, codigo: int, cargo: str, data_contratacao: str):
    """
    Adiciona um novo funcionário ao registro global.

    Args:
        nome (str): Nome do funcionário.
        codigo (int): Código único.
        cargo (str): Cargo a ser ocupado.
        data_contratacao (str): Data da contratação.

    Retorna:
        0 -> Sucesso  
        1 -> Código duplicado  
        2 -> Nome vazio  
        3 -> Parâmetro nulo  
        4 -> Parâmetro incorreto
    """
    if nome is None or codigo is None or cargo is None or data_contratacao is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    if not isinstance(nome, str) or not nome.strip():
        return {'retorno': 2, 'mensagem': 'Nome obrigatório'}
    if not isinstance(codigo, int):
        return {'retorno': 4, 'messagem': 'Parâmetro codigo errado'}
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
    Cria e registra um novo funcionário com a data de contratação atual.

    Args:
        nome (str): Nome completo do funcionário.
        codigo (int): Código identificador único.
        cargo (str): Cargo ocupado.

    Retorna:
        0 -> Sucesso  
        1 -> Código duplicado  
        2 -> Nome obrigatório  
        3 -> Parâmetro nulo  
        4 -> Parâmetro incorreto
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
    Consulta um funcionário pelo código.

    Args:
        codigo (int): código do funcionário a ser consultado
        incluir_inativos (bool): se True, inclui funcionários desligados na busca

    Retorna:
        0 -> funcionário encontrado (ativo ou inativo conforme parâmetro)  
        1 -> funcionário não encontrado  
        2 -> parâmetro inválido  
        3 -> parâmetro nulo
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
    Busca funcionários cujo nome contenha a substring informada (case-insensitive).

    Args:
        nome (str): Nome ou parte do nome a ser consultado.
        incluir_inativos (bool): Se True, inclui funcionários desligados na busca.

    Retorna:
        0 -> Funcionários encontrados  
        1 -> Nenhum funcionário encontrado  
        2 -> Parâmetro nulo  
        3 -> Parâmetro inválido
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
    Lista todos os funcionários registrados.

    Args:
        incluir_inativos (bool): Se True, inclui funcionários desligados.

    Retorna:
        0 -> Lista de funcionários  
        1 -> Nenhum funcionário registrado
    """
    funcionarios = [
        f for f in _todos_funcionarios.values()
        if incluir_inativos or f.ativo()
    ]

    if not funcionarios:
        return {'retorno': 1, 'mensagem': 'Nenhum funcionário registrado', 'dados': []}

    return {'retorno': 0, 'mensagem': 'Funcionários listados com sucesso', 'dados': funcionarios}
