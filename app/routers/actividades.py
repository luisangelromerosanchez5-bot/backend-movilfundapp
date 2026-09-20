import uuid
from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException, status
from app.schemas.actividad import ActividadResponse, ActividadCreate
from app.core.database import get_supabase
from app.core.deps import require_role

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
    imagen_url = row.get("imagen_url") or "assets/images/act_reforestacion_rio.jpg"

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

_mock_activities_db = [
    {
        "id": "act-001",
        "titulo": "Reforestación Río Bosque",
        "descripcion": "Jornada de siembra de 300 especies nativas junto a la comunidad local para proteger la cuenca hídrica.",
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
        "imagen_url": "assets/images/act_reforestacion_rio.jpg",
    },
    {
        "id": "act-002",
        "titulo": "Jornada de Reciclaje Urbano",
        "descripcion": "Separación y recolección de materiales reciclables en parques zonales para fomentar la economía circular con recicladores de oficio.",
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
        "imagen_url": "assets/images/act_reciclaje_urbano.jpg",
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
        "imagen_url": "assets/images/act_humedal_cordoba.jpg",
    },
    {
        "id": "act-004",
        "titulo": "Educación Ambiental Escolar",
        "descripcion": "Talleres interactivos con niños de primaria sobre cuidado del agua y huertas caseras sostenibles.",
        "categoria": "Educación",
        "fecha": "2026-09-25",
        "hora": "10:00 AM",
        "duracion_horas": 2,
        "cupos_totales": 15,
        "cupos_ocupados": 5,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Colegio Ecológico San Rafael",
        "latitud": 4.675000,
        "longitud": -74.060000,
        "radio_permitido_metros": 80,
        "puntos_impacto": 80,
        "tags": ["Talleres", "Niños", "Huertas"],
        "imagen_url": "assets/images/act_educacion_ambiental.jpg",
    },
    {
        "id": "act-005",
        "titulo": "Siembra de Frailejones en Páramo",
        "descripcion": "Restauración ecológica de alta montaña sembrando plántulas de frailejón para salvaguardar las fábricas naturales de agua.",
        "categoria": "Reforestación",
        "fecha": "2026-10-03",
        "hora": "06:30 AM",
        "duracion_horas": 6,
        "cupos_totales": 20,
        "cupos_ocupados": 12,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Páramo de Sumapaz, Sector Laguna",
        "latitud": 4.250000,
        "longitud": -74.250000,
        "radio_permitido_metros": 200,
        "puntos_impacto": 250,
        "tags": ["Páramo", "Agua", "Frailejones"],
        "imagen_url": "assets/images/act_paramo_frailejones.jpg",
    },
    {
        "id": "act-006",
        "titulo": "Censo y Monitoreo de Aves Silvestres",
        "descripcion": "Avistamiento matutino y registro biológico de aves en el sendero ecológico para la base de datos de biodiversidad.",
        "categoria": "Conservación",
        "fecha": "2026-10-12",
        "hora": "06:00 AM",
        "duracion_horas": 3,
        "cupos_totales": 15,
        "cupos_ocupados": 10,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Reserva Natural Cerros Orientales",
        "latitud": 4.610000,
        "longitud": -74.050000,
        "radio_permitido_metros": 100,
        "puntos_impacto": 120,
        "tags": ["Aves", "BioCenso", "Fauna"],
        "imagen_url": "assets/images/act_aves_silvestres.jpg",
    },
    {
        "id": "act-007",
        "titulo": "Clases de Inglés Básico",
        "descripcion": "Enseñanza lúdica de vocabulario y conversación básica en inglés para niños y jóvenes de la comunidad.",
        "categoria": "Educación",
        "fecha": "2026-10-15",
        "hora": "03:00 PM",
        "duracion_horas": 2,
        "cupos_totales": 20,
        "cupos_ocupados": 8,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Centro Comunitario La Esperanza",
        "latitud": 4.609710,
        "longitud": -74.081750,
        "radio_permitido_metros": 100,
        "puntos_impacto": 90,
        "tags": ["Inglés", "Educación", "Jóvenes"],
        "imagen_url": "assets/images/act_clases_ingles.png",
    },
    {
        "id": "act-008",
        "titulo": "Curso de Alfabetización Digital",
        "descripcion": "Capacitación en uso de computadores, internet y herramientas digitales para adultos y jóvenes.",
        "categoria": "Educación",
        "fecha": "2026-10-18",
        "hora": "09:30 AM",
        "duracion_horas": 3,
        "cupos_totales": 15,
        "cupos_ocupados": 11,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Biblioteca Pública Central",
        "latitud": 4.601200,
        "longitud": -74.071000,
        "radio_permitido_metros": 90,
        "puntos_impacto": 110,
        "tags": ["Digital", "Tecnología", "Inclusión"],
        "imagen_url": "assets/images/act_alfabetizacion_digital.png",
    },
    {
        "id": "act-009",
        "titulo": "Taller de Pintura y Óleo",
        "descripcion": "Expresión artística comunitaria plasmando la naturaleza y el cuidado ambiental a través de la pintura.",
        "categoria": "Educación",
        "fecha": "2026-10-20",
        "hora": "02:00 PM",
        "duracion_horas": 3,
        "cupos_totales": 20,
        "cupos_ocupados": 14,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Casa Cultural Los Pinos",
        "latitud": 4.632000,
        "longitud": -74.064000,
        "radio_permitido_metros": 100,
        "puntos_impacto": 100,
        "tags": ["Arte", "Pintura", "Cultura"],
        "imagen_url": "assets/images/act_taller_pintura.png",
    },
    {
        "id": "act-010",
        "titulo": "Comedor Comunitario",
        "descripcion": "Apoyo en la preparación y distribución de almuerzos nutritivos para familias en situación vulnerable.",
        "categoria": "Social",
        "fecha": "2026-10-22",
        "hora": "11:00 AM",
        "duracion_horas": 4,
        "cupos_totales": 25,
        "cupos_ocupados": 19,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Comedor Solidario San José",
        "latitud": 4.589000,
        "longitud": -74.092000,
        "radio_permitido_metros": 120,
        "puntos_impacto": 160,
        "tags": ["Comedor", "Solidaridad", "Alimentos"],
        "imagen_url": "assets/images/act_comedor_comunitario.png",
    },
    {
        "id": "act-011",
        "titulo": "Entrega de Mercados Sector A",
        "descripcion": "Jornada logística de empaque y distribución de mercados con víveres de primera necesidad.",
        "categoria": "Social",
        "fecha": "2026-10-24",
        "hora": "08:00 AM",
        "duracion_horas": 5,
        "cupos_totales": 30,
        "cupos_ocupados": 22,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Centro de Acopio Sector A",
        "latitud": 4.645000,
        "longitud": -74.110000,
        "radio_permitido_metros": 150,
        "puntos_impacto": 180,
        "tags": ["Mercados", "Ayuda", "Comunidad"],
        "imagen_url": "assets/images/act_entrega_mercados.png",
    },
    {
        "id": "act-012",
        "titulo": "Taller de Cocina Saludable",
        "descripcion": "Capacitación práctica en recetas nutritivas y aprovechamiento de alimentos frescos de la huerta.",
        "categoria": "Salud",
        "fecha": "2026-10-27",
        "hora": "03:30 PM",
        "duracion_horas": 3,
        "cupos_totales": 18,
        "cupos_ocupados": 12,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Cocina Taller Nutrivida",
        "latitud": 4.671000,
        "longitud": -74.058000,
        "radio_permitido_metros": 80,
        "puntos_impacto": 110,
        "tags": ["Cocina", "Salud", "Nutrición"],
        "imagen_url": "assets/images/act_cocina_saludable.png",
    },
    {
        "id": "act-013",
        "titulo": "Brigada de Salud Oral",
        "descripcion": "Valoración odontológica preventiva, profilaxis y entrega de kits de higiene dental.",
        "categoria": "Salud",
        "fecha": "2026-10-29",
        "hora": "08:30 AM",
        "duracion_horas": 4,
        "cupos_totales": 20,
        "cupos_ocupados": 16,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Puesto de Salud Bellavista",
        "latitud": 4.572000,
        "longitud": -74.120000,
        "radio_permitido_metros": 100,
        "puntos_impacto": 170,
        "tags": ["SaludOral", "Dientes", "Prevención"],
        "imagen_url": "assets/images/act_salud_oral_1.png",
    },
    {
        "id": "act-014",
        "titulo": "Taller Manejo del Estrés",
        "descripcion": "Sesión al aire libre de mindfulness, técnicas de respiración y relajación para el bienestar emocional.",
        "categoria": "Salud",
        "fecha": "2026-11-02",
        "hora": "07:00 AM",
        "duracion_horas": 2,
        "cupos_totales": 25,
        "cupos_ocupados": 18,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Parque El Virrey",
        "latitud": 4.673000,
        "longitud": -74.054000,
        "radio_permitido_metros": 100,
        "puntos_impacto": 100,
        "tags": ["Bienestar", "Mindfulness", "Estrés"],
        "imagen_url": "assets/images/act_manejo_estres.png",
    },
    {
        "id": "act-015",
        "titulo": "Campaña Donación de Sangre",
        "descripcion": "Jornada móvil de recolección de sangre y concientización sobre la importancia de salvar vidas.",
        "categoria": "Salud",
        "fecha": "2026-11-05",
        "hora": "09:00 AM",
        "duracion_horas": 6,
        "cupos_totales": 40,
        "cupos_ocupados": 27,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Plaza de Bolívar",
        "latitud": 4.598100,
        "longitud": -74.076000,
        "radio_permitido_metros": 150,
        "puntos_impacto": 220,
        "tags": ["Sangre", "Salud", "DonaVida"],
        "imagen_url": "assets/images/act_donacion_sangre.png",
    },
    {
        "id": "act-016",
        "titulo": "Limpieza Parques y Senderos",
        "descripcion": "Recolección de microplásticos y residuos en zonas verdes para proteger la fauna urbana.",
        "categoria": "Conservación",
        "fecha": "2026-11-08",
        "hora": "08:00 AM",
        "duracion_horas": 3,
        "cupos_totales": 25,
        "cupos_ocupados": 15,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Parque Metropolitano Simón Bolívar",
        "latitud": 4.658000,
        "longitud": -74.093000,
        "radio_permitido_metros": 120,
        "puntos_impacto": 130,
        "tags": ["Parques", "Limpieza", "Ambiente"],
        "imagen_url": "assets/images/act_limpieza_parques.png",
    },
    {
        "id": "act-017",
        "titulo": "Feria de Vida Saludable",
        "descripcion": "Feria comunitaria con stands de productos agroecológicos, chequeos médicos y hábitos saludables.",
        "categoria": "Salud",
        "fecha": "2026-11-12",
        "hora": "09:00 AM",
        "duracion_horas": 5,
        "cupos_totales": 35,
        "cupos_ocupados": 20,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Plaza Central de Usaquén",
        "latitud": 4.697000,
        "longitud": -74.032000,
        "radio_permitido_metros": 130,
        "puntos_impacto": 150,
        "tags": ["Feria", "Saludable", "Orgánico"],
        "imagen_url": "assets/images/act_feria_vida_saludable.png",
    },
    {
        "id": "act-018",
        "titulo": "Taller Primeros Auxilios",
        "descripcion": "Entrenamiento certificado en reanimación cardiopulmonar (RCP), vendajes y manejo de emergencias.",
        "categoria": "Salud",
        "fecha": "2026-11-15",
        "hora": "02:00 PM",
        "duracion_horas": 4,
        "cupos_totales": 20,
        "cupos_ocupados": 17,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Sede Cruz Roja Sector Norte",
        "latitud": 4.689000,
        "longitud": -74.053000,
        "radio_permitido_metros": 100,
        "puntos_impacto": 190,
        "tags": ["PrimerosAuxilios", "Emergencias", "RCP"],
        "imagen_url": "assets/images/act_primeros_auxilios.png",
    },
    {
        "id": "act-019",
        "titulo": "Limpiar Zonas Verdes",
        "descripcion": "Desmalezado, arreglo de jardines y recolección de hojarasca en separadores y parques barriales.",
        "categoria": "Conservación",
        "fecha": "2026-11-19",
        "hora": "08:30 AM",
        "duracion_horas": 3,
        "cupos_totales": 22,
        "cupos_ocupados": 14,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Corredor Ecológico Calle 100",
        "latitud": 4.685000,
        "longitud": -74.049000,
        "radio_permitido_metros": 110,
        "puntos_impacto": 120,
        "tags": ["ZonasVerdes", "Jardinería", "Ecología"],
        "imagen_url": "assets/images/act_limpiar_zonas_verdes.png",
    },
    {
        "id": "act-020",
        "titulo": "Huerta Urbana Comunitaria",
        "descripcion": "Siembra de hortalizas, compostaje orgánico y mantenimiento de eras agrícolas urbanas.",
        "categoria": "Reforestación",
        "fecha": "2026-11-22",
        "hora": "09:00 AM",
        "duracion_horas": 4,
        "cupos_totales": 25,
        "cupos_ocupados": 19,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Huerta Comunitaria San Cristóbal",
        "latitud": 4.568000,
        "longitud": -74.088000,
        "radio_permitido_metros": 120,
        "puntos_impacto": 160,
        "tags": ["Huerta", "Compostaje", "Siembra"],
        "imagen_url": "assets/images/act_huerta_urbana.png",
    },
    {
        "id": "act-021",
        "titulo": "Taller de Robótica Junior",
        "descripcion": "Taller de iniciación a la robótica y programación con materiales reciclados y microcontroladores.",
        "categoria": "Educación",
        "fecha": "2026-11-26",
        "hora": "03:00 PM",
        "duracion_horas": 3,
        "cupos_totales": 16,
        "cupos_ocupados": 12,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "FabLab Innovación Comunitaria",
        "latitud": 4.638000,
        "longitud": -74.085000,
        "radio_permitido_metros": 90,
        "puntos_impacto": 140,
        "tags": ["Robótica", "Tecnología", "Niños"],
        "imagen_url": "assets/images/act_robotica_junior.png",
    },
    {
        "id": "act-022",
        "titulo": "Taller de Lectura Infantil",
        "descripcion": "Cuentacuentos y club de lectura al aire libre para fomentar el amor por los libros en niños.",
        "categoria": "Educación",
        "fecha": "2026-11-29",
        "hora": "10:00 AM",
        "duracion_horas": 2,
        "cupos_totales": 20,
        "cupos_ocupados": 15,
        "estado_cupos": "disponible",
        "ubicacion_nombre": "Parque Infantil Los Sauces",
        "latitud": 4.721000,
        "longitud": -74.043000,
        "radio_permitido_metros": 80,
        "puntos_impacto": 90,
        "tags": ["Lectura", "Cuentos", "Infantil"],
        "imagen_url": "assets/images/act_lectura_infantil.png",
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

    results = [ActividadResponse(**a) for a in _mock_activities_db]
    if q:
        term = q.lower()
        results = [
            a for a in results
            if term in a.titulo.lower()
            or term in a.descripcion.lower()
            or term in a.ubicacion_nombre.lower()
        ]
    if categoria and categoria != "Todos":
        results = [a for a in results if a.categoria.lower() == categoria.lower()]

    return results

@router.get("/{activity_id}", response_model=ActividadResponse)
async def get_activity(activity_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            try:
                int_id = int(activity_id)
                res = supabase.table("actividades").select("*").eq("idactividades", int_id).execute()
                if res.data and len(res.data) > 0:
                    return map_supabase_actividad(res.data[0])
            except ValueError:
                pass
        except Exception as e:
            print(f"[Actividades Get] Error: {e}")

    for a in _mock_activities_db:
        if str(a["id"]) == str(activity_id):
            return ActividadResponse(**a)

    return ActividadResponse(
        id=activity_id,
        titulo="Actividad Ecológica",
        descripcion="Jornada comunitaria de conservación ambiental.",
        categoria="Conservación",
        fecha="2026-09-05",
        hora="08:00 AM",
        duracion_horas=4,
        cupos_totales=25,
        cupos_ocupados=10,
        estado_cupos="disponible",
        ubicacion_nombre="Parque Central",
        latitud=4.711000,
        longitud=-74.072100,
        radio_permitido_metros=100,
        puntos_impacto=100,
        tags=["Conservación", "Comunidad"],
        imagen_url="assets/images/act_reforestacion_rio.jpg",
    )

@router.post("", response_model=ActividadResponse, dependencies=[Depends(require_role(["admin", "administrador"]))])
async def create_activity(activity_data: ActividadCreate):
    """Crea una nueva actividad con imagen oficial por defecto (Solo Administrador)"""
    default_img = activity_data.imagen_url or "assets/images/act_reforestacion_rio.jpg"
    new_id = str(uuid.uuid4().int)[:6]
    
    supabase = get_supabase()
    if supabase:
        try:
            record = {
                "nombreactividad": activity_data.titulo,
                "descripcion": activity_data.descripcion,
                "categoria": activity_data.categoria,
                "fechainicio": activity_data.fecha,
                "cupos_totales": activity_data.cupos_totales,
                "ubicacion_nombre": activity_data.ubicacion_nombre,
                "latitud": activity_data.latitud,
                "longitud": activity_data.longitud,
                "imagen_url": default_img,
            }
            res = supabase.table("actividades").insert(record).execute()
            if res.data and len(res.data) > 0:
                return map_supabase_actividad(res.data[0])
        except Exception as e:
            print(f"[Actividades Create] Supabase error: {e}")

    new_act = ActividadResponse(
        id=new_id,
        titulo=activity_data.titulo,
        descripcion=activity_data.descripcion,
        categoria=activity_data.categoria,
        fecha=activity_data.fecha,
        hora=activity_data.hora,
        duracion_horas=activity_data.duracion_horas,
        cupos_totales=activity_data.cupos_totales,
        cupos_ocupados=0,
        estado_cupos="disponible",
        ubicacion_nombre=activity_data.ubicacion_nombre,
        latitud=activity_data.latitud,
        longitud=activity_data.longitud,
        radio_permitido_metros=activity_data.radio_permitido_metros,
        puntos_impacto=activity_data.puntos_impacto,
        tags=activity_data.tags or [activity_data.categoria],
        imagen_url=default_img,
    )
    _mock_activities_db.insert(0, new_act.model_dump())
    return new_act
