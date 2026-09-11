import typer as tp
import json
from pydantic import  BaseModel
from rich.console import  Console
from rich.table import Table
import sqlite3
from datetime import datetime as dt
import time

db_name="gerenciador.db"
json_name="gerenciador.json"
console=Console()
app=tp.Typer()

class Tarefa(BaseModel):
	titulo: str
	descricao: str

def CriarDB():
	db=sqlite3.connect(db_name)
	
	sql="""create table if not exists tarefa(id integer  primary key autoincrement,
						titulo text,
						descricao text,
						status text,
						data datetime)
	"""
	db.execute(sql)
	db.commit()
	db.close()
CriarDB()

def SalvarDB(dados: Tarefa):
	conn=sqlite3.connect(db_name)
	sql="insert into tarefa(titulo,descricao,status,data) values(?,?,?,?)"
	conn.execute(sql,(dados.titulo,dados.descricao,"pendente",dt.now().strftime("%Y-%m-%d %H:%M:%S")))
	conn.commit()
	conn.close()

def Todos():
	conn=sqlite3.connect(db_name)
	sql="select id,titulo,descricao,status,data from tarefa"
	dados=conn.execute(sql).fetchall()
	conn.close()
	return dados

@app.command(help="E obrigatorio inserir o titulo,a decricao e opcional")
def add(titulo: str= tp.Option(...,"-t","--titulo"),descricao: str= tp.Option(None,"-d","--descricao")
):
	dados=Tarefa(titulo= titulo,descricao= descricao)
	SalvarDB(dados)

@app.command()
def list():
	dados=Todos()
	tabela=Table(title="[bold margenta]GERENCIADOR DE TAREFAS[/bold margenta]")
	if not dados:
		raise tp.BadParameter("Nenhum registro")
	tabela.add_column("[bold green]Id[/bold green]")
	tabela.add_column("[bold green]Titulo[/bold green]");tabela.add_column("[bold green]Descricao[/bold green]")
	tabela.add_column("[bold green]Status[/bold green]");tabela.add_column("[bold green]Data[/bold green]")
	[tabela.add_row(str(d[0]),d[1],d[2],d[3],str(d[4])) for d in dados]
	console.print(tabela)

@app.command(help="E obrigatorio inserir o id")
def concluir(id: int= tp.Option(...,"-d")):
	conn=sqlite3.connect(db_name)
	tabela=Table(title="[bold margenta]GERENCIADOR DE TAREFAS[/bold margenta]")
	sql="select titulo,descricao from tarefa where id=? and status like?"
	dados=conn.execute(sql,(id,"%pendente%")).fetchall()

	tabela.add_column("[bold green]Titulo[/bold green]");tabela.add_column("[bold green]Descricao[/bold green]")
	if not dados:
		conn.close()
		raise tp.BadParameter("Tarefa concluida ou nao registrada")

	[tabela.add_row(d[0],d[1]) for d in dados]
	console.print(tabela)
	print("Continuar [S/N]: ",end="")
	op=input()
	if op.upper()=='S':
		sql="update tarefa set status='concluido' where id=?"
		conn.execute(sql,(id,))
		conn.commit()
		tp.secho("dados atualizado",tp.COLOR.GREEN)
	conn.close()

@app.command()
def export():
	dados=Todos()
	if not dados:
		raise tp.BadParameter("Nenhum registro encontrado")
	lista=[{"Id":d[0],"Titulo":d[1],"Descricao":d[2],"Status":d[3],"Data":str(d[4])} for d in dados]
	with open(json_name,"w",encoding="utf-8") as f:
		json.dump(lista,f,indent=4,ensure_ascii=True)
	tp.secho("Dados salvos",color="green")
 
@app.command(help="E obrigatorio inserir ID ou titulo para achar a terefa")
def editar(id: int= tp.Option(None,"-d","--id"),titulo: str=tp.Option(None,"-t","--titulo")):
	db=sqlite3.connect(db_name)
	sql="select titulo,descricao,status from tarefa where titulo like?"
	sql2="select titulo,descricao,status from tarefa where id=?"

	aux1=db.execute(sql2,(id,)).fetchall()
	aux2=db.execute(sql,(f"%{titulo}%",)).fetchall()
	
	if aux1:
		dados=aux1
	elif aux2:
		dados=aux2
	else:
		db.close()
		raise tp.BadParameter("Nenhuma tarefa encontrada")

	tabela=Table()
	tabela.add_column("Titulo")
	tabela.add_column("Descricao")
	tabela.add_column("Status")
	[tabela.add_row(d[0],d[1],d[2]) for d in dados]
	console.print(tabela)

	tabela=Table()
	tabela.add_column("OPCOES")
	tabela.add_row("1 Editar Titulo");tabela.add_row("2 Editar Descricao");tabela.add_row("3 Editar Stutus")
	tabela.add_row("4 Sair")
	console.print(tabela)
	op=input("\nDigite a opcao: ")

	if op=='1':
		titulo_novo=input("Digite o novo titulo: ")
		sql="update tarefa set titulo=? where id=? or titulo like?"
		db.execute(sql,(titulo_novo,id,f"%{titulo}%"))
	elif op=='2':
		descricao_novo=input("Digite a nova descricao: ")
		sql="update tarefa set descricao=? where id=? or titulo like?"
		db.execute(sql,(descricao_novo,id,f"%{titulo}%"))
	elif op=='3':
		status_novo=input("Digite o novo status (concluido/pendente): ")
		if status_novo.lower()!="pendente" or status_novo.lower()!="concluido":
			raise tp.BadParameter(f"Status {status_novo} nao existe")
		sql="update tarefa set status=? where id=? or titulo like?"
		db.execute(sql,(status_novo,id,f"%{titulo}%"))
	elif op=='4':
		tp.secho("Saindo...",color="blue")
		time.sleep(4)
		db.close()
		return
	else:
		db.close()
		raise BadParameter("Opcao invalida")
	tp.secho("Alteracao feita",tp.COLOR.GREEN)
	db.commit()
	db.close()

@app.command(help="E obrigatorio inserir o id")
def deletar(id: int= tp.Option(...,"-d","--id")):
	db=sqlite3.connect(db_name)
	sql="delete from tarefa where id=?"
	if not db.execute("select titulo from tarefa where id=?",(id,)).fetchall():
		db.close()
		raise tp.BadParameter("Id nao encontrado")
	db.execute(sql,(id,))
	db.commit()
	db.close()
	tp.secho("Dados excluidos")

@app.command(help="E obrigatorio inserir o status")
def filtro(status: str=tp.Option(...,"-s","--ststus")):
	if status.lower()!="pendente" and status.lower()!="concluido":
		raise tp.BadParameter(f"Status {status} nao existe")
	db=sqlite3.connect(db_name)
	sql="select id,titulo,descricao,data from tarefa where status like?"
	dados=db.execute(sql,(f"%{status}%",)).fetchall()
	if not dados:
		db.close()
		raise tp.BadParameter("Nenhum tarefa encontrada")

	tabela=Table(title=f"[bold margenta]Tarefas {status}s[/bold margenta]")
	tabela.add_column("[blue]ID[/blue]");tabela.add_column("[blue]Tirulo[/blue]")
	tabela.add_column("[blue]Descricao[/blue]");tabela.add_column("[blue]Data[/blue]")
	[tabela.add_row(d[0],d[1],d[2],d[3]) for d in dados]
	console.print(tabela)
	db.close()

if __name__ == "__main__":
	app()

