import pytest
from modulos import produto
from modulos import funcionario

# Fixture para limpar a base de dados em memória antes de cada teste
@pytest.fixture(autouse=True)
def limpar_bases_de_dados(): # Nome do fixture atualizado para maior clareza
    """
    Executado automaticamente antes de cada teste, este fixture limpa
    os dicionários globais para garantir a independência dos testes.
    """
    funcionario._todos_funcionarios.clear()
    # ALTERAÇÃO: Adicionada a limpeza da base de produtos
    produto._todos_produtos.clear()

# --- Testes para a função auxiliar _valida_codigo_barras ---
class TestValidaCodigoBarras:
    def test_codigo_valido(self):
        """Testa um código EAN-13 válido."""
        # ALTERAÇÃO: Usar um código válido
        assert produto._valida_codigo_barras("7894900011517") is True

    def test_codigo_invalido_checksum(self):
        """Testa um código com dígito verificador incorreto."""
        assert produto._valida_codigo_barras("7891000315503") is False

    def test_comprimento_invalido(self):
        """Testa um código com menos de 13 dígitos."""
        assert produto._valida_codigo_barras("123456") is False

    def test_nao_numerico(self):
        """Testa um código com caracteres não numéricos."""
        assert produto._valida_codigo_barras("abcdefghijklm") is False

    def test_tipo_invalido(self):
        """Testa um input que não é string."""
        assert produto._valida_codigo_barras(1234567890123) is False


# --- Testes para a função consultar_produto_por_codigo ---
class TestConsultarProduto:
    def test_consulta_sucesso(self):
        # ALTERAÇÃO: Usar um código válido
        codigo_valido = "7894900011517"
        produto.registrar_produto("Nescau", "Nestlé", "Achocolatados", codigo_valido, 0.4, 8.50)
        resultado = produto.consultar_produto_por_codigo(codigo_valido)
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == "Produto encontrado com sucesso"
        assert isinstance(resultado['dados'], produto.Produto)
        assert resultado['dados'].codigo == codigo_valido

    def test_produto_nao_encontrado(self):
        """
        Testa a consulta de um produto com código inexistente.
        (Retorno esperado: 2)
        """
        resultado = produto.consultar_produto_por_codigo("1111111111111")
        assert resultado['retorno'] == 2
        assert resultado['mensagem'] == "Produto não encontrado"

    def test_parametro_codigo_errado(self):
        """
        Testa a consulta com um tipo de parâmetro incorreto para o código.
        (Retorno esperado: 3)
        """
        resultado = produto.consultar_produto_por_codigo(12345)
        assert resultado['retorno'] == 3
        assert resultado['mensagem'] == "Parâmetro 'codigo' errado"

    def test_parametro_nulo(self):
        """
        Testa a consulta passando None como parâmetro.
        (Retorno esperado: 4)
        """
        resultado = produto.consultar_produto_por_codigo(None)
        assert resultado['retorno'] == 4
        assert resultado['mensagem'] == "Parâmetro nulo"


# --- Testes para a função registrar_produto ---
class TestRegistrarProduto:
    def test_registro_sucesso(self):
        # ALTERAÇÃO: Usar um código válido
        codigo_valido = "7894900011517"
        resultado = produto.registrar_produto("Nescau", "Nestlé", "Achocolatados", codigo_valido, 0.4, 8.50)
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == "Produto registrado com sucesso"
        assert codigo_valido in produto._todos_produtos
        assert produto._todos_produtos[codigo_valido] == resultado['dados']

    def test_produto_ja_cadastrado(self):
        # ALTERAÇÃO: Usar um código válido
        codigo_valido = "7894900011517"
        produto.registrar_produto("Produto 1", "Marca", "Cat", codigo_valido, 1.0, 1.0)
        resultado = produto.registrar_produto("Produto 2", "Marca", "Cat", codigo_valido, 2.0, 2.0)
        assert resultado['retorno'] == 5
        assert resultado['mensagem'] == "Produto já cadastrado com este código"

    def test_codigo_de_barras_invalido(self):
        """
        Testa a falha ao tentar registrar um produto com código de barras inválido.
        (Retorno esperado: 3)
        """
        resultado = produto.registrar_produto("Nome", "Marca", "Cat", "123", 1.0, 1.0)
        assert resultado['retorno'] == 3
        assert resultado['mensagem'] == "Código de barras inválido"

    def test_parametro_nulo_no_registro(self):
        """
        Testa a falha ao registrar com um dos parâmetros obrigatórios como nulo.
        (Retorno esperado: 4)
        """
        resultado = produto.registrar_produto(None, "Marca", "Cat", "7891000315502", 1.0, 1.0)
        assert resultado['retorno'] == 4
        assert resultado['mensagem'] == "Parâmetro nulo"

