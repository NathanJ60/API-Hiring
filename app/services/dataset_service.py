import uuid
import io
import os
import pandas as pd
import matplotlib
# Utiliser le backend Agg (non-interactif) pour éviter les problèmes de GUI
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from typing import Tuple, Dict
from fastapi import UploadFile, HTTPException

# Stockage en mémoire (dataset_id -> {"dataframe": df, "filename": str})
datasets_storage: Dict[str, dict] = {}


async def create_dataset(file: UploadFile) -> Tuple[str, str, int]:
    """Crée un dataset depuis un fichier CSV et renvoie (id, filename, size)."""
    contents = await file.read()
    try:
        # Lecture du CSV en DataFrame
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de lecture du CSV: {e}")

    dataset_id = str(uuid.uuid4())
    filename = file.filename
    size = len(contents)

    datasets_storage[dataset_id] = {"dataframe": df, "filename": filename, "size": size}
    return dataset_id, filename, size


def list_datasets() -> Dict[str, dict]:
    """Retourne l'ensemble des datasets stockés, sous forme de dict."""
    return {
        dataset_id: {
            "filename": info["filename"],
            "size": info["size"]
        }
        for dataset_id, info in datasets_storage.items()
    }

def get_dataset_info(dataset_id: str) -> dict:
    """Retourne les informations sur un dataset spécifique."""
    if dataset_id not in datasets_storage:
        raise HTTPException(status_code=404, detail="Dataset non trouvé")
    info = datasets_storage[dataset_id]
    return {
        "id": dataset_id,
        "filename": info["filename"],
        "size": info["size"]
    }

def delete_dataset(dataset_id: str) -> None:
    """Supprime un dataset de la mémoire."""
    if dataset_id not in datasets_storage:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    del datasets_storage[dataset_id]

    
def export_dataset_to_excel(dataset_id: str) -> io.BytesIO:
    """Exporte le DataFrame en Excel et renvoie un buffer BytesIO."""
    if dataset_id not in datasets_storage:
        raise HTTPException(status_code=404, detail="Dataset introuvable")

    df = datasets_storage[dataset_id]["dataframe"]

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="data")

    output.seek(0)
    return output
    
def get_dataset_stats(dataset_id: str) -> dict:
    """Retourne les statistiques de base (df.describe()) au format dict."""
    if dataset_id not in datasets_storage:
        raise HTTPException(status_code=404, detail="Dataset introuvable")

    df = datasets_storage[dataset_id]["dataframe"]
    # Conversion en dict puis remplacement des NaN par None pour compatibilité JSON
    stats_df = df.describe(include="all")
    stats = stats_df.replace({float('nan'): None}).to_dict()
    return stats


def generate_plot_pdf(dataset_id: str) -> io.BytesIO:
    """Génère un PDF contenant des histogrammes pour chaque colonne numérique."""
    if dataset_id not in datasets_storage:
        raise HTTPException(status_code=404, detail="Dataset introuvable")

    df = datasets_storage[dataset_id]["dataframe"]

    # Sélection des colonnes numériques
    numeric_cols = df.select_dtypes(include=["int", "float"]).columns

    if numeric_cols.empty:
        raise HTTPException(
            status_code=400,
            detail="Aucune colonne numérique à tracer dans ce dataset."
        )

    pdf_buffer = io.BytesIO()
    # Génération du PDF
    with PdfPages(pdf_buffer) as pdf:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            df[col].plot.hist(ax=ax, bins=30)  # On choisit 30 bins par exemple
            ax.set_title(f"Histogram for '{col}'")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")

            pdf.savefig(fig)
            plt.close(fig)

    pdf_buffer.seek(0)
    return pdf_buffer