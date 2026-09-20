from app.schemas.postulacion import PostulacionResponse
from app.routers.postulaciones import _mock_postulaciones_db
try:
    for p in _mock_postulaciones_db:
        PostulacionResponse(**p)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
