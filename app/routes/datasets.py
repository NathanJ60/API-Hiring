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

@router.post("/", response_model=DatasetInfo)
async def create_dataset(file: UploadFile = File(...)):
    """
    POST /datasets/
    Crée un dataset à partir d'un fichier CSV.
    Retourne : {id, filename, size}
    """
    dataset_id, filename, size = await dataset_service.create_dataset(file)
    return DatasetInfo(id=dataset_id, filename=filename, size=size)
