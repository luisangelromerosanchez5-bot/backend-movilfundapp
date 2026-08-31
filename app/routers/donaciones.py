import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter
from app.schemas.donacion import DonacionCreate, DonacionResponse
from app.core.database import get_supabase

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])

def map_donacion(row: dict) -> DonacionResponse:
    d_id = str(row.get("iddonaciones") or row.get("id") or "")
    user_id = str(row.get("usuarios_idusuarios") or row.get("usuario_id") or "1")
    monto = float(row.get("monto") or 0.0)
    metodo = str(row.get("metodopago") or row.get("metodo_pago") or "PSE")
    estado = str(row.get("estadopago") or row.get("estado") or "Confirmada")
    tx_code = str(row.get("codigo_transaccion") or f"TX-FB-{d_id}")
    proyecto = row.get("proyecto_destino") or "Fondo General de Conservación"
    fecha = datetime.utcnow()
    if row.get("fechadonacion"):
        try:
            fecha = datetime.fromisoformat(str(row["fechadonacion"]))
        except Exception:
            pass

    return DonacionResponse(
        id=d_id,
        usuario_id=user_id,
        monto=monto,
        metodo_pago=metodo,
        estado=estado,
        codigo_transaccion=tx_code,
        proyecto_destino=proyecto,
        fecha=fecha,
    )

@router.post("", response_model=DonacionResponse)
async def create_donacion(data: DonacionCreate):
    supabase = get_supabase()
    if supabase:
        try:
            record = {
                "monto": int(data.monto),
                "metodopago": data.metodo_pago,
                "estadopago": "Confirmada",
                "fechadonacion": datetime.utcnow().strftime("%Y-%m-%d"),
                "anonima": "No",
                "usuarios_idusuarios": int(data.usuario_id) if data.usuario_id.isdigit() else 1,
            }
            res = supabase.table("donaciones").insert(record).execute()
            if res.data and len(res.data) > 0:
                return map_donacion(res.data[0])
        except Exception as e:
            print(f"[Donaciones Router] Supabase insert error: {e}")

    return DonacionResponse(
        id=str(uuid.uuid4()),
        usuario_id=data.usuario_id,
        monto=data.monto,
        metodo_pago=data.metodo_pago,
        estado="completada",
        codigo_transaccion=f"TX-FB-{int(datetime.utcnow().timestamp())}",
        proyecto_destino=data.proyecto_destino,
        fecha=datetime.utcnow(),
    )

@router.get("/usuario/{usuario_id}", response_model=List[DonacionResponse])
async def get_donations_by_user(usuario_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            if usuario_id.isdigit():
                res = supabase.table("donaciones").select("*").eq("usuarios_idusuarios", int(usuario_id)).execute()
            else:
                res = supabase.table("donaciones").select("*").execute()
            if res.data and len(res.data) > 0:
                return [map_donacion(d) for d in res.data]
        except Exception as e:
            print(f"[Donaciones Router] Supabase get error: {e}")

    return []
