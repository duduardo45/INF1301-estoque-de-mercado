from modulos.carrinho import *
from modulos.estoque import *
from modulos.funcionario import * # consultar_funcionario
from modulos.produto import *
from modulos.unidades import * # listar_Unidades, consulta_Unidade
from gera_json import gera_dados_teste

unidade_ativa = None
usuario_atual = None
carrinho_atual = None

def carregar_dados():
    """Carrega todos os dados dos arquivos JSON para a memória."""
    carregar_produtos()
    carregar_funcionarios()
    carregar_estoques()
    carregar_carrinhos()
    carregar_unidades()

def salvar_dados():
    """Salva todos os dados da memória para os arquivos JSON."""
    salvar_produtos()
    salvar_funcionarios()
    salvar_estoques()
    salvar_carrinhos()
    salvar_unidades()


def selecionar_unidade():
    """Permite que o usuário selecione uma unidade existente ou registre uma nova."""
    while True:
        print("\nSeleção de Unidade")
        print("1 - Acessar unidade existente")
        print("2 - Registrar nova unidade")
        print("0 - Sair do sistema")
        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            return 'sair'
        elif escolha == '2':
            opcao_registra_nova_unidade()
        elif escolha == '1':
            unidades = listar_Unidades(incluir_inativas=False)
            if unidades['retorno'] != 0:
                print("Nenhuma unidade ativa disponível.")
                continue

            print("\n--- Unidades Disponíveis ---")
            for u in unidades['dados']:
                print(f"[{u.codigo}] {u.nome}")

            codigo = input("Digite o código da unidade: ")
            try:
                codigo = int(codigo)
            except ValueError:
                print("Código inválido.")
                continue

            resultado = consulta_Unidade(codigo)
            if resultado['retorno'] == 0:
                unidade_escolhida = resultado['dados']
                print(f"Unidade '{unidade_escolhida.nome}' selecionada com sucesso.")
                return unidade_escolhida
            else:
                print(resultado['mensagem'])
        else:
            print("Opção inválida. Tente novamente.")

def identificar_usuario():
    """Permite a identificação como funcionário ou cliente."""
    print("\nIdentificação de Usuário")
    print("1 - Funcionário")
    print("2 - Cliente")
    print("0 - Voltar")
    opcao = input("Você é: ")
    if opcao == '1':
        return identificar_funcionario()
    elif opcao == '2':
        return 'cliente'
    elif opcao == '0':
        global unidade_ativa
        unidade_ativa = None
        return None
    else:
        print("Opção inválida.")
        return None

def identificar_funcionario():
    """Identifica um funcionário pelo seu código."""
    codigo = input("Digite seu código de funcionário (ou 0 para voltar): ")
    if codigo == '0':
        return None
    
    try:
        codigo = int(codigo)
    except ValueError:
        print("Código inválido.")
        return None
    
    # Verifica se o funcionário pertence à unidade ativa
    if unidade_ativa:
        for f in unidade_ativa.funcionarios:
            if f.codigo == codigo:
                if f.ativo():
                    print(f"Funcionário '{f.nome}' identificado.")
                    return f
                else:
                    print("Este funcionário está inativo.")
                    return None
        print("Funcionário não encontrado nesta unidade.")
        return None
    else:
        print("Nenhuma unidade selecionada.")
        return None


def menu_funcionario():
    """Exibe o menu principal para funcionários."""
    while True:
        print("\nMenu do Funcionário")
        print("1 - Gerenciar produtos")
        print("2 - Gerenciar estoque")
        print("3 - Gerenciar funcionários")
        print("4 - Realizar venda")
        print("5 - Gerenciar unidade")
        print("0 - Sair (Trocar de Usuário)")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_produtos()
        elif escolha == '2':
            menu_gerenciar_estoque()
        elif escolha == '3':
            menu_gerenciar_funcionarios()
        elif escolha == '4':
            menu_vendas_funcionario() # carrinho e vendas
        elif escolha == '5':
            menu_gerenciar_unidade()
        elif escolha == '0':
            global usuario_atual
            usuario_atual = None
            return
        else:
            print("Opção inválida.")


