from pydantic import BaseModel
from typing import List, Optional

class ActividadBase(BaseModel):
    titulo: str
    descripcion: str
    categoria: str
    fecha: str
    hora: str
    duracion_horas: int = 2
    cupos_totales: int = 20
    ubicacion_nombre: str
    latitud: float
    longitud: float
    radio_permitido_metros: int = 100
    puntos_impacto: int = 100
    tags: List[str] = []
    imagen_url: Optional[str] = None

class ActividadCreate(ActividadBase):
    pass

class ActividadResponse(ActividadBase):
    id: str
    cupos_ocupados: int = 0
    estado_cupos: str = "disponible"
