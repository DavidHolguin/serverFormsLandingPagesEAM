# API de Captura de Leads

Servidor FastAPI para capturar datos de leads y almacenarlos en Supabase.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno virtual: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Unix)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar variables de entorno en archivo `.env`

## Ejecución

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `POST /api/leads`: Crear un nuevo lead con datos personales
