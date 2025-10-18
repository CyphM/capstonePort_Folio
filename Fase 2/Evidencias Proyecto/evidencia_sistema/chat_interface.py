import streamlit as st
import requests
import json
from knowledge_base.hortifrut_knowledge import HORTIFRUT_KNOWLEDGE
from app.agents.enhanced_metadata_agent import EnhancedHortifrutAgent

# Configuración de la página
st.set_page_config(
    page_title="Hortifrut Metadata Assistant",
    page_icon="",
    layout="wide"
)

def initialize_agent():
    """Inicializar el agente de metadatos"""
    return EnhancedHortifrutAgent()

def main():
    st.title("Hortifrut Metadata Assistant")
    st.markdown("""
    Consulta información sobre **data owners, sistemas y metadatos** de Hortifrut.
    """)
    
    # Inicializar agente
    agent = initialize_agent()
    
    # Sidebar con información útil
    with st.sidebar:
        st.header("Guía Rápida")
        st.markdown("""
        **Ejemplos de consultas:**
        - ¿Quién es el dueño de Genética?
        - ¿Qué sistemas usa Producción?
        - Buscar información de Comercial
        - Mostrar todos los data owners
        """)
        
        st.header("Búsqueda Rápida")
        if st.button("Mostrar todos los Data Owners"):
            owners = agent.get_all_data_owners()
            st.write("**Data Owners:**")
            for owner in owners:
                st.write(f"- {owner}")
    
    # Input principal
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_query = st.text_input(
            "Escribe tu pregunta:",
            placeholder="Ej: dueño de datos de producción, sistemas de genética...",
            key="query_input"
        )
    
    with col2:
        search_type = st.selectbox(
            "Tipo de búsqueda:",
            ["Automática", "Data Owners", "Sistemas", "General"]
        )
    
    # Procesar consulta - PARTE CORREGIDA
    if user_query:
        with st.spinner("Buscando información..."):
            try:
                # Usar el nuevo procesador de consultas
                response = agent.process_query(user_query)
                st.success("**Respuesta:**")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error procesando la consulta: {str(e)}")
    
    # Sección de ejemplos
    st.divider()
    st.subheader("Prueba estos ejemplos:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Dueño de Genética", use_container_width=True):
            st.session_state.query_input = "dueño de genética"
            st.rerun()
    
    with col2:
        if st.button("Sistemas de Producción", use_container_width=True):
            st.session_state.query_input = "sistemas de producción"
            st.rerun()
    
    with col3:
        if st.button("Todos los Data Owners", use_container_width=True):
            st.session_state.query_input = "mostrar todos los dueños"
            st.rerun()

if __name__ == "__main__":
    main()