from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Starbucks Rewards — Uplift Targeting", page_icon="☕", layout="wide")

FEATURES = ["recency_days", "frequency", "monetary", "email_open_rate", "tenure_days"]
DATA = Path(__file__).resolve().parent / "data" / "uplift_campaign.csv"
GREEN, GOLD, CREAM, MUTED, RULE = "#00704A", "#C6A15B", "#F7F4ED", "#6E7C74", "#DAD3C4"

TEXTS = {
    "es": {
        "kicker": "Starbucks Rewards · Campaña de retención a 60 días",
        "title": "¿A quién darle el cupón de $5?",
        "subtitle": "Esta herramienta estima el uplift de cada cliente y muestra qué porcentaje de la base vale la pena contactar.",
        "params": "Parámetros",
        "lang": "Idioma",
        "slider": "Porcentaje de la base a contactar",
        "caption": "{n} clientes · cupón de $5 · ventana de 60 días",
        "qini": "Coeficiente Qini",
        "value_per": "Valor neto por cliente",
        "value_total": "Valor neto total",
        "curve": "Curva Qini",
        "random": "Al azar",
        "contact": "Contactar {pct}%",
        "xlabel": "Porcentaje de la base contactada",
        "ylabel": "Respuestas incrementales acumuladas",
        "policy": "Tabla de políticas",
        "col_contacted": "Contactado",
        "col_customers": "Clientes",
        "col_value_per": "Valor por cliente",
        "col_total": "Valor total",
        "peak_total": "Valor total máximo",
        "peak_per": "Valor por cliente máximo",
        "of_base": "% de la base",
        "net": "${v:,.2f} neto",
        "each": "${v:.2f} cada uno",
    },
    "en": {
        "kicker": "Starbucks Rewards · 60-day retention campaign",
        "title": "Who should get the $5 coupon?",
        "subtitle": "This tool estimates each customer's uplift and shows what share of the base is worth contacting.",
        "params": "Parameters",
        "lang": "Language",
        "slider": "Share of the base to contact",
        "caption": "{n} customers · $5 coupon · 60-day window",
        "qini": "Qini coefficient",
        "value_per": "Net value per customer",
        "value_total": "Total net value",
        "curve": "Qini curve",
        "random": "Random",
        "contact": "Contact {pct}%",
        "xlabel": "Share of the base contacted",
        "ylabel": "Cumulative incremental responses",
        "policy": "Policy table",
        "col_contacted": "Contacted",
        "col_customers": "Customers",
        "col_value_per": "Value per customer",
        "col_total": "Total value",
        "peak_total": "Peak total value",
        "peak_per": "Peak value per customer",
        "of_base": "% of base",
        "net": "${v:,.2f} net",
        "each": "${v:.2f} each",
    },
}

