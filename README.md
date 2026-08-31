# FundAPP Backend API · Fundación Biosferas

API REST desarrollada en **FastAPI** y conectada con **Supabase (PostgreSQL)** para soportar las operaciones de la plataforma web y la extensión móvil de **FundAPP**.

---

## 🛠️ Stack Tecnológico
- **Framework**: FastAPI (Python 3.11+)
- **Base de Datos**: Supabase (PostgreSQL 15+)
- **Seguridad**: JWT (JSON Web Tokens) con algoritmo HS256 y encriptación de contraseñas con `bcrypt`
- **Contenerización**: Docker & Docker Compose

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/luisangelromerosanchez5-bot/backend-movilfundapp.git
   cd backend-movilfundapp
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Variables de entorno**:
   Copia el archivo `.env.example` a `.env` y configura tus credenciales de Supabase:
   ```bash
   cp .env.example .env
   ```

4. **Ejecutar servidor**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Documentación Swagger UI interactiva**:
   Accede a [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 Endpoints Principales

| Módulo | Método | Endpoint | Descripción |
|---|---|---|---|
| **Auth** | `POST` | `/api/v1/auth/login` | Iniciar sesión y emitir JWT |
| **Auth** | `POST` | `/api/v1/auth/register` | Registrar nuevo voluntario |
| **Auth** | `GET` | `/api/v1/auth/me` | Obtener perfil del usuario autenticado |
| **Actividades**| `GET` | `/api/v1/actividades` | Listar actividades con búsqueda y filtros |
| **Postulaciones**| `POST` | `/api/v1/postulaciones` | Postularse a una actividad |
| **Asistencias**| `POST` | `/api/v1/asistencias` | Check-in GPS con validación de geofencing |
| **Asistencias**| `PATCH`| `/api/v1/asistencias/{id}` | Check-out y guardado de pasos del podómetro |
| **Donaciones** | `POST` | `/api/v1/donaciones` | Registrar donación por PSE/Tarjeta/Nequi |
| **Certificados**| `GET` | `/api/v1/certificados/usuario/{id}` | Historial de certificados de voluntariado y donación |
