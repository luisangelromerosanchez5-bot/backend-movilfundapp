from typing import Optional
from supabase import create_client, Client
from app.core.config import settings

supabase_client: Optional[Client] = None

def get_supabase() -> Optional[Client]:
    global supabase_client
    if supabase_client is None and settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        except Exception as e:
            print(f"[Supabase] Error al inicializar cliente Supabase: {e}")
            supabase_client = None
    return supabase_client
