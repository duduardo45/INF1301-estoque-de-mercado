## Repsitório para a matéria INF1310 - Programação Modular da PUC-Rio



**estrutura do projeto:**
```
modulos/
│
├── carrinho.py
│   ├── class Carrinho
│   │   ├── __init__(id, data_hora=None, itens=None, total=None, funcionario=None)
│   │   ├── adiciona_no_carrinho(produto, quantidade)
│   │   ├── remover_do_carrinho(produto, quantidade)
│   │   ├── calcula_total()
│   │   ├── listar_itens(verbose=False)
│   │   ├── limpar_carrinho()
│   │   ├── finaliza_carrinho(funcionario=None)
│
├── estoque.py
│   ├── class Estoque
│   │   ├── __init__(codigo, estoque= None, exposicao= None, capacidades= None)
│   │   ├── __str__()
│   │   ├── registrar_produto(produto, capacidade_estoque, capacidade_exposicao)
│   │   ├── remover_produto(produto)
│   │   ├── listar_em_falta(tipo='ambos')
│   │   ├── percentual_ocupado(produto)
│   │   ├── listar_produtos(detalhado=False)
│   │   ├── atualizar_capacidades(produto, capacidade_estoque=None, capacidade_exposicao=None)
│   │   ├── adicionar_produto(produto, quantidade, destino='estoque')
│   │   ├── mover_para_exposicao(produto, quantidade)
│   │   ├── retirar_venda(venda_dict)
│   │   ├── produto_existe(produto)
│   │   ├── consultar_quantidade(produto)
│   │   ├── verificar_consistencia()
│   ├── registrar_estoque(codigo)
│   ├── listar_todos_estoques()
│
├── funcionario.py
│   ├── class Funcionario
│   │   ├── __init__(nome, codigo, cargo, data_contratacao, data_desligamento=None)
│   │   ├── __str__(resumo_vendas: tuple[int, float] = None)
│   │   ├── atualizar(atributo, valor)
│   │   ├── desligar_funcionario(data_desligamento=None)
│   │   ├── ativo()
│   ├── adiciona_funcionario(nome, codigo, cargo, data_contratacao)
│   ├── novo_funcionario(nome, codigo, cargo)
│   ├── consultar_funcionario(codigo, incluir_inativos=False)
│   ├── consultar_funcionarios_por_nome(nome, incluir_inativos=False)
│   ├── listar_todos_funcionarios(incluir_inativos=False)
│
├── produto.py
│   ├── class Produto
│   │   ├── __init__(nome, marca, categoria, codigo, peso, preco, preco_por_peso=None)
│   │   ├── __str__(quantidade=None)
│   │   ├── calcula_preco(quantidade)
│   ├── consultar_produto_por_codigo(codigo)
│   ├── registrar_produto(nome, marca, categoria, codigo, peso, preco, preco_por_peso=None)
│   ├── atualizar_produto(codigo, novos_dados)
│   ├── pesquisar_produto(texto, filtros={})
│   ├── listar_todos_produtos()
│
├── unidades.py
│   ├── class Localidade
│   │   ├── __init__(nome, codigo, estoque, localizacao, funcionarios, vendas, ativo=True)
│   │   ├── atualizar(atributo, valor)
│   ├── adiciona_Unidade(codigo, nome, localizacao, estoque=None, funcionarios=None, vendas=None)
│   ├── remove_Unidade(codigo)
│   ├── consulta_Unidade(codigo)
│   ├── listar_Unidades(incluir_inativas=False)
│   ├── atualiza_Unidade(codigo, atributo, valor)
│   ├── relatorio_Unidade(codigo, periodo, incluir_inativas=False)

```