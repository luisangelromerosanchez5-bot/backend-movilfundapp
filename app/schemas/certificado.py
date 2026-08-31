from pydantic import BaseModel
from typing import Optional
from datetime import date

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
