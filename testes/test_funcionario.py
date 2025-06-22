import pytest
from datetime import date
from modulos import funcionario
from modulos import produto

# Fixture para garantir que o estado do módulo seja limpo antes de cada teste
@pytest.fixture(autouse=True)
def limpar_bases_de_dados():
    """
    Executado automaticamente antes de cada teste, este fixture limpa
    os dicionários globais de todos os módulos relevantes para garantir
    a independência total dos testes.
    """
    funcionario._todos_funcionarios.clear()
    # ALTERAÇÃO FINAL: Adicionar esta linha para limpar a base de produtos
    produto._todos_produtos.clear()


# --- Testes para a classe Funcionario ---
class TestFuncionarioClass:

    def test_desligar_funcionario(self):
        """Testa o desligamento de um funcionário."""
        hoje = date.today().strftime("%Y/%m/%d")
        f = funcionario.Funcionario("João", 1, "Vendedor", "2023/01/01")
        
        # Desliga com a data de hoje
        resultado = f.desligar_funcionario()
        assert resultado['retorno'] == 0
        assert f.data_desligamento == hoje
        assert f.ativo() is False

        # Tenta desligar novamente
        resultado2 = f.desligar_funcionario()
        assert resultado2['retorno'] == 1
        assert "já desligado" in resultado2['mensagem']

    def test_atualizar_atributo(self):
        """Testa a atualização de atributos do funcionário."""
        f = funcionario.Funcionario("Maria", 2, "Caixa", "2023/01/01")

        # Atualização bem-sucedida
        resultado = f.atualizar("cargo", "Gerente")
        assert resultado['retorno'] == 0
        assert f.cargo == "Gerente"

        # Atributo inexistente
        resultado2 = f.atualizar("salario", 5000.0)
        assert resultado2['retorno'] == 1
        assert "não encontrado" in resultado2['mensagem']
        
        # Parâmetro nulo
        resultado3 = f.atualizar(None, "valor")
        assert resultado3['retorno'] == 2

class TestValidaCodigoBarras:
    def test_codigo_valido(self):
        """Testa um código EAN-13 válido."""
        # ALTERAÇÃO: Substituindo o código inválido por um válido.
        assert produto._valida_codigo_barras("7894900011517") is True

# --- Testes para a função adiciona_funcionario ---
class TestAdicionaFuncionario:

    def test_adicao_sucesso(self):
        """Testa a adição de um funcionário com sucesso."""
        resultado = funcionario.adiciona_funcionario("Carlos Silva", 101, "Estoquista", "2024/01/15")
        assert resultado['retorno'] == 0
        assert 101 in funcionario._todos_funcionarios
        assert funcionario._todos_funcionarios[101].nome == "Carlos Silva"

    def test_codigo_duplicado(self):
        """Testa a falha ao adicionar um funcionário com código já existente."""
        funcionario.adiciona_funcionario("Carlos Silva", 101, "Estoquista", "2024/01/15")
        resultado = funcionario.adiciona_funcionario("Ana Souza", 101, "Vendedora", "2024/02/20")
        assert resultado['retorno'] == 1
        assert "Código já cadastrado" in resultado['mensagem']

    def test_nome_obrigatorio(self):
        """Testa a falha ao adicionar com nome vazio ou nulo."""
        resultado = funcionario.adiciona_funcionario("", 102, "Cargo", "2024/01/01")
        assert resultado['retorno'] == 2
        assert "Nome obrigatório" in resultado['mensagem']

    def test_parametro_nulo(self):
        """Testa a falha com parâmetros nulos."""
        resultado = funcionario.adiciona_funcionario("Nome", None, "Cargo", "2024/01/01")
        assert resultado['retorno'] == 3
        assert "Parâmetro nulo" in resultado['mensagem']
        
    def test_parametro_tipo_incorreto(self):
        """Testa a falha com tipos de parâmetros incorretos."""
        resultado = funcionario.adiciona_funcionario("Nome", "101", "Cargo", "2024/01/01")
        assert resultado['retorno'] == 4
        assert "Parâmetro codigo errado" in resultado['mensagem']


