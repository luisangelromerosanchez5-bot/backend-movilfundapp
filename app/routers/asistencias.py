import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException, status
from app.schemas.asistencia import CheckInRequest, CheckOutRequest, AsistenciaResponse
from app.core.utils import calculate_haversine_distance
from app.core.database import get_supabase
from app.core.deps import require_auth, is_admin_user, get_user_id_from_payload

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

_mock_asistencias_db = {}

@router.get("", response_model=List[AsistenciaResponse])
async def list_asistencias(
    usuario_id: Optional[str] = Query(None, description="Filtrar por usuario (solo Admin)"),
    current_user: dict = Depends(require_auth),
):
    """
    Lista asistencias aplicando RBAC:
    - Admin: Retorna el listado global de todas las asistencias registradas (o filtra por usuario_id).
    - Usuario Regular: Filtra automáticamente para retornar únicamente sus asistencias personales.
    """
    user_id = get_user_id_from_payload(current_user)
    is_admin = is_admin_user(current_user)

    if not is_admin:
        target_user_id = user_id
    else:
        target_user_id = usuario_id

    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table("asistencias").select("*")
            if target_user_id:
                query = query.eq("usuario_id", target_user_id)
            res = query.order("check_in_at", desc=True).execute()
            if res.data and len(res.data) > 0:
                return [AsistenciaResponse(**item) for item in res.data]
        except Exception as e:
            print(f"[Asistencias List] Supabase error: {e}")

    results = list(_mock_asistencias_db.values())
    if target_user_id:
        results = [a for a in results if str(a.get("usuario_id")) == str(target_user_id)]
    return [AsistenciaResponse(**a) for a in results]

@router.post("", response_model=AsistenciaResponse)
async def check_in_asistencia(
    payload: CheckInRequest,
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    # Si no es admin, el check-in se asocia obligatoriamente al usuario autenticado
    effective_user_id = payload.usuario_id if user_role in ["admin", "administrador"] else (user_sub or payload.usuario_id)

    target_lat = 4.711000
    target_lng = -74.072100

    supabase = get_supabase()
    if supabase:
        try:
            if payload.actividad_id.isdigit():
                res_act = supabase.table("actividades").select("*").eq("idactividades", int(payload.actividad_id)).execute()
            else:
                res_act = supabase.table("actividades").select("*").execute()
            if res_act.data and len(res_act.data) > 0:
                row = res_act.data[0]
                target_lat = float(row.get("latitud") or target_lat)
                target_lng = float(row.get("longitud") or target_lng)
        except Exception as e:
            print(f"[Asistencias Checkin] Actividad lookup error: {e}")

    calculated_distance = calculate_haversine_distance(
        lat1=payload.lat_registrada,
        lon1=payload.lng_registrada,
        lat2=target_lat,
        lon2=target_lng,
    )

    asistencia_id = str(uuid.uuid4())
    new_asistencia = {
        "id": asistencia_id,
        "actividad_id": payload.actividad_id,
        "usuario_id": effective_user_id,
        "postulacion_id": payload.postulacion_id,
        "lat_registrada": payload.lat_registrada,
        "lng_registrada": payload.lng_registrada,
        "distancia_metros": int(calculated_distance),
        "precision_gps": payload.precision_gps,
        "check_in_at": datetime.utcnow(),
        "check_out_at": None,
        "pasos_sesion": 0,
        "distancia_km": 0.0,
        "calorias": 0,
        "foto_evidencia_url": None,
    }

    if supabase:
        try:
            supabase_data = {
                **new_asistencia,
                "check_in_at": new_asistencia["check_in_at"].isoformat(),
            }
            res = supabase.table("asistencias").insert(supabase_data).execute()
            if res.data and len(res.data) > 0:
                return AsistenciaResponse(**res.data[0])
        except Exception as e:
            print(f"[Asistencias Checkin] Supabase insert error: {e}")

    _mock_asistencias_db[asistencia_id] = new_asistencia
    return AsistenciaResponse(**new_asistencia)

@router.patch("/{asistencia_id}", response_model=AsistenciaResponse)
async def check_out_asistencia(
    asistencia_id: str,
    payload: CheckOutRequest,
    current_user: dict = Depends(require_auth),
):
    supabase = get_supabase()
    now = datetime.utcnow()

    update_fields = {
        "check_out_at": now.isoformat(),
        "pasos_sesion": payload.pasos_sesion,
        "distancia_km": payload.distancia_km,
        "calorias": payload.calorias,
        "foto_evidencia_url": payload.foto_evidencia_url,
    }

    if supabase:
        try:
            res = supabase.table("asistencias").update(update_fields).eq("id", asistencia_id).execute()
            if res.data and len(res.data) > 0:
                return AsistenciaResponse(**res.data[0])
        except Exception as e:
            print(f"[Asistencias Checkout] Supabase update error: {e}")

    asistencia = _mock_asistencias_db.get(asistencia_id)
    if not asistencia:
        asistencia = {
            "id": asistencia_id,
            "actividad_id": "1",
            "usuario_id": str(current_user.get("sub", "1")),
            "lat_registrada": 4.711000,
            "lng_registrada": -74.072100,
            "distancia_metros": 38,
            "precision_gps": "Alta",
            "check_in_at": now,
            "check_out_at": now,
            "pasos_sesion": payload.pasos_sesion,
            "distancia_km": payload.distancia_km,
            "calorias": payload.calorias,
            "foto_evidencia_url": payload.foto_evidencia_url,
        }
        _mock_asistencias_db[asistencia_id] = asistencia
        return AsistenciaResponse(**asistencia)

    asistencia["check_out_at"] = now
    asistencia["pasos_sesion"] = payload.pasos_sesion
    asistencia["distancia_km"] = payload.distancia_km
    asistencia["calorias"] = payload.calorias
    asistencia["foto_evidencia_url"] = payload.foto_evidencia_url

    return AsistenciaResponse(**asistencia)
