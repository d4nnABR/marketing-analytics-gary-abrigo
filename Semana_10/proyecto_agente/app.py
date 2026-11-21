"""app.py · La ventana para hablar con el agente de Marketing Analytics.

La app NO hace cálculos: muestra el chat y le pasa cada pregunta a agente.py.
Para abrirla, en la terminal (con el entorno virtual activado, dentro de la carpeta del proyecto):

    streamlit run app.py

Partes de este archivo:
  1. Configuración de la página y memoria de la sesión
  2. Barra lateral: herramientas activas, fuentes de datos, nueva conversación y ejemplos
  3. Funciones de ayuda para mostrar las herramientas usadas y la aprobación humana
  4. El chat
"""
import os
import tempfile

import pandas as pd
import streamlit as st

import agente   # el agente: herramientas, FUENTES, cargar_datos y preguntar

# =============================================================== 1. Página y memoria de la sesión
st.set_page_config(page_title="Agente de Marketing Analytics", layout="wide")
st.title("Agente de Marketing Analytics")
st.caption(f"LLM (Large Language Model, modelo grande de lenguaje): {agente.MODELO} · "
           "Las cuentas las hacen las herramientas en Python, no el LLM.")

# st.session_state guarda datos mientras la página está abierta (se borra al recargar)
if "historial" not in st.session_state:
    st.session_state.historial = []        # lo que se le reenvía a Gemini en cada pregunta (la "memoria")
    st.session_state.mensajes = []         # lo que se muestra en pantalla
    st.session_state.activas = {nombre: True for nombre in agente.HERRAMIENTAS}
    st.session_state.pendiente = None      # una pregunta de ejemplo elegida en la barra lateral

# =============================================================== 2. Barra lateral
with st.sidebar:
    # ---- 2a. Herramientas activas: casillas para prender o apagar cada herramienta
    st.header("Herramientas")
    st.caption("Apaguen una para ver qué hace el agente sin ella.")
    for nombre in agente.HERRAMIENTAS:
        st.session_state.activas[nombre] = st.checkbox(nombre, value=st.session_state.activas.get(nombre, True),
                                                       key=f"chk_{nombre}")

    # ---- 2b. Fuentes de datos: ver la configuración y subir otro archivo
    st.header("Fuentes de datos")
    st.caption("Cada herramienta usa los nombres estándar. Suban su archivo y elijan qué columna es cuál.")
    for nombre, conf in agente.FUENTES.items():
        with st.expander(nombre):
            st.write(conf["descripcion"])
            st.write("**Archivo:**", os.path.basename(conf["ruta"]))
            st.write("**Columnas:**", conf["columnas"])
            if conf.get("variables"):
                st.write("**Variables:**", conf["variables"])

            subido = st.file_uploader("Usar otro archivo (.csv o .xlsx)", type=["csv", "xlsx"], key=f"up_{nombre}")
            if subido is not None:
                # Guardamos el archivo subido en una carpeta temporal para que cargar_datos lo pueda leer
                ruta = os.path.join(tempfile.gettempdir(), f"{nombre}_{subido.name}")
                with open(ruta, "wb") as f:
                    f.write(subido.getbuffer())
                tabla = pd.read_excel(ruta) if ruta.endswith(".xlsx") else pd.read_csv(ruta)
                columnas_archivo = list(tabla.columns)
                st.dataframe(tabla.head(3))

                # Para cada nombre estándar, el usuario elige la columna de SU archivo
                mapeo = {}
                for estandar, actual in conf["columnas"].items():
                    indice = columnas_archivo.index(actual) if actual in columnas_archivo else 0
                    mapeo[estandar] = st.selectbox(f"¿Qué columna es '{estandar}'?", columnas_archivo,
                                                   index=indice, key=f"map_{nombre}_{estandar}")
                variables = None
                if "variables" in conf:
                    numericas = [c for c in columnas_archivo if pd.api.types.is_numeric_dtype(tabla[c])]
                    variables = st.multiselect("Variables para segmentar", numericas,
                                               default=[v for v in conf["variables"] if v in numericas],
                                               key=f"vars_{nombre}")

                if st.button("Usar este archivo", key=f"usar_{nombre}"):
                    conf["ruta"] = ruta
                    conf["columnas"] = mapeo
                    if variables is not None:
                        conf["variables"] = variables
                    agente._CACHE.pop(nombre, None)          # olvidar la versión anterior
                    try:
                        filas = len(agente.cargar_datos(nombre))
                        st.success(f"Listo: la fuente '{nombre}' ahora usa su archivo ({filas} filas).")
                    except ValueError as e:
                        st.error(str(e))

    # ---- 2c. Nueva conversación: borra la memoria
    st.header("Conversación")
    if st.button("Nueva conversación"):
        st.session_state.historial = []
        st.session_state.mensajes = []
        st.rerun()

    # ---- 2d. Preguntas de ejemplo: un clic las manda al chat
    st.header("Ejemplos")
    ejemplos = [
        "¿Qué datos tengo disponibles?",
        "Margen US$25 y churn 4% mensual. ¿Cuál es el CLV?",
        "¿Cuál es la elasticidad del segmento Casuales?",
        "Precio US$20, costo US$8, elasticidad -1.4 y 1,000 unidades al mes. ¿Qué precio propones?",
        "¿Le recomendamos Té Chai a quien compra Banana Bread?",
        "Segmenta a los clientes en 3 grupos.",
        "¿Qué es el uplift y por qué necesito un grupo de control?",
        "Margen US$25 y churn de 120%. ¿CLV?",
    ]
    for i, ejemplo in enumerate(ejemplos):
        if st.button(ejemplo, key=f"ej_{i}"):
            st.session_state.pendiente = ejemplo


