from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field
import uuid

class LeadDatosPersonales(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    pais: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    datos_adicionales: Optional[Dict[str, Any]] = None

class NavegacionInfo(BaseModel):
    ip: str
    fecha_hora: datetime = Field(default_factory=datetime.now)
    tiempo_navegacion: Optional[float] = None  # en segundos
    interacciones: Optional[int] = None
    profundidad_scroll: Optional[float] = None  # porcentaje
    pagina_url: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

class LeadCreate(BaseModel):
    canal_id: Optional[uuid.UUID] = None
    empresa_id: uuid.UUID
    pipeline_id: Optional[uuid.UUID] = None
    stage_id: Optional[uuid.UUID] = None
    datos_personales: LeadDatosPersonales
    navegacion_info: NavegacionInfo
