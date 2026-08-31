from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas.actividad import ActividadResponse
from app.core.database import get_supabase

router = APIRouter(prefix="/actividades", tags=["Actividades Ambientales"])

def map_supabase_actividad(row: dict) -> ActividadResponse:
    act_id = str(row.get("idactividades") or row.get("id") or "")
    titulo = row.get("nombreactividad") or row.get("titulo") or "Actividad Fundación"
    descripcion = row.get("descripcion") or "Jornada ambiental de voluntariado y apoyo comunitario."
    categoria = row.get("categoria") or "Voluntariado"
    fecha = row.get("fechainicio") or row.get("fecha") or "2026-09-05"
    hora = row.get("hora") or "08:00 AM"
    duracion = row.get("duracion_horas") or 4
    cupos_totales = row.get("cupos_totales") or 30
    cupos_ocupados = row.get("cupos_ocupados") or 0
    estado_cupos = row.get("estado_cupos") or ("disponible" if cupos_ocupados < cupos_totales else "lleno")
    ubicacion_nombre = row.get("ubicacion_nombre") or f"Ubicación #{row.get('ubicaciones_idubicaciones', 1)}"
    latitud = float(row.get("latitud") or 4.711000)
    longitud = float(row.get("longitud") or -74.072100)
    radio = int(row.get("radio_permitido_metros") or 100)
    puntos = int(row.get("puntos_impacto") or 100)
    tags = row.get("tags") or ["Voluntariado", "Comunidad"]
    imagen_url = row.get("imagen_url") or "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600"

    return ActividadResponse(
        id=act_id,
        titulo=titulo,
        descripcion=descripcion,
        categoria=categoria,
        fecha=fecha,
        hora=hora,
        duracion_horas=duracion,
        cupos_totales=cupos_totales,
        cupos_ocupados=cupos_ocupados,
        estado_cupos=estado_cupos,
        ubicacion_nombre=ubicacion_nombre,
        latitud=latitud,
        longitud=longitud,
        radio_permitido_metros=radio,
        puntos_impacto=puntos,
        tags=tags,
        imagen_url=imagen_url,
    )

@router.get("", response_model=List[ActividadResponse])
async def list_activities(
    q: Optional[str] = Query(None, description="Término de búsqueda"),
    categoria: Optional[str] = Query(None, description="Categoría de actividad"),
):
    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("actividades").select("*").execute()
            if res.data and len(res.data) > 0:
                mapped = [map_supabase_actividad(r) for r in res.data]
                if q:
                    term = q.lower()
                    mapped = [a for a in mapped if term in a.titulo.lower() or term in a.descripcion.lower()]
                if categoria and categoria != "Todos":
                    mapped = [a for a in mapped if a.categoria.lower() == categoria.lower()]
                return mapped
        except Exception as e:
            print(f"[Actividades Router] Supabase error: {e}")

    return []

@router.get("/{activity_id}", response_model=ActividadResponse)
async def get_activity(activity_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            # Buscar por idactividades
            try:
                int_id = int(activity_id)
                res = supabase.table("actividades").select("*").eq("idactividades", int_id).execute()
                if res.data and len(res.data) > 0:
                    return map_supabase_actividad(res.data[0])
            except ValueError:
                pass
        except Exception as e:
            print(f"[Actividades Get] Error: {e}")

    return map_supabase_actividad({"idactividades": activity_id, "nombreactividad": "Actividad"})
