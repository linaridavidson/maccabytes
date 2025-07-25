# maccabyte_helpers.py
import streamlit as st
from cltk.nlp import NLP
cltk_nlp = NLP(language="grc")
from collections import Counter
from lxml import etree
import re
import heapq

@st.cache_resource
def get_cltk_nlp():
    return NLP(language="grc")

# Initialize CLTK NLP for Ancient Greek
# This function is cached to improve performance
cltk_nlp = get_cltk_nlp()
# Helper function to load text files

# === Text Cleaning and Extraction Functions ===
def clean_greek_biblical_text(text, remove_punctuation=True):
    """Cleans Greek biblical text by removing numbers, punctuation, and extra spaces."""
    pattern = r'^\s*\d+\s+|\(\d+\)|\d+|[·.,;:!?“”‘’\'"()\[\]«»]' if remove_punctuation else r'^\s*\d+\s+|\(\d+\)|\d+'
    text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return re.sub(r'\s+', ' ', text).strip()



def extract_greek_text_from_perseus(xml_path):
    """
    Extracts and cleans Greek text from a Perseus XML file.
    """
    parser = etree.XMLParser(recover=True)
    with open(xml_path, "rb") as f:
        tree = etree.parse(f, parser)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    paragraphs = root.xpath("//tei:body//tei:p", namespaces=ns)
    for p in paragraphs:
        if p.text:
            yield clean_greek_biblical_text(p.text)

# === Text Analysis Functions ===

def analyze_text(text):
    doc = cltk_nlp.analyze(text)
    return doc



def get_features(text, mode="lemma"):
    """
    Extracts features (lemmas or POS tags) from the text using CLTK.
    """
    doc = cltk_nlp.analyze(text)
    if mode == "lemma":
        return [t.lemma for t in doc.tokens if t.lemma]
    return [t.pos for t in doc.tokens if t.pos]

# === Text Comparison Functions ===


def compare_texts(lemmas_a, lemmas_b, top_n=20):
    """Compares two lists of lemmata and returns shared and unique lemmas."""
    counts_a = Counter(lemmas_a)
    counts_b = Counter(lemmas_b)

    shared = set(counts_a.keys()) & set(counts_b.keys())
    shared_counts = heapq.nlargest(
        top_n,
        [{"lemma": lemma, "Text A": counts_a[lemma], "Text B": counts_b[lemma]} for lemma in shared],
        key=lambda x: x["Text A"] + x["Text B"]
    )
 # Find unique lemmas
    unique_to_a = list(set(counts_a.keys()) - shared)
    unique_to_b = list(set(counts_b.keys()) - shared)

    return shared_counts[:top_n], unique_to_a, unique_to_b, counts_a, counts_b