# --- Testes para a função novo_funcionario ---
class TestNovoFuncionario:

    def test_novo_funcionario_sucesso(self):
        """Testa o registro de um novo funcionário, verificando a data automática."""
        hoje = date.today().strftime("%Y/%m/%d")
        resultado = funcionario.novo_funcionario("Fernanda Lima", 201, "Gerente")
        assert resultado['retorno'] == 0
        assert 201 in funcionario._todos_funcionarios
        assert funcionario._todos_funcionarios[201].data_contratacao == hoje

    def test_novo_funcionario_codigo_duplicado(self):
        """Testa a falha com código duplicado."""
        funcionario.novo_funcionario("Fernanda Lima", 201, "Gerente")
        resultado = funcionario.novo_funcionario("Jorge Cruz", 201, "Supervisor")
        assert resultado['retorno'] == 1


# --- Testes para a função consultar_funcionario ---
class TestConsultarFuncionario:

    @pytest.fixture
    def setup_consulta(self):
        """Cria um funcionário ativo e um inativo para os testes."""
        funcionario.novo_funcionario("Ativo User", 301, "Ativo")
        funcionario.adiciona_funcionario("Inativo User", 302, "Inativo", "2022/01/01")
        funcionario._todos_funcionarios[302].desligar_funcionario("2023/01/01")

    def test_consultar_ativo_sucesso(self, setup_consulta):
        """Testa a consulta de um funcionário ativo."""
        resultado = funcionario.consultar_funcionario(301)
        assert resultado['retorno'] == 0
        assert resultado['dados'].codigo == 301

    def test_consultar_inativo_sem_permissao(self, setup_consulta):
        """Testa a consulta de um inativo sem o filtro, esperando erro."""
        resultado = funcionario.consultar_funcionario(302)
        assert resultado['retorno'] == 1
        assert "Funcionário inativo" in resultado['mensagem']

    def test_consultar_inativo_com_permissao(self, setup_consulta):
        """Testa a consulta de um inativo com o filtro, esperando sucesso."""
        resultado = funcionario.consultar_funcionario(302, incluir_inativos=True)
        assert resultado['retorno'] == 0
        assert resultado['dados'].codigo == 302

    def test_consultar_nao_encontrado(self, setup_consulta):
        """Testa a consulta de um código inexistente."""
        resultado = funcionario.consultar_funcionario(999)
        assert resultado['retorno'] == 1
        assert "Funcionário não encontrado" in resultado['mensagem']
        
    def test_consultar_codigo_invalido(self):
        """Testa a consulta com um tipo de código inválido."""
        resultado = funcionario.consultar_funcionario("301")
        assert resultado['retorno'] == 2


# --- Testes para a função consultar_funcionario_por_nome ---
class TestConsultarFuncionarioPorNome:

    @pytest.fixture
    def setup_busca_nome(self):
        """Cria funcionários para teste de busca por nome."""
        funcionario.adiciona_funcionario("Marcos Andrade", 401, "Vendedor", "2023/01/10")
        funcionario.adiciona_funcionario("Mariana Silva", 402, "Caixa", "2023/02/15")
        funcionario.adiciona_funcionario("Marcos Pontes", 403, "Vendedor", "2023/03/20")
        
        # Funcionário inativo
        f_inativo = funcionario.Funcionario("Silvia Costa", 404, "Ex-Gerente", "2022/01/01", "2023/12/31")
        funcionario._todos_funcionarios[404] = f_inativo

    def test_busca_parcial_sucesso(self, setup_busca_nome):
        """Testa busca por parte do nome, esperando múltiplos resultados."""
        resultado = funcionario.consultar_funcionario_por_nome("marcos")
        assert resultado['retorno'] == 0
        assert len(resultado['dados']) == 2

    def test_busca_sem_resultado(self, setup_busca_nome):
        """Testa busca por nome que não existe."""
        resultado = funcionario.consultar_funcionario_por_nome("Roberto")
        assert resultado['retorno'] == 1
        assert "Nenhum funcionário encontrado" in resultado['mensagem']

    def test_busca_incluindo_inativos(self, setup_busca_nome):
        """Testa busca por nome que é de um funcionário inativo."""
        # Busca sem incluir inativos
        res1 = funcionario.consultar_funcionario_por_nome("Silvia")
        assert res1['retorno'] == 1 # Não deve encontrar

        # Busca incluindo inativos
        res2 = funcionario.consultar_funcionario_por_nome("Silvia", incluir_inativos=True)
        assert res2['retorno'] == 0
        assert len(res2['dados']) == 1
        assert res2['dados'][0].codigo == 404

