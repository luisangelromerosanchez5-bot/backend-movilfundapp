from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostulacionCreate(BaseModel):
    actividad_id: str
    usuario_id: str
    nombres: Optional[str] = None
    correo: Optional[str] = None
    notas: Optional[str] = None
    actividad_titulo: Optional[str] = None
    actividad_fecha: Optional[str] = None
    actividad_hora: Optional[str] = None
    actividad_ubicacion: Optional[str] = None

class PostulacionResponse(BaseModel):
    id: str
    actividad_id: str
    usuario_id: str
    actividad_titulo: Optional[str] = "Jornada de Voluntariado"
    actividad_categoria: Optional[str] = "Voluntariado"
    actividad_fecha: Optional[str] = "2026-09-05"
    actividad_hora: Optional[str] = "08:00 AM"
    actividad_ubicacion: Optional[str] = "Punto de encuentro"
    voluntario_nombre: Optional[str] = "Voluntario"
    voluntario_correo: Optional[str] = "voluntario@fundapp.org"
    estado: str = "aprobada"
    notas: Optional[str] = None
    created_at: Optional[datetime] = None
