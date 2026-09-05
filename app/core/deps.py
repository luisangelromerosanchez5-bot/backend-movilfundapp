from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token

security = HTTPBearer(auto_error=False)

async def get_current_user_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[dict]:
    if not credentials:
        return None
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
    user_payload: Optional[dict] = Depends(get_current_user_token),
) -> dict:
    if not user_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida. Por favor incluye el Bearer Token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_payload

def require_role(allowed_roles: list[str]):
    async def role_checker(user: dict = Depends(require_auth)) -> dict:
        user_role = str(user.get("rol", "voluntario")).lower()
        allowed = [r.lower() for r in allowed_roles]
        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado. Se requiere uno de los roles: {allowed_roles}",
            )
        return user
    return role_checker
