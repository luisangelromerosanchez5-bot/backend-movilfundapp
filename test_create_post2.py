import asyncio
from app.routers.postulaciones import create_postulacion
from app.schemas.actividades import PostulacionCreate

async def main():
    data = PostulacionCreate(
        actividad_id="28",
        usuario_id="75",
        actividad_titulo="Test JPMercado",
        actividad_fecha="2026-09-22",
        actividad_hora="10:00",
        actividad_ubicacion="Test",
        nombres="JP Mercado",
        correo="jpmercado@gmail.com",
        notas="Test"
    )
    current_user = {"sub": "75", "rol": "voluntario"}
    
    try:
        res = await create_postulacion(data, current_user)
        print(res)
    except Exception as e:
        print("EXCEPTION:", e)

if __name__ == "__main__":
    asyncio.run(main())
