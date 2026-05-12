"""Week 11 Homework — N-back Working Memory Dashboard.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------------
# Page config — must be the first Streamlit call
# -----------------------------------------------------------
st.set_page_config(
    page_title="N-back Working Memory Dashboard",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "nback_working_memory.csv"

# ===========================================================
# TODO 1 — Data loading + error handling
# ===========================================================
if not DATA_PATH.exists():
    st.error("找不到資料檔，請確認 data/nback_working_memory.csv 存在。")
    st.stop()

df_all = pd.read_csv(DATA_PATH)

# Bonus A — status message after loading
st.success(f"資料載入成功：共 {len(df_all):,} 列，{df_all['participant_id'].nunique()} 位受試者。")

# ===========================================================
# Page header
# ===========================================================
st.title("🧠 N-back Working Memory Dashboard")
st.write(
    "Interactive visualization of a synthetic N-back working memory study "
    "(n=200, conditions: 1-back / 2-back / 3-back). 用左側 sidebar 篩選資料。"
)

# ===========================================================
# TODO 2 — Sidebar widgets
# ===========================================================
with st.sidebar:
    st.header("🔬 Filters")

    age_min, age_max = st.slider("Age range", 18, 75, (18, 75))

    sex_choices = st.multiselect("Sex", ["F", "M"], default=["F", "M"])

    selected_conds = st.multiselect(
        "Condition",
        ["1-back", "2-back", "3-back"],
        default=["1-back", "2-back", "3-back"],
    )

    st.markdown("---")
    st.caption("HW Week 11 · NS5116 Spring 2026")

# Apply filters
mask = (
    df_all["age"].between(age_min, age_max)
    & df_all["sex"].isin(sex_choices)
    & df_all["condition"].isin(selected_conds)
)
df = df_all[mask].copy()

# Bonus A — status messages after filtering
if df.empty:
    st.warning("No data matches the current filters. Loosen the sidebar filters.")
    st.stop()
elif len(df) < 30:
    st.warning(f"⚠️ 警告：篩選後僅 N={len(df)} 列，樣本量偏少，統計摘要請謹慎解讀。")
else:
    st.info(f"篩選後共 {len(df):,} 列（{df['participant_id'].nunique()} 位受試者）。")

# ===========================================================
# TODO 3 — Three metrics (always visible above tabs)
# ===========================================================
c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Avg Accuracy", f"{df['accuracy'].mean():.2f}")
c3.metric("Avg RT (ms)", f"{int(df['mean_rt_ms'].mean())} ms")

st.markdown("---")

# ===========================================================
# Bonus B — Multi-tab layout
# ===========================================================
tab_overview, tab_by_cond, tab_raw = st.tabs(["📊 Overview", "🔍 By Condition", "📋 Raw Data"])

# ------ Tab 1: Overview ----------------------------------------
with tab_overview:
    st.subheader("Accuracy by Age and Condition")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = {"1-back": "#4C72B0", "2-back": "#DD8452", "3-back": "#55A868"}
    for cond in selected_conds:
        sub = df[df["condition"] == cond]
        ax.scatter(sub["age"], sub["accuracy"], label=cond,
                   alpha=0.65, color=colors.get(cond), edgecolors="none", s=40)
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Accuracy")
    ax.set_title("Accuracy by Age and Condition")
    ax.set_ylim(0, 1.05)
    ax.legend(title="Condition")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Reaction Time by Age and Condition")
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    for cond in selected_conds:
        sub = df[df["condition"] == cond]
        ax2.scatter(sub["age"], sub["mean_rt_ms"], label=cond,
                    alpha=0.65, color=colors.get(cond), edgecolors="none", s=40)
    ax2.set_xlabel("Age (years)")
    ax2.set_ylabel("Mean RT (ms)")
    ax2.set_title("Reaction Time by Age and Condition")
    ax2.legend(title="Condition")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# ------ Tab 2: By Condition ------------------------------------
with tab_by_cond:
    st.subheader("Group Summary by Condition")

    summary = (
        df.groupby("condition", sort=False)
        .agg(
            N=("participant_id", "count"),
            Accuracy=("accuracy", "mean"),
            RT_ms=("mean_rt_ms", "mean"),
            d_prime=("d_prime", "mean"),
        )
        .reindex(["1-back", "2-back", "3-back"])
        .dropna()
        .reset_index()
    )

    # Show summary table
    st.dataframe(
        summary.rename(columns={"condition": "Condition", "RT_ms": "Avg RT (ms)", "d_prime": "Avg d′"})
        .style.format({"Accuracy": "{:.3f}", "Avg RT (ms)": "{:.0f}", "Avg d′": "{:.2f}"}),
        use_container_width=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        bar_colors = [colors.get(c, "#999") for c in summary["condition"]]
        ax3.bar(summary["condition"], summary["Accuracy"], color=bar_colors, edgecolor="white")
        ax3.set_ylim(0, 1.05)
        ax3.set_xlabel("Condition")
        ax3.set_ylabel("Mean Accuracy")
        ax3.set_title("Mean Accuracy by Condition")
        for i, (cond, val) in enumerate(zip(summary["condition"], summary["Accuracy"])):
            ax3.text(i, val + 0.01, f"{val:.3f}", ha="center", va="bottom", fontsize=9)
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    with col_b:
        fig4, ax4 = plt.subplots(figsize=(5, 4))
        ax4.bar(summary["condition"], summary["RT_ms"], color=bar_colors, edgecolor="white")
        ax4.set_xlabel("Condition")
        ax4.set_ylabel("Mean RT (ms)")
        ax4.set_title("Mean Reaction Time by Condition")
        for i, (cond, val) in enumerate(zip(summary["condition"], summary["RT_ms"])):
            ax4.text(i, val + 5, f"{val:.0f}", ha="center", va="bottom", fontsize=9)
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    # d-prime line chart
    st.subheader("d′ (Sensitivity) by Condition")
    fig5, ax5 = plt.subplots(figsize=(6, 3.5))
    ax5.plot(summary["condition"], summary["d_prime"], marker="o", linewidth=2, color="#C44E52")
    ax5.set_xlabel("Condition")
    ax5.set_ylabel("Mean d′")
    ax5.set_title("Signal Detection Sensitivity Across Conditions")
    ax5.grid(axis="y", linestyle="--", alpha=0.4)
    fig5.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

# ------ Tab 3: Raw Data ----------------------------------------
with tab_raw:
    st.subheader("Filtered Data")

    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="nback_filtered.csv",
        mime="text/csv",
    )
