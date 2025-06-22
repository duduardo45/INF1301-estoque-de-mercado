__all__ = [
    "Estoque",
    "registrar_estoque",
    "listar_todos_estoques",
]



class Estoque:

    def __init__(self, codigo: str, estoque: dict = None, exposicao: dict = None, capacidades: dict = None):
        """
        Inicializa um objeto Estoque com dicionários para controle de quantidade e capacidade.

        Args:
            codigo (str): identificador único do estoque

        Returns:
            None
        """
        self.codigo = codigo
        self.estoque = {}
        self.exposicao = {}
        self.capacidades = {}



    def __str__(self):
        """
        Retorna uma representação legível do estoque.

        Returns:
            str: descrição do estoque
        """
        total_estoque = sum(self.estoque.values())
        total_exposicao = sum(self.exposicao.values())

        faltas_estoque = [codigo for codigo, qtd in self.estoque.items() if qtd == 0]
        faltas_exposicao = [codigo for codigo, qtd in self.exposicao.items() if qtd == 0]

        descricao = f"Estoque: '{self.codigo}'\n"
        descricao += f"Produtos registrados: {len(self.capacidades)}\n"
        descricao += f"Total no estoque interno: {total_estoque}\n"
        descricao += f"Total na exposição: {total_exposicao}\n"

        if faltas_estoque:
            descricao += "Faltando no estoque interno: " + ", ".join(faltas_estoque) + "\n"
        if faltas_exposicao:
            descricao += "Faltando na exposição: " + ", ".join(faltas_exposicao) + "\n"

        return descricao.strip()



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
        codigo = produto.codigo
        if codigo in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto já está registrado."}

        self.estoque[codigo] = 0
        self.exposicao[codigo] = 0
        self.capacidades[codigo] = {
            "estoque": capacidade_estoque,
            "exposicao": capacidade_exposicao
        }
        return {"retorno": 0, "mensagem": "Produto registrado com sucesso."}



    def remover_produto(self, codigo):
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
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não encontrado."}

        if self.estoque.get(codigo, 0) > 0 or self.exposicao.get(codigo, 0) > 0:
            return {"retorno": 2, "mensagem": "Produto ainda possui quantidades em estoque ou exposição."}

        self.estoque.pop(codigo, None)
        self.exposicao.pop(codigo, None)
        self.capacidades.pop(codigo, None)

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

        for codigo in self.capacidades:
            em_estoque = self.estoque[codigo] == 0
            em_exposicao = self.exposicao[codigo] == 0

            if tipo == 'estoque' and em_estoque:
                faltando.append(codigo)
            elif tipo == 'exposicao' and em_exposicao:
                faltando.append(codigo)
            elif tipo == 'ambos' and (em_estoque or em_exposicao):
                faltando.append(codigo)

        return {
            "retorno": 0,
            "mensagem": "Listagem de faltas realizada com sucesso.",
            "dados": faltando
        }



    def percentual_ocupado(self, codigo):
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
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        cap = self.capacidades[codigo]
        ocup_estoque = (self.estoque[codigo] / cap["estoque"]) * 100 if cap["estoque"] else 0
        ocup_exposicao = (self.exposicao[codigo] / cap["exposicao"]) * 100 if cap["exposicao"] else 0

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
        for codigo in self.capacidades:
            if detalhado:
                produtos.append({
                    "codigo": codigo,
                    "estoque": self.estoque[codigo],
                    "exposicao": self.exposicao[codigo],
                    "capacidade_estoque": self.capacidades[codigo]["estoque"],
                    "capacidade_exposicao": self.capacidades[codigo]["exposicao"]
                })
            else:
                produtos.append(codigo)

        return {
            "retorno": 0,
            "mensagem": "Listagem realizada com sucesso.",
            "dados": produtos
        }



    def atualizar_capacidades(self, codigo, capacidade_estoque=None, capacidade_exposicao=None):
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
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado no estoque."}

        if capacidade_estoque is None and capacidade_exposicao is None:
            return {"retorno": 2, "mensagem": "Por favor especifique alguma capacidade a atualizar."}

        if capacidade_estoque is not None:
            self.capacidades[codigo]["estoque"] = capacidade_estoque

        if capacidade_exposicao is not None:
            self.capacidades[codigo]["exposicao"] = capacidade_exposicao

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
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        if codigo not in self.estoque:
            self.estoque[codigo] = 0
        if codigo not in self.exposicao:
            self.exposicao[codigo] = 0

        if destino == 'estoque':
            atual = self.estoque[codigo]
            limite = self.capacidades[codigo]["estoque"]
            if atual + quantidade > limite:
                return {"retorno": 2, "mensagem": "Capacidade de estoque excedida para o produto."}
            self.estoque[codigo] += quantidade
            return {"retorno": 0, "mensagem": "Produto adicionado ao estoque interno."}

        elif destino == 'exposicao':
            atual = self.exposicao[codigo]
            limite = self.capacidades[codigo]["exposicao"]
            if atual + quantidade > limite:
                return {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}
            self.exposicao[codigo] += quantidade
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
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}
        if self.estoque[codigo] < quantidade:
            return {"retorno": 2, "mensagem": "Estoque insuficiente para movimentação."}
        if self.exposicao[codigo] + quantidade > self.capacidades[codigo]["exposicao"]:
            return {"retorno": 3, "mensagem": "Capacidade de exposição excedida para o produto."}

        self.estoque[codigo] -= quantidade
        self.exposicao[codigo] += quantidade
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
        for item, quantidade in venda.items():
            codigo = item.codigo # código do Produto
            if codigo not in self.capacidades:
                return {"retorno": 1, "mensagem": "Produto não cadastrado."}
            if self.exposicao[codigo] < quantidade:
                return {"retorno": 2, "mensagem": "Quantidade insuficiente na exposição para venda."}

            self.exposicao[codigo] -= quantidade
        return {"retorno": 0, "mensagem": "Produtos removidos com sucesso."}



    def produto_existe(self, codigo):
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
        if codigo in self.capacidades:
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
        codigo = produto.codigo
        if codigo not in self.capacidades:
            return {"retorno": 1, "mensagem": "Produto não cadastrado."}

        return {
            "retorno": 0,
            "mensagem": "Consulta realizada com sucesso.",
            "dados": {
                "estoque": self.estoque[codigo],
                "exposicao": self.exposicao[codigo],
                "capacidade_estoque": self.capacidades[codigo]["estoque"],
                "capacidade_exposicao": self.capacidades[codigo]["exposicao"]
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
        for codigo in self.capacidades:
            problemas = []

            if codigo not in self.estoque:
                problemas.append("Produto sem entrada no estoque interno")
            if codigo not in self.exposicao:
                problemas.append("Produto sem entrada na exposição")

            if codigo in self.estoque and codigo in self.capacidades:
                qtd = self.estoque[codigo]
                cap = self.capacidades[codigo]["estoque"]
                if qtd > cap:
                    problemas.append(f"Estoque excede capacidade ({qtd} > {cap})")

            if codigo in self.exposicao and codigo in self.capacidades:
                qtd = self.exposicao[codigo]
                cap = self.capacidades[codigo]["exposicao"]
                if qtd > cap:
                    problemas.append(f"Exposição excede capacidade ({qtd} > {cap})")

            if problemas:
                inconsistencias.append({
                    "codigo": codigo,
                    "problemas": problemas
                })

        # Verifica produtos não registrados em capacidades
        for codigo in set(self.estoque.keys()).union(self.exposicao.keys()):
            if codigo not in self.capacidades:
                inconsistencias.append({
                    "codigo": codigo,
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



_todos_estoques = {}

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
    {"retorno": 0, "mensagem": "Estoque registrado com sucesso"}

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

    _todos_estoques[codigo] = Estoque(codigo=codigo)
    return {"retorno": 0, "mensagem": "Estoque registrado com sucesso"}

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
