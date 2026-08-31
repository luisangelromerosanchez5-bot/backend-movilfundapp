import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.actividad import ActividadCreate, ActividadResponse
from app.core.database import get_supabase

router = APIRouter(prefix="/actividades", tags=["Actividades Ambientales"])

_mock_activities_db = [
    {
        "id": "act-001",
        "titulo": "Reforestación Río Bosque",
        "descripcion": "Jornada de siembra de especies nativas junto a la comunidad local. Se proveen herramientas y refrigerio.",
        "categoria": "Reforestación",
        "fecha": "2026-09-05",
        "hora": "08:00 AM",
        "duracion_horas": 4,
        "cupos_totales": 30,
        "cupos_ocupados": 18,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Vereda El Bosque, Cuenca Alta",
        "latitud": 4.711000,
        "longitud": -74.072100,
        "radio_permitido_metros": 120,
        "puntos_impacto": 150,
        "tags": ["Siembra", "Bosque", "Comunidad"],
        "imagen_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600",
    },
    {
        "id": "act-002",
        "titulo": "Jornada de Reciclaje Urbano",
        "descripcion": "Separación y recolección de materiales reciclables en parques zonales para fomentar la economía circular.",
        "categoria": "Reciclaje",
        "fecha": "2026-09-11",
        "hora": "09:00 AM",
        "duracion_horas": 3,
        "cupos_totales": 20,
        "cupos_ocupados": 15,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Parque Principal Simón Bolívar",
        "latitud": 4.658300,
        "longitud": -74.093900,
        "radio_permitido_metros": 100,
        "puntos_impacto": 100,
        "tags": ["Reciclaje", "Ciudad", "CeroBasura"],
        "imagen_url": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=600",
    },
    {
        "id": "act-003",
        "titulo": "Limpieza de Humedal Córdoba",
        "descripcion": "Recuperación ambiental del ecosistema acuático, retiro de residuos sólidos y censo básico de aves migratorias.",
        "categoria": "Conservación",
        "fecha": "2026-09-19",
        "hora": "07:30 AM",
        "duracion_horas": 5,
        "cupos_totales": 25,
        "cupos_ocupados": 25,
        "estado_cupos": "lleno",
        "ubicacion_nombre": "Humedal Córdoba, Entrada Norte",
        "latitud": 4.701200,
        "longitud": -74.075400,
        "radio_permitido_metros": 150,
        "puntos_impacto": 200,
        "tags": ["Humedal", "Aves", "Conservación"],
        "imagen_url": "https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=600",
    },
]

@router.get("", response_model=List[ActividadResponse])
async def list_activities(
    q: Optional[str] = Query(None, description="Término de búsqueda"),
    categoria: Optional[str] = Query(None, description="Categoría de actividad"),
):
    supabase = get_supabase()
    if supabase:
        try:
            query_builder = supabase.table("actividades").select("*")
            if categoria and categoria != "Todos":
                query_builder = query_builder.eq("categoria", categoria)
            res = query_builder.execute()
            if res.data:
                return [ActividadResponse(**row) for row in res.data]
        except Exception as e:
            print(f"[Actividades Router] Supabase fallback: {e}")

    results = list(_mock_activities_db)
    if q:
        term = q.lower()
        results = [
            a for a in results
            if term in a["titulo"].lower()
            or term in a["descripcion"].lower()
            or term in a["ubicacion_nombre"].lower()
        ]
    if categoria and categoria != "Todos":
        results = [a for a in results if a["categoria"].lower() == categoria.lower()]

    return [ActividadResponse(**a) for a in results]

@router.get("/{activity_id}", response_model=ActividadResponse)
async def get_activity(activity_id: str):
    for a in _mock_activities_db:
        if a["id"] == activity_id:
            return ActividadResponse(**a)
    raise HTTPException(status_code=404, detail="Actividad no encontrada")