def menu_cliente():
    """Exibe o menu principal para clientes."""
    global carrinho_atual
    if not carrinho_atual:
        opcao_criar_novo_carrinho()

    while True:
        print("\nMenu do Cliente")
        print("1 - Visualizar produtos disponíveis na exposição")
        print("2 - Catálogo completo de produtos")
        print("3 - Adicionar itens ao carrinho")
        print("4 - Remover itens do carrinho")
        print("5 - Listar itens do carrinho")
        print("6 - Finalizar compra") # estilo self-checkout
        print("0 - Sair (Trocar de Usuário)")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            opcao_listar_todos_produtos_exibicao()
        elif escolha == '2':
            menu_produtos_disponiveis()
        elif escolha == '3':
            opcao_adicionar_item_ao_carrinho()
        elif escolha == '4':
            opcao_remover_item_do_carrinho()
        elif escolha == '5':
            opcao_listar_itens_do_carrinho()
        elif escolha == '6':
            menu_finalizar_compra_cliente()
        elif escolha == '0':
            global usuario_atual
            usuario_atual = None
            carrinho_atual = None # Limpa o carrinho ao sair
            return
        else:
            print("Opção inválida.")


def main():
    """Função principal que executa o loop do programa."""
    global unidade_ativa, usuario_atual
    print("Bem-vindo ao sistema de gestão de unidades!")
    carregar_dados()
    while True:
        if unidade_ativa is None:
            unidade_ativa = selecionar_unidade()
            if unidade_ativa == 'sair':
                break
            continue

        if usuario_atual is None:
            usuario_atual = identificar_usuario()
            continue

        if usuario_atual == 'cliente':
            menu_cliente()
        elif hasattr(usuario_atual, 'nome'):  # Funcionário
            menu_funcionario()

    print("\nSalvando dados...")
    salvar_dados()
    print("Obrigado por usar o sistema!")


