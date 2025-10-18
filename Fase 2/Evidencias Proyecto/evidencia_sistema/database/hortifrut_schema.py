HORTIFRUT_DATABASE_SCHEMA = {
    "cosechas": {
        "columns": {
            "id": "INT PRIMARY KEY",
            "producto_id": "INT",
            "ubicacion_id": "INT", 
            "encargado_id": "INT",
            "fecha_cosecha": "DATE",
            "cantidad_kg": "DECIMAL(10,2)",
            "calidad": "VARCHAR(50)",
            "lote": "VARCHAR(100)",
            "certificacion": "VARCHAR(100)"
        },
        "description": "Registro de cosechas por producto y ubicación"
    },
    
    "productos": {
        "columns": {
            "id": "INT PRIMARY KEY",
            "nombre": "VARCHAR(100)",
            "especie": "VARCHAR(50)",
            "variedad": "VARCHAR(50)",
            "temporada": "VARCHAR(50)"
        },
        "description": "Catálogo de productos cultivados"
    },
    
    "ubicaciones": {
        "columns": {
            "id": "INT PRIMARY KEY",
            "nombre": "VARCHAR(100)",
            "pais": "VARCHAR(50)",
            "region": "VARCHAR(50)",
            "tipo": "VARCHAR(50)"  # planta, campo, centro distribución
        },
        "description": "Ubicaciones de operaciones de Hortifrut"
    },
    
    "encargados": {
        "columns": {
            "id": "INT PRIMARY KEY", 
            "nombre": "VARCHAR(100)",
            "cargo": "VARCHAR(100)",
            "area": "VARCHAR(100)",
            "email": "VARCHAR(100)"
        },
        "description": "Personal encargado de diferentes áreas"
    }
}