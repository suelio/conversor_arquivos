"""
Motor Central de Conversao de Arquivos (Individual e em Lote)
Autor: Suelio Lima
"""

import time
from pathlib import Path
from typing import Union, Optional, Dict, Any, List
import pandas as pd

from .reader import FileReader
from .writer import FileWriter
from .validator import IntegrityValidator


class FileConverter:
    """Orquestrador de conversoes individuais e em lote com calculo de metricas."""

    @classmethod
    def convert(
        cls,
        source: Union[str, Path],
        target_format: str,
        output_path: Optional[Union[str, Path]] = None,
        delimiter: Optional[str] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Converte um arquivo individual para o formato solicitado.
        
        Args:
            source: Caminho do arquivo de entrada.
            target_format: Formato desejado ('csv', 'txt', 'xlsx', 'parquet', 'json').
            output_path: Caminho ou pasta de destino (opcional).
            delimiter: Delimitador especifico caso o formato seja csv ou txt.
            validate: Se True, recarrega o arquivo gerado para checar integridade.
            
        Returns:
            Dicionario contendo o sumario detalhado da operacao.
        """
        start_time = time.perf_counter()
        source_path = Path(source)

        # 1. Leitura do arquivo
        df, meta_in = FileReader.read(source_path)

        # 2. Definicao do caminho de saida
        clean_target_fmt = target_format.lower().lstrip(".")
        if output_path is None:
            final_target = source_path.with_suffix(f".{clean_target_fmt}")
        else:
            p_out = Path(output_path)
            if p_out.is_dir() or not p_out.suffix:
                final_target = p_out / f"{source_path.stem}.{clean_target_fmt}"
            else:
                final_target = p_out

        # 3. Gravacao no formato de destino
        saved_path, size_out = FileWriter.write(
            df=df,
            target_path=final_target,
            target_format=clean_target_fmt,
            delimiter=delimiter
        )

        elapsed = round(time.perf_counter() - start_time, 4)
        size_in = meta_in["tamanho_origem_bytes"]

        # 4. Calculo de reducao de espaco em disco
        diff_pct = 0.0
        if size_in > 0:
            diff_pct = round(((size_in - size_out) / size_in) * 100, 2)

        # 5. Validacao de integridade
        validation_status = None
        validation_info = {}
        if validate:
            validation_status, validation_info = IntegrityValidator.validate(df, saved_path)

        return {
            "status": "Sucesso",
            "arquivo_origem": str(source_path.resolve()),
            "formato_origem": meta_in["formato"],
            "tamanho_origem_kb": round(size_in / 1024, 2),
            "arquivo_destino": str(saved_path.resolve()),
            "formato_destino": clean_target_fmt.upper(),
            "tamanho_destino_kb": round(size_out / 1024, 2),
            "economia_espaco_pct": diff_pct,
            "linhas": int(len(df)),
            "colunas": int(len(df.columns)),
            "tempo_segundos": elapsed,
            "validacao_ok": validation_status,
            "detalhes_validacao": validation_info
        }

    @classmethod
    def convert_batch(
        cls,
        source_dir: Union[str, Path],
        target_format: str,
        output_dir: Optional[Union[str, Path]] = None,
        delimiter: Optional[str] = None,
        extensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Converte em lote todos os arquivos compativeis de um diretorio.
        """
        start_batch = time.perf_counter()
        in_dir = Path(source_dir)
        if not in_dir.is_dir():
            raise NotADirectoryError(f"O caminho de origem nao e uma pasta valida: {source_dir}")

        out_dir = Path(output_dir) if output_dir else in_dir / "convertidos"
        out_dir.mkdir(parents=True, exist_ok=True)

        target_exts = extensions or [".csv", ".tsv", ".txt", ".xlsx", ".parquet", ".json"]
        files = [p for p in in_dir.iterdir() if p.is_file() and p.suffix.lower() in target_exts]

        results = []
        total_size_in = 0
        total_size_out = 0

        for file_p in files:
            try:
                res = cls.convert(
                    source=file_p,
                    target_format=target_format,
                    output_path=out_dir,
                    delimiter=delimiter,
                    validate=True
                )
                results.append(res)
                total_size_in += (res["tamanho_origem_kb"] * 1024)
                total_size_out += (res["tamanho_destino_kb"] * 1024)
            except Exception as e:
                results.append({
                    "status": "Erro",
                    "arquivo_origem": str(file_p.resolve()),
                    "erro": str(e)
                })

        total_elapsed = round(time.perf_counter() - start_batch, 4)
        savings_pct = 0.0
        if total_size_in > 0:
            savings_pct = round(((total_size_in - total_size_out) / total_size_in) * 100, 2)

        return {
            "pasta_origem": str(in_dir.resolve()),
            "pasta_destino": str(out_dir.resolve()),
            "formato_destino": target_format.upper(),
            "total_arquivos": len(files),
            "sucessos": sum(1 for r in results if r.get("status") == "Sucesso"),
            "falhas": sum(1 for r in results if r.get("status") == "Erro"),
            "economia_total_pct": savings_pct,
            "tempo_total_segundos": total_elapsed,
            "arquivos": results
        }

    @staticmethod
    def select_file_gui() -> Optional[str]:
        """Abre janela grafica do Windows para selecao de arquivo individual."""
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            p = filedialog.askopenfilename(
                title="Selecione o arquivo para conversao",
                filetypes=[
                    ("Arquivos Tabulares", "*.csv *.txt *.tsv *.xlsx *.parquet *.json"),
                    ("Todos os Arquivos", "*.*")
                ]
            )
            root.destroy()
            return p if p else None
        except Exception as e:
            print(f"[Aviso] Interface grafica indisponivel: {e}")
            return None

    @staticmethod
    def select_folder_gui() -> Optional[str]:
        """Abre janela grafica do Windows para selecao de pasta (processamento em lote)."""
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            p = filedialog.askdirectory(title="Selecione a pasta com arquivos para conversao em lote")
            root.destroy()
            return p if p else None
        except Exception as e:
            print(f"[Aviso] Interface grafica indisponivel: {e}")
            return None

    @staticmethod
    def upload_via_colab() -> Optional[str]:
        """Executa upload interativo em sessoes do Google Colab."""
        try:
            from google.colab import files  # type: ignore
            print("[Conversor] Selecione o arquivo do seu computador:")
            uploaded = files.upload()
            if uploaded:
                return next(iter(uploaded))
            return None
        except ImportError:
            print("[Aviso] A funcao upload_via_colab deve ser executada dentro do Google Colab.")
            return None
