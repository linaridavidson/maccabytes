# Structure

# maccabyte_text_analyzer/
# ├── venv/
# ├── main.py
# │   compare.py
# ├── requirements.txt
# ├── perseus/
#       ├── tlg0551/tlg001/tlg0551.tlg001.1st1K-grc1.xml # Polybius
# ├── 1maccabees.txt
# ├── README.md



## REQUIREMENTS.txt
# To run the project, you need to install the required packages.
# You can do this by running the following command in your terminal:
# pip install -r requirements.txt
# This will install all the necessary packages listed in the requirements.txt file. 
# Make sure you have Python and pip installed on your system before running this command.
# If you want to run the project in a virtual environment, you can create one using the following commands:
          #  python -m venv venv
          #  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
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
#           $ py -3.11 --version


import argparse
from cltk import NLP
from collections import Counter
from rich import print
from rich.table import Table

from cltk import text

# Initialize CLTK NLP for Ancient Greek
nlp = NLP(language="grc")

import re

def clean_greek_biblical_text(raw_text, remove_punctuation=True):
    """
    Clean text copied from sources like Elpenor or LXX PDFs.
    Removes verse numbers, extra spaces, and optionally punctuation.
    """
    # Remove verse numbers at line beginnings (e.g. "1 Τότε...") 
    cleaned = re.sub(r'^\s*\d+\s+', '', raw_text, flags=re.MULTILINE)

    # Remove leftover numbers in parentheses (e.g., "(1)")
    cleaned = re.sub(r'\(\d+\)', '', cleaned)

    # Remove all other stray digits (if they snuck in)
    cleaned = re.sub(r'\d+', '', cleaned)
    return clean_greek_biblical_text(text, remove_punctuation=False)

    if remove_punctuation:
        # Remove Greek/English punctuation
        cleaned = re.sub(r'[·.,;:!?“”‘’\'"()\[\]«»]', '', cleaned)

    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned

def analyze_text(text):
    doc = nlp.analyze(text)

    print("\n[bold green]Token Analysis:[/bold green]")
    for token in doc.tokens:
        print(f"[cyan]{token.string}[/cyan] POS: {token.pos}, Lemma: {token.lemma}, Morph: {token.features}")

    print("\n[bold green]Dependency Parsing:[/bold green]")
    for dep in doc.dependencies:
        print(f"[cyan]{dep.head.string}[/cyan] → [magenta]{dep.child.string}[/magenta] ({dep.label})")

    print("\n[bold green]Named Entities:[/bold green]")
    for entity in doc.entities:
        print(f"[yellow]{entity.string}[/yellow] ({entity.label})")

    with open("analysis_results.txt", "w", encoding="utf-8") as f:
        f.write("Token Analysis:\n")
        for token in doc.tokens:
            f.write(f"{token.string} POS: {token.pos}, Lemma: {token.lemma}, Morph: {token.features}\n")
        f.write("\nDependency Parsing:\n")
        for dep in doc.dependencies:
            f.write(f"{dep.head.string} -> {dep.child.string} ({dep.label})\n")
        f.write("\nNamed Entities:\n")
        for entity in doc.entities:
            f.write(f"{entity.string} ({entity.label})\n")

    print("\n[bold green]Analysis complete! Results saved to analysis_results.txt[/bold green]")


def extract_feature_counts(text, mode="lemma"):
    doc = nlp.analyze(text)
    if mode == "lemma":
        return [t.lemma for t in doc.tokens if t.lemma]
    elif mode == "pos":
        return [t.pos for t in doc.tokens if t.pos]
    else:
        raise ValueError("Mode must be 'lemma' or 'pos'")


def compare_texts(text1, text2, mode="lemma", top_n=10):
    freq1 = Counter(extract_feature_counts(text1, mode))
    freq2 = Counter(extract_feature_counts(text2, mode))

    combined = Counter(freq1 + freq2)
    top_items = combined.most_common(top_n)

    table = Table(title=f"Top {top_n} {mode.upper()} Frequencies Comparison")
    table.add_column(f"{mode.capitalize()}")
    table.add_column("Text 1", justify="right")
    table.add_column("Text 2", justify="right")

    for item, _ in top_items:
        table.add_row(item, str(freq1.get(item, 0)), str(freq2.get(item, 0)))

    print(table)
def read_text(source):
    if source.endswith(".txt"):
        with open(source, "r", encoding="utf-8") as f:
            return f.read()
    elif source.endswith(".xml"):
        return extract_greek_text_from_perseus(source)
    else:
        return source



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze or compare Ancient Greek texts using CLTK")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a single text")
    analyze_parser.add_argument("text", help="Text or path to .txt file to analyze")

    # Subcommand: compare
    compare_parser = subparsers.add_parser("compare", help="Compare two texts by lemma or POS")
    compare_parser.add_argument("text1", help="First text or .txt file")
    compare_parser.add_argument("text2", help="Second text or .txt file")
    compare_parser.add_argument("--mode", choices=["lemma", "pos"], default="lemma", help="Feature to compare")
    compare_parser.add_argument("--top", type=int, default=10, help="How many top items to compare")

    args = parser.parse_args()

    if args.command == "analyze":
        text = read_text(args.text)
        analyze_text(text)
    
    elif args.command == "compare":
        text1 = read_text(args.text1)
        text2 = read_text(args.text2)
        compare_texts(text1, text2, mode=args.mode, top_n=args.top)

    else:
        parser.print_help()


from lxml import etree
import os

def extract_greek_text_from_perseus(xml_path):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(xml_path, parser)
    root = tree.getroot()

    # TEI: text > body > div > p
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
    paragraphs = root.xpath("//tei:body//tei:p", namespaces=namespaces)

    greek_text = "\n".join([p.text for p in paragraphs if p.text])
    return greek_text
       
# This code is a simple command-line interface for analyzing and comparing Ancient Greek texts using the CLTK library.
# It allows users to analyze a single text for token analysis, dependency parsing, and named entity