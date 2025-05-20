from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import leads

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

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Captura de Leads"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
