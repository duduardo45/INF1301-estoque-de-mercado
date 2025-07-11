import json

ESTOQUES_JSON = 'dados/estoques.json'

_todos_estoques = {}


__all__ = [
    "Estoque",
    "registrar_estoque",
    "listar_todos_estoques",
    "salvar_estoques",
    "carregar_estoques"
]



class Estoque:

    def __init__(self, codigo: str, estoque: dict = None, exposicao: dict = None, capacidades: dict = None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __init__()

        B) OBJETIVO:
        Inicializar uma nova instância da classe Estoque, estabelecendo seu identificador único e suas estruturas de dados internas para controle de produtos.

        C) ACOPLAMENTO:
        PARÂMETRO 1: codigo (string)
        O identificador único para o estoque (ex: "EST-01").
        PARÂMETRO 2: estoque (dicionário, opcional)
        Dicionário para rastrear as quantidades de produtos no armazenamento interno.
        PARÂMETRO 3: exposicao (dicionário, opcional)
        Dicionário para rastrear as quantidades de produtos na área de exposição (prateleiras).
        PARÂMETRO 4: capacidades (dicionário, opcional)
        Dicionário para definir as capacidades máximas de cada produto no estoque e na exposição.

        RETORNO: Nenhum (é um método construtor).

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `codigo` é uma string.
        - Os demais parâmetros, se fornecidos, são dicionários.

        Assertiva(s) de saída:
        - Uma nova instância da classe `Estoque` é criada com seus atributos definidos, garantindo que os dicionários de controle nunca sejam nulos.

        E) DESCRIÇÃO:
        1. Este método é o construtor da classe.
        2. Atribui o `codigo` recebido ao atributo `self.codigo`.
        3. Para cada um dos parâmetros de dicionário (`estoque`, `exposicao`, `capacidades`), ele verifica se foi fornecido um valor.
        4. Se um parâmetro for `None`, ele inicializa o atributo correspondente como um dicionário vazio para evitar erros em operações futuras.
        5. Se um valor for fornecido, ele é atribuído diretamente.

        F) HIPÓTESES:
        - A validação da unicidade e do formato do `codigo` é feita pela função que chama este construtor (ex: `registrar_estoque`).

        G) RESTRIÇÕES:
        - O construtor não realiza validações profundas nos dicionários recebidos; ele assume que, se fornecidos, estão em um formato coerente.
        """

        if estoque is None:
            estoque = {}
        if exposicao is None:
            exposicao = {}
        if capacidades is None:
            capacidades = {}

        self.codigo = codigo
        self.estoque = estoque
        self.exposicao = exposicao
        self.capacidades = capacidades



    def __str__(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: __str__()

        B) OBJETIVO:
        Fornecer uma representação textual e legível do estado atual do estoque, incluindo totais de itens e listas de produtos em falta.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: Uma string formatada contendo um resumo do estado do estoque.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Estoque`.
        - As chaves dos dicionários `self.estoque` e `self.exposicao` são objetos `Produto` que possuem um atributo `codigo`.

        Assertiva(s) de saída:
        - Retorna uma string que pode ser de múltiplas linhas.

        E) DESCRIÇÃO:
        1. Calcula a soma total de unidades de produtos no estoque interno e na área de exposição.
        2. Identifica os produtos com quantidade zero (em falta) tanto no estoque interno quanto na exposição, coletando seus códigos.
        3. Monta uma string de descrição inicial com o código do estoque, o número total de produtos diferentes registrados e os totais de unidades.
        4. Se houver produtos em falta em qualquer um dos locais, anexa listas formatadas desses produtos à string de descrição.
        5. Retorna a string final, removendo quaisquer espaços em branco extras no final.

        F) HIPÓTESES:
        - A estrutura de dados interna do estoque está consistente (todos os produtos em `estoque` e `exposicao` também estão em `capacidades`).

        G) RESTRIÇÕES:
        - A representação dos produtos em falta é limitada aos seus códigos, não mostrando o nome completo.
        """
        total_estoque = sum(self.estoque.values())
        total_exposicao = sum(self.exposicao.values())

        faltas_estoque = [p.codigo for p, qtd in self.estoque.items() if qtd == 0]
        faltas_exposicao = [p.codigo for p, qtd in self.exposicao.items() if qtd == 0]

        descricao = f"Estoque: '{self.codigo}'\n"
        descricao += f"Produtos registrados: {len(self.capacidades)}\n"
        descricao += f"Total no estoque interno: {total_estoque}\n"
        descricao += f"Total na exposição: {total_exposicao}\n"

        if faltas_estoque:
            descricao += "Faltando no estoque interno: " + ", ".join(faltas_estoque) + "\n"
        if faltas_exposicao:
            descricao += "Faltando na exposição: " + ", ".join(faltas_exposicao) + "\n"

        return descricao.strip()
    


    def to_json(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: to_json()

        B) OBJETIVO:
        Serializar a instância do `Estoque` para um dicionário Python, convertendo os objetos `Produto` (usados como chaves) em seus códigos de string para torná-lo compatível com o formato JSON.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: Um dicionário com os dados do estoque, pronto para ser serializado para JSON.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `self` é uma instância válida de `Estoque`.
        - As chaves dos dicionários `estoque`, `exposicao` e `capacidades` são objetos `Produto` que possuem um atributo `codigo`.

        Assertiva(s) de saída:
        - Retorna um dicionário onde todas as chaves e valores são tipos primitivos (strings, números, dicionários).

        E) DESCRIÇÃO:
        1. Inicia a criação de um dicionário de resultado com o `codigo` do estoque.
        2. Utiliza "dictionary comprehensions" para transformar os dicionários internos:
           a. Para `estoque` e `exposicao`, o novo dicionário usará o `produto.codigo` como chave e a quantidade como valor.
           b. Para `capacidades`, o novo dicionário usará o `produto.codigo` como chave e um dicionário com as capacidades como valor.
        3. Retorna o dicionário completo e formatado para JSON.

        F) HIPÓTESES:
        - A estrutura de dados interna está consistente.

        G) RESTRIÇÕES:
        - A estrutura do dicionário de saída é fixa. Qualquer alteração na classe pode exigir uma atualização neste método.
        """        
        return {
            "codigo": self.codigo,
            "estoque": {p.codigo: qtd for p, qtd in self.estoque.items()},
            "exposicao": {p.codigo: qtd for p, qtd in self.exposicao.items()},
            "capacidades": {
                p.codigo: {"estoque": cap["estoque"], "exposicao": cap["exposicao"]}
                for p, cap in self.capacidades.items()
            }
        }

    @classmethod
    def from_json(cls, data: dict):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: from_json()

        B) OBJETIVO:
        Criar (desserializar) uma instância da classe `Estoque` a partir de um dicionário, recriando a estrutura interna com objetos `Produto` reais ao invés de apenas seus códigos.

        C) ACOPLAMENTO:
        PARÂMETRO 1: data (dicionário)
        Dicionário com os dados do estoque, onde os produtos são representados por seus códigos.

        RETORNO 1: Uma nova instância da classe `Estoque`.

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `data` é um dicionário com a estrutura gerada por `to_json`.
        - Os códigos de produto presentes em `data` devem corresponder a produtos existentes no sistema, que possam ser consultados.

        Assertiva(s) de saída:
        - Retorna uma instância de `Estoque` cujos dicionários internos usam objetos `Produto` como chaves.

        E) DESCRIÇÃO:
        1. Realiza uma importação local da função `consultar_produto_por_codigo` para evitar problemas de importação circular.
        2. Cria uma instância de `Estoque` preliminar, apenas com o código.
        3. Itera sobre os códigos de produto encontrados no dicionário `data["capacidades"]`.
        4. Para cada código, utiliza `consultar_produto_por_codigo` para obter o objeto `Produto` completo correspondente.
        5. Se um produto não for encontrado, lança uma exceção `ValueError`, interrompendo o carregamento.
        6. Usa o objeto `Produto` recuperado como a chave para popular os dicionários `capacidades`, `estoque` e `exposicao` da nova instância.
        7. Retorna a instância de `Estoque` completamente populada.

        F) HIPÓTESES:
        - O módulo de produtos e seus dados já foram carregados no sistema antes da execução desta função.
        - A função `consultar_produto_por_codigo` está disponível e funciona como esperado.

        G) RESTRIÇÕES:
        - O processo de carregamento de estoques depende criticamente do carregamento prévio dos produtos.
        - Lança uma exceção não tratada se um código de produto no JSON não existir, o que pode interromper a inicialização do sistema.
        """    
        from modulos.produto import consultar_produto_por_codigo

        estoque = cls(codigo=data["codigo"])
        for codigo in data["capacidades"]:
            res = consultar_produto_por_codigo(codigo)
            if res["retorno"] != 0:
                raise ValueError(f"Produto {codigo} não encontrado. Inicialize antes de carregar o estoque.")
            produto = res["dados"]
            estoque.capacidades[produto] = data["capacidades"][codigo]
            estoque.estoque[produto] = data["estoque"].get(codigo, 0)
            estoque.exposicao[produto] = data["exposicao"].get(codigo, 0)

        return estoque



    def registrar_produto(self, produto, capacidade_estoque, capacidade_exposicao):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: registrar_produto() (Método de Estoque)

        B) OBJETIVO:
        Registrar um novo produto dentro da instância do estoque, definindo suas capacidades máximas de armazenamento interno e de exposição.

        C) ACOPLAMENTO:
        PARÂMETRO 1: produto (Produto)
        O objeto do produto a ser registrado.
        PARÂMETRO 2: capacidade_estoque (inteiro)
        Capacidade máxima de unidades do produto no estoque interno.
        PARÂMETRO 3: capacidade_exposicao (inteiro)
        Capacidade máxima de unidades do produto na área de exposição.

        RETORNO 1: DICIONÁRIO SE O PRODUTO JÁ ESTIVER REGISTRADO:
        {"retorno": 1, "mensagem": "Produto já está registrado."}

        RETORNO 2: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Produto registrado com sucesso."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `produto` é um objeto com um atributo `codigo`.
        - `capacidade_estoque` e `capacidade_exposicao` são números inteiros.
        - O código do produto não deve existir previamente no dicionário `self.capacidades`.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - Se bem-sucedido, o produto é adicionado aos dicionários `estoque`, `exposicao` e `capacidades` da instância, com quantidades iniciais zeradas.

        E) DESCRIÇÃO:
        1. Extrai o código do objeto `produto`.
        2. Verifica se o código já existe nas `capacidades` do estoque. Se sim, retorna erro.
        3. Inicializa a quantidade do produto como 0 nos dicionários `estoque` e `exposicao`.
        4. Armazena as capacidades de estoque e exposição no dicionário `capacidades`.
        5. Retorna uma mensagem de sucesso.

        F) HIPÓTESES:
        - O objeto `produto` possui um atributo `.codigo` que é uma string.
        - A instância da classe `Estoque` possui os dicionários `estoque`, `exposicao` e `capacidades`.

        G) RESTRIÇÕES:
        - A função modifica o estado interno do objeto `Estoque`.
        """
        if produto in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto já está registrado."}

        self.estoque[produto] = 0
        self.exposicao[produto] = 0
        self.capacidades[produto] = {
            "estoque": capacidade_estoque,
            "exposicao": capacidade_exposicao
        }
        return {"retorno": 0, "mensagem": "Produto registrado com sucesso."}



    def remover_produto(self, produto):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: remover_produto() (Método de Estoque)

        B) OBJETIVO:
        Remover completamente um produto dos registros do estoque, contanto que não haja mais unidades físicas (no estoque interno ou em exposição).

        C) ACOPLAMENTO:
        PARÂMETRO 1: codigo (string)
        Código do produto a ser removido.

        RETORNO 1: DICIONÁRIO SE O PRODUTO NÃO FOR ENCONTRADO:
        {"retorno": 1, "mensagem": "Produto não encontrado."}

        RETORNO 2: DICIONÁRIO SE AINDA HOUVER QUANTIDADES DO PRODUTO:
        {"retorno": 2, "mensagem": "Produto ainda possui quantidades em estoque ou exposição."}

        RETORNO 3: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Produto removido com sucesso."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `codigo` é uma string que corresponde a um produto registrado.
        - A quantidade do produto correspondente deve ser 0 tanto no estoque interno quanto na exposição.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - Se bem-sucedido, todas as entradas referentes ao `codigo` são removidas dos dicionários internos (`estoque`, `exposicao`, `capacidades`).

        E) DESCRIÇÃO:
        1. Verifica se o `codigo` do produto está registrado nas `capacidades`. Se não estiver, retorna erro.
        2. Verifica se a quantidade em `estoque` ou `exposicao` para o produto é maior que zero. Se for, retorna erro.
        3. Se as quantidades estiverem zeradas, remove o produto de cada um dos três dicionários de controle.
        4. Retorna uma mensagem de sucesso.

        F) HIPÓTESES:
        - A estrutura de dados do estoque está consistente.

        G) RESTRIÇÕES:
        - A remoção é bloqueada para evitar a perda de registros de produtos que ainda existem fisicamente.
        """
        if produto not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não encontrado."}

        if self.estoque.get(produto, 0) > 0 or self.exposicao.get(produto, 0) > 0:
            return {"retorno": 2, "mensagem": "Produto ainda possui quantidades em estoque ou exposição."}

        self.estoque.pop(produto, None)
        self.exposicao.pop(produto, None)
        self.capacidades.pop(produto, None)

        return {"retorno": 0, "mensagem": "Produto removido com sucesso."}



    def listar_em_falta(self, tipo='ambos'):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: listar_em_falta() (Método de Estoque)

        B) OBJETIVO:
        Gerar uma lista de códigos de produtos que estão com quantidade zerada, seja no estoque interno, na exposição ou em qualquer um dos dois.

        C) ACOPLAMENTO:
        PARÂMETRO 1: tipo (string, opcional)
        Define o escopo da busca: 'estoque', 'exposicao' ou 'ambos' (padrão).

        RETORNO 1: DICIONÁRIO DE ERRO POR TIPO INVÁLIDO:
        {"retorno": 2, "mensagem": "Tipo inválido. Use 'estoque', 'exposicao' ou 'ambos'."}

        RETORNO 2: DICIONÁRIO DE SUCESSO COM A LISTA:
        {"retorno": 0, "mensagem": "Listagem de faltas realizada com sucesso.", "dados": [<lista de codigos>]}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `tipo` é uma das três strings permitidas: 'estoque', 'exposicao', 'ambos'.

        Assertiva(s) de saída:
        - O retorno é um dicionário contendo o status e, na chave 'dados', uma lista de strings com os códigos dos produtos em falta.

        E) DESCRIÇÃO:
        1. Valida se o parâmetro `tipo` é um dos valores permitidos.
        2. Itera por todos os produtos registrados (`self.capacidades`).
        3. Para cada produto, verifica se sua quantidade é zero no local especificado pelo `tipo`.
        4. Adiciona o código do produto à lista de resultados se a condição for atendida.
        5. Retorna a lista de produtos em falta dentro de um dicionário de sucesso.

        F) HIPÓTESES:
        - Para cada produto em `capacidades`, existe uma entrada correspondente em `estoque` e `exposicao`.

        G) RESTRIÇÕES:
        - A função não diferencia produtos que nunca tiveram entrada daqueles que tiveram e acabaram.
        """
        faltando = []

        if tipo not in ('estoque', 'exposicao', 'ambos'):
            return {"retorno": 2, "mensagem": "Tipo inválido. Use 'estoque', 'exposicao' ou 'ambos'."}

        for produto in self.capacidades:
            em_estoque = self.estoque[produto] == 0
            em_exposicao = self.exposicao[produto] == 0

            if tipo == 'estoque' and em_estoque:
                faltando.append(produto.codigo)
            elif tipo == 'exposicao' and em_exposicao:
                faltando.append(produto.codigo)
            elif tipo == 'ambos' and (em_estoque or em_exposicao):
                faltando.append(produto.codigo)

        return {
            "retorno": 0,
            "mensagem": "Listagem de faltas realizada com sucesso.",
            "dados": faltando
        }



    def percentual_ocupado(self, produto):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: percentual_ocupado() (Método de Estoque)

        B) OBJETIVO:
        Calcular e retornar os percentuais de ocupação de um produto, tanto no estoque interno quanto na exposição, em relação às suas capacidades máximas.

        C) ACOPLAMENTO:
        PARÂMETRO 1: codigo (string)
        Código do produto a ser verificado.

        RETORNO 1: DICIONÁRIO SE O PRODUTO NÃO ESTIVER CADASTRADO:
        {"retorno": 1, "mensagem": "Produto não cadastrado."}

        RETORNO 2: DICIONÁRIO DE SUCESSO COM OS PERCENTUAIS:
        {"retorno": 0, "mensagem": "Percentuais calculados com sucesso.", "dados": {"estoque": <float>, "exposicao": <float>}}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `codigo` é uma string que corresponde a um produto registrado no estoque.

        Assertiva(s) de saída:
        - O retorno é um dicionário contendo o status e, na chave 'dados', um outro dicionário com os percentuais de ocupação.

        E) DESCRIÇÃO:
        1. Verifica se o `codigo` do produto está registrado nas `capacidades`. Se não, retorna erro.
        2. Obtém as capacidades de estoque e exposição para o produto.
        3. Calcula o percentual de ocupação para o estoque interno (quantidade / capacidade).
        4. Calcula o percentual de ocupação para a exposição.
        5. Retorna um dicionário de sucesso contendo os dois percentuais arredondados.

        F) HIPÓTESES:
        - As capacidades armazenadas são maiores que zero para evitar divisão por zero (a função trata o caso de capacidade ser 0).

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        if produto not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        cap = self.capacidades[produto]
        ocup_estoque = (self.estoque[produto] / cap["estoque"]) * 100 if cap["estoque"] else 0
        ocup_exposicao = (self.exposicao[produto] / cap["exposicao"]) * 100 if cap["exposicao"] else 0

        return {
            "retorno": 0,
            "mensagem": "Percentuais calculados com sucesso.",
            "dados": {
                "estoque": round(ocup_estoque, 2),
                "exposicao": round(ocup_exposicao, 2)
            }
        }



    def listar_produtos(self, detalhado=False):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: listar_produtos() (Método de Estoque)

        B) OBJETIVO:
        Fornecer uma lista de todos os produtos registrados neste estoque, de forma simples (só códigos) ou detalhada (com quantidades e capacidades).

        C) ACOPLAMENTO:
        PARÂMETRO 1: detalhado (booleano, opcional)
        Se `True`, retorna uma lista de dicionários com todos os detalhes. Se `False` (padrão), retorna uma lista de strings com os códigos.

        RETORNO 1: DICIONÁRIO DE SUCESSO COM A LISTA DE PRODUTOS:
        {"retorno": 0, "mensagem": "Listagem realizada com sucesso.", "dados": [<lista>]}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `detalhado` é um valor booleano.

        Assertiva(s) de saída:
        - O retorno é um dicionário contendo, na chave 'dados', uma lista de strings ou uma lista de dicionários, dependendo do parâmetro `detalhado`.

        E) DESCRIÇÃO:
        1. Itera sobre todos os códigos de produtos registrados em `self.capacidades`.
        2. Se `detalhado` for `True`, monta um dicionário com todos os dados do produto (código, quantidades, capacidades) e o adiciona à lista de resultados.
        3. Se `detalhado` for `False`, adiciona apenas o código do produto à lista de resultados.
        4. Retorna um dicionário de sucesso com a lista montada.

        F) HIPÓTESES:
        - A estrutura de dados do estoque está consistente.

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        produtos = []
        for produto in self.capacidades:
            if detalhado:
                produtos.append({
                    "codigo": produto.codigo,
                    "estoque": self.estoque[produto],
                    "exposicao": self.exposicao[produto],
                    "capacidade_estoque": self.capacidades[produto]["estoque"],
                    "capacidade_exposicao": self.capacidades[produto]["exposicao"]
                })
            else:
                produtos.append(produto.codigo)

        return {
            "retorno": 0,
            "mensagem": "Listagem realizada com sucesso.",
            "dados": produtos
        }



    def atualizar_capacidades(self, produto, capacidade_estoque=None, capacidade_exposicao=None):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: atualizar_capacidades() (Método de Estoque)

        B) OBJETIVO:
        Modificar a capacidade máxima de armazenamento (interno e/ou exposição) para um produto já registrado.

        C) ACOPLAMENTO:
        PARÂMETRO 1: codigo (string)
        Código do produto a ter suas capacidades atualizadas.
        PARÂMETRO 2: capacidade_estoque (inteiro, opcional)
        Novo valor para a capacidade do estoque interno.
        PARÂMETRO 3: capacidade_exposicao (inteiro, opcional)
        Novo valor para a capacidade da exposição.

        RETORNO 1: DICIONÁRIO SE O PRODUTO NÃO ESTIVER CADASTRADO:
        {"retorno": 1, "mensagem": "Produto não cadastrado no estoque."}

        RETORNO 2: DICIONÁRIO SE NENHUMA CAPACIDADE FOR FORNECIDA:
        {"retorno": 2, "mensagem": "Por favor especifique alguma capacidade a atualizar."}

        RETORNO 3: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Capacidades atualizadas com sucesso."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `codigo` corresponde a um produto existente.
        - Pelo menos um dos parâmetros `capacidade_estoque` ou `capacidade_exposicao` deve ser fornecido.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - Se bem-sucedido, os valores de capacidade no dicionário `self.capacidades` são atualizados.

        E) DESCRIÇÃO:
        1. Verifica se o `codigo` existe no registro de `capacidades`. Se não, retorna erro.
        2. Verifica se ambos os parâmetros de capacidade são nulos. Se sim, retorna erro.
        3. Se `capacidade_estoque` foi fornecida, atualiza o valor correspondente.
        4. Se `capacidade_exposicao` foi fornecida, atualiza o valor correspondente.
        5. Retorna uma mensagem de sucesso.

        F) HIPÓTESES:
        - Nenhuma.

        G) RESTRIÇÕES:
        - A função permite que a nova capacidade seja menor que a quantidade atual de produtos, o que pode criar uma inconsistência a ser tratada por outra função (`verificar_consistencia`).
        """
        if produto not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado no estoque."}

        if capacidade_estoque is None and capacidade_exposicao is None:
            return {"retorno": 2, "mensagem": "Por favor especifique alguma capacidade a atualizar."}

        if capacidade_estoque is not None:
            self.capacidades[produto]["estoque"] = capacidade_estoque

        if capacidade_exposicao is not None:
            self.capacidades[produto]["exposicao"] = capacidade_exposicao

        return {"retorno": 0, "mensagem": "Capacidades atualizadas com sucesso."}



    def adicionar_produto(self, produto, quantidade, destino='estoque'):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: adicionar_produto() (Método de Estoque)

        B) OBJETIVO:
        Aumentar a quantidade de um produto, seja no estoque interno ou na exposição, respeitando os limites de capacidade.

        C) ACOPLAMENTO:
        PARÂMETRO 1: produto (Produto)
        O objeto do produto a ser adicionado.
        PARÂMETRO 2: quantidade (inteiro)
        Número de unidades a serem adicionadas.
        PARÂMETRO 3: destino (string, opcional)
        Local onde adicionar: 'estoque' (padrão) ou 'exposicao'.

        RETORNO 1: DICIONÁRIO SE O PRODUTO NÃO ESTIVER CADASTRADO:
        {"retorno": 1, "mensagem": "Produto não cadastrado."}

        RETORNO 2: DICIONÁRIO SE A CAPACIDADE DO ESTOQUE FOR EXCEDIDA:
        {"retorno": 2, "mensagem": "Capacidade de estoque excedida para o produto."}

        RETORNO 3: DICIONÁRIO SE A CAPACIDADE DA EXPOSIÇÃO FOR EXCEDIDA:
        {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}

        RETORNO 4: DICIONÁRIO SE O DESTINO FOR INVÁLIDO:
        {"retorno": 4, "mensagem": "Destino inválido. Use 'estoque' ou 'exposicao'."}

        RETORNO 5: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Produto adicionado ao estoque interno."} ou {"retorno": 0, "mensagem": "Produto adicionado à exposição."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `produto` está registrado no estoque.
        - `quantidade` é um inteiro positivo.
        - `destino` é 'estoque' ou 'exposicao'.
        - A soma da quantidade atual com a nova quantidade não excede a capacidade do destino.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - Se bem-sucedido, a quantidade no dicionário do `destino` é incrementada.

        E) DESCRIÇÃO:
        1. Extrai o código do objeto `produto` e verifica se ele está registrado.
        2. Se o `destino` for 'estoque':
           a. Verifica se a adição da `quantidade` excede a capacidade do estoque. Se sim, retorna erro.
           b. Incrementa a quantidade em `self.estoque` e retorna sucesso.
        3. Se o `destino` for 'exposicao':
           a. Verifica se a adição da `quantidade` excede a capacidade da exposição. Se sim, retorna erro.
           b. Incrementa a quantidade em `self.exposicao` e retorna sucesso.
        4. Se o `destino` for inválido, retorna erro.

        F) HIPÓTESES:
        - Nenhuma.

        G) RESTRIÇÕES:
        - A função não permite adicionar produtos além da capacidade definida.
        """
        if produto not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        if produto not in self.estoque:
            self.estoque[produto] = 0
        if produto not in self.exposicao:
            self.exposicao[produto] = 0

        if destino == 'estoque':
            atual = self.estoque[produto]
            limite = self.capacidades[produto]["estoque"]
            if atual + quantidade > limite:
                return {"retorno": 2, "mensagem": "Capacidade de estoque excedida para o produto."}
            self.estoque[produto] += quantidade
            return {"retorno": 0, "mensagem": "Produto adicionado ao estoque interno."}

        elif destino == 'exposicao':
            atual = self.exposicao[produto]
            limite = self.capacidades[produto]["exposicao"]
            if atual + quantidade > limite:
                return {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}
            self.exposicao[produto] += quantidade
            return {"retorno": 0, "mensagem": "Produto adicionado à exposição."}

        else:
            return {"retorno": 4, "mensagem": "Destino inválido. Use 'estoque' ou 'exposicao'."}



    def mover_para_exposicao(self, produto, quantidade):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: mover_para_exposicao() (Método de Estoque)

        B) OBJETIVO:
        Transferir uma quantidade de um produto do estoque interno para a área de exposição.

        C) ACOPLAMENTO:
        PARÂMETRO 1: produto (Produto)
        O objeto do produto a ser movimentado.
        PARÂmetro 2: quantidade (inteiro)
        Número de unidades a serem movidas.

        RETORNO 1: DICIONÁRIO SE O PRODUTO NÃO ESTIVER CADASTRADO:
        {"retorno": 1, "mensagem": "Produto não cadastrado."}

        RETORNO 2: DICIONÁRIO SE O ESTOQUE INTERNO FOR INSUFICIENTE:
        {"retorno": 2, "mensagem": "Estoque insuficiente para movimentação."}

        RETORNO 3: DICIONÁRIO SE A CAPACIDADE DA EXPOSIÇÃO FOR EXCEDIDA:
        {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}

        RETORNO 4: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Produto movido para a exposição."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `produto` está registrado.
        - A `quantidade` a ser movida é menor ou igual à quantidade no estoque interno.
        - A `quantidade` a ser movida, somada à quantidade já em exposição, não excede a capacidade da exposição.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - Se bem-sucedido, a `quantidade` é subtraída do estoque interno e somada à exposição.

        E) DESCRIÇÃO:
        1. Verifica se o produto está registrado.
        2. Verifica se há quantidade suficiente no estoque interno para a transferência.
        3. Verifica se a área de exposição tem capacidade para receber a nova quantidade.
        4. Se todas as verificações passarem, decrementa a quantidade do `estoque` e incrementa na `exposicao`.
        5. Retorna sucesso.

        F) HIPÓTESES:
        - Nenhuma.

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        if produto not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}
        if self.estoque[produto] < quantidade:
            return {"retorno": 2, "mensagem": "Estoque insuficiente para movimentação."}
        if self.exposicao[produto] + quantidade > self.capacidades[produto]["exposicao"]:
            return {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}

        self.estoque[produto] -= quantidade
        self.exposicao[produto] += quantidade
        return {"retorno": 0, "mensagem": "Produto movido para a exposição."}



    def retirar_venda(self, venda: dict):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: retirar_venda() (Método de Estoque)

        B) OBJETIVO:
        Dar baixa na quantidade de produtos em exposição que foram vendidos.

        C) ACOPLAMENTO:
        PARÂMETRO 1: venda (dicionário)
        Um dicionário representando os itens vendidos, onde as chaves são objetos `Produto` e os valores são as quantidades.

        RETORNO 1: DICIONÁRIO SE UM PRODUTO DA VENDA NÃO ESTIVER CADASTRADO:
        {"retorno": 1, "mensagem": "Produto não cadastrado."}

        RETORNO 2: DICIONÁRIO SE A QUANTIDADE EM EXPOSIÇÃO FOR INSUFICIENTE:
        {"retorno": 2, "mensagem": "Quantidade insuficiente na exposição para venda."}

        RETORNO 3: DICIONÁRIO DE SUCESSO:
        {"retorno": 0, "mensagem": "Produtos removidos com sucesso."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `venda` é um dicionário no formato {Produto: quantidade}.
        - Todos os produtos na venda existem no estoque.
        - Para cada produto, a quantidade vendida é menor ou igual à quantidade em exposição.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.
        - Se bem-sucedido, a quantidade de cada produto vendido é subtraída da `exposicao`.

        E) DESCRIÇÃO:
        1. Itera sobre os itens e quantidades no dicionário `venda`.
        2. Para cada item, extrai o código do produto.
        3. Verifica se o produto está registrado no estoque.
        4. Verifica se a quantidade em exposição é suficiente para cobrir a venda.
        5. Se qualquer verificação falhar, a função retorna um erro imediatamente e não altera o estado do estoque.
        6. Se todos os itens forem válidos, a função então subtrai a quantidade vendida da `exposicao` para cada item.
        7. Retorna sucesso.

        F) HIPÓTESES:
        - A função é chamada após a validação da venda, mas faz sua própria verificação de consistência.

        G) RESTRIÇÕES:
        - A operação não é atômica no sentido de que, se um item falhar no meio do loop (o que não ocorre no código atual), os anteriores não seriam revertidos. O código atual retorna no primeiro erro, evitando este problema.
        """
        for produto, quantidade in venda.items():
            if produto not in self.capacidades:
                return {"retorno": 1, "mensagem": "Produto não cadastrado."}
            if self.exposicao[produto] < quantidade:
                return {"retorno": 2, "mensagem": "Quantidade insuficiente na exposição para venda."}

            self.exposicao[produto] -= quantidade
        return {"retorno": 0, "mensagem": "Produtos removidos com sucesso."}



    def produto_existe(self, produto):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: produto_existe() (Método de Estoque)

        B) OBJETIVO:
        Verificar de forma simples e direta se um produto está registrado neste estoque.

        C) ACOPLAMENTO:
        PARÂMETRO 1: codigo (string)
        Código do produto a ser verificado.

        RETORNO 1: DICIONÁRIO SE O PRODUTO EXISTE:
        {"retorno": 0, "mensagem": "Produto registrado."}

        RETORNO 2: DICIONÁRIO SE O PRODUTO NÃO EXISTE:
        {"retorno": 1, "mensagem": "Produto não encontrado."}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `codigo` é uma string.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status.

        E) DESCRIÇÃO:
        1. Verifica se o `codigo` existe como chave no dicionário `self.capacidades`.
        2. Retorna o dicionário correspondente ao resultado.

        F) HIPÓTESES:
        - `self.capacidades` é a fonte da verdade para o registro de produtos.

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        if produto in self.capacidades:
            return {"retorno": 0, "mensagem": "Produto registrado."}
        return {"retorno": 1, "mensagem": "Produto não encontrado."}



    def consultar_quantidade(self, produto):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: consultar_quantidade() (Método de Estoque)

        B) OBJETIVO:
        Retornar um relatório completo das quantidades e capacidades de um único produto.

        C) ACOPLAMENTO:
        PARÂMETRO 1: produto (Produto)
        O objeto do produto a ser consultado.

        RETORNO 1: DICIONÁRIO SE O PRODUTO NÃO ESTIVER CADASTRADO:
        {"retorno": 1, "mensagem": "Produto não cadastrado."}

        RETORNO 2: DICIONÁRIO DE SUCESSO COM OS DADOS:
        {"retorno": 0, "mensagem": "Consulta realizada com sucesso.", "dados": {...}}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - `produto` é um objeto que possui o atributo `codigo` correspondente a um produto registrado.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status contendo os dados detalhados do produto na chave 'dados'.

        E) DESCRIÇÃO:
        1. Extrai o código do objeto `produto`.
        2. Verifica se o produto está registrado. Se não, retorna erro.
        3. Monta um dicionário com as quantidades atuais de estoque e exposição, e as capacidades máximas.
        4. Retorna um dicionário de sucesso com os dados coletados.

        F) HIPÓTESES:
        - A estrutura de dados do estoque está consistente.

        G) RESTRIÇÕES:
        - Nenhuma.
        """
        if produto not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        return {
            "retorno": 0,
            "mensagem": "Consulta realizada com sucesso.",
            "dados": {
                "estoque": self.estoque[produto],
                "exposicao": self.exposicao[produto],
                "capacidade_estoque": self.capacidades[produto]["estoque"],
                "capacidade_exposicao": self.capacidades[produto]["exposicao"]
            }
        }



    def verificar_consistencia(self):
        """
        ESPECIFICAÇÃO DE FUNÇÃO:
        A) NOME: verificar_consistencia() (Método de Estoque)

        B) OBJETIVO:
        Realizar uma auditoria interna na estrutura de dados do estoque para encontrar inconsistências, como excesso de capacidade ou produtos não registrados.

        C) ACOPLAMENTO:
        PARÂMETROS: Nenhum.

        RETORNO 1: DICIONÁRIO SE A ESTRUTURA ESTIVER CONSISTENTE:
        {"retorno": 0, "mensagem": "Estrutura consistente."}

        RETORNO 2: DICIONÁRIO SE FOREM ENCONTRADAS INCONSISTÊNCIAS:
        {"retorno": 1, "mensagem": "Inconsistências encontradas.", "dados": [<lista de problemas>]}

        D) CONDIÇÕES DE ACOPLAMENTO:
        Assertiva(s) de entrada:
        - Nenhuma.

        Assertiva(s) de saída:
        - O retorno é um dicionário de status que, em caso de erro, contém uma lista detalhada das inconsistências encontradas.

        E) DESCRIÇÃO:
        1. Itera por todos os produtos registrados em `capacidades` e verifica se:
           a. Eles também existem em `estoque` e `exposicao`.
           b. Suas quantidades atuais não excedem suas capacidades definidas.
        2. Itera por todos os produtos em `estoque` e `exposicao` e verifica se todos eles estão registrados em `capacidades`.
        3. Coleta todas as inconsistências encontradas em uma lista.
        4. Se a lista de inconsistências estiver vazia, retorna sucesso.
        5. Se houver inconsistências, retorna um dicionário de erro com a lista detalhada.

        F) HIPÓTESES:
        - Nenhuma.

        G) RESTRIÇÕES:
        - A função apenas relata problemas, ela não os corrige.
        """
        inconsistencias = []

        # Verifica produtos registrados
        for produto in self.capacidades:
            problemas = []

            if produto not in self.estoque:
                problemas.append("Produto sem entrada no estoque interno")
            if produto not in self.exposicao:
                problemas.append("Produto sem entrada na exposição")

            if produto in self.estoque and produto in self.capacidades:
                qtd = self.estoque[produto]
                cap = self.capacidades[produto]["estoque"]
                if qtd > cap:
                    problemas.append(f"Estoque excede capacidade ({qtd} > {cap})")

            if produto in self.exposicao and produto in self.capacidades:
                qtd = self.exposicao[produto]
                cap = self.capacidades[produto]["exposicao"]
                if qtd > cap:
                    problemas.append(f"Exposição excede capacidade ({qtd} > {cap})")

            if problemas:
                inconsistencias.append({
                    "codigo": produto.codigo,
                    "problemas": problemas
                })

        # Verifica produtos não registrados em capacidades
        for produto in set(self.estoque.keys()).union(self.exposicao.keys()):
            if produto not in self.capacidades:
                inconsistencias.append({
                    "codigo": produto.codigo,
                    "problemas": ["Produto presente no estoque ou exposição mas não registrado nas capacidades"]
                })

        if inconsistencias:
            return {
                "retorno": 1,
                "mensagem": "Inconsistências encontradas.",
                "dados": inconsistencias
            }

        return {
            "retorno": 0,
            "mensagem": "Estrutura consistente."
        }


def salvar_estoques():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: salvar_estoques()

    B) OBJETIVO:
    Persistir em um arquivo JSON o estado atual de todos os estoques registrados no sistema e que estão armazenados na memória.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito. A função realiza uma operação de escrita em arquivo.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O dicionário global `_todos_estoques` contém instâncias da classe `Estoque`.

    Assertiva(s) de saída:
    - O arquivo definido pela constante `ESTOQUES_JSON` é criado ou sobrescrito com os dados de todos os estoques.

    E) DESCRIÇÃO:
    1. Inicializa um dicionário vazio `json_estoques`.
    2. Itera sobre cada par de código-estoque no dicionário global `_todos_estoques`.
    3. Para cada objeto de estoque, invoca seu método `to_json()` para obter sua representação em dicionário serializável.
    4. Adiciona este dicionário ao `json_estoques`, usando o código do estoque como chave.
    5. Abre o arquivo de destino em modo de escrita ("w") com codificação "utf-8".
    6. Utiliza a função `json.dump()` para escrever o conteúdo do dicionário `json_estoques` no arquivo, com formatação indentada para legibilidade.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_estoques` para armazenamento em memória.
    - A constante `ESTOQUES_JSON` contém um caminho de arquivo válido e com permissão de escrita.
    - Cada objeto `Estoque` possui um método `to_json()` funcional.

    G) RESTRIÇÕES:
    - A função sobrescreve completamente o arquivo de destino sem criar backups ou avisos.
    - Possíveis erros de I/O (ex: disco cheio, permissão negada) não são tratados internamente e podem interromper o programa.
    """
    json_estoques = {}

    for codigo, estoque in _todos_estoques.items():
        json_estoques[codigo] = estoque.to_json()

    with open(ESTOQUES_JSON, "w", encoding="utf-8") as f:
        json.dump(json_estoques, f, ensure_ascii=False, indent=4)