# Menus auxiliares com opções descritas:
def menu_gerenciar_produtos():
    """Menu para gerenciar o catálogo global de produtos."""
    while True:
        print("\nGerenciar Produtos")
        print("1 - Registrar novo produto")
        print("2 - Atualizar produto existente")
        print("3 - Catálogo de produtos")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_registrar_novo_produto()
        elif opcao == "2":
            opcao_atualizar_produto_existente()
        elif opcao == "3":
            menu_produtos_disponiveis()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_gerenciar_estoque():
    """Menu para gerenciar o estoque da unidade ativa."""
    while True:
        print("\nGerenciar Estoque")
        print("1 - Registrar produto no estoque da unidade")
        print("2 - Adicionar quantidade")
        print("3 - Mover produto para exposição")
        print("4 - Consultar quantidade e capacidade de um produto")
        print("5 - Atualizar capacidade de um produto")
        print("6 - Excluir registro de produto do estoque")
        print("7 - Listar todos os produtos no estoque da unidade")
        print("8 - Listar produtos em falta")
        print("9 - Verificar consistência do estoque")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_registrar_produto_no_estoque()
        elif opcao == "2":
            opcao_adicionar_quantidade_estoque()
        elif opcao == "3":
            opcao_mover_produto_para_exposicao()
        elif opcao == "4":
            opcao_consultar_quantidade_estoque()
        elif opcao == "5":
            opcao_atualizar_capacidade_produto()
        elif opcao == "6":
            opcao_excluir_produto_estoque()
        elif opcao == "7":
            opcao_listar_todos_produtos_estoque()
        elif opcao == "8":
            opcao_listar_produtos_em_falta()
        elif opcao == "9":
            opcao_verificar_consistencia_estoque()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_gerenciar_funcionarios():
    """Menu para gerenciar os funcionários da unidade ativa."""
    while True:
        print("\nGerenciar Funcionários")
        print("1 - Admitir novo funcionário")
        print("2 - Atualizar dados de funcionário")
        print("3 - Desligar funcionário")
        print("4 - Consultar funcionário por código")
        print("5 - Consultar funcionário por nome")
        print("6 - Listar todos os funcionários da unidade")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_admitir_novo_funcionario()
        elif opcao == "2":
            opcao_atualizar_funcionario()
        elif opcao == "3":
            opcao_desligar_funcionario()
        elif opcao == "4":
            opcao_consultar_funcionario_por_codigo()
        elif opcao == "5":
            opcao_consultar_funcionario_por_nome()
        elif opcao == "6":
            opcao_listar_funcionarios_unidade()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_vendas_funcionario():
    """Menu para funcionários realizarem vendas."""
    global carrinho_atual
    if not carrinho_atual:
        print("\nNenhum carrinho ativo. Crie um para começar.")
    
    while True:
        print("\nRealizar Venda")
        print("1 - Criar novo carrinho")
        print("2 - Adicionar item ao carrinho")
        print("3 - Remover item do carrinho")
        print("4 - Listar itens do carrinho")
        print("5 - Limpar carrinho")
        print("6 - Finalizar venda")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_criar_novo_carrinho()
        elif opcao == "2":
            opcao_adicionar_item_ao_carrinho()
        elif opcao == "3":
            opcao_remover_item_do_carrinho()
        elif opcao == "4":
            opcao_listar_itens_do_carrinho()
        elif opcao == "5":
            opcao_limpar_carrinho()
        elif opcao == "6":
            opcao_finalizar_venda()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_gerenciar_unidade():
    """Menu para consultar e gerenciar a unidade ativa."""
    while True:
        print("\nGerenciar Unidade")
        print("1 - Gerar relatório de movimentações e vendas por período")
        print("2 - Consultar dados da unidade atual")
        print("3 - Atualizar atributos da unidade")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_gerar_relatorio_movimentacoes()
        elif opcao == "2":
            opcao_consultar_dados_unidade()
        elif opcao == "3":
            opcao_atualizar_atributos_unidade()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_produtos_disponiveis():
    """Menu para clientes e funcionários visualizarem o catálogo de produtos."""
    while True:
        print("\nCatálogo de Produtos")
        print("1 - Listar todos os produtos")
        print("2 - Pesquisar produto por nome ou categoria")
        print("3 - Verificar produto por código")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_listar_todos_produtos()
        elif opcao == "2":
            opcao_pesquisar_produto_nome_ou_categoria()
        elif opcao == "3":
            opcao_verificar_produto_por_codigo()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_finalizar_compra_cliente():
    """Menu para o cliente finalizar a compra."""
    print("\nFinalizar Compra")
    print("1 - Finalizar e pagar compra")
    print("0 - Voltar")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        opcao_finalizar_e_pagar_compra()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")


# --- Implementação das Funções de Interface ---

def opcao_registra_nova_unidade():
    print("\n--- Registro de Nova Unidade ---")
    try:
        codigo = int(input("Digite o código da nova unidade: "))
        nome = input("Digite o nome da nova unidade: ")
        lat = float(input("Digite a latitude: "))
        lon = float(input("Digite a longitude: "))
    except ValueError:
        print("Entrada inválida. Código, latitude e longitude devem ser números.")
        return

    localizacao = (lat, lon)
    resultado = adiciona_Unidade(codigo=codigo, nome=nome, localizacao=localizacao)
    print(resultado['mensagem'])

