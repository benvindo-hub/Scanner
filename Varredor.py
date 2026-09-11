import typer as tp
from pathlib import Path
import json
from rich.console import Console 
from rich.table import Table
from pydantic import BaseModel,Field
import sqlite3

console=Console()
app=tp.Typer()

class Verificacao(BaseModel):
	arquivo: str
@app.callback(invoke_without_command=True)
def scan(endereco: str):
	arquivos=Path(endereco)
	tabela=Table()
	table.add_column("[green]Arquivos[/green]")
	with open("Relatorio.json","a") as re:
		for arq in arquivos.glob("**/*.py"),arquivos.glob("**/*.txt"):
			if arq==".py":
				json.dump(arq,re)
			if arq==".txt":
				json.dump(arq,re)
			tabela.add_row(f"[blue]{arq}[/blue]")
	console.print(tabela)
if __name__ == "__main__":
	app
