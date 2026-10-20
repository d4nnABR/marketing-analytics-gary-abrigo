from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Starbucks Rewards — Recomendador", page_icon="☕", layout="wide")

DATA = Path(__file__).resolve().parent / "data"
GREEN, GOLD, CREAM, MUTED, RULE = "#00704A", "#C6A15B", "#F7F4ED", "#6E7C74", "#DAD3C4"
METHODS = ["pop", "item", "user", "svd", "final"]

TEXTS = {
    "es": {
        "kicker": "Starbucks Rewards · Carrusel «Para ti»",
        "title": "¿Qué 3 productos mostrarle a cada cliente?",
        "subtitle": "Esta herramienta recomienda productos con distintos métodos y los compara con lo que los clientes compraron después.",
        "params": "Parámetros",
        "method": "Método de recomendación",
        "customer": "ID de cliente",
        "k_users": "Vecinos (K) del filtrado por cliente",
        "k_svd": "Factores del SVD",
        "methods": {"pop": "Popularidad", "item": "Filtrado por ítem", "user": "Filtrado por cliente",
                    "svd": "SVD", "final": "Final (ítem + respaldo)"},
        "hit": "Hit rate@3",
        "vs_pop": "Frente a popularidad",
        "coverage": "Cobertura",
        "coverage_unit": "de 28 productos",
        "recs": "Recomendaciones",
        "bought": "Ya compró",
        "nothing": "nada todavía",
        "score": "Puntaje",
        "price": "Precio",
        "no_history": "Cliente sin historial: los métodos colaborativos no tienen con qué ordenar. El método final usa la popularidad.",
        "why_item": "porque compró {a}",
        "why_item_none": "porque se parece a lo que compró",
        "why_user": "{n} de sus {k} clientes más parecidos lo compraron",
        "why_svd": "porque su perfil de gustos se parece al de quienes lo compran",
        "why_pop": "lo compró el {p:.0%} de los clientes",
        "compare": "Comparación de métodos",
        "col_method": "Método",
        "col_hit": "Hit rate@3 (%)",
        "col_prec": "Precisión@3",
        "col_cov": "Cobertura",
        "caption": "{n:,} clientes del grupo control que probaron un producto nuevo en 90 días.",
        "xlabel": "Hit rate@3 (%)",
        "truth": "Mostrar la verdad oculta",
        "truth_title": "Hit rate frente a ingreso incremental",
        "col_inc": "Ingreso incremental (US$/cliente)",
        "col_org": "% de aciertos que ya iban a ocurrir",
    },
    "en": {
        "kicker": "Starbucks Rewards · «For you» carousel",
        "title": "Which 3 products should each customer see?",
        "subtitle": "This tool recommends products with different methods and compares them with what customers bought afterwards.",
        "params": "Parameters",
        "method": "Recommendation method",
        "customer": "Customer ID",
        "k_users": "Neighbors (K) for user-based filtering",
        "k_svd": "SVD factors",
        "methods": {"pop": "Popularity", "item": "Item-based filtering", "user": "User-based filtering",
                    "svd": "SVD", "final": "Final (item + fallback)"},
        "hit": "Hit rate@3",
        "vs_pop": "Versus popularity",
        "coverage": "Coverage",
        "coverage_unit": "of 28 products",
        "recs": "Recommendations",
        "bought": "Already bought",
        "nothing": "nothing yet",
        "score": "Score",
        "price": "Price",
        "no_history": "Customer with no history: collaborative methods have nothing to rank with. The final method uses popularity.",
        "why_item": "because they bought {a}",
        "why_item_none": "because it resembles what they bought",
        "why_user": "{n} of their {k} most similar customers bought it",
        "why_svd": "because their taste profile resembles that of its buyers",
        "why_pop": "bought by {p:.0%} of customers",
        "compare": "Method comparison",
        "col_method": "Method",
        "col_hit": "Hit rate@3 (%)",
        "col_prec": "Precision@3",
        "col_cov": "Coverage",
        "caption": "{n:,} control-group customers who tried a new product within 90 days.",
        "xlabel": "Hit rate@3 (%)",
        "truth": "Show the hidden truth",
        "truth_title": "Hit rate versus incremental revenue",
        "col_inc": "Incremental revenue (US$/customer)",
        "col_org": "% of hits that would have happened anyway",
    },
}

