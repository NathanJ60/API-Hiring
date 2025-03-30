from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
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

@router.get("/{dataset_id}/excel/")
def export_dataset_excel(dataset_id: str):
    """
    GET /datasets/{dataset_id}/excel/
    Exporte le dataset au format Excel et renvoie un fichier xlsx.
    """
    buffer = dataset_service.export_dataset_to_excel(dataset_id)
    headers = {
        "Content-Disposition": f'attachment; filename="{dataset_id}.xlsx"'
    }
    return StreamingResponse(buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)


@router.get("/{dataset_id}/stats/")
def get_dataset_stats(dataset_id: str):
    """
    GET /datasets/{dataset_id}/stats/
    Retourne les statistiques (df.describe()) du dataset, au format JSON.
    """
    stats = dataset_service.get_dataset_stats(dataset_id)
    return JSONResponse(content=stats)

@router.get("/{dataset_id}/plot/")
def get_dataset_plot(dataset_id: str):
    """
    GET /datasets/{dataset_id}/plot/
    Génère et renvoie un PDF contenant un histogramme pour chaque colonne numérique du dataset.
    """
    pdf_buffer = dataset_service.generate_plot_pdf(dataset_id)
    headers = {
        "Content-Disposition": f'attachment; filename="{dataset_id}_histograms.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)