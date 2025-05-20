from app.config.settings import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