def opcao_registrar_novo_produto():
    print("\n--- Registrar Novo Produto ---")
    try:
        codigo = input("Código de barras (EAN-13): ")
        nome = input("Nome do produto: ")
        marca = input("Marca: ")
        categoria = input("Categoria: ")
        peso = float(input("Peso: "))
        preco = float(input("Preço: "))
        
        preco_por_peso = None
        vendido_por_peso = input("Vendido por peso? (s/n): ").lower()
        if vendido_por_peso == 's':
            preco_por_peso = float(input("Preço por peso (ex: preço/kg): "))

        resultado = registrar_produto(nome, marca, categoria, codigo, peso, preco, preco_por_peso)
        print(resultado['mensagem'])

    except ValueError:
        print("Entrada inválida. Peso e preço devem ser números.")

def opcao_atualizar_produto_existente():
    print("\n--- Atualizar Produto Existente ---")
    codigo = input("Digite o código do produto a ser atualizado: ")
    
    consulta = consultar_produto_por_codigo(codigo)
    if consulta['retorno'] != 0:
        print(consulta['mensagem'])
        return
    
    produto = consulta['dados']
    print(f"Atualizando produto: {produto.nome} ({produto.codigo})")
    
    dados_atualizacao = {}
    campos = ["nome", "marca", "categoria", "peso", "preco", "preco_por_peso"]
    
    for campo in campos:
        novo_valor = input(f"Novo valor para '{campo}' (ou pressione Enter para pular): ")
        if novo_valor:
            if campo in ["peso", "preco", "preco_por_peso"]:
                try:
                    dados_atualizacao[campo] = float(novo_valor)
                except ValueError:
                    print(f"Valor inválido para {campo}. Pulando.")
            else:
                dados_atualizacao[campo] = novo_valor

    if not dados_atualizacao:
        print("Nenhum dado para atualizar.")
        return

    resultado = atualizar_produto(codigo, dados_atualizacao)
    print(resultado['mensagem'])


def opcao_registrar_produto_no_estoque():
    global unidade_ativa
    print("\n--- Registrar Produto no Estoque da Unidade ---")
    codigo = input("Digite o código do produto (EAN-13): ")
    
    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    
    produto = res_prod['dados']

    try:
        cap_estoque = int(input("Capacidade no estoque interno: "))
        cap_exposicao = int(input("Capacidade na exposição (prateleira): "))
    except ValueError:
        print("Capacidades devem ser números inteiros.")
        return
        
    resultado = unidade_ativa.estoque.registrar_produto(produto, cap_estoque, cap_exposicao)
    print(resultado['mensagem'])


def opcao_adicionar_quantidade_estoque():
    global unidade_ativa
    print("\n--- Adicionar Quantidade ao Estoque ---")
    codigo = input("Digite o código do produto: ")
    
    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']

    try:
        quantidade = int(input("Quantidade a adicionar: "))
    except ValueError:
        print("Quantidade deve ser um número inteiro.")
        return

    destino_in = input("Adicionar em (1 - Estoque interno, 2 - Exposição): ")
    destino = 'estoque' if destino_in == '1' else 'exposicao'
    
    resultado = unidade_ativa.estoque.adicionar_produto(produto, quantidade, destino)
    print(resultado['mensagem'])


def opcao_mover_produto_para_exposicao():
    global unidade_ativa
    print("\n--- Mover Produto para Exposição ---")
    codigo = input("Digite o código do produto: ")

    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']
    
    try:
        quantidade = int(input("Quantidade a mover: "))
    except ValueError:
        print("Quantidade deve ser um número inteiro.")
        return

    resultado = unidade_ativa.estoque.mover_para_exposicao(produto, quantidade)
    print(resultado['mensagem'])


def opcao_consultar_quantidade_estoque():
    global unidade_ativa
    print("\n--- Consultar Quantidade de Produto ---")
    codigo = input("Digite o código do produto: ")

    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']

    resultado = unidade_ativa.estoque.consultar_quantidade(produto)
    if resultado['retorno'] == 0:
        dados = resultado['dados']
        print(f"Produto: {produto.nome} ({produto.codigo})")
        print(f"  Estoque Interno: {dados['estoque']} / {dados['capacidade_estoque']}")
        print(f"  Exposição: {dados['exposicao']} / {dados['capacidade_exposicao']}")
    else:
        print(resultado['mensagem'])


