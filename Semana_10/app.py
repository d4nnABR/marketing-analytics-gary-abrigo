import os
import streamlit as st
import agente
from banco import BANCO

st.set_page_config(page_title="Tutor de Marketing Analytics", page_icon="📊")
st.title("Tutor de Marketing Analytics")


def leer_llave():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")


@st.cache_resource
def conectar(llave):
    return agente.crear_cliente(llave)


llave = leer_llave()
if not llave:
    st.error("Falta GEMINI_API_KEY (en Secrets de Streamlit o en el archivo .env).")
    st.stop()
client, modelo = conectar(llave)

st.session_state.setdefault("mensajes", [])
st.session_state.setdefault("usadas", 0)
st.session_state.setdefault("pendiente", None)


def responder(pregunta):
    ok, aviso = agente.validar(pregunta, st.session_state.usadas)
    st.session_state.mensajes.append({"rol": "user", "texto": pregunta})
    if not ok:
        st.session_state.mensajes.append({"rol": "assistant", "texto": aviso, "traza": []})
        return
    historial = [("user" if m["rol"] == "user" else "model", m["texto"])
                 for m in st.session_state.mensajes[:-1] if m["texto"]]
    st.session_state.usadas += 1
    with st.spinner("Pensando…"):
        try:
            texto, traza = agente.preguntar(client, modelo, pregunta, historial)
        except Exception as e:
            texto, traza = f"No pude contestar: {e}", []
    st.session_state.mensajes.append({"rol": "assistant", "texto": texto, "traza": traza})


tutor, evaluacion = st.tabs(["Tutor", "Evaluación"])

with st.sidebar:
    st.caption(f"Preguntas usadas: {st.session_state.usadas}/{agente.MAX_PREGUNTAS}")
    tema = st.selectbox("Tema", list(BANCO))
    for i, caso in enumerate(BANCO[tema]):
        if st.button(caso["pregunta"], key=f"{tema}-{i}"):
            st.session_state.pendiente = caso["pregunta"]
    if st.button("Borrar conversación"):
        st.session_state.mensajes = []

with tutor:
    for m in st.session_state.mensajes:
        with st.chat_message(m["rol"]):
            st.markdown(m["texto"])
            if m["rol"] == "assistant" and m.get("traza"):
                with st.expander("Herramientas usadas"):
                    for i, t in enumerate(m["traza"], 1):
                        st.code(f"Paso {i}: {t['herramienta']}({t['datos']}) → {t['resultado']}")
            elif m["rol"] == "assistant" and "?" not in m["texto"] and m["texto"] != agente.FUERA_DE_TEMA:
                st.caption("Respuesta sin herramienta: revisar.")

    escrita = st.chat_input(f"Pregunta sobre el curso (máx. {agente.MAX_CHARS} caracteres)")
    pregunta = escrita or st.session_state.pendiente
    if pregunta:
        st.session_state.pendiente = None
        responder(pregunta)
        st.rerun()

with evaluacion:
    st.write("Corre el banco de preguntas y revisa si el agente acierta y usa la herramienta correcta.")
    casos = [(t, c) for t, lista in BANCO.items() for c in lista
             if c.get("herramienta") is None or c["herramienta"] in agente.HERRAMIENTAS]
    st.caption(f"{len(casos)} casos con herramienta disponible. Cada uno gasta de 2 a 3 llamadas al LLM.")
    if st.button("Evaluar banco"):
        filas, aciertos, calificadas = [], 0, 0
        barra = st.progress(0.0)
        for n, (t, caso) in enumerate(casos, 1):
            r = agente.evaluar_caso(client, modelo, caso)
            if r["ok"] is not None:
                calificadas += 1
                aciertos += r["ok"]
            filas.append({"Tema": t, "Pregunta": caso["pregunta"],
                          "Número correcto": {True: "OK", False: "REVISAR", None: "Trampa"}[r["ok"]],
                          "Herramienta correcta": {True: "OK", False: "NO", None: "—"}[r["herramienta_ok"]],
                          "Respuesta": r["respuesta"][:200]})
            barra.progress(n / len(casos))
        st.success(f"Resultado: {aciertos} de {calificadas} preguntas con respuesta conocida")
        st.dataframe(filas, use_container_width=True)
