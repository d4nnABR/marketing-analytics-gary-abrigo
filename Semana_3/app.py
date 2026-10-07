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

st.markdown(
    f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600&display=swap');
    .stApp {{ background: {CREAM}; }}
    html, body, [class*="css"] {{ font-family: Inter, sans-serif; }}
    h1, h2, h3 {{ font-family: Fraunces, serif; color: #1E3932; }}
    [data-testid="stMetricValue"] {{ font-family: Fraunces, serif; color: #1E3932; }}
    [data-testid="stSidebar"] {{ background: #EFEAE0; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .callout {{ border-left: 3px solid {GREEN}; padding: .5rem 1rem; }}
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


st.markdown("##### Starbucks Rewards · 60-day retention campaign")
st.markdown("# Who should get the $5 coupon?")
st.markdown(
    "This tool estimates each customer's uplift from the experiment and shows what share "
    "of the base is worth contacting to leave the most money on the table."
)

df = load_data()

with st.sidebar:
    st.markdown("## Parameters")
    pct = st.slider("Share of the base to contact", 5, 100, 20, 5)
    st.caption(f"{len(df):,} customers · $5 coupon · 60-day window")

test = train_t_learner(df)
xs, ys = qini_curve(test, "uplift")
qini = qini_coefficient(xs, ys, len(test))

n_contact = int(len(test) * pct / 100)
idx = test.sort_values("uplift", ascending=False).head(n_contact).index
value, n_sel = policy_value(test, idx)

c1, c2, c3 = st.columns(3)
c1.metric("Qini coefficient", f"{qini:+.3f}")
c2.metric("Net value per customer", f"${value:+.2f}")
c3.metric("Total net value", f"${value * n_sel:+,.2f}")

st.markdown("## Qini curve")
st.caption("How much better than random the model ranks customers, from highest to lowest predicted uplift.")

fig, ax = plt.subplots(figsize=(10, 4.6))
fig.patch.set_facecolor(CREAM)
ax.set_facecolor(CREAM)
ax.plot(xs, ys, color=GREEN, linewidth=2.6, label=f"T-learner · Qini {qini:+.3f}")
ax.plot([0, 1], [0, ys[-1]], color=MUTED, linewidth=1.4, linestyle="--", label="Random")
ax.axvline(pct / 100, color=GOLD, linewidth=2, linestyle=":", label=f"Contact {pct}%")
ax.set_xlabel("Share of the base contacted")
ax.set_ylabel("Cumulative incremental responses")
ax.grid(axis="y", color=RULE, linewidth=0.8)
ax.set_axisbelow(True)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
for spine in ("left", "bottom"):
    ax.spines[spine].set_color(RULE)
ax.tick_params(colors=MUTED)
ax.legend(frameon=False, loc="upper left")
plt.tight_layout()
st.pyplot(fig, use_container_width=True)

st.markdown("## Policy table")
st.caption("Net value per customer and total, by share of the base contacted.")

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
    use_container_width=True,
    column_config={
        "pct": st.column_config.NumberColumn("Contacted", format="%d%%"),
        "customers": st.column_config.NumberColumn("Customers", format="%d"),
        "per_customer": st.column_config.NumberColumn("Value per customer", format="$%.2f"),
        "total": st.column_config.NumberColumn("Total value", format="$%.2f"),
    },
)

best_total = table.loc[table["total"].idxmax()]
best_per = table.loc[table["per_customer"].idxmax()]
st.markdown(
    f'<div class="callout">Total value peaks at <b>{int(best_total["pct"])}%</b> of the base '
    f'(${best_total["total"]:,.2f}). Value per customer peaks at <b>{int(best_per["pct"])}%</b> '
    f'(${best_per["per_customer"]:.2f}).</div>',
    unsafe_allow_html=True,
)