def opcao_atualizar_capacidade_produto():
    global unidade_ativa
    print("\n--- Atualizar Capacidade de Produto ---")
    codigo = input("Digite o código do produto: ")

    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']

    try:
        cap_est = input("Nova capacidade de estoque (Enter para pular): ")
        cap_exp = input("Nova capacidade de exposição (Enter para pular): ")
        
        cap_estoque = int(cap_est) if cap_est else None
        cap_exposicao = int(cap_exp) if cap_exp else None
        
        resultado = unidade_ativa.estoque.atualizar_capacidades(produto, cap_estoque, cap_exposicao)
        print(resultado['mensagem'])

    except ValueError:
        print("Capacidades devem ser números inteiros.")


def opcao_excluir_produto_estoque():
    global unidade_ativa
    print("\n--- Excluir Registro de Produto do Estoque ---")
    codigo = input("Digite o código do produto: ")

    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']
    
    resultado = unidade_ativa.estoque.remover_produto(produto)
    print(resultado['mensagem'])


def opcao_listar_todos_produtos_estoque():
    global unidade_ativa
    print(f"\n--- Produtos no Estoque da Unidade '{unidade_ativa.nome}' ---")
    resultado = unidade_ativa.estoque.listar_produtos(detalhado=True)
    if not resultado['dados']:
        print("Nenhum produto registrado neste estoque.")
        return
        
    for item in resultado['dados']:
        print(f"Cód: {item['codigo']} | Estoque: {item['estoque']}/{item['capacidade_estoque']} | Exposição: {item['exposicao']}/{item['capacidade_exposicao']}")


def opcao_listar_todos_produtos_exibicao():
    global unidade_ativa
    print(f"\n--- Produtos em Exposição na Unidade '{unidade_ativa.nome}' ---")
    
    produtos_em_exposicao = [
        (p, qtd) for p, qtd in unidade_ativa.estoque.exposicao.items() if qtd > 0
    ]

    if not produtos_em_exposicao:
        print("Nenhum produto em exposição no momento.")
        return

    for produto, quantidade in produtos_em_exposicao:
        print(f"{produto.__str__()} | Quantidade Disponível: {quantidade}")

def opcao_listar_produtos_em_falta():
    global unidade_ativa
    print("\n--- Listar Produtos em Falta ---")
    tipo_in = input("Listar faltas em (1 - Estoque interno, 2 - Exposição, 3 - Ambos): ")
    
    if tipo_in == '1': tipo = 'estoque'
    elif tipo_in == '2': tipo = 'exposicao'
    else: tipo = 'ambos'

    resultado = unidade_ativa.estoque.listar_em_falta(tipo)
    if not resultado['dados']:
        print("Nenhum produto em falta.")
    else:
        print(f"Códigos dos produtos em falta: {', '.join(resultado['dados'])}")


def opcao_verificar_consistencia_estoque():
    global unidade_ativa
    print("\n--- Verificando Consistência do Estoque ---")
    resultado = unidade_ativa.estoque.verificar_consistencia()
    print(resultado['mensagem'])
    if resultado['retorno'] != 0:
        for inconsistencia in resultado['dados']:
            print(f"  Produto Cód: {inconsistencia['codigo']}")
            for problema in inconsistencia['problemas']:
                print(f"    - {problema}")


def opcao_admitir_novo_funcionario():
    global unidade_ativa
    print("\n--- Admitir Novo Funcionário ---")
    try:
        codigo = int(input("Código do novo funcionário: "))
        nome = input("Nome completo: ")
        cargo = input("Cargo: ")
    except ValueError:
        print("Código deve ser um número inteiro.")
        return
    
    # Adiciona ao sistema global de funcionários
    resultado_global = novo_funcionario(nome, codigo, cargo)
    print(resultado_global['mensagem'])
    
    # Se foi sucesso, adiciona na unidade ativa
    if resultado_global['retorno'] == 0:
        consulta = consultar_funcionario(codigo)
        if consulta['retorno'] == 0:
            novo_func_obj = consulta['dados']
            unidade_ativa.funcionarios.append(novo_func_obj)
            print(f"Funcionário '{nome}' adicionado à unidade '{unidade_ativa.nome}'.")
        else:
            print("Erro ao recuperar funcionário para adicionar à unidade.")