st.markdown(
    f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] {{ font-family: Inter, sans-serif; font-size: 15px; }}
    .block-container {{ padding-top: 1.2rem; padding-bottom: 1rem; }}
    h1 {{ font-family: Fraunces, serif; font-size: 1.7rem !important; line-height: 1.15; margin-bottom: .1rem; }}
    h2, h3 {{ font-family: Fraunces, serif; font-size: 1.1rem !important; margin: .4rem 0 .2rem 0; }}
    [data-testid="stMetricValue"] {{ font-family: Fraunces, serif; font-size: 1.5rem; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    return pd.read_csv(DATA)


@st.cache_data
def train_t_learner(df, test_size=0.3, seed=42):
    train, test = train_test_split(df, test_size=test_size, random_state=seed, stratify=df["treatment_group"])
    treated = train[train["treatment_group"] == "treatment"]
    control = train[train["treatment_group"] == "control"]
    m_treated = LogisticRegression(max_iter=1000).fit(treated[FEATURES], treated["responded_60d"])
    m_control = LogisticRegression(max_iter=1000).fit(control[FEATURES], control["responded_60d"])
    test = test.copy()
    X = test[FEATURES]
    test["p_treated"] = m_treated.predict_proba(X)[:, 1]
    test["p_control"] = m_control.predict_proba(X)[:, 1]
    test["uplift"] = test["p_treated"] - test["p_control"]
    return test


def policy_value(test_df, idx):
    sel = test_df.loc[idx]
    treated = sel.loc[sel["treatment_group"] == "treatment", "utilidad_neta_60d"].mean()
    control = sel.loc[sel["treatment_group"] == "control", "margin_60d"].mean()
    return treated - control, len(sel)


def qini_curve(test_df, score_col, steps=40):
    d = test_df.sort_values(score_col, ascending=False).reset_index(drop=True)
    treated = (d["treatment_group"] == "treatment").values
    responded = d["responded_60d"].values
    cum_t = np.cumsum(np.where(treated, responded, 0))
    cum_c = np.cumsum(np.where(~treated, responded, 0))
    n_t = np.cumsum(treated)
    n_c = np.cumsum(~treated)
    n = len(d)
    xs, ys = [0.0], [0.0]
    for i in np.linspace(1, n, steps).astype(int):
        rt = cum_t[i - 1] / n_t[i - 1] if n_t[i - 1] else 0
        rc = cum_c[i - 1] / n_c[i - 1] if n_c[i - 1] else 0
        xs.append(i / n)
        ys.append((rt - rc) * n)
    return np.array(xs), np.array(ys)


def qini_coefficient(xs, ys, n):
    trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    return (trap(ys, xs) - trap(np.linspace(0, ys[-1], len(xs)), xs)) / n


df = load_data()

with st.sidebar:
    options = {"Español": "es", "English": "en"}
    if hasattr(st, "segmented_control"):
        pick = st.segmented_control("Idioma / Language", list(options), default="Español", label_visibility="collapsed")
    else:
        pick = st.radio("Idioma / Language", list(options), horizontal=True, label_visibility="collapsed")
    pick = pick or "Español"
    lang = options[pick]
    t = TEXTS[lang]

    st.markdown(f"## {t['params']}")
    pct = st.slider(t["slider"], 5, 100, 20, 5)
    st.caption(t["caption"].format(n=f"{len(df):,}"))

test = train_t_learner(df)
xs, ys = qini_curve(test, "uplift")
qini = qini_coefficient(xs, ys, len(test))

n_contact = int(len(test) * pct / 100)
idx = test.sort_values("uplift", ascending=False).head(n_contact).index
value, n_sel = policy_value(test, idx)

st.markdown(f"##### {t['kicker']}")
st.markdown(f"# {t['title']}")
st.markdown(t["subtitle"])

c1, c2, c3 = st.columns(3)
c1.metric(t["qini"], f"{qini:+.3f}")
c2.metric(t["value_per"], f"${value:+.2f}")
c3.metric(t["value_total"], f"${value * n_sel:+,.2f}")

left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown(f"## {t['curve']}")
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    ax.plot(xs, ys, color=GREEN, linewidth=2.4, label=f"T-learner · Qini {qini:+.3f}")
    ax.plot([0, 1], [0, ys[-1]], color=MUTED, linewidth=1.3, linestyle="--", label=t["random"])
    ax.axvline(pct / 100, color=GOLD, linewidth=2, linestyle=":", label=t["contact"].format(pct=pct))
    ax.set_xlabel(t["xlabel"])
    ax.set_ylabel(t["ylabel"])
    ax.grid(axis="y", color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(RULE)
    ax.tick_params(colors=MUTED)
    ax.legend(frameon=False, loc="upper right")
    plt.tight_layout()
    st.pyplot(fig, width="stretch")

with right:
    st.markdown(f"## {t['policy']}")
    rows = []
    for p in range(10, 101, 10):
        k = int(len(test) * p / 100)
        ix = test.sort_values("uplift", ascending=False).head(k).index
        v, m = policy_value(test, ix)
        rows.append({"pct": p, "customers": m, "per_customer": v, "total": v * m})
    table = pd.DataFrame(rows)

    st.dataframe(
        table,
        hide_index=True,
        width="stretch",
        height=380,
        column_config={
            "pct": st.column_config.NumberColumn(t["col_contacted"], format="%d%%"),
            "customers": st.column_config.NumberColumn(t["col_customers"], format="%d"),
            "per_customer": st.column_config.NumberColumn(t["col_value_per"], format="$%.2f"),
            "total": st.column_config.NumberColumn(t["col_total"], format="$%.2f"),
        },
    )

    best_total = table.loc[table["total"].idxmax()]
    best_per = table.loc[table["per_customer"].idxmax()]
    st.markdown(
        f"""
        <div style="display:flex; gap:2rem; margin-top:.7rem;">
          <div>
            <div style="color:{MUTED}; font-size:.78rem;">{t['peak_total']}</div>
            <div style="font-family:Fraunces,serif; font-size:1.45rem; line-height:1.1;">{int(best_total['pct'])}% {t['of_base']}</div>
            <div style="color:{MUTED}; font-size:.78rem;">{t['net'].format(v=best_total['total'])}</div>
          </div>
          <div>
            <div style="color:{MUTED}; font-size:.78rem;">{t['peak_per']}</div>
            <div style="font-family:Fraunces,serif; font-size:1.45rem; line-height:1.1;">{int(best_per['pct'])}% {t['of_base']}</div>
            <div style="color:{MUTED}; font-size:.78rem;">{t['each'].format(v=best_per['per_customer'])}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
