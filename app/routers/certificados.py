import uuid
from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends, status
from app.schemas.certificado import CertificadoResponse, CertificadoCreate
from app.core.database import get_supabase
from app.core.deps import require_auth

router = APIRouter(prefix="/certificados", tags=["Certificados"])

def map_certificado(row: dict) -> CertificadoResponse:
    c_id = str(row.get("idcertificados") or row.get("id") or "")
    user_id = str(row.get("usuarios_idusuarios") or row.get("usuario_id") or "1")
    act_id = str(row.get("actividades_idactividades") or row.get("actividad_id") or "")
    nombre_voluntario = row.get("nombrevoluntario") or row.get("destinatario") or "Voluntario Biosferas"
    actividad_titulo = row.get("actividadasociada") or row.get("actividad_titulo") or "Actividad Ambiental"
    codigo = row.get("codigo_verificacion") or f"FB-VOL-2026-{c_id.zfill(4)}"
    tipo = row.get("tipo") or ("donacion" if row.get("monto") else "voluntariado")
    titulo = row.get("titulo") or f"Certificado de {tipo.capitalize()}"
    horas = int(row.get("horas") or 4) if tipo == "voluntariado" else None
    monto = float(row.get("monto") or 0.0) if tipo == "donacion" and row.get("monto") else None
    firmado_por = row.get("firmado_por") or "Dra. Elena Ramos - Directora Ejecutiva"
    documento = str(row.get("documento_identidad") or "1.098.765.432")
    fecha_em = row.get("fecha_emision")
    if isinstance(fecha_em, str):
        try:
            fecha_parsed = datetime.fromisoformat(fecha_em.replace("Z", "")).date()
        except Exception:
            fecha_parsed = date.today()
    elif isinstance(fecha_em, date):
        fecha_parsed = fecha_em
    else:
        fecha_parsed = date.today()

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
        fecha_emision=fecha_parsed,
        estado=row.get("estado") or "aprobado",
        codigo_verificacion=codigo,
        firmado_por=firmado_por,
        destinatario=nombre_voluntario,
        documento_identidad=documento,
    )

@router.get("", response_model=List[CertificadoResponse])
async def list_certificates(
    usuario_id: Optional[str] = Query(None),
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    # RBAC: El admin puede consultar todos o por usuario_id. El voluntario sólo sus propios certificados.
    if user_role in ["admin", "administrador"]:
        target_user = usuario_id
    else:
        target_user = user_sub

    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table("certificados").select("*")
            if target_user:
                if target_user.isdigit():
                    query = query.eq("usuarios_idusuarios", int(target_user))
                else:
                    query = query.eq("usuarios_idusuarios", target_user)
            res = query.execute()
            if res.data:
                return [map_certificado(c) for c in res.data]
        except Exception as e:
            print(f"[Certificados List] Supabase query error: {e}")
    return []

@router.get("/usuario/{usuario_id}", response_model=List[CertificadoResponse])
async def get_certificates_by_user(
    usuario_id: str,
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    # RBAC: Bloquear consulta si no es admin y pide certificados de otra persona
    if user_role not in ["admin", "administrador"] and user_sub != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido: Solo puedes consultar tus propios certificados.",
        )

    supabase = get_supabase()
    if supabase:
        try:
            if usuario_id.isdigit():
                res = supabase.table("certificados").select("*").eq("usuarios_idusuarios", int(usuario_id)).execute()
            else:
                res = supabase.table("certificados").select("*").eq("usuarios_idusuarios", usuario_id).execute()
            if res.data and len(res.data) > 0:
                return [map_certificado(c) for c in res.data]
        except Exception as e:
            print(f"[Certificados Router] Supabase get error: {e}")

    return []

@router.post("", response_model=CertificadoResponse)
async def create_certificate(
    cert_data: CertificadoCreate,
    current_user: dict = Depends(require_auth),
):
    user_role = str(current_user.get("rol", "voluntario")).lower()
    user_sub = str(current_user.get("sub", ""))

    effective_user_id = cert_data.usuario_id if user_role in ["admin", "administrador"] else (user_sub or cert_data.usuario_id)

    supabase = get_supabase()
    codigo_verif = f"FB-{'VOL' if cert_data.tipo == 'voluntariado' else 'DON'}-2026-{str(uuid.uuid4().int)[:6]}"
    
    if supabase:
        try:
            new_row = {
                "nombrevoluntario": cert_data.destinatario or "Voluntario Biosferas",
                "actividadasociada": cert_data.actividad_titulo or "Jornada Ambiental",
                "codigo_verificacion": codigo_verif,
                "usuarios_idusuarios": int(effective_user_id) if effective_user_id and effective_user_id.isdigit() else 1,
            }
            if cert_data.actividad_id and cert_data.actividad_id.isdigit():
                new_row["actividades_idactividades"] = int(cert_data.actividad_id)
            res = supabase.table("certificados").insert(new_row).execute()
            if res.data and len(res.data) > 0:
                return map_certificado(res.data[0])
        except Exception as e:
            print(f"[Certificados Create] Error: {e}")

    return CertificadoResponse(
        id=str(uuid.uuid4()),
        usuario_id=effective_user_id,
        actividad_id=cert_data.actividad_id,
        donacion_id=None,
        tipo=cert_data.tipo,
        titulo=cert_data.titulo,
        actividad_titulo=cert_data.actividad_titulo,
        horas=cert_data.horas,
        monto=cert_data.monto,
        fecha_emision=date.today(),
        estado="aprobado",
        codigo_verificacion=codigo_verif,
        firmado_por="Dra. Elena Ramos - Directora Ejecutiva",
        destinatario=cert_data.destinatario or "Voluntario Biosferas",
        documento_identidad=cert_data.documento_identidad or "1.098.765.432",
    )
