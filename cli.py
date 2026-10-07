#!/usr/bin/env python3
"""
Interface de Linha de Comando (CLI) para o Conversor de Arquivos
Autor: Suelio Lima
"""

import sys
import argparse
from pathlib import Path
from conversor import FileConverter

# Garante compatibilidade com terminais Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_interactive():
    print("=" * 65)
    print("       CONVERSOR DE ARQUIVOS TABULARES MULTI-FORMATO")
    print("                    Autor: Suelio Lima")
    print("=" * 65)

    print("\nModo de Operacao:")
    print("1. Converter um arquivo individual")
    print("2. Converter todos os arquivos de uma pasta (Em Lote)")
    print("3. Sair")
    mode = input("Escolha uma opcao (1, 2 ou 3) [padrao: 1]: ").strip()

    if mode == "3":
        print("Encerrando.")
        return

    if mode == "2":
        # Conversao em lote
        print("\nComo deseja selecionar a pasta de origem?")
        print("1. Abrir explorador de pastas do Windows")
        print("2. Digitar o caminho da pasta")
        f_choice = input("Opcao (1 ou 2) [padrao: 1]: ").strip()

        if f_choice == "2":
            source_dir = input("Digite o caminho da pasta de origem: ").strip()
        else:
            print("[*] Abrindo janela de selecao de pasta...")
            source_dir = FileConverter.select_folder_gui()

        if not source_dir or not Path(source_dir).is_dir():
            print("[!] Pasta invalida ou operacao cancelada.")
            return

        print("\nEscolha o formato de destino:")
        print("1. Parquet (.parquet)")
        print("2. Excel (.xlsx)")
        print("3. CSV (.csv)")
        print("4. JSON (.json)")
        fmt_map = {"1": "parquet", "2": "xlsx", "3": "csv", "4": "json"}
        target_fmt = fmt_map.get(input("Opcao (1-4): ").strip(), "parquet")

        delim = None
        if target_fmt == "csv":
            print("\nDelimitador para CSV: 1-Virgula (,) | 2-Ponto e virgula (;) | 3-Tabulacao (\\t)")
            delim_map = {"1": ",", "2": ";", "3": "\t"}
            delim = delim_map.get(input("Opcao [padrao: 1]: ").strip(), ",")

        print(f"\n[*] Iniciando processamento em lote para formato {target_fmt.upper()}...")
        batch_res = FileConverter.convert_batch(source_dir, target_format=target_fmt, delimiter=delim)
        print("\n[+] Resumo do Lote:")
        print(f"Total de arquivos encontrados: {batch_res['total_arquivos']}")
        print(f"Sucessos: {batch_res['sucessos']} | Falhas: {batch_res['falhas']}")
        print(f"Economia total de espaco: {batch_res['economia_total_pct']}%")
        print(f"Tempo total: {batch_res['tempo_total_segundos']} segundos")
        print(f"Pasta destino: {batch_res['pasta_destino']}")
        return

    # Modo arquivo individual
    print("\nComo deseja selecionar o arquivo?")
    print("1. Abrir explorador de arquivos do Windows")
    print("2. Digitar o caminho do arquivo")
    f_choice = input("Opcao (1 ou 2) [padrao: 1]: ").strip()

    if f_choice == "2":
        source_file = input("Digite o caminho do arquivo: ").strip()
    else:
        print("[*] Abrindo janela de selecao de arquivo...")
        source_file = FileConverter.select_file_gui()

    if not source_file or not Path(source_file).is_file():
        # Fallback para pasta de dados
        default_file = Path(__file__).parent / "data" / "exemplo_vendas.csv"
        if default_file.is_file():
            print(f"[*] Usando arquivo de exemplo: {default_file}")
            source_file = default_file
        else:
            print("[!] Arquivo nao encontrado ou cancelado.")
            return

    print("\nEscolha o formato de saida:")
    print("1. Parquet (.parquet) - Recomendado para alta compactacao")
    print("2. Excel (.xlsx)")
    print("3. CSV (.csv)")
    print("4. TXT Tabulado (.txt)")
    print("5. JSON (.json)")
    fmt_map = {"1": "parquet", "2": "xlsx", "3": "csv", "4": "txt", "5": "json"}
    target_fmt = fmt_map.get(input("Opcao (1-5) [padrao: 1]: ").strip(), "parquet")

    delim = None
    if target_fmt in ["csv", "txt"]:
        print("\nEscolha o delimitador: 1-Virgula (,) | 2-Ponto e virgula (;) | 3-Tabulacao (\\t) | 4-Pipe (|)")
        delim_map = {"1": ",", "2": ";", "3": "\t", "4": "|"}
        delim = delim_map.get(input("Opcao [padrao: 1]: ").strip(), ",")

    custom_out = input("\nNome ou caminho de saida (deixe em branco para salvar na mesma pasta): ").strip()
    out_path = custom_out if custom_out else None

    print("\n[*] Executando conversao...")
    res = FileConverter.convert(source_file, target_format=target_fmt, output_path=out_path, delimiter=delim)

    print("\n[+] Conversao concluida com sucesso!")
    print(f"Arquivo de origem : {res['arquivo_origem']} ({res['tamanho_origem_kb']} KB)")
    print(f"Arquivo de destino: {res['arquivo_destino']} ({res['tamanho_destino_kb']} KB)")
    print(f"Dimensoes         : {res['linhas']} linhas x {res['colunas']} colunas")
    print(f"Variacao de espaco: {res['economia_espaco_pct']}%")
    print(f"Tempo decorrido   : {res['tempo_segundos']}s")
    print(f"Validacao de dados: {'Aprovada (100% integra)' if res['validacao_ok'] else 'Falha na checagem'}")


def main():
    parser = argparse.ArgumentParser(description="Conversor de formatos de arquivos tabulares.")
    parser.add_argument("source", nargs="?", help="Caminho do arquivo de entrada.")
    parser.add_argument("-f", "--format", help="Formato de saida (csv, txt, xlsx, parquet, json).")
    parser.add_argument("-o", "--output", help="Caminho ou pasta de saida.")
    parser.add_argument("-d", "--delimiter", help="Delimitador para CSV ou TXT.")
    parser.add_argument("--batch", action="store_true", help="Ativa modo de conversao em lote para a pasta informada.")

    args = parser.parse_args()

    if not args.source:
        run_interactive()
    elif args.batch:
        if not args.format:
            print("[!] Erro: E necessario informar o formato (-f/--format) no modo batch.")
            sys.exit(1)
        res = FileConverter.convert_batch(args.source, target_format=args.format, output_dir=args.output, delimiter=args.delimiter)
        print(f"[+] Lote concluido: {res['sucessos']} convertidos de {res['total_arquivos']} arquivos. Economia: {res['economia_total_pct']}%.")
    else:
        target_fmt = args.format if args.format else "parquet"
        res = FileConverter.convert(args.source, target_format=target_fmt, output_path=args.output, delimiter=args.delimiter)
        print(f"[+] Concluido: {res['arquivo_destino']} ({res['linhas']} linhas, {res['economia_espaco_pct']}% variacao de tamanho).")


if __name__ == "__main__":
    main()
