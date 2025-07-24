import streamlit as st
from cltk import NLP

# Set up CLTK for Ancient Greek
nlp = NLP(language="grc")

st.title("Ancient Greek Analyzer")

user_text = st.text_area("Enter Ancient Greek text:")

if user_text:
    doc = nlp.analyze(user_text)
    st.subheader("Tokens:")
    st.write([t.string for t in doc.tokens])
    
    st.subheader("Lemmas:")
    st.write([t.lemma for t in doc.tokens if t.lemma])

    st.subheader("Part-of-speech:")
    st.write([t.pos for t in doc.tokens if t.pos])
