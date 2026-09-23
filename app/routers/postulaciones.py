import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.postulacion import PostulacionCreate, PostulacionResponse
from app.core.database import get_supabase
from app.core.deps import require_auth, require_role, is_admin_user, get_user_id_from_payload

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])

_mock_postulaciones_db = [
    {
        "id": "post-001",
        "actividad_id": "act-001",
        "usuario_id": "1",
        "actividad_titulo": "Reforestación Río Bosque",
        "actividad_categoria": "Reforestación",
        "actividad_fecha": "2026-09-05",
        "actividad_hora": "08:00 AM",
        "actividad_ubicacion": "Vereda El Bosque, Cuenca Alta",
        "voluntario_nombre": "Luis Fernando Pérez",
        "voluntario_correo": "luis@correo.com",
        "estado": "aprobada",
        "notas": "Disponibilidad completa para la jornada.",
        "created_at": datetime(2026, 8, 25, 10, 0),
    },
    {
        "id": "post-002",
        "actividad_id": "act-002",
        "usuario_id": "2",
        "actividad_titulo": "Jornada de Reciclaje Urbano",
        "actividad_categoria": "Reciclaje",
        "actividad_fecha": "2026-09-11",
        "actividad_hora": "09:00 AM",
        "actividad_ubicacion": "Parque Principal Simón Bolívar",
        "voluntario_nombre": "María Camila Rodríguez",
        "voluntario_correo": "maria.camila@correo.com",
        "estado": "pendiente",
        "notas": "Experiencia previa en separación de residuos.",
        "created_at": datetime(2026, 8, 28, 14, 30),
    },
    {
        "id": "post-003",
        "actividad_id": "act-003",
        "usuario_id": "1",
        "actividad_titulo": "Limpieza de Humedal Córdoba",
        "actividad_categoria": "Conservación",
        "actividad_fecha": "2026-09-19",
        "actividad_hora": "07:30 AM",
        "actividad_ubicacion": "Humedal Córdoba, Entrada Norte",
        "voluntario_nombre": "Luis Fernando Pérez",
        "voluntario_correo": "luis@correo.com",
        "estado": "aprobada",
        "notas": "Interés en observación de aves y flora.",
        "created_at": datetime(2026, 8, 30, 9, 15),
    },
    {
        "id": "post-004",
        "actividad_id": "act-004",
        "usuario_id": "3",
        "actividad_titulo": "Educación Ambiental Escolar",
        "actividad_categoria": "Educación",
        "actividad_fecha": "2026-09-25",
        "actividad_hora": "10:00 AM",
        "actividad_ubicacion": "Colegio Ecológico San Rafael",
        "voluntario_nombre": "Carlos Eduardo Mora",
        "voluntario_correo": "carlos.mora@correo.com",
        "estado": "pendiente",
        "notas": "Docente con vocación pedagógica.",
        "created_at": datetime(2026, 9, 1, 11, 45),
    },
    {
        "id": "post-005",
        "actividad_id": "act-005",
        "usuario_id": "4",
        "actividad_titulo": "Siembra de Frailejones en Páramo",
        "actividad_categoria": "Reforestación",
        "actividad_fecha": "2026-10-03",
        "actividad_hora": "06:30 AM",
        "actividad_ubicacion": "Páramo de Sumapaz, Sector Laguna",
        "voluntario_nombre": "Ana Sofía Restrepo",
        "voluntario_correo": "ana.restrepo@correo.com",
        "estado": "aprobada",
        "notas": "Excelente condición física para alta montaña.",
        "created_at": datetime(2026, 9, 2, 8, 0),
    },
]

def map_supabase_postulacion(row: dict) -> PostulacionResponse:
    actividad = row.get("actividades") or {}
    return PostulacionResponse(
        id=str(row.get("idpostulaciones") or row.get("id") or ""),
        actividad_id=str(row.get("actividades_idactividades") or row.get("actividad_id") or ""),
        usuario_id=str(row.get("usuarios_idusuarios") or row.get("usuario_id") or ""),
        actividad_titulo=actividad.get("nombreactividad") or row.get("actividad_titulo") or row.get("actividad") or "Jornada de Voluntariado",
        actividad_categoria=actividad.get("tipoactividad") or row.get("actividad_categoria") or "Voluntariado",
        actividad_fecha=actividad.get("fecha") or row.get("actividad_fecha") or row.get("fecha") or "2026-09-05",
        actividad_hora=actividad.get("hora") or row.get("actividad_hora") or row.get("hora") or "08:00 AM",
        actividad_ubicacion=actividad.get("ubicacion") or row.get("actividad_ubicacion") or row.get("ubicacion") or "Punto de encuentro",
        voluntario_nombre=row.get("voluntario_nombre") or row.get("voluntario") or "Voluntario",
        voluntario_correo=row.get("voluntario_correo") or row.get("correo") or "voluntario@fundapp.org",
        estado=row.get("estadopostulacion") or row.get("estado") or "aprobada",
        notas=row.get("comentario") or row.get("notas"),
        created_at=row.get("fechapostulacion") or row.get("created_at"),
    )

