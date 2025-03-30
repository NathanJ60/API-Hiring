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


@app.command(name="list")
def list_datasets():
    """
    Liste tous les datasets disponibles sur le serveur.
    """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        typer.echo("Liste des datasets :")
        for dataset_id, info in data.items():
            typer.echo(f"- {dataset_id} | {info['filename']} ({info['size']} octets)")
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)

@app.command()
def info(dataset_id: str = typer.Option(..., "--dataset-id", "-d", help="ID du dataset à consulter")):
    """
    Récupère les informations (nom, taille) d'un dataset spécifique.
    """
    url = f"{API_URL}{dataset_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        typer.echo(f"Dataset ID: {data['id']}")
        typer.echo(f"Filename:   {data['filename']}")
        typer.echo(f"Size:       {data['size']} octets")
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)

@app.command()
def delete(dataset_id: str = typer.Option(..., "--dataset-id", "-d", help="ID du dataset à supprimer")):
    """
    Supprime un dataset donné de l'API.
    """
    url = f"{API_URL}{dataset_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        typer.echo("Dataset supprimé avec succès.")
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)

@app.command(name="export_excel")
def export_excel(
    dataset_id: str = typer.Option(..., "--dataset-id", "-d", help="ID du dataset à exporter"),
    output_path: str = typer.Option("exported_dataset.xlsx", "--output-path", "-o", help="Chemin de sortie du fichier Excel")
):
    """
    Récupère l'Excel généré par l'API pour un dataset et l'enregistre localement.
    """
    url = f"{API_URL}{dataset_id}/excel/"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        typer.echo(f"Fichier Excel enregistré sous: {output_path}")
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)

@app.command()
def stats(dataset_id: str = typer.Option(..., "--dataset-id", "-d", help="ID du dataset pour obtenir les statistiques")):
    """
    Affiche les statistiques du dataset (df.describe()).
    """
    url = f"{API_URL}{dataset_id}/stats/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        typer.echo("Statistiques du dataset :")
        typer.echo(data)
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)

@app.command()
def plot(
    dataset_id: str = typer.Option(..., "--dataset-id", "-d", help="ID du dataset pour récupérer le PDF des histogrammes"),
    output_path: str = typer.Option("histograms.pdf", "--output-path", "-o", help="Chemin de sortie du fichier PDF")
):
    """
    Récupère le PDF généré (histogrammes) pour un dataset et l'enregistre localement.
    """
    url = f"{API_URL}{dataset_id}/plot/"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        typer.echo(f"Fichier PDF enregistré sous: {output_path}")
    else:
        typer.echo(f"Erreur: {response.status_code}")
        typer.echo(response.text)

if __name__ == "__main__":
    app()