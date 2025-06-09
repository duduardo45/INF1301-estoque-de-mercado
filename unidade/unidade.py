# adiciona_Unidade(id, nome, local, funcionários)
# remove_Unidade(id)
# listar_Unidades()
# consulta_estoque_Unidade(id)
# relatório_Unidade(id)

class Tabelas:
    pass

class Unidade:
    def __init__(self, nome: str, codigo: int, tem_estoque: bool, capacidade: dict, e_sede: bool, grupos: list, localizacao: tuple, tabelas: list) -> None:
        self.nome = nome
        self.codigo = codigo
        self.tem_estoque = tem_estoque
        self.capacidade = capacidade
        self.e_sede = e_sede
        self.grupos = grupos
        self.localização = localizacao
        self.tabelas = tabelas

    
class Grupo:
    def __init__(self, nome: str, descricao: str, unidades: list[Unidade], representante: Unidade) -> None:
        self.nome = nome
        self.descricao = descricao
        self.unidades = unidades
        self.representante = representante