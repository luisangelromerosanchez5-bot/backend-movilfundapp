import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.postulacion import PostulacionCreate, PostulacionResponse
from app.core.database import get_supabase
from app.core.deps import require_auth, require_role

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])

_mock_postulaciones_db = []

@router.get("", response_model=List[PostulacionResponse])
async def list_postulaciones(
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table("postulaciones").select("*")
            # Si no es admin, filtrar solo las del usuario actual
            if user_role not in ["admin", "administrador"]:
                query = query.eq("usuario_id", user_sub)
            res = query.order("created_at", desc=True).execute()
            if res.data:
                return [PostulacionResponse(**p) for p in res.data]
        except Exception as e:
            print(f"[Postulaciones List] Error: {e}")

    results = _mock_postulaciones_db
    if user_role not in ["admin", "administrador"]:
        results = [p for p in results if str(p.get("usuario_id")) == user_sub]
    return [PostulacionResponse(**p) for p in results]

@router.get("/usuario/{usuario_id}", response_model=List[PostulacionResponse])
async def get_postulaciones_by_user(
    usuario_id: str,
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    if user_role not in ["admin", "administrador"] and user_sub != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido: Solo puedes consultar tus propias postulaciones.",
        )

    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("postulaciones").select("*").eq("usuario_id", usuario_id).execute()
            if res.data:
                return [PostulacionResponse(**p) for p in res.data]
        except Exception as e:
            print(f"[Postulaciones User] Error: {e}")

    results = [p for p in _mock_postulaciones_db if str(p.get("usuario_id")) == usuario_id]
    return [PostulacionResponse(**p) for p in results]

@router.post("", response_model=PostulacionResponse)
async def create_postulacion(
    data: PostulacionCreate,
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    effective_user_id = data.usuario_id if user_role in ["admin", "administrador"] else (user_sub or data.usuario_id)

    postulacion_id = str(uuid.uuid4())
    record = {
        "id": postulacion_id,
        "actividad_id": data.actividad_id,
        "usuario_id": effective_user_id,
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

    _mock_postulaciones_db.insert(0, record)
    return PostulacionResponse(**record)

@router.patch("/{postulacion_id}/estado", response_model=PostulacionResponse)
async def update_postulacion_estado(
    postulacion_id: str,
    nuevo_estado: str,
    current_user: dict = Depends(require_role(["admin", "administrador"])),
):
    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("postulaciones").update({"estado": nuevo_estado}).eq("id", postulacion_id).execute()
            if res.data and len(res.data) > 0:
                return PostulacionResponse(**res.data[0])
        except Exception as e:
            print(f"[Postulaciones Update Estado] Error: {e}")

    for p in _mock_postulaciones_db:
        if p["id"] == postulacion_id:
            p["estado"] = nuevo_estado
            return PostulacionResponse(**p)

    raise HTTPException(status_code=404, detail="Postulación no encontrada")
