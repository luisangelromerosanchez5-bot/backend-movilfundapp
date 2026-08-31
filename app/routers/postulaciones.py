import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.schemas.postulacion import PostulacionCreate, PostulacionResponse

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
        "created_at": datetime.utcnow(),
    }
    _mock_postulaciones_db.append(record)
    return PostulacionResponse(**record)
