
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

from pathlib import Path

# =====================================================
# 1. CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Dashboard de estudiantes",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta institucional
COLORS = {
    "azul_oscuro": "#16115E",
    "morado": "#3730AA",
    "naranja": "#FF653F",
    "amarillo": "#FFC85C",
    "fondo": "#F5F6FA",
    "blanco": "#FFFFFF",
    "texto": "#25243A"
}

PALETA = [
    COLORS["azul_oscuro"],
    COLORS["morado"],
    COLORS["naranja"],
    COLORS["amarillo"]
]

# =====================================================
# 2. ESTILOS CSS
# =====================================================

st.markdown(f"""
<style>

.stApp {{
    background-color: {COLORS["fondo"]};
}}

[data-testid="stSidebar"] {{
    background-color: {COLORS["azul_oscuro"]};
}}

[data-testid="stSidebar"] * {{
    color: white !important;
}}

[data-testid="stSidebar"] [data-baseweb="select"] {{
    background-color: white;
}}

[data-testid="stSidebar"] [data-baseweb="select"] * {{
    color: #16115E !important;
}}

h1 {{
    color: {COLORS["azul_oscuro"]};
    font-weight: 800;
}}

h2, h3 {{
    color: {COLORS["azul_oscuro"]};
    font-weight: 700;
}}

.kpi-card {{
    background: white;
    padding: 22px;
    border-radius: 14px;
    border-left: 5px solid {COLORS["naranja"]};
    box-shadow: 0 3px 15px rgba(22,17,94,0.07);
    min-height: 115px;
}}

.kpi-title {{
    color: #77778A;
    font-size: 13px;
    font-weight: 600;
}}

.kpi-value {{
    color: {COLORS["azul_oscuro"]};
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}}

.descripcion {{
    background: #EAE9F7;
    border-left: 4px solid {COLORS["naranja"]};
    padding: 14px 18px;
    border-radius: 8px;
    color: {COLORS["azul_oscuro"]};
    font-size: 14px;
    margin: 12px 0 22px 0;
}}

div[data-testid="stTabs"] button {{
    font-weight: 700;
    color: {COLORS["azul_oscuro"]};
}}

div[data-testid="stTabs"] button[aria-selected="true"] {{
    border-bottom: 3px solid {COLORS["naranja"]};
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. CARGAR BASE DE DATOS
# =====================================================

@st.cache_data
def cargar_datos():

    ruta = (
        Path(__file__).resolve().parent
        / "database"
        / "Estudiantes_Matriculados_en_Programas_Académicos_-_Institución_Universitaria_Colegio_Mayor_de_Antioquia_20261126.csv"
    )

    return pd.read_csv(ruta)


df = cargar_datos()

# Categorías que vamos a utilizar
columnas = [
    "TIPO INSCRIPCION",
    "PROGRAMA",
    "SEXO BIOLOGICO"
]

# Verificar columnas
faltantes = [c for c in columnas if c not in df.columns]

if faltantes:
    st.error(f"Columnas no encontradas: {faltantes}")
    st.stop()


# =====================================================
# 4. ENCABEZADO
# =====================================================

st.markdown(
    f"""
    <div style="
        background: linear-gradient(110deg, #16115E, #3730AA);
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
    ">
        <h1 style="color:white; margin:0;">
            🎓 Dashboard de estudiantes matriculados
        </h1>
        <p style="color:#E3E2FF; font-size:15px; margin-top:10px;">
            Panel de análisis y caracterización de la población estudiantil
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 5. FILTROS INTERCONECTADOS
# =====================================================

st.sidebar.markdown("## 🔎 FILTROS")
st.sidebar.markdown("---")

df_filtrado = df.copy()

selecciones = {}

for columna in columnas:

    categorias = sorted(
        df_filtrado[columna].dropna().unique().tolist(),
        key=str
    )

    seleccion = st.sidebar.selectbox(
        columna,
        options=["Todas"] + categorias,
        key=f"filtro_{columna}"
    )

    selecciones[columna] = seleccion

    if seleccion != "Todas":

        df_filtrado = df_filtrado[
            df_filtrado[columna] == seleccion
        ]


# Botón para limpiar filtros
if st.sidebar.button("🔄 Limpiar filtros", use_container_width=True):

    for columna in columnas:
        st.session_state[f"filtro_{columna}"] = "Todas"

    st.rerun()


# =====================================================
# 6. FUNCIONES AUXILIARES
# =====================================================

def tarjeta(titulo, valor, color):

    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color:{color};">
            <div class="kpi-title">{titulo}</div>
            <div class="kpi-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def descripcion_aleatoria(opciones):

    texto = random.choice(opciones)

    st.markdown(
        f'<div class="descripcion">💡 {texto}</div>',
        unsafe_allow_html=True
    )


def preparar_grafico(fig, altura=420):

    fig.update_layout(
        height=altura,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color=COLORS["azul_oscuro"],
            size=12
        ),
        margin=dict(l=25, r=25, t=35, b=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor=COLORS["azul_oscuro"],
            font_color="white"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#ECECF3",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False
    )

    return fig


# =====================================================
# 7. INDICADORES GENERALES
# =====================================================

st.markdown("## Resumen general")

k1, k2, k3 = st.columns(3)

with k1:
    tarjeta(
        "TOTAL DE ESTUDIANTES",
        f"{len(df_filtrado):,}",
        COLORS["naranja"]
    )

with k2:
    tarjeta(
        "PROGRAMAS DISPONIBLES",
        f"{df_filtrado['PROGRAMA'].nunique():,}",
        COLORS["morado"]
    )

with k3:
    tarjeta(
        "TIPOS DE INSCRIPCIÓN",
        f"{df_filtrado['TIPO INSCRIPCION'].nunique():,}",
        COLORS["amarillo"]
    )

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# 8. PESTAÑAS DEL DASHBOARD
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📋 Tipo de inscripción",
    "🎓 Programas",
    "👥 Sexo biológico"
])


