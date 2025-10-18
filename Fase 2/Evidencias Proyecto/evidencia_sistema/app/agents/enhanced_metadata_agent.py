from database.sqlite_manager import HortifrutDatabase
from app.agents.sql_translator import SQLTranslator
from knowledge_base.hortifrut_knowledge import HORTIFRUT_KNOWLEDGE

class EnhancedHortifrutAgent:
    def __init__(self):
        self.kb = HORTIFRUT_KNOWLEDGE
        self.database = HortifrutDatabase()
        self.sql_translator = SQLTranslator(self.database.get_table_info())
    
    def process_query(self, user_query: str):
        """Procesar consulta - intentar con BD primero, luego con metadatos"""
        
        # Primero intentar con la base de datos real
        db_response = self._try_database_query(user_query)
        if db_response:
            return db_response
        
        # Si falla, usar el sistema de metadatos existente
        return self._fallback_to_metadata(user_query)
    
    def _try_database_query(self, user_query: str):
        """Intentar procesar la consulta con la base de datos"""
        try:
            print(f"Intentando traducir a SQL: {user_query}")
            sql_query = self.sql_translator.natural_language_to_sql(user_query)
            print(f"SQL generado: {sql_query}")
            
            results = self.database.execute_query(sql_query)
            
            if not results.empty:
                return self._format_data_results(results, user_query)
            else:
                return None
                
        except Exception as e:
            print(f"Error en consulta BD: {str(e)}")
            return None
    
    def _format_data_results(self, df, original_query):
        """Formatear resultados de DataFrame a respuesta natural"""
        if df.empty:
            return "No encontré datos que coincidan con tu búsqueda."
        
        response = f"**Encontré {len(df)} resultado(s) para: '{original_query}'**\n\n"
        
        # Mostrar como tabla markdown
        response += "| " + " | ".join(str(col) for col in df.columns) + " |\n"
        response += "|" + "|".join(["---"] * len(df.columns)) + "|\n"
        
        for _, row in df.head(5).iterrows():
            response += "| " + " | ".join(str(x) for x in row) + " |\n"
        
        if len(df) > 5:
            response += f"\n*Mostrando 5 de {len(df)} resultados*"
        
        return response
    
    def _fallback_to_metadata(self, user_query):
        """Volver al sistema de metadatos si falla la BD"""
        from app.agents.metadata_agent import HortifrutMetadataAgent
        metadata_agent = HortifrutMetadataAgent(self.kb)
        return metadata_agent.process_query(user_query)