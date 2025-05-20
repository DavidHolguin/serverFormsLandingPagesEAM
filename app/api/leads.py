from fastapi import APIRouter, HTTPException, Request
from app.models.leads import LeadCreate
from app.services.supabase import supabase
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/")
async def create_lead(lead_data: LeadCreate, request: Request):
    try:
        # Crear un nuevo lead
        lead_id = uuid.uuid4()
        
        # Versiu00f3n absolutamente mu00ednima para pruebas
        lead = {
            "id": str(lead_id),
            "empresa_id": str(lead_data.empresa_id),
            "canal_origen": "forms",
            "estado": "nuevo",
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        # Insertar el lead en la tabla leads usando un enfoque diferente
        try:
            # Verificar la conexiu00f3n con Supabase
            print(f"URL: {supabase.supabase_url}, Key: {supabase.supabase_key[:10]}...")
            
            # Enfoque directo para insertar
            response = supabase.table("leads").insert(lead, count=None).execute()
            print(f"Respuesta completa: {response}")
            
            # Verificar si hay error en la respuesta
            if hasattr(response, 'error') and response.error:
                print(f"Error detallado: {response.error}")
                raise HTTPException(status_code=500, detail=f"Error al crear lead: {response.error}")
        except Exception as db_error:
            print(f"Excepciu00f3n en la inserciu00f3n: {str(db_error)}")
            raise HTTPException(status_code=500, detail=f"Error en la BD: {str(db_error)}")
        
        # Preparar datos personales del lead
        datos_personales = {
            "id": str(uuid.uuid4()),
            "lead_id": str(lead_id),
            "nombre": lead_data.datos_personales.nombre,
            "apellido": lead_data.datos_personales.apellido,
            "email": lead_data.datos_personales.email,
            "telefono": lead_data.datos_personales.telefono,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        # Insertar los datos personales usando el mismo enfoque mejorado
        try:
            # Enfoque directo para insertar datos personales
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
            print(f"Excepciu00f3n en la inserciu00f3n de datos personales: {str(db_error2)}")
            raise HTTPException(status_code=500, detail=f"Error en la BD para datos personales: {str(db_error2)}")
        
        return {
            "success": True,
            "lead_id": str(lead_id),
            "message": "Lead creado exitosamente"
        }
        
    except Exception as e:
        print(f"Error general: {str(e)}")  # Para debug
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}") 
