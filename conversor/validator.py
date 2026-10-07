"""
Modulo de Validacao de Integridade de Dados Pos-Conversao
Autor: Suelio Lima
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
from .reader import FileReader


class IntegrityValidator:
    """Classe responsavel por verificar se a conversao manteve a integridade estrutural."""

    @staticmethod
    def validate(df_original: pd.DataFrame, converted_file_path: Path) -> Tuple[bool, Dict[str, Any]]:
        """
        Reabre o arquivo gerado e compara com os dados originais.
        
        Retorna:
            Tupla contendo: (status_sucesso, detalhes_da_validacao)
        """
        try:
            df_reloaded, _ = FileReader.read(converted_file_path)

            rows_orig, cols_orig = df_original.shape
            rows_reloaded, cols_reloaded = df_reloaded.shape

            rows_match = (rows_orig == rows_reloaded)
            cols_match = (cols_orig == cols_reloaded)

            success = rows_match and cols_match

            details = {
                "valido": success,
                "linhas_originais": rows_orig,
                "linhas_recarregadas": rows_reloaded,
                "colunas_originais": cols_orig,
                "colunas_recarregadas": cols_reloaded,
                "nomes_colunas_preservados": list(df_original.columns) == list(df_reloaded.columns)
            }
            return success, details
        except Exception as e:
            return False, {"valido": False, "erro": str(e)}
