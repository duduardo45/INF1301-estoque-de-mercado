import pytest
# Supondo que as classes de 'estruturas.py' e as de 'estoque.py' estão acessíveis.
# Para este exemplo, vamos assumir que Produto vem de um módulo separado.
from modulos.estruturas import Produto
from modulos.estoque import Estoque, registrar_estoque, _todos_estoques

# --- Fixtures de Teste ---

@pytest.fixture(autouse=True)
def limpar_estoques_globais():
    """Fixture para limpar o registro global de estoques antes de cada teste."""
    _todos_estoques.clear()

@pytest.fixture
def produto_a():
    """Retorna uma instância de um produto A."""
    return Produto(nome="Leite Integral", marca="Marca A", categoria="Laticínios", 
                   codigo="LTC001", peso=1.0, preco=5.00)

@pytest.fixture
def produto_b():
    """Retorna uma instância de um produto B."""
    return Produto(nome="Pão Francês", marca="Padaria", categoria="Padaria",
                   codigo="PDL002", peso=0.05, preco=0.50)

@pytest.fixture
def estoque_vazio():
    """Retorna uma instância de um Estoque vazio."""
    return Estoque(codigo="principal")

@pytest.fixture
def estoque_preparado(estoque_vazio, produto_a, produto_b):
    """Retorna um Estoque com produtos já registrados e com quantidades."""
    estoque_vazio.registrar_produto(produto_a, capacidade_estoque=200, capacidade_exposicao=20)
    estoque_vazio.registrar_produto(produto_b, capacidade_estoque=500, capacidade_exposicao=50)
    estoque_vazio.adicionar_produto(produto_a, 100, 'estoque')
    estoque_vazio.adicionar_produto(produto_a, 10, 'exposicao')
    estoque_vazio.adicionar_produto(produto_b, 300, 'estoque')
    return estoque_vazio

# --- Testes da Classe Estoque ---

