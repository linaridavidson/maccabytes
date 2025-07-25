import streamlit as st
from cltk import NLP
from collections import Counter
import pandas as pd
import os

# Initialize NLP for Ancient Greek
nlp = NLP(language="grc")

# Helper function to load text files
def load_text(filename):
    """Reads the content of a text file and returns it as a string."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# Paths to text files
clean_maccabees_path = r"C:/Users/la18861/maccabytes/1maccabees.txt"
if not os.path.exists(clean_maccabees_path):
    raise FileNotFoundError(f"File not found: {clean_maccabees_path}")
sample_maccabees = load_text(clean_maccabees_path)

# Streamlit UI setup
st.set_page_config(layout="wide")
st.title("Maccabytes - Greek Lemma Comparison Tool - prototype")
st.caption(
    """✨ *Powered by the Classical Language Toolkit (CLTK).*
    Created by Lindsey A. Davidson (github: linaridavidson), PhD, lecturer in Jewish Studies, University of Bristol, UK. 2025.

    This app compares the most frequent **lemmata** (dictionary headwords) found in two passages 
    of Ancient Greek - specifically 1 Maccabees and any other Greek text. It is good to use short sections of text. Useful for studying authorial style, vocabulary overlap, or genre differences.
    """
)

# Text input columns
col1, col2 = st.columns(2)

with col1:
    st.header("Text A")
    if st.button("📜 Load 1 Maccabees"):
        st.session_state.text_a = sample_maccabees
    text_a = st.text_area("Enter first Greek text", height=200, key="text_a")

with col2:
    st.header("Text B")
    text_b = st.text_area("Enter second Greek text", height=200, key="text_b", value="")

# Function to process and analyze text
def process_text(text):
    """Tokenizes and lemmatizes Greek text using CLTK."""
    doc = nlp.analyze(text)
    return [t.lemma for t in doc.tokens if t.lemma and t.lemma.isalpha()]

# Function to compare texts
def compare_texts(lemmas_a, lemmas_b):
    """Compares two lists of lemmata and returns shared and unique lemmas."""
    counts_a = Counter(lemmas_a)
    counts_b = Counter(lemmas_b)

    shared = set(counts_a.keys()) & set(counts_b.keys())
    shared_counts = [
        {"lemma": lemma, "Text A": counts_a[lemma], "Text B": counts_b[lemma]}
        for lemma in shared
    ]
    shared_counts.sort(key=lambda x: x["Text A"] + x["Text B"], reverse=True)

    unique_to_a = sorted(set(counts_a.keys()) - shared)
    unique_to_b = sorted(set(counts_b.keys()) - shared)

    return shared_counts, unique_to_a, unique_to_b, counts_a, counts_b

# Perform comparison if both texts are provided
if text_a.strip() and text_b.strip():
    st.write("Processing texts...")

    # Process texts
    lemmas_a = process_text(text_a)
    lemmas_b = process_text(text_b)

    # Compare texts
    shared_counts, unique_to_a, unique_to_b, counts_a, counts_b = compare_texts(lemmas_a, lemmas_b)

    # Display results
    st.subheader("📊 Top Shared Lemmas")
    df_shared = pd.DataFrame(shared_counts[:20])
    st.dataframe(df_shared)

    st.bar_chart(df_shared.set_index("lemma"))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Text A: Top Lemmas")
        for lemma, count in counts_a.most_common(10):
            st.write(f"{lemma} — {count}×")

    with col2:
        st.subheader("Text B: Top Lemmas")
        for lemma, count in counts_b.most_common(10):
            st.write(f"{lemma} — {count}×")

    st.subheader("Unique Lemmas")
    st.write("**Unique to Text A:**", ", ".join(unique_to_a[:10]))
    st.write("**Unique to Text B:**", ", ".join(unique_to_b[:10]))