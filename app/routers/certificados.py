from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.certificado import CertificadoResponse
from app.core.database import get_supabase

router = APIRouter(prefix="/certificados", tags=["Certificados"])

def map_certificado(row: dict) -> CertificadoResponse:
    c_id = str(row.get("idcertificados") or row.get("id") or "")
    user_id = str(row.get("usuarios_idusuarios") or row.get("usuario_id") or "1")
    act_id = str(row.get("actividades_idactividades") or row.get("actividad_id") or "")
    nombre_voluntario = row.get("nombrevoluntario") or row.get("destinatario") or "Voluntario Biosferas"
    actividad_titulo = row.get("actividadasociada") or row.get("actividad_titulo") or "Actividad Ambiental"
    codigo = row.get("codigo_verificacion") or f"FB-VOL-2026-00{c_id}"
    tipo = row.get("tipo") or "voluntariado"
    titulo = row.get("titulo") or f"Certificado de {tipo.capitalize()}"
    horas = row.get("horas") or 14
    monto = float(row.get("monto") or 0.0) if row.get("monto") else None
    firmado_por = row.get("firmado_por") or "Dra. Elena Ramos - Directora Ejecutiva"
    documento = str(row.get("documento_identidad") or "1.098.765.432")

    return CertificadoResponse(
        id=c_id,
        usuario_id=user_id,
        actividad_id=act_id,
        donacion_id=None,
        tipo=tipo,
        titulo=titulo,
        actividad_titulo=actividad_titulo,
        horas=horas,
        monto=monto,
        fecha_emision=date(2026, 8, 15),
        estado="aprobado",
        codigo_verificacion=codigo,
        firmado_por=firmado_por,
        destinatario=nombre_voluntario,
        documento_identidad=documento,
    )

@router.get("/usuario/{usuario_id}", response_model=List[CertificadoResponse])
async def get_certificates_by_user(usuario_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            if usuario_id.isdigit():
                res = supabase.table("certificados").select("*").eq("usuarios_idusuarios", int(usuario_id)).execute()
            else:
                res = supabase.table("certificados").select("*").execute()
            if res.data and len(res.data) > 0:
                return [map_certificado(c) for c in res.data]
        except Exception as e:
            print(f"[Certificados Router] Supabase get error: {e}")

    return []

@router.get("/{cert_id}", response_model=CertificadoResponse)
async def get_certificate_by_id(cert_id: str):
    supabase = get_supabase()
    if supabase:
        try:
            if cert_id.isdigit():
                res = supabase.table("certificados").select("*").eq("idcertificados", int(cert_id)).execute()
                if res.data and len(res.data) > 0:
                    return map_certificado(res.data[0])
        except Exception as e:
            print(f"[Certificados Get] Supabase error: {e}")

    raise HTTPException(status_code=404, detail="Certificado no encontrado")
