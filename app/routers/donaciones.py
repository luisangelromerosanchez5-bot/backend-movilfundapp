import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter
from app.schemas.donacion import DonacionCreate, DonacionResponse

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])

_mock_donaciones_db = []

@router.post("", response_model=DonacionResponse)
async def create_donacion(data: DonacionCreate):
    donacion_id = str(uuid.uuid4())
    tx_code = f"TX-FB-{int(datetime.utcnow().timestamp())}"
    record = {
        "id": donacion_id,
        "usuario_id": data.usuario_id,
        "monto": data.monto,
        "metodo_pago": data.metodo_pago,
        "estado": "completada",
        "codigo_transaccion": tx_code,
        "proyecto_destino": data.proyecto_destino,
        "fecha": datetime.utcnow(),
    }
    _mock_donaciones_db.append(record)
    return DonacionResponse(**record)

@router.get("/usuario/{usuario_id}", response_model=List[DonacionResponse])
async def get_donations_by_user(usuario_id: str):
    return [DonacionResponse(**d) for d in _mock_donaciones_db if d["usuario_id"] == usuario_id]
