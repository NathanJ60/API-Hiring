from pydantic import BaseModel, Field

class DatasetInfo(BaseModel):
    id: str = Field(..., description="Identifiant unique du dataset")
    filename: str = Field(..., description="Nom du fichier")
    size: int = Field(..., description="Taille du fichier en octets")