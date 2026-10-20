"""Recomendador de productos. Correr con: streamlit run app.py"""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Recomendador — Laboratorio", page_icon="☕", layout="wide")

DATA = Path(__file__).parent / "data"
VERDE, NARANJA, GRIS = "#00704A", "#C4512F", "#9A988E"
METODOS = ["Popularidad", "Filtrado por ítem", "Filtrado por cliente", "SVD", "Final (ítem + respaldo)"]


@st.cache_data
def cargar():
    catalogo = pd.read_csv(DATA / "catalogo.csv")
    hist = pd.read_csv(DATA / "ordenes_historial.csv")
    hold = pd.read_csv(DATA / "ordenes_holdout.csv")
    exp = pd.read_csv(DATA / "experimento.csv")
    clientes = pd.read_csv(DATA / "clientes.csv")
    productos = list(catalogo["item"])
    M = (pd.crosstab(hist["customer_id"], hist["item"]) > 0).astype(int).reindex(
        index=clientes["customer_id"], columns=productos, fill_value=0)
    X = M.values.astype(np.float32)
    H = (pd.crosstab(hold["customer_id"], hold["item"]) > 0).astype(int).reindex(
        index=M.index, columns=productos, fill_value=0).values
    NUEVO = H * (1 - X)
    NUEVO[:, productos.index("Agua")] = 0
    es_control = (exp.set_index("customer_id").loc[M.index, "grupo"] == "control").values
    return productos, M.index.values, X, NUEVO, es_control, catalogo.set_index("item")["precio"].reindex(productos).values


productos, ids, X, NUEVO, es_control, precios = cargar()
COL_AGUA = productos.index("Agua")
popularidad = X.sum(axis=0)
tiene_historial = X.sum(axis=1) > 0
elegibles = (NUEVO.sum(axis=1) > 0) & es_control


@st.cache_data
def similitud_items():
    S = np.round(cosine_similarity(X.T), 6)
    np.fill_diagonal(S, 0)
    return S


@st.cache_data
def modelo_svd(k):
    svd = TruncatedSVD(n_components=k, random_state=0)
    Z = svd.fit_transform(X)
    return Z @ svd.components_


S_IT = similitud_items()


def vecinos(filas, K):
    sims = np.round(cosine_similarity(X[filas], X), 6)
    sims[np.arange(len(filas)), filas] = 0
    orden = np.argsort(-sims, axis=1, kind="stable")[:, :K]
    return orden, np.take_along_axis(sims, orden, axis=1)


def puntajes(metodo, filas, K, k_svd):
    filas = np.asarray(filas)
    if metodo == "Popularidad":
        return np.tile(popularidad.astype(float), (len(filas), 1))
    if metodo == "Filtrado por ítem":
        return X[filas] @ S_IT
    if metodo == "Filtrado por cliente":
        orden, sims = vecinos(filas, K)
        return np.stack([sims[i] @ X[orden[i]] for i in range(len(filas))])
    if metodo == "SVD":
        return modelo_svd(k_svd)[filas]

    return np.where(tiene_historial[filas][:, None], X[filas] @ S_IT, popularidad[None, :].astype(float))


def top3(scores, filas):
    s = np.where(X[filas] > 0, -np.inf, scores).astype(float)
    s[:, COL_AGUA] = -np.inf
    return np.argsort(-s, axis=1, kind="stable")[:, :3]


@st.cache_data(show_spinner="Calculando recomendaciones para los 8,000 clientes…")
def top3_todos(metodo, K, k_svd, bloque=500):
    partes = []
    for ini in range(0, len(X), bloque):
        filas = np.arange(ini, min(ini + bloque, len(X)))
        partes.append(top3(puntajes(metodo, filas, K, k_svd), filas))
    return np.vstack(partes)


@st.cache_data
def comparar(muestra, K, k_svd, semilla=0):
    rng = np.random.default_rng(semilla)
    cand = np.where(elegibles)[0]
    filas = np.sort(rng.choice(cand, size=muestra, replace=False)) if muestra < len(cand) else cand
    out = {}
    for m in METODOS:
        t_all = top3_todos(m, K, k_svd)
        t = t_all[filas]
        aciertos = np.take_along_axis(NUEVO[filas], t, axis=1).sum(axis=1)
        out[m] = {"hit rate@3": float((aciertos > 0).mean()), "precisión@3": float((aciertos / 3).mean()),
                  "cobertura (de 28)": int(len(np.unique(t_all)))}
    return pd.DataFrame(out).T, len(filas)


def porque(metodo, fila, producto_j, K):
    x_vec = X[fila]
    if metodo == "Filtrado por ítem" or (metodo.startswith("Final") and tiene_historial[fila]):
        compras = [(productos[i], S_IT[i, producto_j]) for i in np.where(x_vec > 0)[0] if i != COL_AGUA]
        compras = sorted(compras, key=lambda t: -t[1])[:2]
        if compras:
            return "porque compró " + " y ".join(f"{p} (similitud {s:.2f})" for p, s in compras)
        return "porque se parece a lo que compró"
    if metodo == "Filtrado por cliente":
        orden, _ = vecinos(np.array([fila]), K)
        n = int(X[orden[0], producto_j].sum())
        return f"{n} de sus {K} clientes más parecidos lo compraron"
    if metodo == "SVD":
        return "porque su perfil de gustos (resumido en pocos factores) se parece al de quienes lo compran"
    return f"es de lo más comprado: lo compró el {popularidad[producto_j] / len(X):.0%} de los clientes"


