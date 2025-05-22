from openai import OpenAI
from app.config.settings import OPENAI_API_KEY, OPENAI_MODEL
from typing import List, Dict, Any
import json

# Crear cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

async def extract_personal_data_from_conversation(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extrae múltiples conjuntos de datos personales de una conversación utilizando la API de OpenAI.
    Identifica cada conjunto de datos por su número de teléfono que es el identificador único.
    
    Args:
        messages: Lista de mensajes de la conversación en formato de diccionario
        
    Returns:
        Dictionary con los grupos de datos personales extraídos organizados por teléfono
    """
    
    # Convertir los mensajes al formato adecuado para análisis
    formatted_content = "\n\n".join([f"{msg.get('origen', 'system')}: {msg.get('contenido', '')}" for msg in messages])
    
    prompt = f"""
Busca y extrae TODOS los conjuntos de datos personales que puedas encontrar en la conversación.

Cada vez que encuentres un conjunto completo de datos personales (un lead potencial) debes extraerlo.
Debes detectar cuando hay cambios en los nombres o teléfonos, ya que esto indica que se está hablando de
una persona diferente.

Es muy importante que agrupes correctamente los datos que pertenecen a la misma persona y no mezcles información
de diferentes personas.

Utiliza el número de teléfono como identificador principal para agrupar los datos de cada persona.

Estructura la respuesta SOLO en formato JSON siguiendo esta estructura exacta:
{{
  "leads": [
    {{
      "telefono": "string", // Identificador único principal
      "datos_personales": [
        {{
          "nombre": "string o null",
          "apellido": "string o null",
          "email": "string o null",
          "telefono": "string", // Mismo valor que el identificador principal
          "programa_interes": "string o null",
          "datos_adicionales": {{
            // Cualquier otro dato personal relevante
          }}
        }}
      ]
    }}
  ]
}}

Conversación:
{formatted_content}
"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en extraer y agrupar datos personales de conversaciones. Tu tarea es identificar a todos los leads potenciales."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        # Obtener la respuesta generada
        extracted_data_str = response.choices[0].message.content
        
        try:
            # Intentar parsear la respuesta JSON
            extracted_data = json.loads(extracted_data_str)
            
            # Verificar que la estructura sea correcta
            if "leads" not in extracted_data or not isinstance(extracted_data["leads"], list):
                return {"success": False, "error": "La respuesta de OpenAI no tiene el formato esperado"}
                
            return {"success": True, "data": extracted_data}
            
        except json.JSONDecodeError as json_err:
            return {"success": False, "error": f"Error al decodificar la respuesta JSON: {str(json_err)}"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
