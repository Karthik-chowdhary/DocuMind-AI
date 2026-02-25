from rich.console import Console
from rich.panel import Panel
from rich import print
from rich.progress import Progress
import threading
import time
import questionary
import json
import os



console = Console()
def interface():
    console.print(
        Panel.fit(
            "[bold cyan]DocuMind CLI[/bold cyan]\nChoose an option below:",
            border_style="green"
        )
    )

    choice = questionary.select(
        "Select:",
        choices=[
            "Upload PDF",
            "Select PDF",
            "Back"
        ]
    ).ask()
    return choice

def PDF_selection():
    cdir = os.getcwd()
    dir = os.path.join(cdir,"available_pdfs.json")
    with open(dir,'r') as file:
        data = json.load(file)
    data.append("Back")
    choice = questionary.select(
        "Select:",
        choices= data
    ).ask()
    return choice

class LoadModelProgress:

    def __init__(self):
        self.model_loaded = False
        self.model_class = None

    def load_model(self):
        from langchain_huggingface import HuggingFaceEmbeddings
        self.model_loaded = True
        self.model_class = HuggingFaceEmbeddings
    def show_progress(self):
        with Progress() as progress:
            task = progress.add_task("Loading Model...", total=30)

            while not progress.finished:
                if self.model_loaded:
                    progress.update(task, completed=30)
                    break
                else:
                    progress.update(task, advance=1)
                    time.sleep(0.5)

    def start(self):
        thread = threading.Thread(target=self.load_model)
        thread.start()
        self.show_progress()
        thread.join()

        return self.model_class
    