import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter
from app.schemas.donacion import DonacionCreate, DonacionResponse
from app.core.database import get_supabase

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

    supabase = get_supabase()
    if supabase:
        try:
            supabase_record = {
                **record,
                "fecha": record["fecha"].isoformat(),
            }
            res = supabase.table("donaciones").insert(supabase_record).execute()
            if res.data:
                return DonacionResponse(**res.data[0])
        except Exception as e:
            print(f"[Donaciones Router] Supabase fallback: {e}")

    _mock_donaciones_db.append(record)
    return DonacionResponse(**record)

@router.get("/usuario/{usuario_id}", response_model=List[DonacionResponse])
async def get_donations_by_user(usuario_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("donaciones").select("*").eq("usuario_id", usuario_id).execute()
            if res.data:
                return [DonacionResponse(**d) for d in res.data]
        except Exception as e:
            print(f"[Donaciones Router] Supabase fallback: {e}")

    return [DonacionResponse(**d) for d in _mock_donaciones_db if d["usuario_id"] == usuario_id]