class TestEstoque:

    def test_registrar_produto(self, estoque_vazio, produto_a):
        """Testa o registro de um novo produto no estoque."""
        resultado = estoque_vazio.registrar_produto(produto_a, 100, 10)
        assert resultado["retorno"] == 0
        assert produto_a.codigo in estoque_vazio.capacidades
        assert estoque_vazio.estoque[produto_a.codigo] == 0

        # Testa registrar um produto duplicado
        resultado_duplicado = estoque_vazio.registrar_produto(produto_a, 50, 5)
        assert resultado_duplicado["retorno"] == 1

    def test_remover_produto(self, estoque_vazio, produto_a):
        """Testa a remoção de um produto do estoque."""
        estoque_vazio.registrar_produto(produto_a, 100, 10)
        
        # Teste de remoção bem-sucedida (produto com estoque zerado)
        resultado_sucesso = estoque_vazio.remover_produto(produto_a.codigo)
        assert resultado_sucesso["retorno"] == 0
        assert produto_a.codigo not in estoque_vazio.capacidades

        # Teste de falha (produto ainda em estoque)
        estoque_vazio.registrar_produto(produto_a, 100, 10)
        estoque_vazio.adicionar_produto(produto_a, 5, 'estoque')
        resultado_falha = estoque_vazio.remover_produto(produto_a.codigo)
        assert resultado_falha["retorno"] == 2

    def test_adicionar_produto(self, estoque_preparado, produto_a):
        """Testa a adição de produtos, respeitando as capacidades."""
        # Adição bem-sucedida
        resultado_sucesso = estoque_preparado.adicionar_produto(produto_a, 50, 'estoque')
        assert resultado_sucesso["retorno"] == 0
        assert estoque_preparado.estoque[produto_a.codigo] == 150

        # Falha por exceder capacidade
        resultado_falha = estoque_preparado.adicionar_produto(produto_a, 100, 'estoque')
        assert resultado_falha["retorno"] == 2
        
        # Falha por destino inválido
        resultado_invalido = estoque_preparado.adicionar_produto(produto_a, 1, 'prateleira')
        assert resultado_invalido["retorno"] == 4

    def test_mover_para_exposicao(self, estoque_preparado, produto_a):
        """Testa a movimentação de produtos do estoque para a exposição."""
        # Movimentação bem-sucedida
        resultado_sucesso = estoque_preparado.mover_para_exposicao(produto_a, 5)
        assert resultado_sucesso["retorno"] == 0
        assert estoque_preparado.estoque[produto_a.codigo] == 95
        assert estoque_preparado.exposicao[produto_a.codigo] == 15

        # Falha por estoque insuficiente
        resultado_falha_qtd = estoque_preparado.mover_para_exposicao(produto_a, 1000)
        assert resultado_falha_qtd["retorno"] == 2
        
        # Falha por capacidade de exposição excedida
        resultado_falha_cap = estoque_preparado.mover_para_exposicao(produto_a, 10)
        assert resultado_falha_cap["retorno"] == 3

    def test_retirar_venda(self, estoque_preparado, produto_a, produto_b):
        """Testa a baixa de produtos da exposição após uma venda."""
        venda = {produto_a: 3, produto_b: 50}
        estoque_preparado.adicionar_produto(produto_b, 50, 'exposicao')
        
        resultado_sucesso = estoque_preparado.retirar_venda(venda)
        assert resultado_sucesso["retorno"] == 0
        assert estoque_preparado.exposicao[produto_a.codigo] == 7
        assert estoque_preparado.exposicao[produto_b.codigo] == 0

        # Falha por quantidade insuficiente na exposição
        venda_grande = {produto_a: 10}
        resultado_falha = estoque_preparado.retirar_venda(venda_grande)
        assert resultado_falha["retorno"] == 2

    def test_listar_em_falta(self, estoque_vazio, produto_a, produto_b):
        """Testa a listagem de produtos com estoque zerado."""
        estoque_vazio.registrar_produto(produto_a, 100, 10) # em falta em ambos
        estoque_vazio.registrar_produto(produto_b, 100, 10)
        estoque_vazio.adicionar_produto(produto_b, 10, 'estoque') # em falta só na exposição
        
        res_ambos = estoque_vazio.listar_em_falta('ambos')
        assert sorted(res_ambos['dados']) == sorted([produto_a.codigo, produto_b.codigo])
        
        res_estoque = estoque_vazio.listar_em_falta('estoque')
        assert res_estoque['dados'] == [produto_a.codigo]

        res_exposicao = estoque_vazio.listar_em_falta('exposicao')
        assert sorted(res_exposicao['dados']) == sorted([produto_a.codigo, produto_b.codigo])
        
    def test_percentual_ocupado(self, estoque_preparado, produto_a):
        """Testa o cálculo do percentual de ocupação."""
        # Estoque: 100/200 = 50% | Exposição: 10/20 = 50%
        resultado = estoque_preparado.percentual_ocupado(produto_a.codigo)
        assert resultado['retorno'] == 0
        assert resultado['dados']['estoque'] == 50.0
        assert resultado['dados']['exposicao'] == 50.0

    def test_verificar_consistencia(self, estoque_preparado, produto_a):
        """Testa a verificação de consistência da estrutura de dados."""
        # Teste com estrutura consistente
        resultado_ok = estoque_preparado.verificar_consistencia()
        assert resultado_ok['retorno'] == 0

        # Forçando uma inconsistência (quantidade > capacidade)
        estoque_preparado.estoque[produto_a.codigo] = 300
        resultado_nok = estoque_preparado.verificar_consistencia()
        assert resultado_nok['retorno'] == 1
        assert len(resultado_nok['dados']) > 0
        assert "Estoque excede capacidade" in resultado_nok['dados'][0]['problemas'][0]

# --- Testes da Função registrar_estoque ---

class TestRegistrarEstoque:

    def test_registro_sucesso(self):
        """Testa o registro de um novo estoque no sistema."""
        resultado = registrar_estoque("filial_centro")
        assert resultado["retorno"] == 0
        assert "filial_centro" in _todos_estoques
        assert isinstance(_todos_estoques["filial_centro"], Estoque)

    def test_registro_duplicado(self):
        """Testa a falha ao registrar um estoque com código duplicado."""
        registrar_estoque("filial_sul")
        resultado = registrar_estoque("filial_sul")
        assert resultado["retorno"] == 1

    def test_codigo_invalido(self):
        """Testa a falha ao usar um código inválido (vazio ou nulo)."""
        res_nulo = registrar_estoque(None)
        assert res_nulo["retorno"] == 3
        
        res_vazio = registrar_estoque("   ")
        assert res_vazio["retorno"] == 2