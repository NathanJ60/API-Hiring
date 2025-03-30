# client/main.py
import typer
import requests

app = typer.Typer(help="CLI pour interagir avec l'API de gestion de datasets.")
API_URL = "http://localhost:8000/datasets/"  # À adapter selon ta configuration

@app.command()
def hello(name: str = typer.Option(..., "--name", "-n", help="Nom de la personne à saluer")):
    """
    Commande test : Affiche un message de bienvenue.
    """
    typer.echo(f"Bonjour, {name} !")

@app.command()
def create(file_path: str = typer.Option(..., "--file-path", "-f", help="Chemin vers le fichier CSV à uploader")):
    """
    Crée un dataset sur le serveur à partir d'un fichier CSV local.
    """
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "text/csv")}
            response = requests.post(API_URL, files=files)
    except Exception as e:
        typer.echo(f"Erreur lors de l'ouverture du fichier: {e}")
        raise typer.Exit(code=1)
    
    if response.status_code == 200:
        typer.echo("Dataset créé avec succès !")
        typer.echo(response.json())
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)


if __name__ == "__main__":
    app()