# =====================================================
# PESTAÑA 1: TIPO DE INSCRIPCIÓN
# =====================================================

with tab1:

    st.subheader("Caracterización por tipo de inscripción")

    descripcion_aleatoria([
        "El tipo de inscripción permite identificar las diferentes modalidades de ingreso de los estudiantes.",
        "Esta categoría facilita el análisis de la composición de los estudiantes según su forma de vinculación académica.",
        "Conocer los tipos de inscripción ayuda a comprender la dinámica de acceso a los programas académicos."
    ])

    datos = (
        df_filtrado["TIPO INSCRIPCION"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )

    datos.columns = ["Categoría", "Estudiantes"]

    c1, c2 = st.columns([1.5, 1])

    with c1:

        fig = px.bar(
            datos,
            x="Categoría",
            y="Estudiantes",
            color="Categoría",
            color_discrete_sequence=PALETA,
            text="Estudiantes",
            title="Distribución de estudiantes por inscripción"
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate="%{x}<br>Estudiantes: %{y:,}<extra></extra>"
        )

        fig.update_layout(showlegend=False)

        st.plotly_chart(
            preparar_grafico(fig),
            use_container_width=True
        )

    with c2:

        fig = px.pie(
            datos,
            names="Categoría",
            values="Estudiantes",
            hole=0.65,
            color_discrete_sequence=PALETA,
            title="Participación por tipo de inscripción"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            marker=dict(line=dict(color="white", width=3))
        )

        st.plotly_chart(
            preparar_grafico(fig),
            use_container_width=True
        )


# =====================================================
# PESTAÑA 2: PROGRAMAS
# =====================================================

with tab2:

    st.subheader("Distribución por programas académicos")

    descripcion_aleatoria([
        "El análisis por programa permite identificar la distribución de estudiantes entre las diferentes ofertas académicas.",
        "Esta categoría permite reconocer los programas con mayor participación dentro de la población estudiantil.",
        "La distribución por programas proporciona una visión general de las preferencias y la composición académica."
    ])

    datos = (
        df_filtrado["PROGRAMA"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )

    datos.columns = ["Programa", "Estudiantes"]

    datos = datos.sort_values(
        "Estudiantes",
        ascending=True
    )

    fig = px.bar(
        datos,
        x="Estudiantes",
        y="Programa",
        orientation="h",
        color="Estudiantes",
        color_continuous_scale=[
            COLORS["azul_oscuro"],
            COLORS["morado"],
            COLORS["naranja"],
            COLORS["amarillo"]
        ],
        text="Estudiantes",
        title="Estudiantes matriculados por programa"
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )

    fig.update_layout(
        coloraxis_showscale=False,
        yaxis_title="",
        xaxis_title="Cantidad de estudiantes"
    )

    altura = max(420, len(datos) * 32)

    st.plotly_chart(
        preparar_grafico(fig, altura),
        use_container_width=True
    )


# =====================================================
# PESTAÑA 3: SEXO BIOLÓGICO
# =====================================================

with tab3:

    st.subheader("Caracterización por sexo biológico")

    descripcion_aleatoria([
        "Esta categoría permite observar la composición de la población estudiantil según el sexo biológico registrado.",
        "La distribución facilita la caracterización de los estudiantes y permite identificar su participación porcentual.",
        "El análisis de esta variable contribuye a describir las características demográficas de la población matriculada."
    ])

    datos = (
        df_filtrado["SEXO BIOLOGICO"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )

    datos.columns = ["Sexo biológico", "Estudiantes"]

    c1, c2 = st.columns([1, 1.5])

    with c1:

        fig = px.pie(
            datos,
            names="Sexo biológico",
            values="Estudiantes",
            hole=0.68,
            color_discrete_sequence=[
                COLORS["morado"],
                COLORS["naranja"],
                COLORS["amarillo"],
                COLORS["azul_oscuro"]
            ],
            title="Participación por sexo biológico"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=3))
        )

        st.plotly_chart(
            preparar_grafico(fig),
            use_container_width=True
        )

    with c2:

        fig = px.bar(
            datos,
            x="Sexo biológico",
            y="Estudiantes",
            color="Sexo biológico",
            color_discrete_sequence=PALETA,
            text="Estudiantes",
            title="Cantidad de estudiantes por sexo biológico"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            preparar_grafico(fig),
            use_container_width=True
        )


# =====================================================
# 9. PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align:center; color:#77778A; padding:15px;">
        Dashboard de estudiantes matriculados
        <br>
        Desarrollado con Python, Pandas, Streamlit y Plotly
    </div>
    """,
    unsafe_allow_html=True
)

