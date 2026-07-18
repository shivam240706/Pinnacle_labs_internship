"""
app.py
------
Streamlit front-end for the Sentiment Analysis project.

Milestone scope (M3): single-text input -> live sentiment result.
(Batch CSV upload + charts are added in later milestones.)
"""

import streamlit as st
from streamlit.runtime import exists as streamlit_runtime_exists

if not streamlit_runtime_exists():
    raise SystemExit("This is a Streamlit app. Run it with: streamlit run app.py")

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from analyze import analyze_sentiment

st.set_page_config(
    page_title="Feedback Sentiment Analyzer",
    page_icon="💬",
    layout="centered",
)

# --- Header -----------------------------------------------------------
st.title("💬 Feedback Sentiment Analyzer")
st.caption(
    "Paste any customer review or feedback message below to instantly see "
    "whether it reads as Positive, Negative, or Neutral."
)

# --- Input --------------------------------------------------------------
text_input = st.text_area(
    "Customer feedback",
    placeholder="e.g. The delivery was late but the support team fixed it quickly.",
    height=120,
)

analyze_clicked = st.button("Analyze Sentiment", type="primary")

# --- Result ---------------------------------------------------------
LABEL_STYLE = {
    "Positive": ("🟢", "#16A34A"),
    "Negative": ("🔴", "#DC2626"),
    "Neutral":  ("⚪", "#64748B"),
}

if analyze_clicked:
    if not text_input.strip():
        st.warning("Please enter some text first — there's nothing to analyze yet.")
    else:
        result = analyze_sentiment(text_input)
        emoji, color = LABEL_STYLE[result["label"]]

        st.markdown(
            f"### {emoji} Result: "
            f"<span style='color:{color}'>{result['label']}</span>",
            unsafe_allow_html=True,
        )

        # Compound score as an intuitive progress bar from -1 to +1
        normalized = (result["score"] + 1) / 2  # maps -1..1 -> 0..1
        st.progress(normalized, text=f"Confidence score: {result['score']:+.2f} (range -1 to +1)")

        with st.expander("How was this calculated?"):
            st.write(
                "This uses **VADER**, a rule-based sentiment model. It scores each "
                "word's emotional weight, adjusts for negation ('not good') and "
                "intensity ('VERY good!'), then combines them into one **compound "
                "score** from -1 (very negative) to +1 (very positive)."
            )
            st.json(result["scores"])

# --- Batch Analysis (M4) ---------------------------------------------
st.divider()
st.header("📂 Batch Analysis — CSV Upload")
st.caption(
    "Upload a CSV of customer feedback (e.g. a survey export or review dump) "
    "to analyze hundreds of entries at once."
)

if "batch_results" not in st.session_state:
    st.session_state.batch_results = None

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
    except Exception:
        st.error(
            "Couldn't read this file as a CSV. Please make sure it's a valid "
            "comma-separated .csv file and try again."
        )
        raw_df = None

    if raw_df is None:
        pass  # error already shown above
    elif raw_df.empty:
        st.warning("This CSV has no rows to analyze.")
    else:
        text_column = st.selectbox(
            "Which column contains the feedback text?", raw_df.columns
        )

        if st.button("Run Batch Analysis", type="primary"):
            with st.spinner(f"Analyzing {len(raw_df)} rows..."):
                outcomes = raw_df[text_column].astype(str).apply(analyze_sentiment)
                raw_df["Sentiment"] = outcomes.apply(lambda r: r["label"])
                raw_df["Score"] = outcomes.apply(lambda r: round(r["score"], 3))
            st.session_state.batch_results = raw_df
            st.session_state.batch_text_column = text_column

if st.session_state.batch_results is not None:
    results_df = st.session_state.batch_results
    st.success(f"Analyzed {len(results_df)} entries.")

    # Quick KPI summary - business-friendly at-a-glance view
    counts = results_df["Sentiment"].value_counts()
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Positive", int(counts.get("Positive", 0)))
    col2.metric("🔴 Negative", int(counts.get("Negative", 0)))
    col3.metric("⚪ Neutral", int(counts.get("Neutral", 0)))

    st.dataframe(results_df, use_container_width=True)

    csv_bytes = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Results as CSV",
        data=csv_bytes,
        file_name="sentiment_results.csv",
        mime="text/csv",
    )

    # --- Distribution chart (M5) ---------------------------------
    st.subheader("📊 Sentiment Distribution")
    fig = px.pie(
        results_df,
        names="Sentiment",
        color="Sentiment",
        color_discrete_map={
            "Positive": "#16A34A",
            "Negative": "#DC2626",
            "Neutral": "#64748B",
        },
        hole=0.45,
    )
    fig.update_traces(textinfo="label+percent")
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- Word Cloud (M5) ------------------------------------------
    st.subheader("☁️ Word Cloud")
    wc_filter = st.radio(
        "Show words from:",
        ["All feedback", "Positive only", "Negative only"],
        horizontal=True,
    )
    text_column = st.session_state.batch_text_column

    if wc_filter == "Positive only":
        pool = results_df.loc[results_df["Sentiment"] == "Positive", text_column]
    elif wc_filter == "Negative only":
        pool = results_df.loc[results_df["Sentiment"] == "Negative", text_column]
    else:
        pool = results_df[text_column]

    combined_text = " ".join(pool.astype(str))

    if combined_text.strip():
        cloud = WordCloud(
            width=900, height=400, background_color="#FAFAF7", colormap="viridis"
        ).generate(combined_text)
        fig_wc, ax = plt.subplots(figsize=(9, 4))
        ax.imshow(cloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig_wc, use_container_width=True)
    else:
        st.info(f"No '{wc_filter}' feedback found to build a word cloud.")

# --- Footer -----------------------------------------------------------
st.divider()
st.caption("Built with Python, NLTK (VADER) & Streamlit · Pinnacle Labs Internship 2026")
