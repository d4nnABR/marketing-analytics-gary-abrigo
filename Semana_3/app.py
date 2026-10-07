"""
Laboratorio Final — Starbucks Rewards (app de Streamlit)

Permite a alguien de negocio (que no programa) explorar los resultados del laboratorio:
el Qini del T-learner y la tabla de políticas, con un control interactivo (% a contactar).

Correr local:  streamlit run app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Laboratorio Final — Starbucks Rewards", page_icon="☕", layout="wide")

GREEN = "#00704A"
ORANGE = "#C4512F"
GRAY = "#9A988E"
FEATURES = ["recency_days", "frequency", "monetary", "email_open_rate", "tenure_days"]

# Ruta relativa al archivo -> funciona en local y en Streamlit Cloud
DATA_PATH = Path(__file__).resolve().parent / "data" / "uplift_campaign.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_data
def entrenar_t_learner(df: pd.DataFrame, test_size: float = 0.30, seed: int = 42):
    train, test = train_test_split(
        df, test_size=test_size, random_state=seed, stratify=df["treatment_group"]
    )

    # T-learner: un modelo por grupo (dos regresiones logísticas)
    train_t = train[train["treatment_group"] == "treatment"]
    train_c = train[train["treatment_group"] == "control"]

    modelo_tratado = LogisticRegression(max_iter=1000)
    modelo_control = LogisticRegression(max_iter=1000)
    modelo_tratado.fit(train_t[FEATURES], train_t["responded_60d"])
    modelo_control.fit(train_c[FEATURES], train_c["responded_60d"])

    test = test.copy()
    X_test = test[FEATURES]
    test["p_tratado"] = modelo_tratado.predict_proba(X_test)[:, 1]
    test["p_control"] = modelo_control.predict_proba(X_test)[:, 1]
    test["uplift_estimado"] = test["p_tratado"] - test["p_control"]
    return test


def valor_de_la_politica(test_df, seleccionados):
    # Valor NETO: utilidad_neta_60d (tratados) menos margin_60d (control del mismo grupo)
    sel = test_df.loc[seleccionados]
    valor_tratado = sel.loc[sel["treatment_group"] == "treatment", "utilidad_neta_60d"].mean()
    valor_control = sel.loc[sel["treatment_group"] == "control", "margin_60d"].mean()
    return valor_tratado - valor_control, len(sel)


def curva_qini(test_df, score_col, steps=40):
    orden = test_df.sort_values(score_col, ascending=False).reset_index(drop=True)
    es_tratado = (orden["treatment_group"] == "treatment").values
    respondio = orden["responded_60d"].values

    acum_t = np.cumsum(np.where(es_tratado, respondio, 0))
    acum_c = np.cumsum(np.where(~es_tratado, respondio, 0))
    n_t = np.cumsum(es_tratado)
    n_c = np.cumsum(~es_tratado)

    n = len(orden)
    xs, ys = [0.0], [0.0]
    for i in np.linspace(1, n, steps).astype(int):
        tasa_t = acum_t[i - 1] / n_t[i - 1] if n_t[i - 1] > 0 else 0
        tasa_c = acum_c[i - 1] / n_c[i - 1] if n_c[i - 1] > 0 else 0
        xs.append(i / n)
        ys.append((tasa_t - tasa_c) * n)
    return np.array(xs), np.array(ys)


def coeficiente_qini(xs, ys, n):
    try:
        trap = np.trapezoid
    except AttributeError:
        trap = np.trapz
    area_modelo = trap(ys, xs)
    area_azar = trap(np.linspace(0, ys[-1], len(xs)), xs)
    return (area_modelo - area_azar) / n


# --- Título ---
st.title("Laboratorio Final — Starbucks Rewards ☕")
st.caption(
    "¿A qué porcentaje de la base conviene enviarle el cupón de $5? "
    "Esta app muestra el Qini del T-learner y el valor neto por cada nivel de contacto."
)

df = load_data()

with st.sidebar:
    st.header("Parámetros")
    pct_contactar = st.slider("% de la base a contactar", min_value=5, max_value=100, value=20, step=5)
    st.caption(f"{len(df):,} clientes · campaña a 60 días")

test = entrenar_t_learner(df)

xs_uplift, ys_uplift = curva_qini(test, "uplift_estimado")
qini = coeficiente_qini(xs_uplift, ys_uplift, len(test))

col1, col2 = st.columns([3, 2])

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs_uplift, ys_uplift, color=GREEN, linewidth=3, label=f"T-learner (Qini={qini:+.3f})")
    ax.plot([0, 1], [0, ys_uplift[-1]], color=GRAY, linestyle="--", label="Al azar")
    ax.axvline(pct_contactar / 100, color=ORANGE, linestyle=":", linewidth=2, label=f"{pct_contactar}% elegido")
    ax.set_xlabel("% de la base contactada")
    ax.set_ylabel("Respuestas incrementales acumuladas")
    ax.set_title("Curva Qini del T-learner")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    n_c = int(len(test) * pct_contactar / 100)
    idx = test.sort_values("uplift_estimado", ascending=False).head(n_c).index
    valor_cliente, n = valor_de_la_politica(test, idx)

    st.metric("Coeficiente Qini", f"{qini:+.3f}")
    st.metric("Valor neto por cliente", f"${valor_cliente:+.2f}")
    st.metric("Valor neto total", f"${valor_cliente * n:+,.2f}")
    st.caption(f"Contactando {n:,} clientes ({pct_contactar}% del set de prueba)")

# --- Tabla de políticas ---
st.subheader("Tabla de políticas")
filas = []
for pct in range(10, 101, 10):
    nc = int(len(test) * pct / 100)
    ix = test.sort_values("uplift_estimado", ascending=False).head(nc).index
    vc, nn = valor_de_la_politica(test, ix)
    filas.append({
        "pct_contactado": pct,
        "n_contactados": nn,
        "valor_por_cliente": round(vc, 2),
        "valor_total": round(vc * nn, 2),
    })
tabla = pd.DataFrame(filas)

st.dataframe(
    tabla.style.apply(
        lambda r: ["background-color: #E8F5E9" if r["pct_contactado"] == pct_contactar else "" for _ in r],
        axis=1,
    ),
    use_container_width=True,
)

mejor_total = tabla.loc[tabla["valor_total"].idxmax()]
st.success(
    f"El valor TOTAL se maximiza contactando al {mejor_total['pct_contactado']}% "
    f"(≈ ${mejor_total['valor_total']:,.2f} netos). El valor POR CLIENTE es máximo en el 10%."
)

st.info(
    "Regla de decisión: contactar primero a los de mayor **uplift** (Persuadable). "
    "Evitar Sleeping Dog y Lost Cause. Comparación de modelos y deciles en el notebook."
)
