from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class AnalyzeConversationRequest(BaseModel):
    conversation_id: uuid.UUID
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ExtractedPersonalData(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    programa_interes: Optional[str] = None
    datos_adicionales: Optional[Dict[str, Any]] = None
    
class LeadGroup(BaseModel):
    telefono: str  # Identificador único del grupo
    leads: List[ExtractedPersonalData]
    
class AnalyzeConversationResponse(BaseModel):
    success: bool
    data: Optional[List[LeadGroup]] = None
    error: Optional[str] = None
    conversation_id: Optional[str] = None
    message_count: Optional[int] = None
    total_leads_found: Optional[int] = None
