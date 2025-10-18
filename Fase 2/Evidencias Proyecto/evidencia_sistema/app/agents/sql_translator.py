import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SQLTranslator:
    def __init__(self, database_schema):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.schema = database_schema
    
    def natural_language_to_sql(self, user_query: str):
        """Convertir pregunta natural a SQL usando OpenAI directo"""
        
        system_prompt = f"""
        Eres un experto en SQL y en la base de datos de Hortifrut. Convierte preguntas en español a consultas SQL válidas.

        ESQUEMA DE LA BASE DE DATOS:
        {self._format_schema_for_prompt()}

        REGLAS IMPORTANTES:
        1. Devuelve SOLO el query SQL, sin explicaciones ni texto adicional
        2. Usa JOINs para relacionar tablas cuando necesites datos de múltiples tablas
        3. Siempre incluye LIMIT 10 al final para evitar resultados demasiado grandes
        4. Usa LIKE para búsquedas de texto parcial (ej: WHERE productos.nombre LIKE '%arándano%')
        5. Para el año actual usa 2024
        6. Usa nombres de columnas exactos del esquema

        EJEMPLOS:
        - "cosecha de arándanos" → "SELECT * FROM cosechas JOIN productos ON cosechas.producto_id = productos.id WHERE productos.nombre LIKE '%arándano%' LIMIT 10"
        - "encargados de planta santiago" → "SELECT encargados.* FROM encargados JOIN cosechas ON encargados.id = cosechas.encargado_id JOIN ubicaciones ON cosechas.ubicacion_id = ubicaciones.id WHERE ubicaciones.nombre LIKE '%santiago%' LIMIT 10"
        - "cuántos kilos de frutilla se cosecharon" → "SELECT SUM(cantidad_kg) as total_kg FROM cosechas JOIN productos ON cosechas.producto_id = productos.id WHERE productos.nombre LIKE '%frutilla%' LIMIT 10"

        Ahora convierte esta pregunta: "{user_query}"
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0
            )
            
            sql_query = response.choices[0].message.content.strip()
            print(f"🔍 SQL generado: {sql_query}")
            return self._validate_sql(sql_query)
            
        except Exception as e:
            raise Exception(f"Error traduciendo a SQL: {str(e)}")
    
    def _format_schema_for_prompt(self):
        """Formatear esquema para el prompt del LLM"""
        schema_text = ""
        for table, columns in self.schema.items():
            schema_text += f"TABLA: {table}\n"
            schema_text += f"COLUMNAS: {', '.join(columns)}\n\n"
        return schema_text
    
    def _validate_sql(self, sql_query: str):
        """Validar que el SQL sea seguro"""
        dangerous_keywords = ["DELETE", "UPDATE", "DROP", "INSERT", "ALTER", "CREATE", "TRUNCATE"]
        
        for keyword in dangerous_keywords:
            if keyword.upper() in sql_query.upper():
                raise Exception(f"Query contiene operación peligrosa: {keyword}")
        
        # Asegurar que tenga LIMIT
        if "LIMIT" not in sql_query.upper():
            sql_query += " LIMIT 10"
        
        return sql_query