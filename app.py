import streamlit as st
import google.generativeai as genai

# Configuración de seguridad: Trae la llave desde los "Secrets" de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Error: Falta configurar la API Key en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(page_title="AgroFlow 360", page_icon="🚜")
st.title("🚜 AgroFlow 360")
st.subheader("Engine de Rentabilidad de Maquinaria - Argentina 2026")

with st.sidebar:
    st.header("Datos de la Operación")
    ha = st.number_input("Hectáreas anuales", value=3000)
    rinde = st.number_input("Rinde promedio soja (qq/ha)", value=32.0)
    consumo = st.number_input("Consumo equipo viejo (L/ha)", value=16.0)
    st.info("Cálculos: Gasoil US$ 1.10/L | Mejora rinde 2.7% | Cuota 0% USD")

if st.button("🚀 Generar Informe de Ahorro Real"):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash", 
        system_instruction="""Eres AgroFlow Engine. Reglas:
        1. Ahorro Gasoil: (Consumo Viejo - (Consumo Viejo * 0.745)) * Hectáreas * 1.10.
        2. Rinde Recuperado: (Rinde * 0.027) * Hectáreas * Precio Soja.
        3. Cuota: US$ 820.000 / 4 (Banco Provincia Tasa 0%).
        Buscá el precio de la soja Rosario hoy usando Google Search y mostrá el desglose matemático."""
    )
    
    with st.spinner("Conectando con MatbaRofex y procesando..."):
        try:
            prompt = f"Dashboard para {ha} ha, rinde {rinde} qq y consumo {consumo} L. Mostrá el ahorro anual en USD y el porcentaje de la cuota que se paga solo."
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Falla en el motor: {e}")
