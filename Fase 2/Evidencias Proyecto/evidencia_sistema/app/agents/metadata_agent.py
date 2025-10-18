from knowledge_base.hortifrut_knowledge import HORTIFRUT_KNOWLEDGE

class HortifrutMetadataAgent:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        
    def find_data_owner(self, area: str):
        """Encontrar dueño por área de negocio"""
        area_lower = area.lower()
        for owner, info in self.kb["data_owners"].items():
            for owner_area in info["areas"]:
                if area_lower in owner_area.lower():
                    return {
                        "owner": owner,
                        "areas": info["areas"],
                        "systems": info["systems"]
                    }
        return None
    
    def get_systems_by_area(self, area: str):
        """Obtener sistemas por área"""
        return self.kb["systems_by_area"].get(area, [])
    
    def get_areas_by_system(self, system: str):
        """Obtener áreas que usan un sistema específico"""
        areas = []
        for area, systems in self.kb["systems_by_area"].items():
            if system in systems:
                areas.append(area)
        return areas
    
    def search_all_areas(self, query: str):
        """Búsqueda general en todas las áreas"""
        results = []
        query_lower = query.lower()
        
        for area, systems in self.kb["systems_by_area"].items():
            if query_lower in area.lower():
                owner_info = self.find_data_owner(area)
                results.append({
                    "area": area,
                    "systems": systems,
                    "owner": owner_info["owner"] if owner_info else "No asignado"
                })
        
        return results
    
    def get_all_data_owners(self):
        """Obtener lista completa de data owners"""
        return list(self.kb["data_owners"].keys())

    def detect_area_in_query(self, query: str):
        """Detectar áreas de negocio en consultas en español"""
        query_lower = query.lower()
        
        # Mapeo de sinónimos y variaciones
        area_mapping = {
            "producción": ["producción", "produccion", "cosecha", "cultivo", "cultivos"],
            "genética": ["genética", "genetica", "adn", "genoma"],
            "comercial": ["comercial", "ventas", "comercio", "vendedores"],
            "contraloría": ["contraloría", "contraloria", "control", "finanzas", "contabilidad"],
            "rmbh": ["rmbh", "recursos humanos", "r.h.", "personal"],
            "operaciones": ["operaciones", "logística", "logistica", "distribución", "distribucion"],
            "labones": ["labones", "labon", "laboratorio", "labs"]
        }
        
        for area_key, keywords in area_mapping.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return area_key
        return None

    def format_owner_response(self, owner_data):
        """Formatear respuesta sobre data owners"""
        response = f"**Data Owner:** {owner_data['owner']}\n\n"
        response += "**Áreas a cargo:**\n"
        for area in owner_data['areas']:
            response += f"- {area}\n"
        
        response += "\n**Sistemas utilizados:**\n"
        for system in owner_data['systems']:
            response += f"- {system}\n"
        
        return response

    def process_query(self, user_query: str):
        """Procesar consultas en lenguaje natural"""
        query_lower = user_query.lower()
        
        # Detectar área objetivo
        target_area = self.detect_area_in_query(user_query)
        
        # Consultas sobre data owners
        if any(keyword in query_lower for keyword in ["dueño", "owner", "responsable", "encargado"]):
            if target_area:
                result = self.find_data_owner(target_area)
                if result:
                    return self.format_owner_response(result)
                else:
                    return f"No encontré un data owner específico para el área '{target_area}'"
            else:
                return "Por favor especifica de qué área necesitas el data owner (ej: genética, producción, comercial)"
        
        # Consultas sobre sistemas
        elif any(keyword in query_lower for keyword in ["sistema", "sistemas", "software", "plataforma", "usa"]):
            if target_area:
                # Buscar todas las áreas que coincidan con el target_area
                areas_with_system = []
                for area, systems in self.kb["systems_by_area"].items():
                    area_lower = area.lower()
                    if target_area in area_lower:
                        areas_with_system.append(area)
                
                if areas_with_system:
                    response = f"**Sistemas utilizados en áreas relacionadas con '{target_area.title()}':**\n\n"
                    for area in areas_with_system:
                        systems = self.get_systems_by_area(area)
                        owner_info = self.find_data_owner(area)
                        response += f"**{area}**:\n"
                        response += f"- Sistemas: {', '.join(systems)}\n"
                        if owner_info:
                            response += f"- Data Owner: {owner_info['owner']}\n"
                        response += "\n"
                    return response
                else:
                    return f"No encontré sistemas específicos para el área '{target_area}'"
            else:
                return "Por favor especifica de qué área necesitas conocer los sistemas (ej: genética, producción, comercial)"
        
        # Búsqueda general
        else:
            results = self.search_all_areas(user_query)
            if results:
                response = f"**Resultados para '{user_query}':**\n\n"
                for result in results:
                    response += f"**Área:** {result['area']}\n"
                    response += f"**Data Owner:** {result['owner']}\n"
                    response += f"**Sistemas:** {', '.join(result['systems'])}\n\n"
                return response
            else:
                return f"No encontré resultados específicos para '{user_query}'. Prueba con términos como: producción, genética, comercial, sistemas, dueño"