def carregar_estoques():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: carregar_estoques()

    B) OBJETIVO:
    Ler os dados de estoques de um arquivo JSON e carregá-los para a memória, populando o dicionário global `_todos_estoques`.

    C) ACOPLAMENTO:
    PARÂMETROS: Nenhum.

    RETORNO: Nenhum valor explícito. A função modifica o estado do dicionário global `_todos_estoques`.

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - O arquivo especificado pela constante `ESTOQUES_JSON` deve existir.
    - O conteúdo do arquivo deve ser um JSON válido que represente um dicionário de estoques.
    - Todos os produtos referenciados nos dados dos estoques já devem ter sido carregados no sistema.

    Assertiva(s) de saída:
    - O dicionário global `_todos_estoques` é preenchido com as instâncias de `Estoque` recriadas a partir dos dados do arquivo.

    E) DESCRIÇÃO:
    1. Utiliza um bloco `try-except` para tratar o caso de o arquivo não existir (`FileNotFoundError`), retornando silenciosamente se for o caso.
    2. Se o arquivo existir, ele é aberto e seu conteúdo JSON é carregado para um dicionário `json_estoques`.
    3. Itera sobre cada par de código-dados no dicionário carregado.
    4. Para cada item, invoca o método de classe `Estoque.from_json()` para criar uma nova instância de `Estoque`.
    5. Armazena a instância recém-criada no dicionário global `_todos_estoques`, usando o código como chave.

    F) HIPÓTESES:
    - A função `carregar_produtos` foi executada antes desta para garantir que os produtos possam ser encontrados.
    - A classe `Estoque` implementa um método de classe `from_json()` funcional.

    G) RESTRIÇÕES:
    - A função não trata exceções que podem ser levantadas por `Estoque.from_json` (como `ValueError`, `KeyError`), o que pode interromper o processo de carregamento se o arquivo de dados estiver inconsistente.
    """
    try:
        with open(ESTOQUES_JSON, "r", encoding="utf-8") as f:
            json_estoques = json.load(f)
    except FileNotFoundError:
        return

    for codigo, estoque_json in json_estoques.items():
        _todos_estoques[codigo] = Estoque.from_json(estoque_json)


def registrar_estoque(codigo: str):
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: registrar_estoque()

    B) OBJETIVO:
    Criar uma nova instância de `Estoque` e registrá-la no dicionário global de estoques do sistema, garantindo a unicidade do seu código.

    C) ACOPLAMENTO:
    PARÂMETRO 1: codigo (string)
    O identificador único para o novo estoque a ser criado.

    RETORNO 1: DICIONÁRIO DE ERRO POR PARÂMETRO NULO:
    {"retorno": 3, "mensagem": "Parâmetro nulo"}

    RETORNO 2: DICIONÁRIO DE ERRO POR CÓDIGO INVÁLIDO:
    {"retorno": 2, "mensagem": "Parâmetro 'codigo' incorreto"}

    RETORNO 3: DICIONÁRIO DE ERRO POR ESTOQUE JÁ REGISTRADO:
    {"retorno": 1, "mensagem": "Estoque já registrado com este código"}

    RETORNO 4: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Estoque registrado com sucesso", dados: <objeto Estoque>}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - `codigo` é uma string não nula e não vazia.
    - O `codigo` não deve existir como chave no dicionário `_todos_estoques`.

    Assertiva(s) de saída:
    - O retorno é um dicionário de status.
    - Se bem-sucedido, uma nova instância de `Estoque` é criada e adicionada ao `_todos_estoques`.

    E) DESCRIÇÃO:
    1. Verifica se o `codigo` é nulo.
    2. Verifica se o `codigo` é uma string válida e não vazia.
    3. Verifica se o `codigo` já está em uso no dicionário `_todos_estoques`.
    4. Se as validações passarem, cria uma nova instância da classe `Estoque`.
    5. Adiciona a nova instância ao dicionário `_todos_estoques` usando o código como chave.
    6. Retorna um dicionário de sucesso.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_estoques` para armazenar as instâncias.
    - A classe `Estoque` está definida e disponível.

    G) RESTRIÇÕES:
    - O armazenamento dos estoques é em memória e não persiste após o término da execução.
    """
    if codigo is None:
        return {"retorno": 3, "mensagem": "Parâmetro nulo"}

    if not isinstance(codigo, str) or not codigo.strip():
        return {"retorno": 2, "mensagem": "Parâmetro 'codigo' incorreto"}

    if codigo in _todos_estoques:
        return {"retorno": 1, "mensagem": "Estoque já registrado com este código"}

    estoque = Estoque(codigo=codigo)
    _todos_estoques[codigo] = estoque
    return {"retorno": 0, "mensagem": "Estoque registrado com sucesso", "dados": estoque}

