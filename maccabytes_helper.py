# maccabyte_helpers.py

from cltk import NLP
from collections import Counter
from lxml import etree
import re

nlp = NLP(language="grc")

def clean_greek_biblical_text(text, remove_punctuation=True):
    text = re.sub(r'^\s*\d+\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\(\d+\)', '', text)
    text = re.sub(r'\d+', '', text)
    if remove_punctuation:
        text = re.sub(r'[·.,;:!?“”‘’\'"()\[\]«»]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_greek_text_from_perseus(xml_path):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(xml_path, parser)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    paragraphs = root.xpath("//tei:body//tei:p", namespaces=ns)
    return "\n".join([p.text for p in paragraphs if p.text])

def analyze_text(text):
    doc = nlp.analyze(text)
    tokens_data = [
        {"Word": t.string, "Lemma": t.lemma, "POS": t.pos, "Morph": t.features}
        for t in doc.tokens if t.string.strip()
    ]
    return tokens_data

def compare_texts(text1, text2, mode="lemma", top_n=10):
    def get_features(text):
        doc = nlp.analyze(text)
        if mode == "lemma":
            return [t.lemma for t in doc.tokens if t.lemma]
        else:
            return [t.pos for t in doc.tokens if t.pos]

    freq1 = Counter(get_features(text1))
    freq2 = Counter(get_features(text2))
    all_items = Counter(freq1 + freq2).most_common(top_n)

    return [
        {"Item": item, "Text 1": freq1.get(item, 0), "Text 2": freq2.get(item, 0)}
        for item, _ in all_items
    ]

# streamlit_app.py

import streamlit as st
from maccabyte_helpers import (
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
