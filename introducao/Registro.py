import typer as tp
from pydantic import BaseModel,EmailStr
from rich.console import Console
from rich.table import Table
import json
import sqlite3

console=Console()
app=tp.Typer()
json_name="contatos.json"
db_name="contatos.db"

class Contato(BaseModel):
	nome: str
	telefone: str
	email: EmailStr

def CriarDB():
	conn=sqlite3.connect(db_name)
	conn.execute("create database if not exists Contatos(id int primary key autoincrement,telefone text,email text unique)")
	conn.commit()
	conn.close()

def SalvarDB(dados: Contato):
	conn=sqlite3.connect(db_name)

	conn.execute("insert or ignore into  contatos (nome,telefone,email) values(?,?,?)",
		(dados.nome,dados.telefone,dados.email))
	conn.commit()
	conn.close()

@app.command()
def BuscarTodos():
	db=sqlite3.connect(db_name)
	dados=db.execute("select nome,telefone,email from contatos").fetchall()
	db.close()
	return dados

def list():
	conn=sqlite3.connect(db_name)
	sql="select telefone from contatos"
	dados=conn.execute(sql).fetchall()
	conn.close()
	tabela=Table()
	tabela.add_column("[bold green]Contatos[/bold green]")
	if dados is None:
		tabela.add_row("[red]Nenhum contato registrado[/red]")
		console.print(tabela)
		tp.Exit(1)
	[tabela.add_row(f"[blue]{d}[/blue]") for d in dados]
	console.print(tabela)

@app.command
def find(nome: str):
	conn=sqlite3.connect(db_mame)
	sql="select telefone from  contatos name like?"
	dados=conn.execute(sql,(f"%{nome}%",)).fetchall()
	conn.close()
	tabela=Table()
	tabela.add_column("[bold green]Contatos[/bold green]")
	if not dados: 
		tabela.add_row("[red]Nenhum contato encontrado[/red]")
		console.print(tabela)
		tp.Exit(1)
	[tabela.add_row(f"[blue]{d}[/blue]") for d in dados]
	console.print(tabela)

@app.command()
def add(nome: str,telefone: str, email: str):
	try:
		dados=Contato(nome=nome,telefone=telefone,email=email)
		CriarDB()
		SalvarDB(dados)
	
		lista=[{"nome":t[0],"telefone":t[1],"email":t[2]} for t in dados] 
		with open(json_name,"w",encoding="utf-8") as f:
			json.dump(dados,f,indent=4,ensure_ascii=True)
	except:
		tp.secho("ERRRO: verifique os dados",fg=tp.colors.RED)

if __name__ == "__main__":
	app()
