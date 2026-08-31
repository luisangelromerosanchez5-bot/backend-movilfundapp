from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DonacionCreate(BaseModel):
    usuario_id: str
    monto: float
    metodo_pago: str # 'creditCard', 'pse', 'nequiDaviplata'
    proyecto_destino: Optional[str] = "Fondo General de Conservación"

class DonacionResponse(BaseModel):
    id: str
    usuario_id: str
    monto: float
    metodo_pago: str
    estado: str = "completada"
    codigo_transaccion: str
    proyecto_destino: Optional[str] = None
    fecha: datetime
