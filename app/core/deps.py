from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token

# Esquema de autenticación Bearer para OpenAPI / Swagger
security = HTTPBearer(auto_error=True, scheme_name="BearerAuth", description="Introduce el token JWT obtenido en /auth/login (formato: Bearer <token>)")

async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida. Por favor incluye el Bearer Token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

async def require_auth(
    user_payload: dict = Depends(get_current_user_token),
) -> dict:
    return user_payload

def is_admin_user(user: dict) -> bool:
    if user.get("es_admin") is True:
        return True
    role = str(user.get("rol") or user.get("role") or "").lower()
    return role in ["admin", "administrador"]

def get_user_id_from_payload(user: dict) -> str:
    return str(user.get("sub") or user.get("id") or "")

def require_role(allowed_roles: list[str]):
    async def role_checker(user: dict = Depends(require_auth)) -> dict:
        user_role = str(user.get("rol") or user.get("role") or "voluntario").lower()
        if user.get("es_admin") is True:
            user_role = "admin"
        allowed = [r.lower() for r in allowed_roles]
        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: Se requiere uno de los roles: {allowed_roles}. Tu rol actual es: '{user_role}'.",
            )
        return user
    return role_checker
