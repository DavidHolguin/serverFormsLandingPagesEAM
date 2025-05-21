from fastapi import APIRouter, HTTPException, Request
from app.models.leads import LeadCreate
from app.services.supabase import supabase
import uuid
from datetime import datetime
import json

router = APIRouter()

@router.post("/")
async def create_lead(lead_data: LeadCreate, request: Request):
    try:
        # Crear un nuevo lead
        lead_id = uuid.uuid4()
        
        # Versión mínima para pruebas
        lead = {
            "id": str(lead_id),
            "empresa_id": str(lead_data.empresa_id),
            "canal_origen": "forms",
            "canal_id": str(lead_data.canal_id) if lead_data.canal_id else None,
            "pipeline_id": str(lead_data.pipeline_id) if lead_data.pipeline_id else None,
            "stage_id": str(lead_data.stage_id) if lead_data.stage_id else None,
            "estado": "nuevo",
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        # Insertar el lead en la tabla leads
        try:
            # Verificar la conexión con Supabase
            print(f"URL: {supabase.supabase_url}, Key: {supabase.supabase_key[:10]}...")
            
            # Enfoque directo para insertar
            response = supabase.table("leads").insert(lead, count=None).execute()
            print(f"Respuesta completa: {response}")
            
            # Verificar si hay error en la respuesta
            if hasattr(response, 'error') and response.error:
                print(f"Error detallado: {response.error}")
                raise HTTPException(status_code=500, detail=f"Error al crear lead: {response.error}")
        except Exception as db_error:
            print(f"Excepción en la inserción: {str(db_error)}")
            raise HTTPException(status_code=500, detail=f"Error en la BD: {str(db_error)}")
        
        # Preparar datos personales del lead
        datos_personales = {
            "id": str(uuid.uuid4()),
            "lead_id": str(lead_id),
            "nombre": lead_data.datos_personales.nombre,
            "apellido": lead_data.datos_personales.apellido,
            "email": lead_data.datos_personales.email,
            "telefono": lead_data.datos_personales.telefono,
            "pais": lead_data.datos_personales.pais,
            "ciudad": lead_data.datos_personales.ciudad,
            "direccion": lead_data.datos_personales.direccion,
            "datos_adicionales": lead_data.datos_personales.datos_adicionales,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        # Insertar los datos personales
        try:
            response_personal = supabase.table("lead_datos_personales").insert(datos_personales, count=None).execute()
            print(f"Respuesta de datos personales: {response_personal}")
            
            # Verificar si hay error en la respuesta
            if hasattr(response_personal, 'error') and response_personal.error:
                # Si hay error, intenta eliminar el lead creado previamente
                supabase.table("leads").delete().eq("id", str(lead_id)).execute()
                print(f"Error detallado en datos personales: {response_personal.error}")
                raise HTTPException(status_code=500, detail=f"Error al crear datos personales: {response_personal.error}")
        except Exception as db_error2:
            # Si hay error, intenta eliminar el lead creado previamente
            try:
                supabase.table("leads").delete().eq("id", str(lead_id)).execute()
            except:
                pass  # Si no puede eliminar, continuamos de todos modos
            print(f"Excepción en la inserción de datos personales: {str(db_error2)}")
            raise HTTPException(status_code=500, detail=f"Error en la BD para datos personales: {str(db_error2)}")
        
        # Manejar los datos de tracking si existen
        if lead_data.tracking_data:
            tracking_data = {
                "id": str(uuid.uuid4()),
                "lead_id": str(lead_id),
                "session": lead_data.tracking_data.session.dict() if lead_data.tracking_data.session else None,
                "interactions": lead_data.tracking_data.interactions.dict() if lead_data.tracking_data.interactions else None,
                "environment": lead_data.tracking_data.environment.dict() if lead_data.tracking_data.environment else None,
                "events": [event.dict() for event in lead_data.tracking_data.events] if lead_data.tracking_data.events else None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            
            try:
                response_tracking = supabase.table("lead_tracking_data").insert(tracking_data, count=None).execute()
                print(f"Respuesta de tracking data: {response_tracking}")
                
                # Verificar si hay error en la respuesta
                if hasattr(response_tracking, 'error') and response_tracking.error:
                    print(f"Error detallado en tracking data: {response_tracking.error}")
                    # Continuamos aunque haya error en tracking data, no es crítico
            except Exception as tracking_error:
                print(f"Excepción en la inserción de tracking data: {str(tracking_error)}")
                # Continuamos aunque haya error en tracking data, no es crítico
        
        return {
            "success": True,
            "lead_id": str(lead_id),
            "message": "Lead creado exitosamente"
        }
        
    except Exception as e:
        print(f"Error general: {str(e)}")  # Para debug
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}") 
