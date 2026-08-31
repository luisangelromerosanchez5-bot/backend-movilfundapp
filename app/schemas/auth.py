from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    nombres: str
    apellidos: str
    correo: str
    password: str
    fecha_nacimiento: Optional[str] = None
    telefono: Optional[str] = None

class UserUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    foto_url: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    nombres: str
    apellidos: str
    correo: str
    fecha_nacimiento: Optional[str] = None
    telefono: Optional[str] = None
    rol: str = "voluntario"
    foto_url: Optional[str] = None
    meta_anual_horas: int = 20
    horas_acumuladas: int = 0
    total_certificados: int = 0
    total_donaciones: float = 0.0

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
