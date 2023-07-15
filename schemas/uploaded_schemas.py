from fastapi import UploadFile
from pydantic import BaseModel


class CreateUpload(BaseModel):
    file: UploadFile
    filename: str
    comment: str
    source: str
    source_id: int


class UpdateUpload(BaseModel):
    id: int
    file: str
    comment: str
    source: str
    source_id: int
