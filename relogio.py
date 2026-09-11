from datetime import datetime
import time
from rich.console import Console
from rich.table import Table
import os

agora=datetime.now()
hora=agora.hour
min=agora.minute
sec=agora.second
console=Console()
while True:
	sec+=1
	if sec==60:
		sec=0
		min+=1
		if min==60:
			min=0
			hora+=1
	tabela=Table()
	tabela.add_column("RELOGIO")
	tabela.add_row(f"[bold green]{hora:02d}:{min:02d}:{sec:02d}\r[/bold green]")
	console.print(tabela)
	time.sleep(1)
	os.system("clear")
