from pydantic import BaseModel
from typing import Optional
from datetime import date

class CertificadoCreate(BaseModel):
    usuario_id: str
    actividad_id: Optional[str] = None
    donacion_id: Optional[str] = None
    tipo: str = "voluntariado" # 'voluntariado', 'donacion'
    titulo: str = "Certificado de Voluntariado"
    actividad_titulo: str = "Jornada Ambiental"
    horas: Optional[int] = 4
    monto: Optional[float] = None
    destinatario: Optional[str] = "Voluntario Biosferas"
    documento_identidad: Optional[str] = "1.098.765.432"

class CertificadoResponse(BaseModel):
    id: str
    usuario_id: str
    actividad_id: Optional[str] = None
    donacion_id: Optional[str] = None
    tipo: str # 'voluntariado', 'donacion'
    titulo: str
    actividad_titulo: str
    horas: Optional[int] = None
    monto: Optional[float] = None
    fecha_emision: date
    estado: str = "aprobado"
    codigo_verificacion: str
    firmado_por: str
    destinatario: str
    documento_identidad: str
