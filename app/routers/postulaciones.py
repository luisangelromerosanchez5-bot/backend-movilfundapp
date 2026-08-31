import uuid
from datetime import datetime
from fastapi import APIRouter
from app.schemas.postulacion import PostulacionCreate, PostulacionResponse
from app.core.database import get_supabase

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])

_mock_postulaciones_db = []

@router.post("", response_model=PostulacionResponse)
async def create_postulacion(data: PostulacionCreate):
    postulacion_id = str(uuid.uuid4())
    record = {
        "id": postulacion_id,
        "actividad_id": data.actividad_id,
        "usuario_id": data.usuario_id,
        "estado": "aprobada",
        "notas": data.notas,
        "created_at": datetime.utcnow(),
    }

    supabase = get_supabase()
    if supabase:
        try:
            supabase_record = {
                **record,
                "created_at": record["created_at"].isoformat(),
            }
            res = supabase.table("postulaciones").insert(supabase_record).execute()
            if res.data:
                return PostulacionResponse(**res.data[0])
        except Exception as e:
            print(f"[Postulaciones Router] Supabase fallback: {e}")

    _mock_postulaciones_db.append(record)
    return PostulacionResponse(**record)