st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: Inter, sans-serif; font-size: 15px; }
    .block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
    h1 { font-family: Fraunces, serif; font-size: 1.7rem !important; line-height: 1.15; margin-bottom: .1rem; }
    h2, h3 { font-family: Fraunces, serif; font-size: 1.1rem !important; margin: .4rem 0 .2rem 0; }
    [data-testid="stMetricValue"] { font-family: Fraunces, serif; font-size: 1.5rem; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    catalog = pd.read_csv(DATA / "catalogo.csv")
    hist = pd.read_csv(DATA / "ordenes_historial.csv")
    hold = pd.read_csv(DATA / "ordenes_holdout.csv")
    exp = pd.read_csv(DATA / "experimento.csv")
    clients = pd.read_csv(DATA / "clientes.csv")
    products = list(catalog["item"])
    M = (pd.crosstab(hist["customer_id"], hist["item"]) > 0).astype(int).reindex(
        index=clients["customer_id"], columns=products, fill_value=0)
    X = M.values.astype(np.float32)
    H = (pd.crosstab(hold["customer_id"], hold["item"]) > 0).astype(int).reindex(
        index=M.index, columns=products, fill_value=0).values
    NEW = H * (1 - X)
    NEW[:, products.index("Agua")] = 0
    is_control = (exp.set_index("customer_id").loc[M.index, "grupo"] == "control").values
    prices = catalog.set_index("item")["precio"].reindex(products).values
    return products, M.index.values, X, NEW, is_control, prices


products, ids, X, NEW, is_control, prices = load_data()
WATER = products.index("Agua")
popularity = X.sum(axis=0)
has_history = X.sum(axis=1) > 0
eligible = (NEW.sum(axis=1) > 0) & is_control


@st.cache_data
def item_similarity():
    S = np.round(cosine_similarity(X.T), 6)
    np.fill_diagonal(S, 0)
    return S


@st.cache_data
def svd_scores(k):
    svd = TruncatedSVD(n_components=k, random_state=0)
    return svd.fit_transform(X) @ svd.components_


S_IT = item_similarity()


def neighbors(rows, K):
    sims = np.round(cosine_similarity(X[rows], X), 6)
    sims[np.arange(len(rows)), rows] = 0
    order = np.argsort(-sims, axis=1, kind="stable")[:, :K]
    return order, np.take_along_axis(sims, order, axis=1)


def scores(method, rows, K, k_svd):
    rows = np.asarray(rows)
    if method == "pop":
        return np.tile(popularity.astype(float), (len(rows), 1))
    if method == "item":
        return X[rows] @ S_IT
    if method == "user":
        order, sims = neighbors(rows, K)
        return np.stack([sims[i] @ X[order[i]] for i in range(len(rows))])
    if method == "svd":
        return svd_scores(k_svd)[rows]
    return np.where(has_history[rows][:, None], X[rows] @ S_IT, popularity[None, :].astype(float))


def top3(s, rows):
    s = np.where(X[rows] > 0, -np.inf, s).astype(float)
    s[:, WATER] = -np.inf
    return np.argsort(-s, axis=1, kind="stable")[:, :3]


@st.cache_data(show_spinner=False)
def top3_all(method, K, k_svd, block=500):
    parts = []
    for start in range(0, len(X), block):
        rows = np.arange(start, min(start + block, len(X)))
        parts.append(top3(scores(method, rows, K, k_svd), rows))
    return np.vstack(parts)


@st.cache_data(show_spinner="…")
def compare(K, k_svd):
    rows = np.where(eligible)[0]
    out = {}
    for m in METHODS:
        t_all = top3_all(m, K, k_svd)
        hits = np.take_along_axis(NEW[rows], t_all[rows], axis=1).sum(axis=1)
        out[m] = {"hit": float((hits > 0).mean()), "prec": float((hits / 3).mean()),
                  "cov": int(len(np.unique(t_all)))}
    return pd.DataFrame(out).T, len(rows)


@st.cache_data
def hidden_truth():
    vo = pd.read_csv(DATA / "verdad_oculta_cliente_producto.csv")
    pi = vo.pivot(index="customer_id", columns="item", values="p_incremental").reindex(
        index=ids, columns=products).fillna(0).values
    po = vo.pivot(index="customer_id", columns="item", values="p_organica").reindex(
        index=ids, columns=products).fillna(0).values
    return pi, po


def reason(t, method, row, j, K):
    if method == "item" or (method == "final" and has_history[row]):
        bought = [(products[i], S_IT[i, j]) for i in np.where(X[row] > 0)[0] if i != WATER]
        bought = sorted(bought, key=lambda b: -b[1])[:2]
        if bought:
            return t["why_item"].format(a=" / ".join(f"{p} ({s:.2f})" for p, s in bought))
        return t["why_item_none"]
    if method == "user":
        order, _ = neighbors(np.array([row]), K)
        return t["why_user"].format(n=int(X[order[0], j].sum()), k=K)
    if method == "svd":
        return t["why_svd"]
    return t["why_pop"].format(p=popularity[j] / len(X))


with st.sidebar:
    options = {"Español": "es", "English": "en"}
    if hasattr(st, "segmented_control"):
        pick = st.segmented_control("Idioma / Language", list(options), default="Español", label_visibility="collapsed")
    else:
        pick = st.radio("Idioma / Language", list(options), horizontal=True, label_visibility="collapsed")
    lang = options[pick or "Español"]
    t = TEXTS[lang]
    names = t["methods"]

    st.markdown(f"## {t['params']}")
    method = st.selectbox(t["method"], METHODS, index=4, format_func=names.get)
    cid = st.number_input(t["customer"], min_value=int(ids.min()), max_value=int(ids.max()), value=14, step=1)
    K = st.slider(t["k_users"], 5, 300, 30, 5)
    k_svd = st.slider(t["k_svd"], 2, 24, 6)

table, n_eval = compare(K, k_svd)
row = int(np.where(ids == cid)[0][0])

st.markdown(f"##### {t['kicker']}")
st.markdown(f"# {t['title']}")
st.markdown(t["subtitle"])

hit = table.loc[method, "hit"]
base = table.loc["pop", "hit"]
c1, c2, c3 = st.columns(3)
c1.metric(t["hit"], f"{hit:.1%}")
c2.metric(t["vs_pop"], f"{hit / base - 1:+.0%}")
c3.metric(t["coverage"], f"{int(table.loc[method, 'cov'])}", t["coverage_unit"], delta_color="off")

left, right = st.columns([2, 3], gap="large")

with left:
    st.markdown(f"## {t['recs']} · #{int(cid)}")
    bought = [products[j] for j in np.where(X[row] > 0)[0]]
    st.caption(f"{t['bought']}: " + (", ".join(bought) if bought else t["nothing"]))
    if not has_history[row] and method in ("item", "user", "svd"):
        st.warning(t["no_history"])
    sc = scores(method, [row], K, k_svd)
    for rank, j in enumerate(top3(sc, np.array([row]))[0], start=1):
        with st.container(border=True):
            st.markdown(f"**{rank}. {products[j]}** · {t['price']} ${prices[j]:.2f} · {t['score']} {sc[0, j]:.2f}")
            st.caption(reason(t, method, row, j, K))

with right:
    st.markdown(f"## {t['compare']}")
    st.caption(t["caption"].format(n=n_eval))
    shown = pd.DataFrame({
        t["col_method"]: [names[m] for m in METHODS],
        t["col_hit"]: (table["hit"] * 100).round(1).values,
        t["col_prec"]: table["prec"].round(3).values,
        t["col_cov"]: table["cov"].astype(int).values,
    })
    st.dataframe(shown, hide_index=True, width="stretch")

    fig, ax = plt.subplots(figsize=(7, 2.6))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    labels = [names[m] for m in METHODS]
    colors = [GREEN if m == method else MUTED for m in METHODS]
    ax.barh(labels, table["hit"].values * 100, color=colors)
    ax.invert_yaxis()
    ax.set_xlabel(t["xlabel"])
    ax.grid(axis="x", color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(RULE)
    ax.tick_params(colors=MUTED)
    plt.tight_layout()
    st.pyplot(fig, width="stretch")

    if (DATA / "verdad_oculta_cliente_producto.csv").exists() and st.checkbox(t["truth"]):
        pi, po = hidden_truth()
        every = np.arange(len(X))[:, None]
        rows_t = []
        for m in METHODS:
            tk = top3_all(m, K, k_svd)
            inc_n, org_n = pi[every, tk].sum(), po[every, tk].sum()
            rows_t.append({
                t["col_method"]: names[m],
                t["col_hit"]: round(table.loc[m, "hit"] * 100, 1),
                t["col_inc"]: round((pi[every, tk] * prices[tk]).sum(axis=1).mean(), 3),
                t["col_org"]: round(org_n / (org_n + inc_n) * 100, 1),
            })
        st.markdown(f"## {t['truth_title']}")
        st.dataframe(pd.DataFrame(rows_t), hide_index=True, width="stretch")
