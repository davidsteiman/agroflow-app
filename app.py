import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="AgroFlow 360", page_icon="🚜")

st.title("🚜 AgroFlow 360")
st.subheader("Simulador de Rentabilidad de Maquinaria")
st.markdown("---")

# --- BARRA LATERAL (ENTRADA DE DATOS) ---
with st.sidebar:
    st.header("Configuración")
    # Aquí es donde pondrás la llave que sacaste en el Paso 1
    user_api_key = st.text_input("AIzaSyArEbKhkSY4iLrvxhXIQPG128tYVINCulk", type="password")
    
    st.header("Datos del Productor")
    ha = st.number_input("Hectáreas anuales:", value=2500)
    rinde = st.number_input("Rinde promedio (qq/ha):", value=32.0)
    consumo = st.number_input("Consumo actual (L/ha):", value=15.0)

# --- LÓGICA DEL MOTOR (SYSTEM INSTRUCTIONS) ---
if st.button("🚀 Calcular Rentabilidad Real"):
    if not user_api_key:
        st.error("Por favor, ingresa tu API Key en la barra lateral.")
    else:
        try:
            genai.configure(api_key=user_api_key)
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash", # Modelo rápido y gratis
                system_instruction="Eres AgroFlow Engine. Reglas: Gasoil 1.10 USD/L, Ahorro combustible 25.5%, Rinde recuperado 2.7%. Crédito Banco Provincia 0% USD a 4 años. Muestra el desglose matemático."
            )
            
            # Pedimos el informe
            prompt = f"Genera un Dashboard de rentabilidad para {ha} hectáreas, rinde de {rinde} qq y consumo de {consumo} L/ha. Busca el precio de la soja hoy en Rosario."
            
            with st.spinner("Conectando con MatbaRofex y calculando..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.success("Informe generado con éxito.")
        except Exception as e:
            st.error(f"Error técnico: {e}")
