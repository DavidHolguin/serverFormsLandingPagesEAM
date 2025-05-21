import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Validar configuración
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Las variables de entorno SUPABASE_URL y SUPABASE_KEY son requeridas")

if not OPENAI_API_KEY:
    raise ValueError("La variable de entorno OPENAI_API_KEY es requerida")
