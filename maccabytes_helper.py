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

