## Repsitório para a matéria INF1310 - Programação Modular da PUC-Rio



**estrutura sugerida pro projeto:**

app/
│
├── produto.py
│   ├── class Produto
│   │   ├── calcular_valor_total(quantidade)
│   ├── adicionar_produto(produto: Produto, localidade_id)
│   ├── atualizar_produto(codigo_barras, dados)
│   ├── excluir_produto(codigo_barras)
│   ├── consultar_produto_por_codigo(codigo)
│   ├── pesquisar_produto(texto, filtros={})
│
├── estoque.py
│   ├── ajustar_estoque(codigo_produto, localidade_id, delta, tipo)
│   ├── verificar_alertas_estoque()
│   ├── prever_falta_estoque(codigo_produto, localidade_id)
│
├── venda.py
│   ├── class Venda
│   ├── criar_carrinho()
│   ├── adicionar_item_carrinho(carrinho, codigo_produto, quantidade)
│   ├── registrar_venda(carrinho, funcionario_id=None)
│   ├── gerar_historico_venda(venda)
│
├── localidade.py
│   ├── class Localidade
│   ├── adicionar_localidade(dados)
│   ├── editar_localidade(codigo, novos_dados)
│   ├── remover_localidade(codigo)
│   ├── obter_faltas(tipo="local")
│   ├── identificar_localidade_com_estoque(codigo_produto)
│
├── grupo.py
│   ├── class Grupo
│   ├── criar_grupo(nome, descricao, localidades)
│   ├── editar_grupo(nome_grupo, novos_dados)
│   ├── remover_grupo(nome_grupo)
│   ├── sincronizar_localidades_com_grupo()
│   ├── pesquisar_grupo(texto)
│
├── funcionario.py
│   ├── class Funcionario
│   ├── admitir_funcionario(dados)
│   ├── desligar_funcionario(codigo_funcionario)
│   ├── alterar_funcionario(codigo, novos_dados)
│   ├── consultar_funcionarios(filtros)
│   ├── atualizar_tabela_local_de_funcionarios()
│
├── permissao.py
│   ├── class NivelAcesso
│   ├── associar_nivel_a_posicao(posicao, niveis)
│   ├── verificar_permissao(funcionario_id, acao)
│
├── autenticacao.py
│   ├── autenticar_usuario(login, senha)
│   ├── autenticar_cracha(cracha_id, localidade_id)
│
├── relatorios.py
│   ├── gerar_relatorio(tipo, filtros)
│   ├── gerar_relatorio_estoque(localidade_id, filtros)
│   ├── gerar_relatorio_vendas(grupo_ou_rede, filtros)
│
├── alerta.py
│   ├── enviar_alerta_falta_local(produto, destino)
│   ├── enviar_alerta_falta_regional(produto, grupo)
│   ├── enviar_alerta_falta_global(produto, rede)
│
└── main.py
    ├── inicializar_banco_dados()
    ├── carregar_interface_usuario()
