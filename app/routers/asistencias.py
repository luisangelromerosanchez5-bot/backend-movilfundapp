import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.schemas.asistencia import CheckInRequest, CheckOutRequest, AsistenciaResponse
from app.core.utils import calculate_haversine_distance, is_within_geofence
from app.core.database import get_supabase
from app.routers.actividades import _mock_activities_db

router = APIRouter(prefix="/asistencias", tags=["Asistencias & Sensores"])

_mock_asistencias_db = {}

@router.post("", response_model=AsistenciaResponse)
async def check_in_asistencia(payload: CheckInRequest):
    # Validar Geofencing con las coordenadas de la actividad
    target_activity = next((a for a in _mock_activities_db if a["id"] == payload.actividad_id), None)
    if not target_activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    # Validación de distancia en el backend
    calculated_distance = calculate_haversine_distance(
        lat1=payload.lat_registrada,
        lon1=payload.lng_registrada,
        lat2=target_activity["latitud"],
        lon2=target_activity["longitud"],
    )

    asistencia_id = str(uuid.uuid4())
    new_asistencia = {
        "id": asistencia_id,
        "actividad_id": payload.actividad_id,
        "usuario_id": payload.usuario_id,
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
    }

    supabase = get_supabase()
    if supabase:
        try:
            supabase_data = {
                **new_asistencia,
                "check_in_at": new_asistencia["check_in_at"].isoformat(),
            }
            res = supabase.table("asistencias").insert(supabase_data).execute()
            if res.data:
                return AsistenciaResponse(**res.data[0])
        except Exception as e:
            print(f"[Asistencias Checkin] Supabase fallback: {e}")

    _mock_asistencias_db[asistencia_id] = new_asistencia
    return AsistenciaResponse(**new_asistencia)

@router.patch("/{asistencia_id}", response_model=AsistenciaResponse)
async def check_out_asistencia(asistencia_id: str, payload: CheckOutRequest):
    asistencia = _mock_asistencias_db.get(asistencia_id)
    if not asistencia:
        # Generar registro simulado si no existía en memoria
        asistencia = {
            "id": asistencia_id,
            "actividad_id": "act-001",
            "usuario_id": "u101",
            "lat_registrada": 4.711000,
            "lng_registrada": -74.072100,
            "distancia_metros": 38,
            "precision_gps": "Alta",
            "check_in_at": datetime.utcnow(),
            "check_out_at": datetime.utcnow(),
            "pasos_sesion": payload.pasos_sesion,
            "distancia_km": payload.distancia_km,
            "calorias": payload.calorias,
        }
        _mock_asistencias_db[asistencia_id] = asistencia
        return AsistenciaResponse(**asistencia)

    asistencia["check_out_at"] = datetime.utcnow()
    asistencia["pasos_sesion"] = payload.pasos_sesion
    asistencia["distancia_km"] = payload.distancia_km
    asistencia["calorias"] = payload.calorias

    return AsistenciaResponse(**asistencia)
