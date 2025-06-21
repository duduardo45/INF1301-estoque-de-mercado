from datetime import date, datetime
from estruturas import Funcionario, Estoque, Carrinho


__all__ = [
    "adiciona_Unidade",
    "remove_Unidade",
    "consulta_Unidade",
    "listar_Unidades",
    "relatorio_Unidade"
]

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

    def atualizar(self, atributo:str, valor):
        if not hasattr(self, atributo):
            return {"retorno": 1, "mensagem": f"Atributo '{atributo}' não encontrado no produto."}

        setattr(self, atributo, valor)
        return {"retorno": 0, "mensagem": f"Atributo '{atributo}' atualizado com sucesso."}


def adiciona_Unidade(codigo:int, nome:str, localizacao:tuple[float,float], estoque:Estoque=None, funcionarios:list[Funcionario]=None, vendas: list[Carrinho]=None):
    """
    Cadastra uma nova unidade no sistema.

    Args:
        codigo (int): Identificador único da unidade.
        nome (str): Nome da unidade.
        localizacao (tuple): Tupla com a Latitude e Longitude da unidade.
        capacidade_max (int): Capacidade máxima de armazenamento.
        permissao (str): Categoria do usuário

    Returns:
        0 -> Dados válidos → sucesso  
        1 -> código já existente → erro “Código duplicado”  
        2 -> nome vazio → erro “Nome obrigatório”  
        3 -> Qualquer parâmetro nulo → erro “Parâmetro nulo”  
        4 -> Qualquer parâmetro obrigatório incorreto → erro “Parâmetro {param} errado” 
    """
    # 4: Parâmetro nulo 
    if codigo is None or nome is None or localizacao is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    # 5: Parâmetro incorreto 
    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}
    if not isinstance(nome, str):
        return {'retorno': 4, 'mensagem': 'Parâmetro nome errado'}
    if not isinstance(localizacao, tuple) or len(localizacao) != 2 or not all(isinstance(p, float) for p in localizacao):
        return {'retorno': 4, 'mensagem': 'Parâmetro localizacao errado'}
    
    # 1: Código duplicado 
    if codigo in _unidades:
        return {'retorno': 1, 'mensagem': 'Código duplicado'}
    
    # 2: Nome obrigatório 
    if not nome:
        return {'retorno': 2, 'mensagem': 'Nome obrigatório'}
    
    # caso não sejam especificados define como vazios
    if estoque is None:
        estoque = Estoque()
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
    # 0: Sucesso 
    return {'retorno': 0, 'mensagem': 'Unidade adicionada com sucesso'}

def remove_Unidade(codigo: int):
    """
    Marca uma unidade como removida (não a exclui permanentemente).

    Args:
        codigo (int): O código da unidade a ser removida.

    Returns:
        0 -> codigo existente → marca como removida  
        1 -> codigo inexistente → erro “Unidade não encontrada”
        2 -> codigo inexistente → erro “Unidade já removida”
        3 -> Qualquer parâmetro nulo → erro “Parâmetro nulo”  
        4 -> Qualquer parâmetro incorrêto → erro “Parâmetro {param} errado” 
    """
        
    # 3: Parâmetro nulo 
    if codigo is None:
        return {'retorno': 3, 'mensagem': 'Parâmetro nulo'}

    # 4: Parâmetro incorreto 
    if not isinstance(codigo, int):
        return {'retorno': 4, 'mensagem': 'Parâmetro codigo errado'}
    
    # 1: Unidade não encontrada 
    unidade_obj = _unidades.get(codigo)
    if not unidade_obj:
        return {'retorno': 1, 'mensagem': 'Unidade não encontrada'}
    
    #2: Unidade já removida
    if not unidade_obj.ativo:
        return {'retorno': 2, 'mensagem': 'Unidade já removida'}

    unidade_obj.ativo = False
    # 0: Sucesso 
    return {'retorno': 0, 'mensagem': 'Unidade marcada como removida'}

