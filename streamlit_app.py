
# streamlit_app.py

import streamlit as st
from maccabytes_helper import (
    clean_greek_biblical_text,
    extract_greek_text_from_perseus,
    analyze_text,
    compare_texts,
)

st.set_page_config(page_title="Maccabyte", layout="wide")
st.title("📚 Maccabyte – Ancient Greek Text Analyzer")

option = st.sidebar.selectbox("Choose mode", ["Analyze one text", "Compare two texts"])

def read_text_input(label):
    method = st.radio(f"{label}: Choose Input Method", ["Paste text", "Upload .txt", "Upload Perseus XML"])
    if method == "Paste text":
        return st.text_area(f"{label}: Paste Greek text", height=200)
    elif method == "Upload .txt":
        file = st.file_uploader(f"{label}: Upload .txt file", type="txt")
        if file:
            return clean_greek_biblical_text(file.read().decode("utf-8"))
    elif method == "Upload Perseus XML":
        file = st.file_uploader(f"{label}: Upload Perseus XML file", type="xml")
        if file:
            return extract_greek_text_from_perseus(file)

# Single analysis
if option == "Analyze one text":
    text = read_text_input("Text")
    if text and st.button("Run Analysis"):
        results = analyze_text(text)
        st.subheader("Token-Level Analysis")
        st.dataframe(results)

# Comparison
else:
    col1, col2 = st.columns(2)
    with col1:
        text1 = read_text_input("Text 1")
    with col2:
        text2 = read_text_input("Text 2")

    mode = st.radio("Compare by:", ["lemma", "pos"])
    top_n = st.slider("Top N items to compare", 5, 50, 15)

    if text1 and text2 and st.button("Compare Texts"):
        comp = compare_texts(text1, text2, mode=mode, top_n=top_n)
        st.subheader("Frequency Comparison")
        st.dataframe(comp)
