import os
import sys

# Load environment variables if needed
from app.core.config import settings
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

try:
    res = supabase.table("postulaciones").select("*, actividades(*)").eq("usuarios_idusuarios", 73).execute()
    print("DATA INT:", res.data)
except Exception as e:
    print("ERROR INT:", e)

try:
    res2 = supabase.table("postulaciones").select("*, actividades(*)").eq("usuarios_idusuarios", "73").execute()
    print("DATA STR:", res2.data)
except Exception as e:
    print("ERROR STR:", e)
