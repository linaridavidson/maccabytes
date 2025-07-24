


MACCABYTES PROTOTYPE (c)2025
Lindsey A. Davidson 
github = linaridavidson


...and now for something completely different...

This is a prototype, work in progress.
Maccabytes is a NLP tool using CLTK and running Python 3.11

To run a clean setup, open PowerShall (not as Admin)
move to your project folder ~maccabytes

```bash
cd C:\Users\la18861\maccabytes

If that folder doesn't exist yet, you can create it:
```bash
mkdir C:\Users\~\maccabytes
cd C:\Users\~\maccabytes

Create a virtual Python 3.11 env so that CLTK will run properly
```bash
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

Your prompt in powershell should now start with (venv)

Install all required packages
```bash
pip install --upgrade pip
pip install cltk streamlit lxml rich




Run the app (app.py)
Make sure you're still in your environment and project folder.
In powershell, run:

cd C:\Users\la18861\maccabytes
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
streamlit run app.py

You should see output like this:
Local URL: http://localhost:8501

Click or copy that link into your browser!


You can have the text boxes pre-filled with the 1maccabees.txt and a clean version of Polybius (tlg0001):


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


...
Or you can have blank boxes and insert your own texts to compare. If you want to change to blank boxes, go to app.py, and for the text input put:

#col1, col2 = st.columns(2)

##Boxes that are empty
#with col1:
#    st.header("Text A - Maccabees")
#    text_a = st.text_area("Enter Maccabees text", height=200)

#with col2:
#    st.header("Text B - Polybius")
#    text_b = st.text_area("Enter Polybius text", height=200)




‎𐤀 CLTK version '1.5.0'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/

Pipeline for language 'Ancient Greek' (ISO: 'grc'): `GreekNormalizeProcess`, `GreekSpacyProcess`, `GreekEmbeddingsProcess`, `StopsProcess`.

⸖ ``GreekSpacyProcess`` using OdyCy model by Center for Humanities Computing Aarhus from https://huggingface.co/chcaa . Please cite: https://aclanthology.org/2023.latechclfl-1.14
⸖ ``LatinEmbeddingsProcess`` using word2vec model by University of Oslo from http://vectors.nlpl.eu/ . Please cite: https://aclanthology.org/W17-0237/