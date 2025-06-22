from datetime import date
from .produto import Produto


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
            itens = {}

        self.id = id
        self.data_hora = data_hora
        self.itens = itens
        self.total = total
        self.funcionario = funcionario



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