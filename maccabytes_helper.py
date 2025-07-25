# maccabyte_helpers.py

from cltk import NLP
from collections import Counter
from lxml import etree
import re


nlp = NLP(language="grc")

def clean_greek_biblical_text(text, remove_punctuation=True):
    """Cleans Greek biblical text by removing numbers, punctuation, and extra spaces."""
    text = re.sub(r'^\s*\d+\s+|\(\d+\)|\d+', '', text, flags=re.MULTILINE)
    if remove_punctuation:
        text = re.sub(r'[·.,;:!?“”‘’\'"()\[\]«»]', '', text)
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
    raw_text = "\n".join([p.text for p in paragraphs if p.text])
    # Clean the extracted text before returning
    return clean_greek_biblical_text(raw_text)
# filepath: c:\Users\la18861\maccabytes\maccabytes_helper.py


def analyze_text(text):
    """
    Tokenizes and lemmatizes Greek text using CLTK.
    Returns a list of dictionaries with word, lemma, POS, and morphological features.
    """
    doc = nlp.analyze(text)
    tokens_data = [
        {"Word": t.string, "Lemma": t.lemma, "POS": t.pos, "Morph": t.features}
        for t in doc.tokens if t.string.strip()
    ]
    return tokens_data

def get_features(text, mode="lemma"):
    """
    Extracts features (lemmas or POS tags) from the text using CLTK.
    """
    doc = nlp.analyze(text)
    if mode == "lemma":
        return [t.lemma for t in doc.tokens if t.lemma]
    return [t.pos for t in doc.tokens if t.pos]

#def compare_texts(text1, text2, mode="lemma", top_n=10):
#    """
 #   Compares two texts and returns shared and unique features (lemmas or POS tags).
  #  """
  #  # Extract features
  #  features1 = get_features(text1, mode)
  #  features2 = get_features(text2, mode)

    # Count frequencies
  #  freq1 = Counter(features1)
  #  freq2 = Counter(features2)

    # Find shared and unique items
  #  shared_items = set(freq1.keys()) & set(freq2.keys())
  #  shared_counts = [
  #      {"Item": item, "Text 1": freq1[item], "Text 2": freq2[item]}
  #      for item in shared_items
  #  ]
 #   shared_counts.sort(key=lambda x: x["Text 1"] + x["Text 2"], reverse=True)

 #   return shared_counts[:top_n], freq1, freq2

def compare_texts(lemmas_a, lemmas_b, top_n=20):
    """Compares two lists of lemmata and returns shared and unique lemmas."""
    counts_a = Counter(lemmas_a)
    counts_b = Counter(lemmas_b)

    shared = set(counts_a.keys()) & set(counts_b.keys())
    shared_counts = [
        {"lemma": lemma, "Text A": counts_a[lemma], "Text B": counts_b[lemma]}
        for lemma in shared
    ]
    shared_counts.sort(key=lambda x: x["Text A"] + x["Text B"], reverse=True)

    # Find unique lemmas
    unique_to_a = list(set(counts_a.keys()) - set(counts_b.keys()))
    unique_to_b = list(set(counts_b.keys()) - set(counts_a.keys()))

    return shared_counts[:top_n], unique_to_a, unique_to_b, counts_a, counts_b

    print("Shared Lemmas:", shared_counts)
    print("Unique to Text A:", unique_to_a)
    print("Unique to Text B:", unique_to_b)