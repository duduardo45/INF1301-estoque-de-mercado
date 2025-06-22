from modulos.carrinho import *
from modulos.estoque import *
from modulos.funcionario import * # consultar_funcionario
from modulos.produto import *
from modulos.unidades import * # listar_Unidades, consulta_Unidade

unidade_ativa = None
usuario_atual = None
carrinho_atual = None

def carregar_dados():
    carregar_carrinhos()
    carregar_estoques()
    carregar_funcionarios()
    carregar_unidades()

def salvar_dados():
    salvar_carrinhos()
    salvar_estoques()
    salvar_funcionarios()
    salvar_unidades()


def selecionar_unidade():
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
            pass
        elif escolha == '1':
            unidades = listar_Unidades(incluir_inativas=False)
            if unidades['retorno'] != 0:
                print("Nenhuma unidade disponível.")
                return

            print("\n--- Unidades Disponíveis ---")
            for u in unidades['dados']:
                print(f"[{u.codigo}] {u.nome}")

            codigo = input("Digite o código da unidade: ")
            try:
                codigo = int(codigo)
            except ValueError:
                print("Código inválido.")
                return

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
    codigo = input("Digite seu código de funcionário (ou 0 para voltar): ")
    if codigo == '0':
        return None
    
    try:
            codigo = int(codigo)
    except ValueError:
        print("Código inválido.")
        return
    resultado = consultar_funcionario(codigo)
    if resultado['retorno'] == 0:
        funcionario_atual = resultado['dados']
        print(f"Funcionário '{funcionario_atual.nome}' identificado.")
        return funcionario_atual
    else:
        print(resultado['mensagem'])
        return None


def menu_funcionario():
    while True:
        print("\nMenu do Funcionário")
        print("1 - Gerenciar produtos")
        print("2 - Gerenciar estoque")
        print("3 - Gerenciar funcionários")
        print("4 - Realizar venda")
        print("5 - Gerenciar unidade")
        print("0 - Voltar")
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
    while True:
        print("\nMenu do Cliente")
        print("1 - Visualizar produtos disponíveis na exposição")
        print("2 - Menu de todos os produtos")
        print("3 - Adicionar itens ao carrinho")
        print("4 - Remover itens do carrinho")
        print("5 - Listar itens do carrinho")
        print("6 - Finalizar compra") # estilo self-checkout
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            opcao_listar_todos_produtos_exibicao()
            pass
        elif escolha == '2':
            menu_produtos_disponiveis()
        elif escolha == '3':
            opcao_adicionar_item_ao_carrinho()
            pass
        elif escolha == '4':
            opcao_remover_item_do_carrinho()
            pass
        elif escolha == '5':
            opcao_listar_itens_do_carrinho()
            pass
        elif escolha == '6':
            menu_finalizar_compra_cliente()
        elif escolha == '0':
            global usuario_atual
            usuario_atual = None
            return
        else:
            print("Opção inválida.")


def main():
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

    print("\n\nObrigado por usar o sistema!")
    salvar_dados()




# Menus auxiliares com opções descritas:
def menu_gerenciar_produtos():
    print("\nGerenciar Produtos")
    print("1 - Registrar novo produto")
    print("2 - Atualizar produto existente")
    print("3 - Verificar produtos disponíveis")
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
    print("\nGerenciar Estoque")
    print("1 - Registrar produto no estoque")
    print("2 - Adicionar quantidade")
    print("3 - Mover produto para exposição")
    print("4 - Consultar quantidade e capacidade de um produto")
    print("5 - Atualizar capacidade de um produto")
    print("6 - Excluir registro de produto do estoque")
    print("7 - Listar todos os produtos")
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
    print("\nRelatórios da Unidade")
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
    print("\nCatálogo de Produtos")
    print("1 - Listar todos os produtos")
    print("2 - Pesquisar produto por nome ou categoria")
    print("3 - Verificar produto por codigo")
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


def opcao_registra_nova_unidade(): pass
def opcao_registrar_novo_produto(): pass
def opcao_atualizar_produto_existente(): pass
def opcao_registrar_produto_no_estoque(): pass
def opcao_adicionar_quantidade_estoque(): pass
def opcao_mover_produto_para_exposicao(): pass
def opcao_consultar_quantidade_estoque(): pass
def opcao_atualizar_capacidade_produto(): pass
def opcao_excluir_produto_estoque(): pass
def opcao_listar_todos_produtos_estoque(): pass
def opcao_listar_todos_produtos_exibicao(): pass
def opcao_listar_produtos_em_falta(): pass
def opcao_verificar_consistencia_estoque(): pass
def opcao_admitir_novo_funcionario(): pass
def opcao_atualizar_funcionario(): pass
def opcao_desligar_funcionario(): pass
def opcao_consultar_funcionario_por_codigo(): pass
def opcao_consultar_funcionario_por_nome(): pass
def opcao_listar_funcionarios_unidade(): pass
def opcao_criar_novo_carrinho(): pass
def opcao_adicionar_item_ao_carrinho(): pass
def opcao_remover_item_do_carrinho(): pass
def opcao_listar_itens_do_carrinho(): pass
def opcao_limpar_carrinho(): pass
def opcao_finalizar_venda(): pass
def opcao_gerar_relatorio_movimentacoes(): pass
def opcao_consultar_dados_unidade(): pass
def opcao_atualizar_atributos_unidade(): pass
def opcao_listar_todos_produtos(): pass
def opcao_pesquisar_produto_nome_ou_categoria(): pass
def opcao_verificar_produto_por_codigo(): pass
def opcao_finalizar_e_pagar_compra(): pass


if __name__ == '__main__':
    main()
