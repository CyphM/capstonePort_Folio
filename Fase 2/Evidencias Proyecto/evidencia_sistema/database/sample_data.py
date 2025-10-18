SAMPLE_DATA = {
    "productos": [
        {"id": 1, "nombre": "Arándanos Premium", "especie": "Arándano", "variedad": "Biloxi", "temporada": "2024"},
        {"id": 2, "nombre": "Frambuesas Orgánicas", "especie": "Frambuesa", "variedad": "Heritage", "temporada": "2024"},
        {"id": 3, "nombre": "Frutillas", "especie": "Frutilla", "variedad": "Albion", "temporada": "2024"},
        {"id": 4, "nombre": "Morangas", "especie": "Mora", "variedad": "Tupi", "temporada": "2024"}
    ],
    
    "ubicaciones": [
        {"id": 1, "nombre": "Planta Santiago", "pais": "Chile", "region": "Región Metropolitana", "tipo": "planta"},
        {"id": 2, "nombre": "Campo Perú Norte", "pais": "Perú", "region": "La Libertad", "tipo": "campo"},
        {"id": 3, "nombre": "Planta Marruecos", "pais": "Marruecos", "region": "Agadir", "tipo": "planta"},
        {"id": 4, "nombre": "Centro Distribución Europa", "pais": "España", "region": "Huelva", "tipo": "distribucion"}
    ],
    
    "encargados": [
        {"id": 1, "nombre": "María González", "cargo": "Jefa de Producción", "area": "Producción", "email": "maria.gonzalez@hortifrut.com"},
        {"id": 2, "nombre": "Carlos Rodríguez", "cargo": "Encargado de Calidad", "area": "Calidad", "email": "carlos.rodriguez@hortifrut.com"},
        {"id": 3, "nombre": "Ana Silva", "cargo": "Supervisora de Cosecha", "area": "Cosecha", "email": "ana.silva@hortifrut.com"},
        {"id": 4, "nombre": "Pedro Martínez", "cargo": "Jefe de Logística", "area": "Logística", "email": "pedro.martinez@hortifrut.com"}
    ],
    
    "cosechas": [
        {"id": 1, "producto_id": 1, "ubicacion_id": 1, "encargado_id": 1, "fecha_cosecha": "2024-03-15", "cantidad_kg": 1500.50, "calidad": "Premium", "lote": "ARAND-SCL-2024-001", "certificacion": "GlobalGAP"},
        {"id": 2, "producto_id": 1, "ubicacion_id": 2, "encargado_id": 3, "fecha_cosecha": "2024-03-20", "cantidad_kg": 2800.75, "calidad": "Extra", "lote": "ARAND-PER-2024-002", "certificacion": "Organic"},
        {"id": 3, "producto_id": 2, "ubicacion_id": 3, "encargado_id": 2, "fecha_cosecha": "2024-04-05", "cantidad_kg": 1200.25, "calidad": "Premium", "lote": "FRAMB-MAR-2024-001", "certificacion": "GlobalGAP"}
    ]
}