# --- Testes para a função atualizar_produto ---
class TestAtualizarProduto:
    
    @pytest.fixture
    def produto_existente(self):
        """Cria um produto padrão para ser usado nos testes de atualização."""
        codigo = "7894900011517" # Nescau
        p = produto.registrar_produto("Nescau 2.0", "Nestlé", "Achocolatados", codigo, 400.0, 8.99)
        return p['dados']

    def test_atualizacao_sucesso(self, produto_existente):
        """
        Testa a atualização bem-sucedida de um produto.
        (Retorno esperado: 0)
        """
        novos_dados = {"nome": "Nescau 3.0", "preco": 9.50}
        resultado = produto.atualizar_produto(produto_existente.codigo, novos_dados)
        
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == "Produto atualizado com sucesso"
        assert produto_existente.nome == "Nescau 3.0"
        assert produto_existente.preco == 9.50

    def test_atualizar_produto_nao_encontrado(self):
        """
        Testa a falha ao tentar atualizar um produto que não existe.
        (Retorno esperado: 2)
        """
        resultado = produto.atualizar_produto("1111111111111", {"preco": 10.0})
        assert resultado['retorno'] == 2
        assert resultado['mensagem'] == "Produto não encontrado"

    def test_atualizar_campo_invalido(self, produto_existente):
        """
        Testa a falha ao tentar atualizar um campo não permitido (ex: 'codigo').
        (Retorno esperado: 3)
        """
        resultado = produto.atualizar_produto(produto_existente.codigo, {"codigo": "novo_codigo"})
        assert resultado['retorno'] == 3
        assert "Campo inválido para atualização: codigo" in resultado['mensagem']

    def test_atualizar_com_parametro_nulo(self, produto_existente):
        """
        Testa a falha ao chamar a função com parâmetros nulos.
        (Retorno esperado: 4)
        """
        res1 = produto.atualizar_produto(None, {"preco": 1.0})
        res2 = produto.atualizar_produto(produto_existente.codigo, None)
        assert res1['retorno'] == 4
        assert res2['retorno'] == 4


# --- Testes para a função pesquisar_produto ---
class TestPesquisarProduto:

    @pytest.fixture
    def setup_produtos_pesquisa(self):
        """Cria um conjunto de produtos para os testes de pesquisa."""
        produto.registrar_produto("Leite Integral", "Marca A", "Laticínios", "7890000000017", 1.0, 5.00)
        produto.registrar_produto("Leite Desnatado", "Marca B", "Laticínios", "7890000000024", 1.0, 5.50)
        produto.registrar_produto("Café em Pó", "Marca A", "Mercearia", "7890000000031", 0.5, 12.00)
        produto.registrar_produto("Suco de Laranja", "Marca C", "Bebidas", "7890000000048", 1.0, 7.00)

    def test_pesquisa_por_texto_simples(self, setup_produtos_pesquisa):
        """
        Testa uma busca por texto simples que deve encontrar múltiplos resultados.
        """
        resultado = produto.pesquisar_produto("leite")
        assert resultado['retorno'] == 0
        assert len(resultado['dados']) == 2
        assert "2 produto(s) encontrado(s)" in resultado['mensagem']

    def test_pesquisa_case_insensitive(self, setup_produtos_pesquisa):
        """
        Testa se a busca por texto ignora maiúsculas/minúsculas.
        """
        resultado = produto.pesquisar_produto("LeItE")
        assert len(resultado['dados']) == 2

    def test_pesquisa_com_filtro(self, setup_produtos_pesquisa):
        """
        Testa a combinação de busca por texto e filtro por atributo.
        """
        # Busca por "leite" apenas da "Marca A"
        resultado = produto.pesquisar_produto("leite", filtros={"marca": "Marca A"})
        assert len(resultado['dados']) == 1
        assert resultado['dados'][0].nome == "Leite Integral"

    def test_pesquisa_sem_resultados(self, setup_produtos_pesquisa):
        """
        Testa uma busca que não deve retornar nenhum produto.
        """
        resultado = produto.pesquisar_produto("chocolate")
        assert len(resultado['dados']) == 0
        assert "0 produto(s) encontrado(s)" in resultado['mensagem']

    def test_pesquisa_com_filtro_sem_match(self, setup_produtos_pesquisa):
        """
        Testa uma busca onde o texto corresponde mas o filtro não.
        """
        resultado = produto.pesquisar_produto("leite", filtros={"marca": "Marca C"})
        assert len(resultado['dados']) == 0
        
    def test_pesquisa_parametro_nulo(self):
        """
        Testa a chamada da função com o parâmetro de texto nulo.
        (Retorno esperado: 4)
        """
        resultado = produto.pesquisar_produto(None)
        assert resultado['retorno'] == 4
        assert resultado['mensagem'] == "Parâmetro nulo"