def opcao_atualizar_funcionario():
    print("\n--- Atualizar Dados de Funcionário ---")
    try:
        codigo = int(input("Código do funcionário a ser atualizado: "))
    except ValueError:
        print("Código inválido.")
        return

    # Procura o funcionário na unidade ativa
    func_obj = None
    for f in unidade_ativa.funcionarios:
        if f.codigo == codigo:
            func_obj = f
            break
    
    if not func_obj:
        print("Funcionário não encontrado nesta unidade.")
        return

    print(f"Atualizando: {func_obj.nome}")
    atributo = input("Qual atributo deseja atualizar (nome, cargo): ").lower()
    if atributo not in ["nome", "cargo"]:
        print("Atributo inválido.")
        return
        
    valor = input(f"Novo valor para '{atributo}': ")
    resultado = func_obj.atualizar(atributo, valor)
    print(resultado['mensagem'])


def opcao_desligar_funcionario():
    print("\n--- Desligar Funcionário ---")
    try:
        codigo = int(input("Código do funcionário a ser desligado: "))
    except ValueError:
        print("Código inválido.")
        return

    func_obj = None
    for f in unidade_ativa.funcionarios:
        if f.codigo == codigo:
            func_obj = f
            break
            
    if not func_obj:
        print("Funcionário não encontrado nesta unidade.")
        return

    resultado = func_obj.desligar_funcionario()
    print(resultado['mensagem'])


def opcao_consultar_funcionario_por_codigo():
    print("\n--- Consultar Funcionário por Código ---")
    try:
        codigo = int(input("Digite o código do funcionário: "))
    except ValueError:
        print("Código inválido.")
        return

    resultado = consultar_funcionario(codigo, incluir_inativos=True)
    if resultado['retorno'] == 0:
        print(resultado['dados'].__str__())
    else:
        print(resultado['mensagem'])


def opcao_consultar_funcionario_por_nome():
    print("\n--- Consultar Funcionário por Nome ---")
    nome = input("Digite o nome ou parte do nome a ser buscado: ")
    resultado = consultar_funcionario_por_nome(nome, incluir_inativos=True)
    
    print(resultado['mensagem'])
    if resultado['retorno'] == 0:
        for func in resultado['dados']:
            print(f"- {func.__str__()}")


def opcao_listar_funcionarios_unidade():
    global unidade_ativa
    print(f"\n--- Funcionários da Unidade '{unidade_ativa.nome}' ---")
    
    incluir_inativos = input("Incluir funcionários inativos? (s/n): ").lower() == 's'
    
    lista_filtrada = [
        f for f in unidade_ativa.funcionarios if incluir_inativos or f.ativo()
    ]
    
    if not lista_filtrada:
        print("Nenhum funcionário para exibir.")
        return

    for func in lista_filtrada:
        print(func.__str__())


def opcao_criar_novo_carrinho():
    global carrinho_atual
    if carrinho_atual and carrinho_atual.itens:
        confirm = input("Já existe um carrinho ativo. Deseja criar um novo e limpar o anterior? (s/n): ").lower()
        if confirm != 's':
            return

    resultado = criar_carrinho()
    carrinho_atual = resultado['dados']
    print(resultado['mensagem'])


