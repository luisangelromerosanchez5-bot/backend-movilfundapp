from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, actividades, postulaciones, asistencias, donaciones, certificados

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
