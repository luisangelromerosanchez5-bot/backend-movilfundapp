from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostulacionCreate(BaseModel):
    actividad_id: str
    usuario_id: str
    nombres: Optional[str] = None
    correo: Optional[str] = None
    notas: Optional[str] = None

class PostulacionResponse(BaseModel):
    id: str
    actividad_id: str
    usuario_id: str
    estado: str = "aprobada"
    created_at: Optional[datetime] = None
