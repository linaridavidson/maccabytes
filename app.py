import streamlit as st
from cltk import NLP
from collections import Counter
import pandas as pd

from maccabytes_helper import extract_greek_text_from_perseus

import os
print("Current working directory:", os.getcwd())

import os

xml_path = r"polybius.xml"
if not os.path.exists(xml_path):
    raise FileNotFoundError(f"File not found: {xml_path}")
sample_polybius = extract_greek_text_from_perseus(xml_path)

sample_polybius = extract_greek_text_from_perseus(
    r"polybius.xml"
)
# Read sample texts from local files
def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

sample_maccabees = load_text("1maccabees.txt")
sample_polybius = load_text("polybius.xml")



# Setup
st.set_page_config(layout="wide")
nlp = NLP(language="grc")

st.title("Maccabytes - Greek Lemma Comparator")
st.caption(

    """✨ *Powered by the Classical Language Toolkit (CLTK).
    
    This app compares the most frequent **lemmata** (dictionary headwords) found in two passages 
    of Ancient Greek - specifically 1 Maccabees and Polybius. Useful for studying authorial style, vocabulary overlap, or genre differences.

    Paste or type Greek text correctly (1 Maccabees and Polybius) in both fields below to begin.
    
    Compare the top lemmata of two pieces of Ancient Greek text - Maccabees and Polybius - side by side.
    """)


col1, col2 = st.columns(2)

with col1:
    st.header("Text A")
    if st.button("📜 Load 1 Maccabees"):
        st.session_state.text_a = sample_maccabees
    text_a = st.text_area("Enter first Greek text", height=200, key="text_a")

with col2:
    st.header("Text B")
    if st.button("🏛️ Load Polybius"):
        st.session_state.text_b = sample_polybius
    text_b = st.text_area("Enter second Greek text", height=200, key="text_b")


if text_a.strip() and text_b.strip():
    doc_a = nlp.analyze(text_a)
    doc_b = nlp.analyze(text_b)

    lemmas_a = [t.lemma for t in doc_a.tokens if t.lemma and t.lemma.isalpha()]
    lemmas_b = [t.lemma for t in doc_b.tokens if t.lemma and t.lemma.isalpha()]

    counts_a = Counter(lemmas_a)
    counts_b = Counter(lemmas_b)

    # Shared lemmata
    shared = set(counts_a.keys()) & set(counts_b.keys())
    shared_counts = [
        {"lemma": lemma, "Text A": counts_a[lemma], "Text B": counts_b[lemma]}
        for lemma in shared
    ]
    shared_counts.sort(key=lambda x: x["Text A"] + x["Text B"], reverse=True)

    st.subheader("📊 Top Shared Lemmas")
    df_shared = pd.DataFrame(shared_counts[:20])
    st.dataframe(df_shared)

    st.bar_chart(df_shared.set_index("lemma"))

    with col1:
        st.subheader("Text A: Top Lemmas")
        for lemma, count in counts_a.most_common(10):
            st.write(f"{lemma} — {count}×")

    with col2:
        st.subheader("Text B: Top Lemmas")
        for lemma, count in counts_b.most_common(10):
            st.write(f"{lemma} — {count}×")
