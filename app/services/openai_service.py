from openai import OpenAI
from app.config.settings import OPENAI_API_KEY, OPENAI_MODEL
from typing import List, Dict, Any

# Crear cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

async def extract_personal_data_from_conversation(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extrae datos personales de una conversación utilizando la API de OpenAI.
    
    Args:
        messages: Lista de mensajes de la conversación en formato de diccionario
        
    Returns:
        Dictionary con los datos personales extraídos
    """
    
    # Convertir los mensajes al formato adecuado para análisis
    formatted_content = "\n\n".join([f"{msg.get('origen', 'system')}: {msg.get('contenido', '')}" for msg in messages])
    
    prompt = f"""
Extrae los siguientes datos personales de la conversación proporcionada. Es importante que identifiques los datos 
más actuales si hay información repetida o contradictoria. Si no encuentras algún dato, deja el campo como null.

Estructura la respuesta SOLO en formato JSON siguiendo esta estructura exacta:
{{
  "nombre": string o null,
  "apellido": string o null,
  "email": string o null,
  "telefono": string o null,
  "programa_interes": string o null,
  "datos_adicionales": {{
    // Cualquier otro dato personal relevante que hayas encontrado
  }}
}}

Conversación:
{formatted_content}
"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en extraer datos personales de conversaciones."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        # Obtener la respuesta generada
        extracted_data = response.choices[0].message.content
        return {"success": True, "data": extracted_data}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
