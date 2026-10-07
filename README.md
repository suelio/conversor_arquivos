# Conversor de Formatos de Arquivos Tabulares

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/suelio/conversor_arquivos/blob/main/Converter_Arquivos.ipynb)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Pandas](https://img.shields.io/badge/pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![PyArrow](https://img.shields.io/badge/pyarrow-12.0%2B-d22128.svg)](https://arrow.apache.org/)

O **Conversor de Arquivos** e uma biblioteca e ferramenta de linha de comando em Python projetada para transformar, padronizar e otimizar conjuntos de dados tabulares entre diversos formatos: **CSV**, **TXT**, **XLSX**, **Parquet** e **JSON**.

A ferramenta resolve problemas comuns de interoperabilidade em pipelines de dados, oferecendo deteccao automatica de codificacoes e delimitadores, processamento em lote para diretorios completos, medicao de taxas de compressao em disco e validacao automatizada de integridade estrutural.

---

## Principais Funcionalidades

### 1. Ingestao e Inspecao Inteligente
- **Suporte Multi-Formato**: Leitura e escrita entre CSV, TXT, TSV, planilhas Excel (.xlsx, .xls), arquivos colunares Parquet e documentos JSON.
- **Autodetecao de Delimitadores e Encodings**: Identifica autonomamente separadores (virgula, ponto e virgula, tabulacao, pipe) e codificacoes (UTF-8, Latin1, CP1252), permitindo a leitura de arquivos legados ou formatados no padrao regional brasileiro sem quebras de formato.

### 2. Conversao Individual e em Lote (Batch Processing)
- **Arquivo Unico**: Conversao rapida com opcao de sobrescrever ou definir caminhos e nomes personalizados.
- **Processamento em Lote**: Converte pastas inteiras de uma so vez, criando automaticamente o diretorio de saida e gerando um sumario consolidado de sucessos, falhas e economia de armazenamento.

### 3. Validacao de Integridade e Metricas de Desempenho
- **Checagem Pos-Conversao**: Recarrega o arquivo gerado para verificar se o numero de linhas, colunas e cabeçalhos se manteve identico ao original.
- **Relatorio de Compressao**: Apresenta comparativo de tamanho em kilobytes (KB), variacao percentual de espaco em disco e tempo de execucao em segundos.

### 4. Múltiplas Formas de Utilizacao
- **Biblioteca Python**: Integracao direta com scripts de manipulacao e pipelines analiticos.
- **CLI Interativa**: Navegacao guiada por menus no terminal com suporte a janela grafica do Windows para selecao de arquivos e pastas.
- **CLI Automatizada**: Suporte a flags e argumentos de linha de comando (`--format`, `--batch`, `--output`).
- **Google Colab**: Notebook com botao nativo de upload para uso imediato em nuvem.

---

## Estrutura do Repositorio

```text
conversor_arquivos/
|-- conversor/                    # Pacote Python modular
|   |-- __init__.py               # Exports principais
|   |-- reader.py                 # Ingestao inteligente e deteccao de encodings
|   |-- writer.py                 # Gravacao nos formatos suportados
|   |-- engine.py                 # Orquestrador central e conversao em lote
|   `-- validator.py              # Validacao estrutural de integridade
|
|-- data/                         # Exemplos práticos para testes
|   |-- exemplo_vendas.csv        # CSV com delimitador ';' e acentuacao
|   |-- exemplo_clientes.txt      # TXT com tabulacao (\t)
|   `-- exemplo_produtos.json     # JSON estruturado
|
|-- notebooks/
|   `-- demonstracao.ipynb        # Notebook com fluxo didatico
|
|-- Converter_Arquivos.ipynb      # Notebook oficial com suporte a Google Colab
|-- cli.py                        # Interface de linha de comando (interativa e direta)
|-- environment.yml               # Configuracao para Anaconda/Conda
|-- requirements.txt              # Dependencias para pip
|-- .gitignore                    # Arquivos ignorados pelo Git
|-- LICENSE                       # Licenca MIT
`-- README.md                     # Documentacao oficial do projeto
```

---

## Instalacao

### Com Anaconda / Conda (Recomendado)

```bash
# Criar ambiente dedicado
conda env create -f environment.yml
conda activate conversor_arquivos

# Ou instalar no ambiente atual
conda install --file requirements.txt -y
```

### Com Pip

```bash
pip install -r requirements.txt
```

---

## Exemplos de Uso

### 1. No Google Colab
Abra o notebook diretamente pelo link oficial:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/suelio/conversor_arquivos/blob/main/Converter_Arquivos.ipynb)

---

### 2. Como Biblioteca Python em seus Scripts

```python
from conversor import FileConverter

# Conversao simples de CSV para Parquet com validacao automatica
resultado = FileConverter.convert(
    source="data/exemplo_vendas.csv",
    target_format="parquet",
    validate=True
)

print(f"Destino: {resultado['arquivo_destino']}")
print(f"Reducao de tamanho: {resultado['economia_espaco_pct']}%")
print(f"Integridade: {resultado['validacao_ok']}")

# Conversao em lote de uma pasta inteira para Excel
res_lote = FileConverter.convert_batch(
    source_dir="data",
    target_format="xlsx",
    output_dir="data/saida_excel"
)
print(f"Total de arquivos convertidos: {res_lote['sucessos']}")
```

---

### 3. Via Linha de Comando (CLI)

#### Modo Direto por Argumentos
```bash
# Converter um arquivo para Parquet
python cli.py data/exemplo_vendas.csv -f parquet

# Converter para CSV definindo ponto e virgula como delimitador
python cli.py data/exemplo_produtos.json -f csv -d ";"

# Converter todos os arquivos de uma pasta em lote para Excel
python cli.py data --batch -f xlsx -o data/relatorios_excel
```

#### Modo Interativo
Execute sem parametros para acessar o menu guiado:
```bash
python cli.py
```
O menu permite escolher entre abrir a janela grafica do Windows para selecao do arquivo/pasta ou digitar o caminho manualmente.

---

## Autor

- **Suelio Lima**
  - GitHub: [@suelio](https://github.com/suelio)
  - Repositorio: [github.com/suelio/conversor_arquivos](https://github.com/suelio/conversor_arquivos)

---

## Licenca

Este projeto e distribuido sob os termos da licenca **MIT**. Consulte o arquivo [LICENSE](LICENSE) para obter mais informacoes.