def opcao_adicionar_item_ao_carrinho():
    global carrinho_atual, unidade_ativa
    if not carrinho_atual:
        print("Nenhum carrinho ativo. Crie um novo primeiro.")
        return
    
    codigo = input("Digite o código do produto para adicionar: ")
    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']

    # Verifica se o produto está na exposição da unidade
    if produto not in unidade_ativa.estoque.exposicao or unidade_ativa.estoque.exposicao[produto] <= 0:
        print("Produto indisponível na exposição.")
        return

    try:
        qtd = float(input("Digite a quantidade: "))
    except ValueError:
        print("Quantidade inválida.")
        return

    resultado = carrinho_atual.adiciona_no_carrinho(produto, qtd)
    print(resultado['mensagem'])


def opcao_remover_item_do_carrinho():
    global carrinho_atual
    if not carrinho_atual or not carrinho_atual.itens:
        print("Carrinho está vazio.")
        return
        
    codigo = input("Digite o código do produto para remover: ")
    res_prod = consultar_produto_por_codigo(codigo)
    if res_prod['retorno'] != 0:
        print(res_prod['mensagem'])
        return
    produto = res_prod['dados']

    try:
        qtd = float(input("Digite a quantidade a remover: "))
    except ValueError:
        print("Quantidade inválida.")
        return
    
    resultado = carrinho_atual.remover_do_carrinho(produto, qtd)
    print(resultado['mensagem'])


def opcao_listar_itens_do_carrinho():
    global carrinho_atual
    if not carrinho_atual:
        print("Nenhum carrinho ativo.")
        return

    resultado = carrinho_atual.listar_itens(verbose=True)
    print("\n--- Itens no Carrinho ---")
    if resultado['retorno'] != 0:
        print(resultado['mensagem'])
    else:
        for item_str in resultado['dados']:
            print(f"- {item_str}")
        total = carrinho_atual.calcula_total()
        print("-------------------------")
        print(f"Total: R$ {total:.2f}")


def opcao_limpar_carrinho():
    global carrinho_atual
    if not carrinho_atual:
        print("Nenhum carrinho ativo.")
        return
    
    resultado = carrinho_atual.limpar_carrinho()
    print(resultado['mensagem'])


def _finalizar_compra_logica():
    global carrinho_atual, unidade_ativa, usuario_atual
    if not carrinho_atual or not carrinho_atual.itens:
        print("O carrinho está vazio.")
        return

    total = carrinho_atual.calcula_total()
    print(f"Total da compra: R$ {total:.2f}")
    
    confirm = input("Confirmar e finalizar a compra? (s/n): ").lower()
    if confirm != 's':
        print("Compra cancelada.")
        return

    # Tenta dar baixa no estoque
    resultado_baixa = unidade_ativa.estoque.retirar_venda(carrinho_atual.itens)
    if resultado_baixa['retorno'] != 0:
        print(f"Erro ao finalizar a compra: {resultado_baixa['mensagem']}")
        print("Verifique os itens e quantidades no carrinho.")
        return
        
    # Se a baixa foi bem-sucedida, finaliza o carrinho
    funcionario_responsavel = usuario_atual if hasattr(usuario_atual, 'nome') else None
    carrinho_atual.finaliza_carrinho(funcionario=funcionario_responsavel)
    
    # Adiciona à lista de vendas da unidade
    unidade_ativa.vendas.append(carrinho_atual)
    
    print("\nCompra finalizada com sucesso!")
    
    # Limpa o carrinho atual para a próxima compra
    carrinho_atual = None
    if usuario_atual == 'cliente': # recria para o cliente poder continuar
        opcao_criar_novo_carrinho()


def opcao_finalizar_venda():
    print("\n--- Finalizar Venda (Funcionário) ---")
    _finalizar_compra_logica()


def opcao_finalizar_e_pagar_compra():
    print("\n--- Finalizar Compra (Cliente) ---")
    _finalizar_compra_logica()


