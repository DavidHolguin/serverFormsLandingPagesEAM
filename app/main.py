import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import leads, conversations

# Configurar logging para Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener puerto de Railway o usar 8000 como predeterminado
port = int(os.environ.get("PORT", 8000))
logger.info(f"Configurando la aplicación para ejecutarse en el puerto {port}")

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Captura de Leads",
    description="Servicio para capturar datos de leads y almacenarlos en Supabase",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, deberías especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])

@app.get("/")
async def root():
    logger.info("Endpoint raíz accedido - la aplicación está en funcionamiento")
    return {
        "message": "Bienvenido a la API de Captura de Leads",
        "status": "online",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