def consulta_Unidade(codigo:int):
    """
    Consulta os dados de uma unidade, retornando o objeto referente a unidade buscada
    
    Args:
        codigo (int): O código da unidade a ser consultada.
        
    Returns:
        0 -> codigo existente → objeto Unidade retornado  
        1 -> codigo existente de Unidade desativada → objeto Unidade retornado
        2 -> codigo inexistente → resultado vazio / nulo 
        3 -> Qualquer parâmetro incorreto → erro “Parâmetro {param} errado” 
        4 -> Qualquer parâmetro nulo → erro “Parâmetro nulo”  
    """
    # 2: Parâmetro nulo 
    if codigo is None:
        return {'retorno': 4, 'mensagem': 'Parâmetro nulo'}
        
    # 3: Parâmetro incorreto 
    if not isinstance(codigo, int):
        return {'retorno': 3, 'mensagem': 'Parâmetro codigo errado'}
    
    unidade = _unidades.get(codigo)

    if not unidade:
        return {'retorno': 2, 'mensagem': 'Unidade não encontrada', 'dados': None}
    
    if not unidade.ativo:
        return {'retorno': 1, 'mensagem': 'Unidade desativada', 'dados': unidade}
    # 0: Sucesso 
    return {'retorno': 0, 'mensagem': 'Unidade encontrada com sucesso', 'dados': unidade}

def listar_Unidades(incluir_inativas:bool=False):
    """
    Retorna a lista de unidades ativas ou uma lista vazia.
    
    Args:
        incluir_inativas (bool): Booleano para decidir se as unidades inativas devem ser incluidas na listagem.

    Returns:
    0 -> chama a função → lista  
    1 -> Base vazia → lista vazia 
    """

    if incluir_inativas:
        return {'retorno': 0, 'dados': list(_unidades.values())}

    ativas = [unidade for unidade in _unidades.values() if getattr(unidade, 'ativo', False)]
    
    # 1: Base vazia 
    if not ativas:
        return {'retorno': 1, 'dados': []}
        
    # 0: Sucesso 
    return {'retorno': 0, 'dados': ativas}

def atualiza_Unidade(codigo: int, atributo: str, valor):
    """
    Atualiza um atributo de uma unidade específica.

    Args:
        codigo (int): Código da unidade a ser atualizada.
        atributo (str): Nome do atributo a ser atualizado.
        valor: Novo valor para o atributo.

    Retorna:
        0 -> Unidade encontrada e atributo atualizado com sucesso  
        1 -> Unidade não encontrada  
        2 -> Unidade desativada  
        3 -> Parâmetro nulo  
        4 -> Parâmetro incorreto  
        5 -> Atributo não encontrado na unidade  
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
    Gera um relatório, retornando todas as informações daquela unidade.
    
    Args:
        codigo (int): O codigo da unidade a ser buscada
        periodo (tuple): lista com 2 elementos str, o primeiro sendo a data mais anterior, em formato YYYY/MM/DD e o segundo a data mais próxima, em formato YYYY/MM/DD
        
    Returns:
    0 -> dados válidos → relatório completo gerado  
    1 -> Unidade sem movimentações no período → relatório vazio, retorno “Sem dados”  
    2 -> codigo inexistente → erro “Unidade não encontrada”  
    3 -> Período futuro → erro “Período inválido”  
    4 -> Qualquer parâmetro nulo → erro “Parâmetro nulo”  
    5 -> Qualquer parâmetro incorrêto → erro “Parâmetro {param} errado”   
    """

    # 4 -> Qualquer parâmetro nulo → erro “Parâmetro nulo”
    if codigo is None or periodo is None:
        return {'retorno': 4, 'mensagem': 'Parâmetro nulo'}
        
    # 5 -> Qualquer parâmetro incorrêto → erro “Parâmetro {param} errado” 
    if not isinstance(codigo, int):
        return {'retorno': 5, 'mensagem': 'Parâmetro codigo errado'}
    if not isinstance(periodo, tuple) or len(periodo) != 2 or not all(isinstance(p, str) for p in periodo):
        return {'retorno': 5, 'mensagem': 'Parâmetro periodo errado'}

    # 2 -> codigo inexistente → erro “Unidade não encontrada” 
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

    # 3 -> Período futuro → erro “Período inválido”
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

    # 1 -> Unidade sem movimentações no período → relatório vazio
    if not vendas_no_periodo and not movimentacoes_funcionarios:
        return {'retorno': 1, 'mensagem': 'Sem dados'}

    # 0 -> dados válidos → relatório completo gerado
    resultado = {
        'retorno': 0, 
        'mensagem':'Relatório completo gerado',
        'dados': {
            'codigo': codigo, 
            'nome': unidade_obj.nome, # Acessando como atributo do objeto
            'movimentacoes_funcionarios': movimentacoes_funcionarios,
            'vendas_no_periodo': vendas_no_periodo
        }
    }
    if incluir_inativas:
        resultado['ativo'] = unidade_obj.ativo
    return resultado