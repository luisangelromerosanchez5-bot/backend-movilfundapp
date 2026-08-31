import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserLogin, UserRegister, UserUpdate, UserResponse, TokenResponse
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.database import get_supabase

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Almacén en memoria de fallback
_mock_users_db = {
    "luis@correo.com": {
        "id": "a1010000-0000-0000-0000-000000000001",
        "nombres": "Luis Fernando",
        "apellidos": "Pérez Gómez",
        "correo": "luis@correo.com",
        "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # 123456
        "fecha_nacimiento": "2001-05-02",
        "telefono": "+57 312 456 7890",
        "rol": "voluntario",
        "foto_url": None,
        "meta_anual_horas": 20,
        "horas_acumuladas": 14,
        "total_certificados": 3,
        "total_donaciones": 120000.0,
    }
}

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    supabase = get_supabase()
    if supabase:
        try:
            res = supabase.table("usuarios").select("*").eq("correo", credentials.email).execute()
            if res.data and len(res.data) > 0:
                user_data = res.data[0]
                if verify_password(credentials.password, user_data.get("password_hash", "")):
                    token = create_access_token(user_data["id"])
                    return TokenResponse(
                        access_token=token,
                        token_type="bearer",
                        user=UserResponse(**user_data),
                    )
        except Exception as e:
            print(f"[Auth Router] Fallback to local DB due to: {e}")

    user = _mock_users_db.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    token = create_access_token(user["id"])
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user),
    )

@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    supabase = get_supabase()
    user_id = str(uuid.uuid4())
    hashed = get_password_hash(data.password)

    new_user = {
        "id": user_id,
        "nombres": data.nombres,
        "apellidos": data.apellidos,
        "correo": data.correo,
        "password_hash": hashed,
        "fecha_nacimiento": data.fecha_nacimiento,
        "telefono": data.telefono,
        "rol": "voluntario",
        "foto_url": None,
        "meta_anual_horas": 20,
        "horas_acumuladas": 0,
        "total_certificados": 0,
        "total_donaciones": 0.0,
    }

    if supabase:
        try:
            res = supabase.table("usuarios").insert(new_user).execute()
            if res.data:
                token = create_access_token(user_id)
                return TokenResponse(
                    access_token=token,
                    token_type="bearer",
                    user=UserResponse(**new_user),
                )
        except Exception as e:
            print(f"[Auth Register] Fallback to local DB: {e}")

    _mock_users_db[data.correo] = new_user
    token = create_access_token(user_id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**new_user),
    )

@router.get("/me", response_model=UserResponse)
async def get_me():
    user = list(_mock_users_db.values())[0]
    return UserResponse(**user)
