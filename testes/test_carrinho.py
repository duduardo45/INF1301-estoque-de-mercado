import pytest
from datetime import date

# Supondo que as classes Produto e Funcionario estão em um módulo 'estruturas'
# ou similarmente acessíveis.
from modulos.estruturas import Produto, Funcionario
from modulos.carrinho import Carrinho

# --- Fixtures para criar objetos de teste reutilizáveis ---

@pytest.fixture
def produto_a():
    """Retorna uma instância de um produto com preço unitário."""
    return Produto(nome="Suco de Uva", marca="Marca Suco", categoria="Bebidas", 
                   codigo="BEB001", peso=1.0, preco=8.50)

@pytest.fixture
def produto_b():
    """Retorna uma instância de um produto vendido por peso."""
    return Produto(nome="Presunto Cozido", marca="Marca Frios", categoria="Frios",
                   codigo="FRS002", peso=1.0, preco=0, preco_por_peso=30.00)

@pytest.fixture
def funcionario_teste():
    """Retorna uma instância de um funcionário."""
    return Funcionario(nome="João da Silva", codigo=101, cargo="Caixa",
                       data_contratacao="2024-01-15")

@pytest.fixture
def carrinho_vazio():
    """Retorna uma instância de um Carrinho vazio."""
    return Carrinho(id=1, data_hora=None, itens={})

@pytest.fixture
def carrinho_com_itens(produto_a, produto_b):
    """Retorna um Carrinho com alguns itens já adicionados."""
    # Cria uma instância nova e independente de Carrinho
    carrinho = Carrinho(id=2, data_hora=None, itens={})
    carrinho.adiciona_no_carrinho(produto_a, 2)
    carrinho.adiciona_no_carrinho(produto_b, 0.5)
    return carrinho

# --- Testes para a classe Carrinho ---

class TestCarrinho:

    def test_adiciona_no_carrinho(self, carrinho_vazio, produto_a):
        """Testa adicionar um novo produto e atualizar a quantidade de um existente."""
        # Adiciona novo produto
        res1 = carrinho_vazio.adiciona_no_carrinho(produto_a, 3)
        assert res1['retorno'] == 0
        assert produto_a in carrinho_vazio.itens
        assert carrinho_vazio.itens[produto_a] == 3

        # Adiciona mais do mesmo produto (atualiza quantidade)
        res2 = carrinho_vazio.adiciona_no_carrinho(produto_a, 2)
        assert res2['retorno'] == 1
        assert carrinho_vazio.itens[produto_a] == 5
        
        # Testa parâmetros inválidos
        res_nulo = carrinho_vazio.adiciona_no_carrinho(None, 1)
        assert res_nulo['retorno'] == 3
        res_qtd_invalida = carrinho_vazio.adiciona_no_carrinho(produto_a, 0)
        assert res_qtd_invalida['retorno'] == 2

    def test_remover_do_carrinho(self, carrinho_com_itens, produto_a):
        """Testa a remoção parcial e total de um produto do carrinho."""
        # Remove uma quantidade parcial (existiam 2, remove 1)
        res1 = carrinho_com_itens.remover_do_carrinho(produto_a, 1)
        assert res1['retorno'] == 0
        assert carrinho_com_itens.itens[produto_a] == 1

        # Remove o restante do produto (remove 1 ou mais)
        res2 = carrinho_com_itens.remover_do_carrinho(produto_a, 1)
        assert res2['retorno'] == 0
        assert produto_a not in carrinho_com_itens.itens

        # Tenta remover um produto que não está no carrinho
        res_nao_encontrado = carrinho_com_itens.remover_do_carrinho(produto_a, 1)
        assert res_nao_encontrado['retorno'] == 1
        
    def test_calcula_total(self, carrinho_com_itens):
        """Testa o cálculo do valor total dos itens no carrinho."""
        # Valor esperado: (2 * 8.50) + (0.5 * 30.00) = 17.00 + 15.00 = 32.00
        total = carrinho_com_itens.calcula_total()
        assert total == 32.00
        assert carrinho_com_itens.total == 32.00

    def test_listar_itens(self, carrinho_com_itens, carrinho_vazio, produto_a, produto_b):
        """Testa os modos de listagem de itens (resumido e detalhado)."""
        # Teste com carrinho cheio
        res_resumido = carrinho_com_itens.listar_itens()
        assert res_resumido['retorno'] == 0
        # A ordem pode variar, então verificamos o conteúdo
        assert (produto_a.codigo, 2) in res_resumido['dados']
        assert (produto_b.codigo, 0.5) in res_resumido['dados']

        res_detalhado = carrinho_com_itens.listar_itens(verbose=True)
        assert res_detalhado['retorno'] == 0
        assert isinstance(res_detalhado['dados'][0], str)
        assert "Produto: Suco de Uva" in res_detalhado['dados'][0] or "Produto: Presunto Cozido" in res_detalhado['dados'][0]
        
        # Teste com carrinho vazio
        res_vazio = carrinho_vazio.listar_itens()
        assert res_vazio['retorno'] == 1
        assert "Carrinho vazio" in res_vazio['mensagem']

    def test_limpar_carrinho(self, carrinho_com_itens):
        """Testa se o carrinho é esvaziado corretamente."""
        assert len(carrinho_com_itens.itens) > 0  # Garante que não está vazio
        
        resultado = carrinho_com_itens.limpar_carrinho()
        assert resultado['retorno'] == 0
        assert not carrinho_com_itens.itens  # Verifica se o dicionário está vazio

    def test_finaliza_carrinho(self, carrinho_com_itens, funcionario_teste):
        """Testa a finalização do carrinho, registrando funcionário e data."""
        hoje = date.today().strftime("%Y/%m/%d")
        
        resultado = carrinho_com_itens.finaliza_carrinho(funcionario_teste)
        assert resultado['retorno'] == 0
        assert carrinho_com_itens.funcionario == funcionario_teste
        assert carrinho_com_itens.data_hora == hoje