
# progressbar.py : barra di progresso utilizzando la libreria rich

from rich.progress import Progress
import time

with Progress() as progress:
	task1 = progress.add_task("[cyan]Process 1...",total=10)
	task2 = progress.add_task("[yellow]Process 2...",total=5)
	while not progress.finished:
		time.sleep(0.5)
		progress.update(task1, advance=1)
		progress.update(task2, advance=1)
		