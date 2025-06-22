import pytest
from datetime import date, datetime, timedelta
import os

# Importações dos seus módulos
from modulos import unidades
from modulos import produto
from modulos import funcionario
from modulos import carrinho
from modulos import estoque

# --- INÍCIO DAS MODIFICAÇÕES PARA GERAR ARQUIVO DE RESULTADO ---

# Nome do arquivo que guardará os resultados
NOME_ARQUIVO_RESULTADOS = "resultados_testes.txt"

@pytest.fixture(scope="session", autouse=True)
def setup_arquivo_resultados(request):
    """
    Fixture que é executada uma única vez no início da sessão de testes.
    Ela cria/limpa o arquivo de resultados e escreve um cabeçalho.
    """
    with open(NOME_ARQUIVO_RESULTADOS, "w", encoding="utf-8") as f:
        f.write(f"Resultados dos Testes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n")
    
    # O yield passa o controle para os testes serem executados
    yield
    
    # Este código é executado no final de toda a sessão de testes
    with open(NOME_ARQUIVO_RESULTADOS, "a", encoding="utf-8") as f:
        f.write("\n" + "="*50 + "\n")
        f.write("Fim da execução dos testes.\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook do Pytest para acessar o resultado de cada teste.
    Este código é um padrão para capturar o resultado e anexá-lo ao nó do teste.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(scope="function", autouse=True)
def log_resultado_teste(request):
    """
    Fixture que é executada para cada função de teste.
    Ela espera o teste terminar e então escreve o resultado no arquivo.
    """
    # O yield passa o controle para a função de teste ser executada
    yield
    
    # Este código é executado após cada teste
    node = request.node
    report = getattr(node, "rep_call", None) # rep_call é a fase de execução do teste
    
    if report:
        status = "PASS" if report.passed else "FAIL"
        # Pega o nome da classe e o nome da função de teste
        test_name = node.name
        class_name = node.parent.name if hasattr(node.parent, 'name') else "Testes Gerais"
        
        with open(NOME_ARQUIVO_RESULTADOS, "a", encoding="utf-8") as f:
            f.write(f"[{status}] {class_name} :: {test_name}\n")


# --- FIM DAS MODIFICAÇÕES ---


# Fixture para garantir que o estado do módulo de unidades seja limpo antes de cada teste
@pytest.fixture(autouse=True)
def clean_unidades_module():
    """
    Este fixture é executado automaticamente antes de cada teste.
    Ele limpa o dicionário interno `_unidades` no módulo `unidades`
    para garantir que os testes sejam independentes e não interfiram uns com os outros.
    """
    unidades._unidades.clear()
    produto._todos_produtos.clear()
    funcionario._todos_funcionarios.clear()


# Testes para a função adiciona_Unidade
class TestAdicionaUnidade:

    def test_adiciona_unidade_sucesso(self):
        """
        Testa o caso de sucesso da função adiciona_Unidade.
        Verifica se a função retorna 0 e a mensagem correta.
        Também confirma se a unidade foi de fato adicionada.
        (Retorno esperado: 0)
        """
        codigo = 1
        nome = "Unidade Central"
        localizacao = (-22.9068, -43.1729)
        
        resultado = unidades.adiciona_Unidade(codigo, nome, localizacao)
        
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == 'Unidade adicionada com sucesso'
        assert codigo in unidades._unidades

    def test_codigo_duplicado(self):
        """
        Testa a falha ao tentar adicionar uma unidade com um código já existente.
        (Retorno esperado: 1)
        """
        codigo = 1
        nome = "Unidade Central"
        localizacao = (-22.9068, -43.1729)
        
        unidades.adiciona_Unidade(codigo, nome, localizacao) # Adiciona a primeira vez
        resultado = unidades.adiciona_Unidade(codigo, "Outra Unidade", localizacao) # Tenta adicionar novamente
        
        assert resultado['retorno'] == 1
        assert resultado['mensagem'] == 'Código duplicado'

    def test_nome_vazio(self):
        """
        Testa a falha ao tentar adicionar uma unidade com um nome vazio.
        (Retorno esperado: 2)
        """
        resultado = unidades.adiciona_Unidade(1, "", (-22.9068, -43.1729))
        assert resultado['retorno'] == 2
        assert resultado['mensagem'] == 'Nome obrigatório'

    def test_parametro_nulo(self):
        """
        Testa a falha ao passar parâmetros nulos.
        (Retorno esperado: 3)
        """
        assert unidades.adiciona_Unidade(None, "Nome", (-22.0, -43.0))['retorno'] == 3
        assert unidades.adiciona_Unidade(1, None, (-22.0, -43.0))['retorno'] == 3
        assert unidades.adiciona_Unidade(1, "Nome", None)['retorno'] == 3
        assert unidades.adiciona_Unidade(None, None, None)['retorno'] == 3

    def test_parametro_incorreto(self):
        """
        Testa a falha com tipos de parâmetros incorretos.
        (Retorno esperado: 4)
        """
        assert unidades.adiciona_Unidade("1", "Nome", (-22.0, -43.0))['retorno'] == 4
        assert unidades.adiciona_Unidade(1, 123, (-22.0, -43.0))['retorno'] == 4
        assert unidades.adiciona_Unidade(1, "Nome", [-22.0, -43.0])['retorno'] == 4
        assert unidades.adiciona_Unidade(1, "Nome", (-22.0,))['retorno'] == 4
        assert unidades.adiciona_Unidade(1, "Nome", ("lat", "lon"))['retorno'] == 4


# Testes para a função remove_Unidade
class TestRemoveUnidade:

    def test_remove_unidade_sucesso(self):
        """
        Testa a remoção (desativação) de uma unidade com sucesso.
        (Retorno esperado: 0)
        """
        codigo = 1
        unidades.adiciona_Unidade(codigo, "Unidade a ser Removida", (-1.0, -1.0))
        
        resultado = unidades.remove_Unidade(codigo)
        
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == 'Unidade marcada como removida'
        assert unidades._unidades[codigo].ativo is False

    def test_remove_unidade_nao_encontrada(self):
        """
        Testa a falha ao tentar remover uma unidade com código inexistente.
        (Retorno esperado: 1)
        """
        resultado = unidades.remove_Unidade(999)
        assert resultado['retorno'] == 1
        assert resultado['mensagem'] == 'Unidade não encontrada'

    def test_remove_unidade_ja_removida(self):
        """
        Testa a falha ao tentar remover uma unidade que já foi removida.
        (Retorno esperado: 2)
        """
        codigo = 1
        unidades.adiciona_Unidade(codigo, "Unidade a ser Removida", (-1.0, -1.0))
        unidades.remove_Unidade(codigo) # Remove a primeira vez
        
        resultado = unidades.remove_Unidade(codigo) # Tenta remover novamente
        
        assert resultado['retorno'] == 2
        assert resultado['mensagem'] == 'Unidade já removida'

    def test_remove_parametro_nulo(self):
        """
        Testa a falha ao passar um código nulo.
        (Retorno esperado: 3)
        """
        resultado = unidades.remove_Unidade(None)
        assert resultado['retorno'] == 3
        assert resultado['mensagem'] == 'Parâmetro nulo'

    def test_remove_parametro_incorreto(self):
        """
        Testa a falha ao passar um código com tipo incorreto.
        (Retorno esperado: 4)
        """
        resultado = unidades.remove_Unidade("1")
        assert resultado['retorno'] == 4
        assert resultado['mensagem'] == 'Parâmetro codigo errado'

# Testes para a função consulta_Unidade
class TestConsultaUnidade:

    def setup_method(self):
        """
        Configura o ambiente para os testes de consulta,
        adicionando uma unidade ativa e uma inativa.
        """
        unidades.adiciona_Unidade(1, "Unidade Ativa", (-1.0, -1.0))
        unidades.adiciona_Unidade(2, "Unidade Inativa", (-2.0, -2.0))
        unidades.remove_Unidade(2)

    def test_consulta_unidade_ativa_sucesso(self):
        """
        Testa a consulta de uma unidade ativa.
        (Retorno esperado: 0)
        """
        resultado = unidades.consulta_Unidade(1)
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == 'Unidade encontrada com sucesso'
        assert resultado['dados'].codigo == 1
        assert resultado['dados'].ativo is True

    def test_consulta_unidade_desativada(self):
        """
        Testa a consulta de uma unidade desativada.
        (Retorno esperado: 1)
        """
        resultado = unidades.consulta_Unidade(2)
        assert resultado['retorno'] == 1
        assert resultado['mensagem'] == 'Unidade desativada'
        assert resultado['dados'].codigo == 2
        assert resultado['dados'].ativo is False

    def test_consulta_unidade_nao_encontrada(self):
        """
        Testa a consulta de uma unidade com código inexistente.
        (Retorno esperado: 2)
        """
        resultado = unidades.consulta_Unidade(999)
        assert resultado['retorno'] == 2
        assert resultado['mensagem'] == 'Unidade não encontrada'
        assert resultado['dados'] is None

    def test_consulta_parametro_incorreto(self):
        """
        Testa a falha com tipo de parâmetro incorreto.
        (Retorno esperado: 3)
        """
        resultado = unidades.consulta_Unidade("1")
        assert resultado['retorno'] == 3
        assert resultado['mensagem'] == 'Parâmetro codigo errado'
        
    def test_consulta_parametro_nulo(self):
        """
        Testa a falha com parâmetro nulo.
        (Retorno esperado: 4)
        """
        resultado = unidades.consulta_Unidade(None)
        assert resultado['retorno'] == 4
        assert resultado['mensagem'] == 'Parâmetro nulo'

# Testes para a função listar_Unidades
class TestListarUnidades:

    def test_listar_unidades_sucesso(self):
        """
        Testa a listagem padrão (apenas ativas) e com inativas.
        (Retorno esperado: 0)
        """
        unidades.adiciona_Unidade(1, "Unidade Ativa 1", (-1.0, -1.0))
        unidades.adiciona_Unidade(2, "Unidade Ativa 2", (-2.0, -2.0))
        unidades.adiciona_Unidade(3, "Unidade Inativa", (-3.0, -3.0))
        unidades.remove_Unidade(3)

        # Testa listando apenas ativas
        resultado_ativas = unidades.listar_Unidades()
        assert resultado_ativas['retorno'] == 0
        assert len(resultado_ativas['dados']) == 2
        assert all(u.ativo for u in resultado_ativas['dados'])

        # Testa listando todas
        resultado_todas = unidades.listar_Unidades(incluir_inativas=True)
        assert resultado_todas['retorno'] == 0
        assert len(resultado_todas['dados']) == 3

    def test_listar_base_vazia(self):
        """
        Testa a listagem quando não há unidades cadastradas.
        (Retorno esperado: 1)
        """
        resultado = unidades.listar_Unidades()
        assert resultado['retorno'] == 1
        assert resultado['dados'] == []


# Testes para a função relatorio_Unidade
class TestRelatorioUnidade:

    def setup_method(self):
        """
        Configuração complexa para o teste de relatório.
        Cria produtos, funcionários e vendas (carrinhos) em datas específicas.
        """
        # Produtos
        self.p1 = produto.registrar_produto("Arroz", "MarcaA", "Grãos", "7890000000017", 1.0, 5.0)['dados']
        
        # Funcionários
        self.f1 = funcionario.Funcionario("João", 101, "Caixa", "2023/01/10")
        self.f2 = funcionario.Funcionario("Maria", 102, "Gerente", "2023/03/15", data_desligamento="2023/05/20")
        
        # Vendas (Carrinhos)
        carrinho1 = carrinho.Carrinho(id=1001)
        carrinho1.adiciona_no_carrinho(self.p1, 2) # Total 10.0
        carrinho1.calcula_total()
        carrinho1.data_hora = "2023/04/15" # Dentro do período
        carrinho1.funcionario = self.f1
        
        carrinho2 = carrinho.Carrinho(id=1002)
        carrinho2.adiciona_no_carrinho(self.p1, 5) # Total 25.0
        carrinho2.calcula_total()
        carrinho2.data_hora = "2023/06/25" # Fora do período
        carrinho2.funcionario = self.f1

        # Unidade
        unidades.adiciona_Unidade(
            codigo=1,
            nome="Unidade Relatório",
            localizacao=(-10.0, -10.0),
            funcionarios=[self.f1, self.f2],
            vendas=[carrinho1, carrinho2]
        )
        unidades.adiciona_Unidade(2, "Unidade Vazia", (-11.0, -11.0))
        unidades.adiciona_Unidade(3, "Unidade Inativa", (-12.0, -12.0))
        unidades.remove_Unidade(3)


    def test_relatorio_sucesso(self):
        """
        Testa a geração de um relatório completo com dados válidos.
        (Retorno esperado: 0)
        """
        periodo = ("2023/03/01", "2023/05/30")
        resultado = unidades.relatorio_Unidade(1, periodo)
        
        assert resultado['retorno'] == 0
        assert resultado['mensagem'] == 'Relatório completo gerado'
        
        dados = resultado['dados']
        assert dados['codigo'] == 1
        assert len(dados['vendas_no_periodo']) == 1
        assert dados['vendas_no_periodo'][0]['id_venda'] == 1001
        
        mov_funcs = dados['movimentacoes_funcionarios']
        assert len(mov_funcs) == 2
        assert any(m['evento'] == 'Contratação' and m['codigo'] == 102 for m in mov_funcs)
        assert any(m['evento'] == 'Desligamento' and m['codigo'] == 102 for m in mov_funcs)


    def test_relatorio_sem_dados_no_periodo(self):
        """
        Testa a geração de um relatório para um período sem movimentações.
        (Retorno esperado: 1)
        """
        periodo = ("2024/01/01", "2024/01/31")
        resultado = unidades.relatorio_Unidade(1, periodo)
        assert resultado['retorno'] == 1
        assert resultado['mensagem'] == 'Sem dados'

    def test_relatorio_unidade_nao_encontrada(self):
        """
        Testa a tentativa de gerar relatório para uma unidade inexistente.
        (Retorno esperado: 2)
        """
        periodo = ("2023/01/01", "2023/12/31")
        resultado = unidades.relatorio_Unidade(codigo=999, periodo=periodo)
        assert resultado['retorno'] == 2
        assert resultado['mensagem'] == 'Unidade não encontrada'

    def test_relatorio_periodo_invalido(self):
        """
        Testa a falha com períodos inválidos (data futura, data de início após a de fim).
        (Retorno esperado: 3)
        """
        amanha = (date.today() + timedelta(days=1)).strftime("%Y/%m/%d")
        futuro = ("2030/01/01", "2030/01/31")
        invertido = ("2023/12/31", "2023/01/01")

        # Testa com período no futuro (relativo a hoje)
        res_futuro_hoje = unidades.relatorio_Unidade(1, (amanha, amanha))
        assert res_futuro_hoje['retorno'] == 3
        assert res_futuro_hoje['mensagem'] == 'Período inválido'
        
        # Testa com período com data de início > data de fim
        res_invertido = unidades.relatorio_Unidade(1, invertido)
        assert res_invertido['retorno'] == 3
        assert res_invertido['mensagem'] == 'Período inválido'


    def test_relatorio_parametro_nulo(self):
        """
        Testa a falha com parâmetros nulos.
        (Retorno esperado: 4)
        """
        assert unidades.relatorio_Unidade(None, ("2023/01/01", "2023/01/31"))['retorno'] == 4
        assert unidades.relatorio_Unidade(1, None)['retorno'] == 4
        
    def test_relatorio_parametro_incorreto(self):
        """
        Testa a falha com tipos de parâmetros ou formatos incorretos.
        (Retorno esperado: 5)
        """
        assert unidades.relatorio_Unidade("1", ("2023/01/01", "2023/01/31"))['retorno'] == 5
        assert unidades.relatorio_Unidade(1, ["2023/01/01", "2023/01/31"])['retorno'] == 5
        assert unidades.relatorio_Unidade(1, ("2023-01-01", "2023-01-31"))['retorno'] == 5 # Formato de data errado