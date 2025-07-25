


MACCABYTES PROTOTYPE (c)2025
Lindsey A. Davidson 
github = linaridavidson

.

...and now for something completely different...

*This is a prototype, work in progress.*
*Maccabytes* is a NLP tool using CLTK and running Python 3.11 and using a Streamlit app interface.

✨ *Powered by the Classical Language Toolkit (CLTK).*
Created by Lindsey A. Davidson (github: linaridavidson), PhD, lecturer in Jewish Studies, University of Bristol, UK. 2025.

This app compares the most frequent lemmata (dictionary headwords) found in two passages of Ancient Greek - specifically meant for 1 Maccabees and another Greek text - in short sections. 
    
 In later versions it will have more text samples from the drop down menu. 
    
For the app to be able to run, it is good to use short sections of text. 
    
This tool is useful for studying authorial style, vocabulary overlap, or genre differences.
The README guidance below for installing this project is beginner-friendly.

.

REQUIREMENTS

 To run the project, you need to install the required packages.
 You can do this by running the following command in your terminal:
        `pip install -r requirements.txt`
 This will install all the necessary packages listed in the requirements.txt file. 
Make sure you have Python and pip installed on your system before running this command.
If you want to run the project in a virtual environment, you can create one using the following commands:
            python -m venv venv
            source venv/bin/activate  # On Windows use  `\venv\Scripts\Activate`
After activating the virtual environment, you can install the requirements again:
            `pip install -r requirements.txt`
lxml
    `pip install lxml`
rich
    `pip install rich`
cltk
    `pip install cltk`
streamlit
    `pip install streamlit`



Virtual Python 3.11 environment to use CLTK

Make sure you have Python 3.11 installed on your system. CLTK needs Python 3.11 to run properly, not the latest Python.
 You can download it from the official Python website: https://www.python.org/downloads/
 You can check your Python version by running: 
 ```bash
 $ python --version
 ```
 If you have Python 3.11 installed, you can run the project using the following command:
 To run 3.11, type this into your terminal:
 ```bash
     $ py -3.11 --version
```

First step: fork the project from GitHub and run Terminal to launch the app interface in a local host url:

```bash
cd C:\Users\la18861\maccabytes
```
If that folder doesn't exist yet, you can create it:

```bash
mkdir C:\Users\~\maccabytes
cd C:\Users\~\maccabytes
```
Create a virtual Python 3.11 env so that CLTK will run properly

```bash
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```
Your prompt in powershell should now start with (venv)

Install all required packages
```bash
pip install --upgrade pip
pip install cltk streamlit lxml rich
```



MAKE THE PROJECT AND RUN THE APP TO ANALYZE TWO GREEK TEXTS:

In PowerShell (don't run as Admin), or your preferred Windows terminal, run:
```bash
cd C:\Users\la18861\maccabytes
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
streamlit run app.py
```
You should see output like this:

     Local URL: http://localhost:8501

Click or copy that link into your browser!


With Maccabytes, you can have the text boxes pre-filled with the 1maccabees.txt and a clean version of Polybius (tlg0001) by updating the app.py code:

```bash
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
```

...
Or you can have blank boxes and insert your own texts to compare. If you want to change to blank boxes, go to app.py, and for the text input put:
```bash
#col1, col2 = st.columns(2)

##Boxes that are empty
#with col1:
#    st.header("Text A - Maccabees")
#    text_a = st.text_area("Enter Maccabees text", height=200)

#with col2:
#    st.header("Text B - Polybius")
#    text_b = st.text_area("Enter Polybius text", height=200)
```


Thank you to the creators of CLTK!

‎𐤀 CLTK version '1.5.0'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/

Pipeline for language 'Ancient Greek' (ISO: 'grc'): `GreekNormalizeProcess`, `GreekSpacyProcess`, `GreekEmbeddingsProcess`, `StopsProcess`.

⸖ ``GreekSpacyProcess`` using OdyCy model by Center for Humanities Computing Aarhus from https://huggingface.co/chcaa . Please cite: https://aclanthology.org/2023.latechclfl-1.14
⸖ ``LatinEmbeddingsProcess`` using word2vec model by University of Oslo from http://vectors.nlpl.eu/ . Please cite: https://aclanthology.org/W17-0237/