def listar_todos_estoques():
    """
    ESPECIFICAÇÃO DE FUNÇÃO:
    A) NOME: listar_todos_estoques()

    B) OBJETIVO:
    Retornar uma lista de todos os estoques registrados no sistema.

    C) ACOPLAMENTO:
    Sem parâmetros de entrada.

    RETORNO 1: DICIONÁRIO SE NÃO HOUVER ESTOQUES:
    {"retorno": 1, "mensagem": "Nenhum estoque registrado", "dados": []}

    RETORNO 2: DICIONÁRIO DE SUCESSO:
    {"retorno": 0, "mensagem": "Estoques listados com sucesso", "dados": [<lista de objetos Estoque>]}

    D) CONDIÇÕES DE ACOPLAMENTO:
    Assertiva(s) de entrada:
    - Nenhuma.

    Assertiva(s) de saída:
    - O retorno é um dicionário com a chave "dados" contendo uma lista de objetos Estoque.

    E) DESCRIÇÃO:
    1. Obtém todos os estoques registrados em `_todos_estoques`.
    2. Retorna um dicionário com a lista ou uma mensagem informando que não há estoques registrados.

    F) HIPÓTESES:
    - Existe um dicionário global `_todos_estoques`.

    G) RESTRIÇÕES:
    - A função retorna todos os objetos, o que pode consumir memória em bases grandes.
    """
    estoques = [
        e for e in _todos_estoques.values()
    ]

    if not estoques or len(_todos_estoques) == 0:
        return {'retorno': 1, 'mensagem': 'Nenhum estoque registrado', 'dados': []}

    return {'retorno': 0, 'mensagem': 'Estoques listados com sucesso', 'dados': estoques}
