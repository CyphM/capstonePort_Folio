import sqlite3
import pandas as pd
from database.hortifrut_schema import HORTIFRUT_DATABASE_SCHEMA
from database.sample_data import SAMPLE_DATA

class HortifrutDatabase:
    def __init__(self, db_path="hortifrut_data.db"):
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Crear base de datos y poblar con datos de ejemplo"""
        self.connection = sqlite3.connect(self.db_path)
        
        # Crear tablas
        for table_name, table_info in HORTIFRUT_DATABASE_SCHEMA.items():
            self._create_table(table_name, table_info["columns"])
        
        # Insertar datos de ejemplo
        self._populate_sample_data()
    
    def _create_table(self, table_name, columns):
        """Crear tabla en SQLite"""
        columns_def = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
    
    def _populate_sample_data(self):
        """Poblar con datos de ejemplo"""
        for table_name, records in SAMPLE_DATA.items():
            for record in records:
                placeholders = ", ".join(["?"] * len(record))
                columns = ", ".join(record.keys())
                query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                cursor = self.connection.cursor()
                cursor.execute(query, list(record.values()))
        
        self.connection.commit()
    
    def execute_query(self, sql_query: str):
        """Ejecutar consulta SQL y retornar resultados"""
        try:
            df = pd.read_sql_query(sql_query, self.connection)
            return df
        except Exception as e:
            raise Exception(f"Error ejecutando query: {str(e)}")
    
    def get_table_info(self):
        """Obtener información del esquema para el NLP"""
        schema_info = {}
        cursor = self.connection.cursor()
        
        for table_name in HORTIFRUT_DATABASE_SCHEMA.keys():
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema_info[table_name] = [col[1] for col in columns]  # nombre de columnas
        
        return schema_info