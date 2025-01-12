# Conversor de Formatos de Arquivos

Este script converte arquivos entre os formatos **TXT**, **CSV** e **XLSX**, permitindo a manipulação de delimitadores e a escolha do formato de saída. Ele é útil para quem precisa transformar dados entre diferentes formatos de arquivo de maneira rápida e eficiente.

---

## Funcionalidades

- **Conversão de formatos**: Converte arquivos entre TXT, CSV e XLSX.
- **Delimitadores personalizados**: Para arquivos CSV, é possível escolher entre diferentes delimitadores (vírgula, ponto e vírgula, pipe, tabulação).
- **Manutenção de dados**: Preserva os dados originais durante a conversão.
- **Interface interativa**: O script guia o usuário passo a passo durante o processo de conversão.

---

## Como Usar

### 1. Instalação das Dependências

Antes de executar o script, certifique-se de que as bibliotecas necessárias estão instaladas. Você pode instalá-las usando o seguinte comando:

```bash
pip install pandas openpyxl
```

### 2. Executando o Script

- Execute o script no seu ambiente Python.
- Siga as instruções fornecidas pelo script:
  1. **Digite o nome do arquivo de entrada** (com extensão, ex: `dados.txt`).
  2. **Verifique as primeiras linhas do arquivo** para confirmar se está correto.
  3. **Escolha o formato de saída** (TXT, CSV ou XLSX).
  4. **Escolha o delimitador** (se o formato de saída for CSV).
  5. **Digite o nome do arquivo de saída** (sem extensão, ex: `resultado`).
  6. **Digite o caminho onde deseja salvar o arquivo** (deixe em branco para usar o diretório atual).

---

## Exemplo de Uso

### Arquivo de Entrada (`dados.txt`):

```plaintext
Nome    Idade   Cidade
Alice   30      São Paulo
Bob     25      Rio de Janeiro
Charlie 35      Belo Horizonte
```

### Execução do Script:

1. Digite o nome do arquivo: `dados.txt`
2. O arquivo está correto? `1` (Sim)
3. Escolha o formato de saída: `2` (CSV)
4. Escolha o delimitador: `1` (Vírgula)
5. Digite o nome do arquivo de saída: `resultado`
6. Digite o caminho onde deseja salvar o arquivo: (deixe em branco)

### Arquivo de Saída (`resultado.csv`):

```csv
Nome,Idade,Cidade
Alice,30,São Paulo
Bob,25,Rio de Janeiro
Charlie,35,Belo Horizonte
```

---

## Licença

Este projeto está licenciado sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Autor

- **Suelio Lima**
  - Email: suelio@gmail.com
  - GitHub: [suelio](https://github.com/suelio)

---

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Adicionando nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Problemas Conhecidos

- O script não suporta arquivos com múltiplas colunas que usam diferentes delimitadores. Certifique-se de que o arquivo de entrada esteja formatado corretamente.