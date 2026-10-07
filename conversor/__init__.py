"""
Conversor de Formatos de Arquivos
Autor: Suelio Lima
"""

from .reader import FileReader
from .writer import FileWriter
from .validator import IntegrityValidator
from .engine import FileConverter

__version__ = "2.0.0"
__all__ = ["FileConverter", "FileReader", "FileWriter", "IntegrityValidator"]
