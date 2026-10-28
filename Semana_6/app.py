from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from kmodes.kprototypes import KPrototypes
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Segmentación de clientes", page_icon="🧩", layout="wide")

CARPETA = Path(__file__).resolve().parent
NUM = ["ingreso_anual", "gasto_total", "compras_tienda", "compras_web", "compras_catalogo",
       "visitas_web_mes", "recencia_dias", "hijos_pequenos", "edad"]
CAT = ["educacion", "estado_civil"]
TECNICAS = ["k-means", "Jerárquico", "DBSCAN", "Mezcla gaussiana", "k-prototypes"]


def limpiar_columnas(df):
    # Orange guarda los encabezados con prefijos como "m#" o "D#"
    df.columns = df.columns.str.replace(r"^[a-zA-Z]*#", "", regex=True)
    return df.rename(columns={"respondio_ultima_campana": "respondio"})


@st.cache_data
def cargar_clientes():
    return limpiar_columnas(pd.read_csv(CARPETA / "clientes_retail.csv"))


@st.cache_data
def cargar_segmentos():
    return limpiar_columnas(pd.read_csv(CARPETA / "segmentos_notebook.csv"))


@st.cache_data
def ajustar_tecnicas(k, eps, min_muestras):
    c = cargar_clientes()
    z = StandardScaler().fit_transform(c[NUM])
    mixto = pd.concat([pd.DataFrame(z, columns=NUM), c[CAT].reset_index(drop=True)], axis=1)
    grupos = {
        "k-means": KMeans(k, n_init=10, random_state=0).fit_predict(z),
        "Jerárquico": AgglomerativeClustering(k, linkage="ward").fit_predict(z),
        "DBSCAN": DBSCAN(eps=eps, min_samples=min_muestras).fit_predict(z),
        "Mezcla gaussiana": GaussianMixture(k, random_state=0, n_init=5).fit_predict(z),
        "k-prototypes": KPrototypes(n_clusters=k, init="Cao", random_state=0, n_init=3)
        .fit_predict(mixto.values, categorical=[len(NUM), len(NUM) + 1]),
    }
    return z, grupos


def perfil(df, col):
    t = df.groupby(col).agg(Clientes=("gasto_total", "size"), gasto=("gasto_total", "sum"),
                            **{"Gasto promedio": ("gasto_total", "mean")})
    t["% de clientes"] = 100 * t["Clientes"] / t["Clientes"].sum()
    t["% del gasto"] = 100 * t["gasto"] / t["gasto"].sum()
    t = t.drop(columns="gasto").round(1)
    t.index = t.index.astype(str)
    return t[["Clientes", "% de clientes", "Gasto promedio", "% del gasto"]]


st.title("Segmentación de clientes")
st.caption("Grupo 5 · Visor de grupos y comparador de técnicas con 2,205 clientes de una tienda minorista.")

visor, comparador, recomendacion = st.tabs(["Visor de grupos", "Comparador de técnicas", "Recomendación"])

with visor:
    archivo = st.file_uploader("Suba un CSV con una columna de grupos (de Orange o del notebook)", type="csv")
    if archivo is None:
        df = cargar_segmentos()
        st.info("Mostrando `segmentos_notebook.csv`, el resultado del notebook. Suba otro CSV para verlo.")
    else:
        df = limpiar_columnas(pd.read_csv(archivo))
        if "gasto_total" not in df.columns and "id_cliente" in df.columns:
            df = df.merge(cargar_clientes(), on="id_cliente", how="left")

    if "gasto_total" not in df.columns:
        st.error("El archivo necesita la columna `gasto_total` o `id_cliente` para unirlo con los clientes.")
        st.stop()

    candidatas = [col for col in df.columns if df[col].nunique() <= 20 and col not in ("hijos_pequenos", "hijos_adolescentes")]
    preferida = next((col for col in ("Cluster", "cluster", "seg_kproto") if col in candidatas), candidatas[0])
    col = st.selectbox("Columna de grupos", candidatas, index=candidatas.index(preferida))

    tabla = perfil(df, col)
    izq, der = st.columns([1, 1])
    with izq:
        fig = px.bar(tabla.reset_index(), x=col, y="Clientes", text="Clientes",
                     color=col, title="Clientes por grupo")
        fig.update_layout(showlegend=False, xaxis_title="Grupo")
        st.plotly_chart(fig, width="stretch")
    with der:
        st.markdown("**Perfil de los grupos**")
        st.dataframe(tabla, width="stretch")
        variables = [v for v in NUM if v in df.columns]
        if variables:
            with st.expander("Promedio de cada variable por grupo"):
                st.dataframe(df.groupby(col)[variables].mean().round(1), width="stretch")

    if {"ingreso_anual", "gasto_total"} <= set(df.columns):
        fig = px.scatter(df.assign(**{col: df[col].astype(str)}), x="ingreso_anual", y="gasto_total",
                         color=col, opacity=0.6, title="Ingreso anual frente a gasto total",
                         labels={"ingreso_anual": "Ingreso anual", "gasto_total": "Gasto total"})
        st.plotly_chart(fig, width="stretch")

