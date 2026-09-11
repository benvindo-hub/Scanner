import typer as tp
import sqlite3
import sys
from datetime import datetime 
from rich.console import Console
from rich.table import Table
from pydantic  import BaseModel
from loguru import logger as lg

name_json="Arquivos_Json/Scanner_Relatorio.json"
name_db="Arquivos_DB/Scanner.db"

lg.remove()
lg.add(sys.stdout,format="<level>{level: <8}</level> | {message}")
lg.add("Atquivos_Log/app.log",format="{time} <level
