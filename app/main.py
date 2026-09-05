from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.routers import auth, actividades, postulaciones, asistencias, donaciones, certificados, admin

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API REST de Fundación Biosferas para FundAPP (Móvil y Web)",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(actividades.router, prefix=settings.API_V1_STR)
app.include_router(postulaciones.router, prefix=settings.API_V1_STR)
app.include_router(asistencias.router, prefix=settings.API_V1_STR)
app.include_router(donaciones.router, prefix=settings.API_V1_STR)
app.include_router(certificados.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="API REST de Fundación Biosferas para FundAPP (Móvil y Web)",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Ingresa el token JWT obtenido en /api/v1/auth/login",
        }
    }
    # Candado global para Swagger
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "docs": "/docs",
        "version": "1.0.0",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
