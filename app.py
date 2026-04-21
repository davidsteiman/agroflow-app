import streamlit as st
import google.generativeai as genai
import os

# 1. Recuperar la clave de forma segura (la configuraremos luego en Streamlit)
api_key = st.secrets["GOOGLE_API_KEY"]

# Configuración de la App
st.set_page_config(page_title="AgroFlow 360", page_icon="🚜")
st.title("🚜 AgroFlow 360")
st.markdown("### Simulador de Rentabilidad Real - Argentina 2026")

# Entrada de datos del usuario
with st.sidebar:
    st.header("Datos del Productor")
    ha = st.number_input("Hectáreas anuales", value=2500)
    rinde = st.number_input("Rinde promedio (qq/ha)", value=32.0)
    consumo = st.number_input("Consumo actual (L/ha)", value=15.0)

# Lógica del motor
if st.button("🚀 Calcular Rentabilidad"):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction="Eres AgroFlow Engine. Reglas: Gasoil 1.10 USD/L, Ahorro combustible 25.5%, Rinde recuperado 2.7%. Crédito Banco Provincia Tasa 0% USD a 4 años."
        )
        
        prompt = f"Calculá el ahorro para {ha} ha, rinde {rinde} qq y consumo {consumo} L. Buscá precio soja hoy en Rosario."
        
        with st.spinner("Consultando mercados y calculando..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.success("Informe generado con éxito.")
    except Exception as e:
        st.error(f"Error: {e}. Asegúrate de haber configurado la API Key correctamente.")