def opcao_gerar_relatorio_movimentacoes():
    global unidade_ativa
    print("\n--- Gerar Relatório da Unidade ---")
    try:
        data_inicio = input("Data de início (AAAA/MM/DD): ")
        data_fim = input("Data de fim (AAAA/MM/DD): ")
    except:
        print("Formato de data inválido.")
        return

    periodo = (data_inicio, data_fim)
    resultado = relatorio_Unidade(unidade_ativa.codigo, periodo)

    print(f"\n{resultado['mensagem']}")
    if resultado['retorno'] == 0:
        dados = resultado['dados']
        print(f"Relatório para: {dados['nome']} (Cód: {dados['codigo']})")
        print(f"Período: {data_inicio} a {data_fim}")
        
        print("\n--- Movimentações de Funcionários ---")
        if not dados['movimentacoes_funcionarios']:
            print("Nenhuma movimentação no período.")
        else:
            for mov in dados['movimentacoes_funcionarios']:
                print(f"  [{mov['data']}] {mov['evento']}: {mov['nome']} (Cód: {mov['codigo']})")
        
        print("\n--- Vendas no Período ---")
        if not dados['vendas_no_periodo']:
            print("Nenhuma venda no período.")
        else:
            total_vendas = 0
            for venda in dados['vendas_no_periodo']:
                print(f"  Venda ID: {venda['id_venda']} | Data: {venda['data']} | Total: R$ {venda['total']:.2f}")
                total_vendas += venda['total']
            print("---------------------------------")
            print(f"Total arrecadado no período: R$ {total_vendas:.2f}")


def opcao_consultar_dados_unidade():
    global unidade_ativa
    print("\n--- Dados da Unidade Atual ---")
    print(f"Nome: {unidade_ativa.nome}")
    print(f"Código: {unidade_ativa.codigo}")
    print(f"Localização: {unidade_ativa.localizacao}")
    print(f"Status: {'Ativa' if unidade_ativa.ativo else 'Inativa'}")
    print(f"Total de funcionários: {len(unidade_ativa.funcionarios)}")
    print(f"Total de vendas registradas: {len(unidade_ativa.vendas)}")
    print("\n--- Resumo do Estoque ---")
    print(unidade_ativa.estoque)


def opcao_atualizar_atributos_unidade():
    global unidade_ativa
    while True:
        print("\n--- Atualizar Atributos da Unidade ---")
        print("1 - Atualizar nome")
        print("2 - Atualizar localização")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            novo_nome = input("Digite o novo nome: ")
            resultado = atualiza_Unidade(unidade_ativa.codigo, 'nome', novo_nome)
            print(resultado['mensagem'])
        elif escolha == '2':
            try:
                nova_lat = float(input("Nova latitude: "))
                nova_lon = float(input("Nova longitude: "))
                nova_loc = (nova_lat, nova_lon)
                resultado = atualiza_Unidade(unidade_ativa.codigo, 'localizacao', nova_loc)
                print(resultado['mensagem'])
            except ValueError:
                print("Valores de localização inválidos.")
        elif escolha == '0':
            return
        else:
            print("Opção inválida.")


def opcao_listar_todos_produtos():
    print("\n--- Catálogo Completo de Produtos ---")
    resultado = listar_todos_produtos()
    if resultado['retorno'] != 0:
        print(resultado['mensagem'])
        return
    
    for produto in resultado['dados']:
        print(produto)


def opcao_pesquisar_produto_nome_ou_categoria():
    print("\n--- Pesquisar Produto ---")
    texto = input("Digite o nome, marca ou categoria para pesquisar: ")
    resultado = pesquisar_produto(texto)
    
    print(resultado['mensagem'])
    if resultado['retorno'] == 0 and resultado['dados']:
        for produto in resultado['dados']:
            print(f"- {produto}")


def opcao_verificar_produto_por_codigo():
    print("\n--- Verificar Produto por Código ---")
    codigo = input("Digite o código do produto (EAN-13): ")
    resultado = consultar_produto_por_codigo(codigo)
    
    if resultado['retorno'] == 0:
        print(resultado['dados'])
    else:
        print(resultado['mensagem'])


if __name__ == '__main__':
    main()
