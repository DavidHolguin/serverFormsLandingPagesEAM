from fastapi import APIRouter, HTTPException, Request
from app.models.conversations import AnalyzeConversationRequest, AnalyzeConversationResponse, ExtractedPersonalData
from app.services.supabase import supabase
from app.services.openai_service import extract_personal_data_from_conversation
import uuid
from datetime import datetime
import json

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeConversationResponse)
async def analyze_conversation(request_data: AnalyzeConversationRequest, request: Request):
    """
    Analiza los mensajes de una conversación dentro de un rango de fechas 
    y extrae datos personales utilizando OpenAI.
    
    Args:
        request_data: Datos de la solicitud que incluyen el ID de la conversación y el rango de fechas
        
    Returns:
        Datos personales extraídos de la conversación
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
                message_count=0
            )
        
        # Utilizar OpenAI para extraer datos personales
        analysis_result = await extract_personal_data_from_conversation(messages)
        
        if not analysis_result["success"]:
            return AnalyzeConversationResponse(
                success=False,
                error=f"Error al analizar la conversación: {analysis_result.get('error')}",
                conversation_id=conversation_id,
                message_count=len(messages)
            )
        
        # Parsear la respuesta JSON de OpenAI
        try:
            extracted_data = json.loads(analysis_result["data"])
            personal_data = ExtractedPersonalData(**extracted_data)
            
            return AnalyzeConversationResponse(
                success=True,
                data=personal_data,
                conversation_id=conversation_id,
                message_count=len(messages)
            )
        except Exception as e:
            return AnalyzeConversationResponse(
                success=False,
                error=f"Error al procesar la respuesta de OpenAI: {str(e)}",
                conversation_id=conversation_id,
                message_count=len(messages)
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
