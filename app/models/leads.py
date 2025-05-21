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

class SessionData(BaseModel):
    startTime: Optional[int] = None
    lastActivity: Optional[int] = None
    isActive: Optional[bool] = True
    timeOnPage: Optional[int] = None
    visitCount: Optional[int] = None
    pageUrl: Optional[str] = None
    referrer: Optional[str] = None

class InteractionsData(BaseModel):
    totalClicks: Optional[int] = None
    buttonClicks: Optional[int] = None
    linkClicks: Optional[int] = None
    formInteractions: Optional[int] = None
    formFocusTime: Optional[int] = None
    scrollDepth: Optional[int] = None
    maxScrollDepth: Optional[int] = None

class EnvironmentData(BaseModel):
    viewport: Optional[str] = None
    screenSize: Optional[str] = None
    deviceType: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

class EventData(BaseModel):
    timestamp: Optional[int] = None
    type: Optional[str] = None
    data: Optional[Dict[str, Any]] = {}

class TrackingData(BaseModel):
    session: Optional[SessionData] = Field(default_factory=SessionData)
    interactions: Optional[InteractionsData] = Field(default_factory=InteractionsData)
    environment: Optional[EnvironmentData] = Field(default_factory=EnvironmentData)
    events: Optional[List[EventData]] = Field(default_factory=list)

class LeadCreate(BaseModel):
    canal_id: Optional[uuid.UUID] = None
    empresa_id: uuid.UUID
    pipeline_id: Optional[uuid.UUID] = None
    stage_id: Optional[uuid.UUID] = None
    datos_personales: LeadDatosPersonales
    navegacion_info: NavegacionInfo
    tracking_data: Optional[TrackingData] = None
