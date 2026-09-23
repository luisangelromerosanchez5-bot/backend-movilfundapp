import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.donacion import DonacionCreate, DonacionResponse
from app.core.database import get_supabase
from app.core.deps import require_auth

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

_mock_donaciones_db = []

@router.get("", response_model=List[DonacionResponse])
async def list_donaciones(
    usuario_id: Optional[str] = Query(None),
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    if user_role in ["admin", "administrador"]:
        target_user = usuario_id
    else:
        target_user = user_sub

    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table("donaciones").select("*")
            if target_user:
                if target_user.isdigit():
                    query = query.eq("usuarios_idusuarios", int(target_user))
                else:
                    query = query.eq("usuarios_idusuarios", target_user)
            res = query.order("fechadonacion", desc=True).execute()
            if res.data:
                return [map_donacion(d) for d in res.data]
        except Exception as e:
            print(f"[Donaciones List] Error: {e}")
            
    # Fallback to mock DB
    results = [DonacionResponse(**d) for d in _mock_donaciones_db]
    if target_user:
        results = [d for d in results if str(d.usuario_id) == str(target_user)]
    return sorted(results, key=lambda d: d.fecha, reverse=True)

@router.post("", response_model=DonacionResponse)
async def create_donacion(
    data: DonacionCreate,
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))
    effective_user_id = data.usuario_id if user_role in ["admin", "administrador"] else (user_sub or data.usuario_id)

    supabase = get_supabase()
    if supabase:
        try:
            record = {
                "monto": int(data.monto),
                "metodopago": data.metodo_pago,
                "estadopago": "Confirmada",
                "fechadonacion": datetime.utcnow().strftime("%Y-%m-%d"),
                "anonima": "No",
                "usuarios_idusuarios": int(effective_user_id) if effective_user_id.isdigit() else 1,
            }
            res = supabase.table("donaciones").insert(record).execute()
            if res.data and len(res.data) > 0:
                return map_donacion(res.data[0])
        except Exception as e:
            print(f"[Donaciones Router] Supabase insert error: {e}")

    # Fallback to mock DB
    new_d = DonacionResponse(
        id=str(uuid.uuid4()),
        usuario_id=effective_user_id,
        monto=data.monto,
        metodo_pago=data.metodo_pago,
        estado="completada",
        codigo_transaccion=f"TX-FB-{uuid.uuid4().hex[:8].upper()}",
        proyecto_destino="Fondo General de Conservación",
        fecha=datetime.utcnow(),
    )
    _mock_donaciones_db.insert(0, new_d.model_dump())
    return new_d