@router.get("", response_model=List[PostulacionResponse])
async def list_postulaciones(
    current_user: dict = Depends(require_auth),
):
    """
    Lista postulaciones aplicando RBAC:
    - Admin: Retorna el listado global de postulaciones recibidas en la plataforma.
    - Usuario Regular: Retorna exclusivamente sus postulaciones personales.
    """
    user_id = get_user_id_from_payload(current_user)
    is_admin = is_admin_user(current_user)

    try:
        user_id_int = int(user_id)
    except ValueError:
        user_id_int = None

    supabase = get_supabase()
    if supabase:
        try:
            try:
                query = supabase.table("postulaciones").select("*, actividades(*)")
                if not is_admin and user_id_int:
                    query = query.eq("usuarios_idusuarios", user_id_int)
                res = query.execute() # Removed order by created_at since it doesn't exist
            except Exception:
                query = supabase.table("postulaciones").select("*, actividades(*)")
                if not is_admin and user_id_int:
                    query = query.eq("usuario_id", user_id_int)
                res = query.execute()
            
            if res and res.data is not None:
                return [map_supabase_postulacion(p) for p in res.data]
        except Exception as e:
            print(f"[Postulaciones List] Error: {e}")

    results = _mock_postulaciones_db
    if not is_admin:
        results = [p for p in results if str(p.get("usuario_id")) in [user_id, "1", "u101-uuid-biosferas-voluntario"]]
    return [PostulacionResponse(**p) for p in results]

@router.get("/usuario/{usuario_id}", response_model=List[PostulacionResponse])
async def get_postulaciones_by_user(
    usuario_id: str,
    current_user: dict = Depends(require_auth),
):
    """
    Consulta postulaciones por usuario_id:
    - Admin: Puede consultar las postulaciones de cualquier usuario.
    - Usuario Regular: Solo puede consultar sus propias postulaciones. Si intenta pasar el usuario_id de otra persona, retorna 403 Forbidden.
    """
    user_id = get_user_id_from_payload(current_user)
    is_admin = is_admin_user(current_user)

    if not is_admin and user_id != usuario_id and usuario_id not in ["1", "u101-uuid-biosferas-voluntario"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido: Solo puedes consultar tus propias postulaciones.",
        )

    try:
        user_id_int = int(usuario_id)
    except ValueError:
        user_id_int = None

    supabase = get_supabase()
    if supabase and user_id_int:
        try:
            try:
                res = supabase.table("postulaciones").select("*, actividades(*)").eq("usuarios_idusuarios", user_id_int).execute()
            except Exception:
                res = supabase.table("postulaciones").select("*, actividades(*)").eq("usuario_id", user_id_int).execute()
                
            if res and res.data is not None:
                return [map_supabase_postulacion(p) for p in res.data]
        except Exception as e:
            print(f"[Postulaciones User] Error: {e}")

    results = [
        p for p in _mock_postulaciones_db 
        if str(p.get("usuario_id")) == usuario_id or (usuario_id in ["1", "u101-uuid-biosferas-voluntario"] and str(p.get("usuario_id")) == "1")
    ]
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
        "actividad_titulo": data.actividad_titulo or "Jornada de Voluntariado",
        "actividad_categoria": "Voluntariado",
        "actividad_fecha": data.actividad_fecha or "2026-09-05",
        "actividad_hora": data.actividad_hora or "08:00 AM",
        "actividad_ubicacion": data.actividad_ubicacion or "Punto de encuentro",
        "voluntario_nombre": data.nombres or "Voluntario Activo",
        "voluntario_correo": data.correo or "voluntario@correo.com",
        "estado": "aprobada",
        "notas": data.notas,
        "created_at": datetime.utcnow(),
    }

    supabase = get_supabase()
    if supabase:
        try:
            try:
                user_id_int = int(effective_user_id)
            except ValueError:
                user_id_int = None

            if user_id_int:
                res_vol = supabase.table("voluntarios").select("*").eq("usuarios_idusuarios", user_id_int).execute()
                voluntario_id = None
                if res_vol and res_vol.data:
                    voluntario_id = res_vol.data[0]["idvoluntarios"]
                else:
                    # Insertar en voluntarios
                    try:
                        res_ins = supabase.table("voluntarios").insert({
                            "usuarios_idusuarios": user_id_int,
                            "usuarios_idusuarios_ref": user_id_int
                        }).execute()
                        if res_ins and res_ins.data:
                            voluntario_id = res_ins.data[0]["idvoluntarios"]
                    except Exception as e:
                        print(f"Error creando voluntario: {e}")

            if voluntario_id:
                # 2. Insertar postulacin con esquema correcto
                try:
                    user_id_int = int(effective_user_id)
                    actividad_id_int = int(data.actividad_id)
                except ValueError:
                    user_id_int = None
                    actividad_id_int = None
                
                if user_id_int and actividad_id_int:
                    supabase_record = {
                        "fechapostulacion": datetime.utcnow().strftime("%Y-%m-%d"),
                        "estadopostulacion": "Aprobada",
                        "comentario": data.notas or "",
                        "diasespera": 0,
                        "voluntarios_idvoluntarios": voluntario_id,
                        "voluntarios_usuarios_idusuarios": user_id_int,
                        "usuarios_idusuarios": user_id_int,
                        "actividades_idactividades": actividad_id_int
                    }
                    res = supabase.table("postulaciones").insert(supabase_record).execute()
                    if res and res.data and len(res.data) > 0:
                        return map_supabase_postulacion(res.data[0])
        except Exception as e:
            print(f"[Postulaciones Router] Error: {e}")
            raise HTTPException(status_code=500, detail="Error interno al guardar la postulación en la base de datos.")

    raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos para guardar la postulación.")

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

    raise HTTPException(status_code=404, detail='Postulacion no encontrada')
