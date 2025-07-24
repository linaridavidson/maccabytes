import streamlit as st
from cltk import NLP
from collections import Counter
import pandas as pd
import os

print("Current working directory:", os.getcwd())

def load_text(filename):
    """Reads the content of a text file and returns it as a string."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

clean_polybius_path = r"C:/Users/la18861/maccabytes/polybius1.txt"
if not os.path.exists(clean_polybius_path):
    raise FileNotFoundError(f"File not found: {clean_polybius_path}")
sample_polybius = load_text(clean_polybius_path)

clean_maccabees_path = r"C:/Users/la18861/maccabytes/1maccabees.txt"
if not os.path.exists(clean_maccabees_path):
    raise FileNotFoundError(f"File not found: {clean_maccabees_path}")
sample_maccabees = load_text(clean_maccabees_path)

from maccabytes_helper import extract_greek_text_from_perseus


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
# Create a button for the comparison
if st.button("Compare Texts and Show Results"):
    # This block will execute ONLY when the button is clicked

    st.write("Performing lemma comparison... Please wait.") # Optional: show a loading message

    try:
        # 1. Your CLTK-based Lemma Extraction and Comparison Logic
        #    This is where you'd call your functions that use CLTK to:
        #    a. Tokenize text_a and text_b
        #    b. Lemmatize the tokens
        #    c. Compare the resulting lemmas (e.g., find common ones, unique ones, frequencies)

        # Placeholder for your actual logic:
        # Let's simulate some results for demonstration
        # In a real scenario, this 'lemmatized_a' and 'lemmatized_b' would come from CLTK
        # For simplicity, I'll just split by spaces here, but you'd use CLTK tokenization/lemmatization
        words_a = text_a.lower().split()
        words_b = text_b.lower().split()

        # Dummy lemmatization (replace with actual CLTK lemmatizer)
        lemmas_a = [word.replace('.', '').replace(',', '') for word in words_a] # Simplified
        lemmas_b = [word.replace('.', '').replace(',', '') for word in words_b] # Simplified

        # Calculate common and unique lemmas (example logic)
        set_lemmas_a = set(lemmas_a)
        set_lemmas_b = set(lemmas_b)

        common_lemmas = sorted(list(set_lemmas_a.intersection(set_lemmas_b)))
        unique_to_a = sorted(list(set_lemmas_a.difference(set_lemmas_b)))
        unique_to_b = sorted(list(set_lemmas_b.difference(set_lemmas_a)))

        # 2. Display the Results
        st.header("Comparison Results")

        if common_lemmas:
            st.subheader("Common Lemmas:")
            st.write(", ".join(common_lemmas))
        else:
            st.info("No common lemmas found between the two texts.")

        if unique_to_a:
            st.subheader("Lemmas Unique to Text A:")
            st.write(", ".join(unique_to_a))

        if unique_to_b:
            st.subheader("Lemmas Unique to Text B:")
            st.write(", ".join(unique_to_b))

        # You might also want to show lemma frequencies, a comparative table, etc.
        # Example: showing top 10 lemmas in each text
        from collections import Counter
        freq_a = Counter(lemmas_a)
        freq_b = Counter(lemmas_b)

        st.subheader("Top Lemmas in Text A:")
        for lemma, count in freq_a.most_common(5): # Adjust number as needed
            st.write(f"- {lemma}: {count}")

        st.subheader("Top Lemmas in Text B:")
        for lemma, count in freq_b.most_common(5): # Adjust number as needed
            st.write(f"- {lemma}: {count}")


    except Exception as e:
        st.error(f"An error occurred during comparison: {e}")
        st.info("Please ensure your input texts are valid Greek and your CLTK setup is correct.")

# --- End of Results Button and Display Logic ---
