import asyncio
from app.core.config import settings
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

try:
    query = supabase.table("postulaciones").select("*, actividades(*)")
    res = query.eq("usuarios_idusuarios", "73").execute()
    print("Success:", res.data)
except Exception as e:
    print("Error:", e)