# =============================================================== 3. Funciones de ayuda
def mostrar_pasos(pasos):
    """Debajo de cada respuesta: qué herramientas usó el agente, con qué datos y qué devolvieron."""
    if not pasos:
        st.caption("No usó herramientas en esta respuesta (si dio un número, lo calculó el LLM solo: verifíquenlo).")
        return
    with st.expander(f"Herramientas que usó ({len(pasos)})"):
        for p in pasos:
            st.markdown(f"**{p['herramienta']}**")
            st.json({"datos": p["datos"], "resultado": p["resultado"]}, expanded=False)


def necesita_aprobacion(pasos):
    """True si alguna herramienta devolvió requiere_aprobacion_humana = True (por ejemplo proponer_precio)."""
    for p in pasos or []:
        if isinstance(p["resultado"], dict) and p["resultado"].get("requiere_aprobacion_humana"):
            return True
    return False


def mostrar_aprobacion(i, mensaje):
    """Aviso con botones Aprobar / Rechazar. La decisión queda guardada en el mensaje."""
    decision = mensaje.get("decision")
    if decision:
        st.info(f"Decisión humana: {decision}")
        return
    st.warning("Esta propuesta cambia el precio más de 5%: necesita aprobación humana.")
    col1, col2 = st.columns(2)
    if col1.button("Aprobar", key=f"aprobar_{i}"):
        mensaje["decision"] = "aprobada"
        st.rerun()
    if col2.button("Rechazar", key=f"rechazar_{i}"):
        mensaje["decision"] = "rechazada"
        st.rerun()


# =============================================================== 4. El chat
# 4a. Mostrar la conversación hasta ahora
for i, m in enumerate(st.session_state.mensajes):
    with st.chat_message(m["rol"]):
        st.markdown(m["texto"])
        if m["rol"] == "assistant":
            mostrar_pasos(m.get("pasos"))
            if necesita_aprobacion(m.get("pasos")):
                mostrar_aprobacion(i, m)

# 4b. Recibir una pregunta nueva (escrita o elegida en los ejemplos)
pregunta = st.chat_input("Pregúntenle algo del curso...")
if st.session_state.pendiente:
    pregunta, st.session_state.pendiente = st.session_state.pendiente, None

if pregunta:
    st.session_state.mensajes.append({"rol": "user", "texto": pregunta})
    menu = {n: f for n, f in agente.HERRAMIENTAS.items() if st.session_state.activas.get(n, True)}
    with st.spinner("Pensando..."):
        try:
            respuesta, historial, pasos = agente.preguntar(pregunta, st.session_state.historial,
                                                           mostrar=False, herramientas=menu)
            st.session_state.historial = historial
        except Exception as e:      # por ejemplo, error 429 repetido o llave inválida
            respuesta, pasos = f"No pude responder: {type(e).__name__}: {e}", []
    st.session_state.mensajes.append({"rol": "assistant", "texto": respuesta, "pasos": pasos})
    st.rerun()
