import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

from src.config import settings


st.set_page_config(page_title="Dashboard IoT", layout="wide")


@st.cache_resource
def get_engine():
    return create_engine(settings.database_url)


@st.cache_data(ttl=60)
def load_data(view_name: str) -> pd.DataFrame:
    allowed_views = {
        "avg_temp_por_dispositivo",
        "leituras_por_hora",
        "temp_max_min_por_dia",
        "resumo_por_ambiente",
    }
    if view_name not in allowed_views:
        raise ValueError("View nao permitida.")

    return pd.read_sql(f"SELECT * FROM {view_name}", get_engine())


st.title("Dashboard de Temperaturas IoT")

try:
    df_avg_temp = load_data("avg_temp_por_dispositivo")
    df_leituras_hora = load_data("leituras_por_hora")
    df_temp_max_min = load_data("temp_max_min_por_dia")
    df_resumo = load_data("resumo_por_ambiente")
except Exception as exc:
    st.error("Nao foi possivel carregar os dados. Execute o PostgreSQL e o script de ingestao primeiro.")
    st.code(str(exc))
    st.stop()

total_leituras = int(df_avg_temp["total_leituras"].sum()) if not df_avg_temp.empty else 0
temperatura_media = (
    float((df_resumo["temperatura_media"] * df_resumo["total_leituras"]).sum() / total_leituras)
    if total_leituras and not df_resumo.empty
    else 0
)
dispositivos = len(df_avg_temp)

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Total de leituras", f"{total_leituras:,}".replace(",", "."))
metric_col2.metric("Dispositivos", dispositivos)
metric_col3.metric("Temperatura media geral", f"{temperatura_media:.1f} °C")

st.header("Media de temperatura por dispositivo")
fig1 = px.bar(
    df_avg_temp,
    x="device_id",
    y="avg_temp",
    text="avg_temp",
    color="avg_temp",
    color_continuous_scale="Tealrose",
    labels={"device_id": "Dispositivo", "avg_temp": "Temperatura media (°C)"},
)
st.plotly_chart(fig1, use_container_width=True)

st.header("Leituras por hora do dia")
fig2 = px.line(
    df_leituras_hora,
    x="hora",
    y="contagem",
    markers=True,
    labels={"hora": "Hora", "contagem": "Quantidade de leituras"},
)
st.plotly_chart(fig2, use_container_width=True)

st.header("Temperaturas maximas, minimas e medias por dia")
fig3 = px.line(
    df_temp_max_min,
    x="data",
    y=["temp_max", "temp_min", "temp_media"],
    markers=True,
    labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Indicador"},
)
st.plotly_chart(fig3, use_container_width=True)

st.header("Resumo por ambiente")
st.dataframe(df_resumo, use_container_width=True, hide_index=True)
