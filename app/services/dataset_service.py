import uuid
import io
import pandas as pd

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