st.title("☕ Recomendador de productos")
st.caption("Ayuda a decidir qué 3 productos mostrar a cada cliente en el carrusel «Para ti» y qué método conviene "
           "llevar al siguiente experimento, comparando cuánto aciertan con datos que ningún método vio.")

with st.sidebar:
    st.header("Parámetros")
    metodo = st.selectbox("Método de recomendación", METODOS, index=4)
    K = st.slider("Vecinos (K) del filtrado por cliente", 5, 300, 30, step=5)
    k_svd = st.slider("Factores del SVD", 2, 24, 6)
    st.markdown("---")
    st.markdown("**Cómo leerlo.** El hit rate mide si el cliente probó algo recomendado; "
                "no mide si lo probó *porque* se le recomendó.")

tab1, tab2, tab3 = st.tabs(["Recomendar", "Comparar métodos", "La verdad oculta"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        cid = st.number_input("ID de cliente", min_value=int(ids.min()), max_value=int(ids.max()), value=14, step=1)
    fila = int(np.where(ids == cid)[0][0])
    yaquedo = [productos[j] for j in np.where(X[fila] > 0)[0]]
    with c2:
        st.write("**Ya compró:**", ", ".join(yaquedo) if yaquedo else "nada todavía")

    sin_historial = not tiene_historial[fila]
    if sin_historial and metodo not in ("Popularidad", "Final (ítem + respaldo)"):
        st.warning("Este cliente no tiene historial: los métodos colaborativos no tienen nada que ordenar y dan "
                   "puntaje 0 a todo. Para estos clientes se usa la popularidad como respaldo.")
    sc = puntajes(metodo, [fila], K, k_svd)
    t = top3(sc, np.array([fila]))[0]
    st.subheader(f"3 recomendaciones — {metodo}")
    for rank, j in enumerate(t, start=1):
        with st.container(border=True):
            a, b = st.columns([1, 3])
            a.metric(f"#{rank}", productos[j])
            b.write(f"**Puntaje:** {sc[0, j]:.2f} · **Precio:** ${precios[j]:.2f}")
            b.write("Por qué: " + porque(metodo, fila, j, K))

with tab2:
    st.write("Comparación sobre clientes del grupo **control** que probaron un producto nuevo en los 90 días "
             "(sin carrusel, así que un acierto es una compra que ocurrió sola).")
    n_max = int(elegibles.sum())
    muestra = st.slider("Clientes a evaluar", 100, n_max, n_max, step=100)
    tabla, n_eval = comparar(muestra, K, k_svd)
    st.caption(f"Evaluados {n_eval:,} de {n_max:,} clientes elegibles. La cobertura cuenta los productos distintos "
               "que el método le recomienda a alguno de los 8,000 clientes (catálogo de 28 productos, sin Agua).")
    mostrar = tabla.copy()
    mostrar["hit rate@3"] = (mostrar["hit rate@3"] * 100).round(1)
    mostrar["precisión@3"] = mostrar["precisión@3"].round(3)
    st.dataframe(mostrar.rename(columns={"hit rate@3": "hit rate@3 (%)"}))
    st.bar_chart(tabla["hit rate@3"] * 100, color=VERDE)
    base = tabla.loc["Popularidad", "hit rate@3"]
    mejor = tabla["hit rate@3"].idxmax()
    st.success(f"Mayor hit rate: **{mejor}** ({tabla.loc[mejor, 'hit rate@3']:.1%}), "
               f"{tabla.loc[mejor, 'hit rate@3'] / base - 1:+.0%} frente a la popularidad ({base:.1%}).")

with tab3:
    st.write("En la vida real nadie conoce estas columnas. Acá se comparan contra el hit rate: "
             "acertar no es lo mismo que causar una compra.")
    ruta_cp = DATA / "verdad_oculta_cliente_producto.csv"
    if not ruta_cp.exists():
        st.info("Falta `data/verdad_oculta_cliente_producto.csv` para mostrar esta pestaña.")
    elif st.checkbox("Destapar la verdad oculta"):
        @st.cache_data
        def cargar_verdad():
            vo = pd.read_csv(ruta_cp)
            pi = vo.pivot(index="customer_id", columns="item", values="p_incremental").reindex(
                index=ids, columns=productos).fillna(0).values
            po = vo.pivot(index="customer_id", columns="item", values="p_organica").reindex(
                index=ids, columns=productos).fillna(0).values
            return pi, po

        pi, po = cargar_verdad()
        todas = np.arange(len(X))[:, None]
        filas_v = []
        tabla_h, _ = comparar(n_max, K, k_svd)
        for m in METODOS:
            t = top3_todos(m, K, k_svd)
            inc = (pi[todas, t] * precios[t]).sum(axis=1).mean()
            inc_n = pi[todas, t].sum()
            org_n = po[todas, t].sum()
            filas_v.append({"Método": m, "Hit rate@3 (control)": round(tabla_h.loc[m, "hit rate@3"], 3),
                            "Ingreso incremental (US$/cliente)": round(inc, 3),
                            "% de compras que ya iban a ocurrir": round(org_n / (org_n + inc_n), 3)})
        st.dataframe(pd.DataFrame(filas_v).set_index("Método"))
        st.caption("El hit rate exagera la ventaja de los métodos personalizados sobre la popularidad: una parte "
                   "importante de lo que aciertan ya iba a ocurrir sin recomendación.")