with comparador:
    st.write("Las cinco técnicas usan las mismas 9 variables numéricas estandarizadas. "
             "k-prototypes además usa educación y estado civil.")
    a, b, c_ = st.columns(3)
    k = a.slider("Número de grupos (k)", 2, 8, 3)
    eps = b.slider("DBSCAN: radio (eps)", 0.5, 3.0, 1.5, 0.1)
    min_muestras = c_.slider("DBSCAN: mínimo de vecinos", 3, 30, 10)

    with st.spinner("Ajustando las técnicas..."):
        z, grupos = ajustar_tecnicas(k, eps, min_muestras)
    clientes = cargar_clientes()

    filas = []
    for nombre, g in grupos.items():
        validos = g != -1
        n = len(set(g[validos]))
        tamanos = pd.Series(g[validos]).value_counts().sort_index()
        sil = silhouette_score(z[validos], g[validos]) if n > 1 else np.nan
        filas.append({"Técnica": nombre, "Grupos": n,
                      "Tamaños": ", ".join(str(t) for t in tamanos),
                      "Ruido (sin grupo)": int((~validos).sum()),
                      "Silueta": round(sil, 3)})
    resumen = pd.DataFrame(filas).set_index("Técnica")
    st.dataframe(resumen, width="stretch")
    st.caption("Silueta: de -1 a 1, más alta = grupos más separados. En DBSCAN se calcula sin los puntos de ruido.")

    izq, der = st.columns([1, 1])
    with izq:
        ari = pd.DataFrame([[adjusted_rand_score(grupos[x], grupos[y]) for y in TECNICAS] for x in TECNICAS],
                           index=TECNICAS, columns=TECNICAS).round(2)
        fig = px.imshow(ari, text_auto=True, color_continuous_scale="Greens", zmin=0, zmax=1,
                        title="¿Qué tanto coinciden? (índice de Rand ajustado, 1 = idénticas)")
        st.plotly_chart(fig, width="stretch")
    with der:
        elegida = st.selectbox("Ver los grupos de", TECNICAS)
        xy = PCA(2, random_state=0).fit_transform(z)
        vista = pd.DataFrame({"Componente 1": xy[:, 0], "Componente 2": xy[:, 1],
                              "Grupo": pd.Series(grupos[elegida]).astype(str).replace("-1", "Ruido")})
        fig = px.scatter(vista, x="Componente 1", y="Componente 2", color="Grupo", opacity=0.6,
                         title=f"{elegida} en dos dimensiones (PCA)")
        st.plotly_chart(fig, width="stretch")
        st.dataframe(perfil(clientes.assign(Grupo=grupos[elegida]), "Grupo"), width="stretch")

with recomendacion:
    st.subheader("Qué segmentación darle a marketing")
    st.markdown(
        "1. **Tres segmentos con k-means**: clientes de alto gasto (~25%, gastan unos US$ 1,300), "
        "de gasto medio (~29%, ~US$ 670) y de bajo gasto (~46%, ~US$ 85).\n"
        "2. **Por qué k-means:** tiene la mejor silueta (0.25) y es la técnica más fácil de explicar: "
        "cada cliente va al grupo cuyo promedio se le parece más.\n"
        "3. **k-prototypes da los mismos grupos** (coincidencia de 0.99), así que agregar educación y estado civil "
        "no cambió la segmentación; esas variables sirven para describir cada grupo, no para formarlo."
    )
    st.caption("Valores con k = 3 y DBSCAN con eps = 1.5 y 10 vecinos (los parámetros por defecto del comparador).")
