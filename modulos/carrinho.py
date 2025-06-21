from datetime import date
from modulos.produto import Produto


__all__ = [
    "Carrinho",
]


class Carrinho:
    def __init__(self, id:int, data_hora:str=None, itens:dict=None, total:float=None, funcionario: 'Funcionario'=None):
        """
        Inicializa um objeto Carrinho com identificador, data, itens, total e funcionário associado.

        Args:
            id (int): identificador único do carrinho
            data_hora (str, opcional): data da compra no formato 'YYYY/MM/DD' fica como None até ser terminada
            itens (dict): dicionário de produtos e quantidades
            total (float, opcional): valor total da compra preenchido quando calculado
            funcionario (Funcionario, opcional): funcionário responsável pela venda

        Retorna:
            None
        """
        if itens is None:
            itens = []

        self.id = id
        self.data_hora = data_hora
        self.itens = itens  
        self.total = total
        self.funcionario = funcionario



    def adiciona_no_carrinho(self, produto: Produto, qtd: float):
        """
        Adiciona um produto ao carrinho com uma determinada quantidade.
        Caso o produto já exista, a quantidade é somada à existente.

        Args:
            produto (Produto): Produto a ser adicionado.
            qtd (float): Quantidade a ser adicionada.

        Retorna:
            0 -> Produto novo adicionado com sucesso  
            1 -> Produto existente, quantidade atualizada  
            2 -> Parâmetro inválido  
            3 -> Parâmetro nulo
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
        Remove uma quantidade de um produto do carrinho. Remove o produto completamente se a quantidade for igual ou superior à registrada.

        Args:
            produto (Produto): Produto a ser removido.
            quantidade (float): Quantidade a ser removida.

        Retorna:
            0 -> Produto removido com sucesso  
            1 -> Produto não encontrado no carrinho  
            2 -> Quantidade inválida  
            3 -> Parâmetro nulo
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
        Calcula o valor total dos itens no carrinho.

        Retorna:
            float: valor total da compra
        """
        total = 0
        for item in self.itens.keys():
            produto = item
            quantidade = self.itens[item]
            preco = produto.calcula_preco(quantidade)
            total += preco
        self.total = total
        return total
    


    def listar_itens(self, verbose: bool = False):
        """
        Lista todos os itens do carrinho. Pode mostrar nomes e preços detalhados se verbose=True.

        Args:
            verbose (bool): Se True, mostra detalhes dos produtos.

        Retorna:
            0 -> Itens listados com sucesso  
            1 -> Carrinho vazio
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
        Remove todos os produtos do carrinho, esvaziando-o completamente.

        Retorna:
            0 -> Carrinho esvaziado com sucesso
        """
        self.itens.clear()
        return {'retorno': 0, 'mensagem': 'Carrinho esvaziado com sucesso'}



    def finaliza_carrinho(self, funcionario: 'Funcionario'):
        """
        Finaliza o carrinho, registrando a data e o funcionário responsável.

        Args:
            funcionario (Funcionario): funcionário que realizou a venda

        Retorna:
            0 -> carrinho finalizado com sucesso
        """
        self.data_hora = date.today().strftime("%Y/%m/%d")
        self.funcionario = funcionario
        return {'retorno': 0, 'mensagem': 'Carrinho finalizado'}