import streamlit as st
import google.generativeai as genai

# 1. Configuración de Seguridad
# Esto busca la llave en los "Secrets" de Streamlit para que nadie la vea
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Falta configurar la API Key en Advanced Settings.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Interfaz Visual
st.set_page_config(page_title="AgroFlow 360", page_icon="🚜")
st.title("🚜 AgroFlow 360")
st.markdown("### Simulador de Rentabilidad Real - Mercado Argentina 2026")

with st.sidebar:
    st.header("Datos del Productor")
    ha = st.number_input("Hectáreas anuales", value=2500)
    rinde = st.number_input("Rinde promedio (qq/ha)", value=32.0)
    consumo = st.number_input("Consumo gasoil actual (L/ha)", value=15.0)
    st.info("Cálculos basados en Gasoil a US$ 1.10/L y mejora de rinde del 2.7%")

# 3. Motor Lógico (Tu System Instruction)
if st.button("🚀 Calcular Ahorro y Generar Informe"):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction="""Eres AgroFlow Engine. Reglas innegociables:
        1. Ahorro Gasoil: (Consumo Viejo - (Consumo Viejo * 0.75)) * Hectáreas * 1.10.
        2. Rinde Recuperado: (Rinde * 0.027) * Hectáreas * Precio Soja.
        3. Cuota: US$ 820.000 / 4 (Banco Provincia Tasa 0%).
        Busca el precio de soja Rosario hoy con Google Search."""
    )
    
    prompt = f"Generá informe para {ha} ha, rinde {rinde} qq y consumo {consumo} L. Mostrá el desglose matemático."
    
    with st.spinner("Consultando MatbaRofex y calculando..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error del motor: {e}")
