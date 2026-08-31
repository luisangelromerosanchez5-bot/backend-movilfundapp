from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CheckInRequest(BaseModel):
    actividad_id: str
    usuario_id: str
    lat_registrada: float
    lng_registrada: float
    distancia_metros: int
    precision_gps: str = "Alta"
    postulacion_id: Optional[str] = None

class CheckOutRequest(BaseModel):
    asistencia_id: str
    pasos_sesion: int
    distancia_km: float
    calorias: int = 0

class AsistenciaResponse(BaseModel):
    id: str
    actividad_id: str
    usuario_id: str
    postulacion_id: Optional[str] = None
    lat_registrada: float
    lng_registrada: float
    distancia_metros: int
    precision_gps: str
    check_in_at: datetime
    check_out_at: Optional[datetime] = None
    pasos_sesion: int = 0
    distancia_km: float = 0.0
    calorias: int = 0
