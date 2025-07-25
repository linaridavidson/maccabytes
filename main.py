# Structure

# maccabyte_text_analyzer/
# ├── venv/
# ├── main.py
# │   app.py
# ├── maccabytes_helper.py
# ├── cltk_data/
# │   requirements.txt
# ├── perseus/
#       ├── polybius1.txt # a clean Polybius text from Perseus https://vocab.perseus.org/editions/
# ├── 1maccabees.txt # a clean 1 Maccabees text from https://www.ellopos.net/elpenor/greek-texts/septuagint/chapter.asp?book=21
# ├── README.md


# ├── requirements.txt
# To run the project, you need to install the required packages.
# You can do this by running the following command in your terminal:
# pip install -r requirements.txt
# This will install all the necessary packages listed in the requirements.txt file. 
# Make sure you have Python and pip installed on your system before running this command.
# If you want to run the project in a virtual environment, you can create one using the following commands:
          #  python -m venv venv
          #  source venv/bin/activate  # On Windows use `.\venv\Scripts\Activate.ps1`
# After activating the virtual environment, you can install the requirements again:
          #  pip install -r requirements.txt
# lxml
    # pip install lxml
# rich
    # pip install rich
# cltk
    # pip install cltk
# streamlit
    # pip install streamlit



## PROJECT MACCABYTES

#Make sure you have Python 3.11 installed on your system. CLTK needs Python 3.11 to run properly.
# You can download it from the official Python website: https://www.python.org/downloads/
# You can check your Python version by running: 
# $ python --version
# If you have Python 3.11 installed, you can run the project using the following command:
# To run 3.11, type this into your terminal:
#     $ py -3.11 --version


import argparse
from cltk import NLP
from collections import Counter
from rich import print
from rich.table import Table
from lxml import etree
import re
import os

# Initialize CLTK NLP for Ancient Greek
nlp = NLP(language="grc")

def clean_greek_biblical_text(raw_text, remove_punctuation=True):
    """
    Cleans Greek biblical text by removing numbers, punctuation, and extra spaces.
    """
    cleaned = re.sub(r'^\s*\d+\s+|\(\d+\)|\d+', '', raw_text, flags=re.MULTILINE)
    if remove_punctuation:
        cleaned = re.sub(r'[·.,;:!?“”‘’\'"()\[\]«»]', '', cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()

def extract_greek_text_from_perseus(xml_path):
    """
    Extracts Greek text from a Perseus XML file.
    """
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(xml_path, parser)
    root = tree.getroot()
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
    paragraphs = root.xpath("//tei:body//tei:p", namespaces=namespaces)
    return "\n".join([p.text for p in paragraphs if p.text])

def analyze_text(text, save_to_file=False):
    """
    Analyzes a Greek text for tokens, dependencies, and entities.
    """
    doc = nlp.analyze(text)
    print("\n[bold green]Token Analysis:[/bold green]")
    for token in doc.tokens:
        print(f"[cyan]{token.string}[/cyan] POS: {token.pos}, Lemma: {token.lemma}, Morph: {token.features}")
    if save_to_file:
        with open("analysis_results.txt", "w", encoding="utf-8") as f:
            for token in doc.tokens:
                f.write(f"{token.string} POS: {token.pos}, Lemma: {token.lemma}, Morph: {token.features}\n")

def extract_feature_counts(text, mode="lemma"):
    """
    Extracts specific features (lemmas or POS tags) from a text using CLTK.
    
    Args:
        text (str): The input text to analyze.
        mode (str): The feature to extract. Options are "lemma" or "pos".
    
    Returns:
        list: A list of extracted features (lemmas or POS tags).
    """
    doc = nlp.analyze(text)
    if mode == "lemma":
        return [t.lemma for t in doc.tokens if t.lemma and t.lemma.isalpha()]
    elif mode == "pos":
        return [t.pos for t in doc.tokens if t.pos]
    else:
        raise ValueError("Invalid mode. Use 'lemma' or 'pos'.")

def compare_texts(text1, text2, mode="lemma", top_n=10):
    """
    Compares two texts by lemma or POS and prints a frequency table.
    """
    freq1 = Counter(extract_feature_counts(text1, mode))
    freq2 = Counter(extract_feature_counts(text2, mode))
    combined = Counter()
    combined.update(freq1)
    combined.update(freq2)
    table = Table(title=f"Top {top_n} {mode.upper()} Frequencies Comparison")
    table.add_column(f"{mode.capitalize()}")
    table.add_column("Text 1", justify="right")
    table.add_column("Text 2", justify="right")
    for item, _ in combined.most_common(top_n):
        table.add_row(item, str(freq1.get(item, 0)), str(freq2.get(item, 0)))
    print(table)

def read_text(source):
    """
    Reads text from a .txt or .xml file.
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")
    if source.endswith(".txt"):
        with open(source, "r", encoding="utf-8") as f:
            return f.read()
    elif source.endswith(".xml"):
        return extract_greek_text_from_perseus(source)
    else:
        raise ValueError("Unsupported file type. Only .txt and .xml are supported.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze or compare Ancient Greek texts using CLTK")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a single text")
    analyze_parser.add_argument("text", help="Text or path to .txt file to analyze")
    compare_parser = subparsers.add_parser("compare", help="Compare two texts by lemma or POS")
    compare_parser.add_argument("text1", help="First text or .txt file")
    compare_parser.add_argument("text2", help="Second text or .txt file")
    compare_parser.add_argument("--mode", choices=["lemma", "pos"], default="lemma", help="Feature to compare")
    compare_parser.add_argument("--top", type=int, default=10, help="How many top items to compare")
    args = parser.parse_args()
    commands = {
        "analyze": lambda args: analyze_text(read_text(args.text)),
        "compare": lambda args: compare_texts(
            read_text(args.text1), read_text(args.text2), mode=args.mode, top_n=args.top
        ),
    }
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

# This code is a simple command-line interface for analyzing and comparing Ancient Greek texts using the CLTK library.
# It allows users to analyze a single text for token analysis, dependency parsing, and named entity