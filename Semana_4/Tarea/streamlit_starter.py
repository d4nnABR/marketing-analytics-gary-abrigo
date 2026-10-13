"""
Laboratorio de Recomendación — PUNTO DE PARTIDA para su propia app de Streamlit.
Complete los `# TODO`.

El objetivo: una app donde alguien de negocio (que no sabe programar) pueda explorar sus recomendadores:
elegir un cliente y un método, ver sus 3 recomendaciones con el "porque", y comparar los métodos
(hit rate y cobertura) — con al menos un control interactivo.

Correr con:  streamlit run streamlit_starter.py
"""
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Recomendador — Laboratorio", page_icon="☕", layout="wide")

VERDE = "#00704A"
NARANJA = "#C4512F"
GRIS = "#9A988E"


@st.cache_data
def cargar():
    catalogo = pd.read_csv("data/catalogo.csv")
    hist = pd.read_csv("data/ordenes_historial.csv")
    hold = pd.read_csv("data/ordenes_holdout.csv")
    exp = pd.read_csv("data/experimento.csv")
    clientes = pd.read_csv("data/clientes.csv")
    productos = list(catalogo["item"])
    M = (pd.crosstab(hist["customer_id"], hist["item"]) > 0).astype(int).reindex(
        index=clientes["customer_id"], columns=productos, fill_value=0)
    X = M.values.astype(np.float32)
    H = (pd.crosstab(hold["customer_id"], hold["item"]) > 0).astype(int).reindex(
        index=M.index, columns=productos, fill_value=0).values
    NUEVO = H * (1 - X)                                   # probó algo NUEVO en el holdout
    NUEVO[:, productos.index("Agua")] = 0
    es_control = (exp.set_index("customer_id").loc[M.index, "grupo"] == "control").values
    return productos, M.index.values, X, NUEVO, es_control


productos, ids, X, NUEVO, es_control = cargar()
COL_AGUA = productos.index("Agua")
popularidad = X.sum(axis=0)

# TODO 1: la tabla de similitudes producto × producto (con la diagonal en 0), calculada UNA vez
S_it = ...   # <-- reemplacen esto (cosine_similarity entre las columnas de X)


def puntajes(metodo, x_vec, K):
    """Puntajes de los 29 productos para UN cliente (x_vec = su vector de 0/1)."""
    if metodo == "Popularidad":
        return popularidad.astype(float)
    if metodo == "Filtrado por ítem":
        # TODO 2: suma de las similitudes de cada producto con lo que el cliente ya compró
        return ...   # <-- reemplacen esto
    # TODO 3: filtrado por cliente: similitud del cliente con TODOS los demás, sus K vecinos más parecidos
    #         y la suma de sus compras ponderada por esa similitud
    sims = cosine_similarity(x_vec[None, :], X)[0]
    return ...       # <-- reemplacen esto


def top3(scores, x_vec):
    s = np.where(x_vec > 0, -np.inf, scores).astype(float)   # no recomendar lo ya comprado
    s[COL_AGUA] = -np.inf                                     # ni el Agua
    return np.argsort(-s)[:3]


# --- Título ---
st.title("☕ Recomendador de productos")
st.caption("TODO: escriban aquí una frase sobre qué decisión de negocio ayuda a tomar esta app.")

# TODO 4: barra lateral con los controles interactivos (mínimo UNO): un selector del método
#         (st.selectbox) y un slider con el número de vecinos K (st.slider)
with st.sidebar:
    st.header("Parámetros")
    metodo = ...     # <-- reemplacen esto
    K = ...          # <-- reemplacen esto

tab1, tab2 = st.tabs(["Recomendar", "Comparar métodos"])

with tab1:
    cid = st.number_input("ID de cliente", min_value=int(ids.min()), max_value=int(ids.max()), value=14, step=1)
    fila = int(np.where(ids == cid)[0][0])
    x_vec = X[fila].copy()
    st.write("Ya compró:", [productos[j] for j in np.where(x_vec > 0)[0]])

    # TODO 5: muestren las 3 recomendaciones con su puntaje y, para cada una, el "porque"
    #         - por ítem: "porque compró X (similitud 0.87)"
    #         - por cliente: "N de sus K vecinos más parecidos lo compraron"
    #         - popularidad: "es de lo más comprado"
    #         (y qué hacen con un cliente SIN historial: los métodos colaborativos dan puntaje 0)

with tab2:
    # TODO 6: tabla de comparación (hit rate@3 y cobertura de cada método) calculada sobre los clientes del grupo
    #         CONTROL que probaron algo nuevo (NUEVO.sum(axis=1) > 0 y es_control), con al menos un control
    #         interactivo (por ejemplo, un slider con cuántos clientes evaluar o el K del filtrado por cliente).
    #         Pista: es la misma lógica de hit_rate_at_k del notebook.
    st.info("Reemplacen cada TODO con su propio código. Revisen el notebook del laboratorio para la lógica exacta de cada pieza.")