class TestConsultarProduto:
    def test_consulta_sucesso(self):
        """
        Testa a consulta de um produto que existe.
        (Retorno esperado: 0)
        """
        # ALTERAÇÃO: Usando um código válido para o registro.
        codigo_valido = "7894900011517"
        produto.registrar_produto("Nescau", "Nestlé", "Achocolatados", codigo_valido, 0.4, 8.50)
        
        resultado = produto.consultar_produto_por_codigo(codigo_valido)
        
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == "Produto encontrado com sucesso"
        assert isinstance(resultado['dados'], produto.Produto)
        assert resultado['dados'].codigo == codigo_valido

# --- Testes para a função listar_todos_funcionarios ---
class TestListarTodosFuncionarios:

    @pytest.fixture
    def setup_listagem(self):
        """Cria 2 funcionários ativos e 1 inativo."""
        funcionario.novo_funcionario("Ativo 1", 501, "Cargo")
        funcionario.novo_funcionario("Ativo 2", 502, "Cargo")
        f_inativo = funcionario.Funcionario("Inativo 1", 503, "Cargo", "2022/01/01", "2023/01/01")
        funcionario._todos_funcionarios[503] = f_inativo

    def test_listar_apenas_ativos(self, setup_listagem):
        """Testa a listagem padrão, que deve retornar apenas funcionários ativos."""
        resultado = funcionario.listar_todos_funcionarios()
        assert resultado['retorno'] == 0
        assert len(resultado['dados']) == 2
        # Verifica se todos na lista estão ativos
        assert all(f.ativo() for f in resultado['dados'])

    def test_listar_todos_incluindo_inativos(self, setup_listagem):
        """Testa a listagem com o filtro para incluir inativos."""
        resultado = funcionario.listar_todos_funcionarios(incluir_inativos=True)
        assert resultado['retorno'] == 0
        assert len(resultado['dados']) == 3

    def test_listar_com_base_vazia(self):
        """Testa a listagem quando não há funcionários registrados."""
        resultado = funcionario.listar_todos_funcionarios()
        assert resultado['retorno'] == 1
        assert "Nenhum funcionário registrado" in resultado['mensagem']

class TestRegistrarProduto:
    def test_registro_sucesso(self):
        """
        Testa o registro bem-sucedido de um novo produto.
        (Retorno esperado: 0)
        """
        # ALTERAÇÃO: Usando um código válido.
        codigo_valido = "7894900011517"
        resultado = produto.registrar_produto("Nescau", "Nestlé", "Achocolatados", codigo_valido, 0.4, 8.50)
        
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == "Produto registrado com sucesso"
        assert codigo_valido in produto._todos_produtos
        assert produto._todos_produtos[codigo_valido] == resultado['dados']

    def test_produto_ja_cadastrado(self):
        """
        Testa a falha ao tentar registrar um produto com um código já existente.
        (Retorno esperado: 5)
        """
        # ALTERAÇÃO: Usando um código válido.
        codigo_valido = "7894900011517"
        produto.registrar_produto("Produto 1", "Marca", "Cat", codigo_valido, 1.0, 1.0)
        resultado = produto.registrar_produto("Produto 2", "Marca", "Cat", codigo_valido, 2.0, 2.0)

        assert resultado['retorno'] == 5
        assert resultado['mensagem'] == "Produto já cadastrado com este código"