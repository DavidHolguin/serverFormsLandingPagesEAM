from fastapi import APIRouter, HTTPException, Request
from app.models.conversations import AnalyzeConversationRequest, AnalyzeConversationResponse, ExtractedPersonalData, LeadGroup
from app.services.supabase import supabase
from app.services.openai_service import extract_personal_data_from_conversation
import uuid
from datetime import datetime
import json
from typing import List

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeConversationResponse)
async def analyze_conversation(request_data: AnalyzeConversationRequest, request: Request):
    """
    Analiza los mensajes de una conversación dentro de un rango de fechas 
    y extrae múltiples conjuntos de datos personales utilizando OpenAI.
    Agrupa los datos por número de teléfono (identificador único).
    
    Args:
        request_data: Datos de la solicitud que incluyen el ID de la conversación y el rango de fechas
        
    Returns:
        Grupos de datos personales extraídos de la conversación
    """
    try:
        conversation_id = str(request_data.conversation_id)
        
        # Construcción de la consulta para obtener mensajes
        query = supabase.table("mensajes").select("*").eq("conversacion_id", conversation_id)
        
        # Aplicar filtro de fechas si se proporcionan
        if request_data.start_date:
            query = query.gte("created_at", request_data.start_date.isoformat())
        if request_data.end_date:
            query = query.lte("created_at", request_data.end_date.isoformat())
            
        # Ordenar por fecha de creación
        query = query.order("created_at", desc=False)
        
        # Ejecutar la consulta
        response = query.execute()
        
        # Verificar si hay mensajes
        messages = response.data
        if not messages or len(messages) == 0:
            return AnalyzeConversationResponse(
                success=False,
                error="No se encontraron mensajes para la conversación en el rango de fechas especificado",
                conversation_id=conversation_id,
                message_count=0,
                total_leads_found=0
            )
        
        # Utilizar OpenAI para extraer datos personales
        analysis_result = await extract_personal_data_from_conversation(messages)
        
        if not analysis_result["success"]:
            return AnalyzeConversationResponse(
                success=False,
                error=f"Error al analizar la conversación: {analysis_result.get('error')}",
                conversation_id=conversation_id,
                message_count=len(messages),
                total_leads_found=0
            )
        
        # Procesar la respuesta de OpenAI que ya viene como diccionario
        try:
            extracted_data = analysis_result["data"]
            leads_data = extracted_data.get("leads", [])
            
            # Convertir la respuesta al formato de nuestro modelo
            lead_groups: List[LeadGroup] = []
            
            for lead_entry in leads_data:
                telefono = lead_entry.get("telefono", "")
                datos_personales_list = lead_entry.get("datos_personales", [])
                
                # Convertir cada item de datos_personales a nuestro modelo ExtractedPersonalData
                leads = []
                for datos in datos_personales_list:
                    lead_data = ExtractedPersonalData(
                        nombre=datos.get("nombre"),
                        apellido=datos.get("apellido"),
                        email=datos.get("email"),
                        telefono=datos.get("telefono"),
                        programa_interes=datos.get("programa_interes"),
                        datos_adicionales=datos.get("datos_adicionales", {})
                    )
                    leads.append(lead_data)
                
                # Crear el grupo de leads para este teléfono
                if telefono and leads:
                    lead_group = LeadGroup(telefono=telefono, leads=leads)
                    lead_groups.append(lead_group)
            
            total_leads = sum(len(group.leads) for group in lead_groups)
            
            return AnalyzeConversationResponse(
                success=True,
                data=lead_groups,
                conversation_id=conversation_id,
                message_count=len(messages),
                total_leads_found=total_leads
            )
        except Exception as e:
            return AnalyzeConversationResponse(
                success=False,
                error=f"Error al procesar la respuesta de OpenAI: {str(e)}",
                conversation_id=conversation_id,
                message_count=len(messages),
                total_leads_found=0
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
