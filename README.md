## Repsitório para a matéria INF1310 - Programação Modular da PUC-Rio



**estrutura sugerida pro projeto:**
```
app/
│
├── produto.py
│   ├── class Produto
│   │   ├── calcular_preco(quantidade)
│   ├── registrar_produto(nome: str, marca: str, categoria: str, codigo: str, peso: float, preco: float, preco_por_peso: float = None)
│   ├── atualizar_produto(codigo: int, dados: dict)
│   ├── consultar_produto_por_codigo(codigo: int)
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
├── funcionario.py
│   ├── class Funcionario
│   ├── admitir_funcionario(dados)
│   ├── desligar_funcionario(codigo_funcionario)
│   ├── alterar_funcionario(codigo, novos_dados)
│   ├── consultar_funcionarios(filtros)
│   ├── atualizar_tabela_local_de_funcionarios()
│
└── main.py
    ├── inicializar_banco_dados()
    ├── carregar_interface_usuario()
```