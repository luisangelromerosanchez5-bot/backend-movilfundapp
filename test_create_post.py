import asyncio
from app.routers.postulaciones import create_postulacion
from app.schemas.actividades import PostulacionCreate

async def main():
    data = PostulacionCreate(
        actividad_id="1",
        usuario_id="73",  # Paola
        actividad_titulo="Test",
        actividad_fecha="2026-09-22",
        actividad_hora="10:00",
        actividad_ubicacion="Test",
        nombres="Paola",
        correo="paola2@gmail.com",
        notas="Test"
    )
    current_user = {"sub": "73", "rol": "voluntario"}
    
    res = await create_postulacion(data, current_user)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
