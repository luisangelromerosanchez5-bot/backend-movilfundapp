from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.certificado import CertificadoResponse
from app.core.database import get_supabase

router = APIRouter(prefix="/certificados", tags=["Certificados"])

_mock_certificados_db = [
    {
        "id": "cert-001",
        "usuario_id": "a1010000-0000-0000-0000-000000000001",
        "actividad_id": "act-001",
        "donacion_id": None,
        "tipo": "voluntariado",
        "titulo": "Certificado de Voluntariado",
        "actividad_titulo": "Reforestación Río Bosque",
        "horas": 14,
        "monto": None,
        "fecha_emision": date(2026, 8, 15),
        "estado": "aprobado",
        "codigo_verificacion": "FB-VOL-2026-0892",
        "firmado_por": "Dra. Elena Ramos - Directora Ejecutiva",
        "destinatario": "Luis Fernando Pérez Gómez",
        "documento_identidad": "1.098.765.432",
    },
    {
        "id": "cert-002",
        "usuario_id": "a1010000-0000-0000-0000-000000000001",
        "actividad_id": None,
        "donacion_id": "don-001",
        "tipo": "donacion",
        "titulo": "Certificado de Donación",
        "actividad_titulo": "Aporte Proyecto Cuencas Vivas",
        "horas": None,
        "monto": 70000.0,
        "fecha_emision": date(2026, 7, 28),
        "estado": "aprobado",
        "codigo_verificacion": "FB-DON-2026-0411",
        "firmado_por": "Carlos Mendoza - Tesorería Fundación",
        "destinatario": "Luis Fernando Pérez Gómez",
        "documento_identidad": "1.098.765.432",
    },
    {
        "id": "cert-003",
        "usuario_id": "a1010000-0000-0000-0000-000000000001",
        "actividad_id": "act-003",
        "donacion_id": None,
        "tipo": "voluntariado",
        "titulo": "Certificado de Voluntariado",
        "actividad_titulo": "Censo de Aves y Reforestación",
        "horas": 6,
        "monto": None,
        "fecha_emision": date(2026, 8, 28),
        "estado": "en_proceso",
        "codigo_verificacion": "FB-VOL-2026-PEND",
        "firmado_por": "En revisión por coordinación",
        "destinatario": "Luis Fernando Pérez Gómez",
        "documento_identidad": "1.098.765.432",
    },
]

@router.get("/usuario/{usuario_id}", response_model=List[CertificadoResponse])
async def get_certificates_by_user(usuario_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("certificados").select("*").eq("usuario_id", usuario_id).execute()
            if res.data and len(res.data) > 0:
                return [CertificadoResponse(**c) for c in res.data]
        except Exception as e:
            print(f"[Certificados Router] Supabase fallback: {e}")

    return [CertificadoResponse(**c) for c in _mock_certificados_db]

@router.get("/{cert_id}", response_model=CertificadoResponse)
async def get_certificate_by_id(cert_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("certificados").select("*").eq("id", cert_id).execute()
            if res.data and len(res.data) > 0:
                return CertificadoResponse(**res.data[0])
        except Exception as e:
            print(f"[Certificados Router] Supabase fallback: {e}")

    cert = next((c for c in _mock_certificados_db if c["id"] == cert_id), None)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    return CertificadoResponse(**cert)
