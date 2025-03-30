from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any

from app.schemas import DatasetInfo
from app.services import dataset_service

router = APIRouter()

@router.get("/")
def list_all_datasets() -> Any:
    """
    GET /datasets/
    Retourne la liste de tous les datasets stockés.
    """
    return dataset_service.list_datasets()

@router.get("/{dataset_id}")
async def get_dataset_info(dataset_id: str) -> DatasetInfo:
    """
    GET /datasets/{dataset_id}
    Retourne les informations sur un dataset spécifique.
    """
    info = dataset_service.get_dataset_info(dataset_id)
    return DatasetInfo(id=info["id"], filename=info["filename"], size=info["size"])


@router.post("/", response_model=DatasetInfo)
async def create_dataset(file: UploadFile = File(...)):
    """
    POST /datasets/
    Crée un dataset à partir d'un fichier CSV.
    Retourne : {id, filename, size}
    """
    dataset_id, filename, size = await dataset_service.create_dataset(file)
    return DatasetInfo(id=dataset_id, filename=filename, size=size)

@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: str):
    """
    DELETE /datasets/{dataset_id}
    Supprime un dataset.
    """
    dataset_service.delete_dataset(dataset_id)
    return {"status": "success", "message": f"Dataset {dataset_id} deleted."}
