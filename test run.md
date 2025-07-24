# Structure

# maccabyte_text_analyzer/
# ├── venv/
# ├── main.py
# ├── requirements.txt
# ├── README.md



## REQUIREMENTS
# To run the project, you need to install the required packages.
# You can do this by running the following command in your terminal:
            pip install -r requirements.txt
# This will install all the necessary packages listed in the requirements.txt file. 
# Make sure you have Python and pip installed on your system before running this command.
# If you want to run the project in a virtual environment, you can create one using the following commands:
            python -m venv venv
            source venv/bin/activate  # On Windows use `venv\Scripts\activate`
# After activating the virtual environment, you can install the requirements again:
            pip install -r requirements.txt



## PROJECT MACCABYTES

from cltk import NLP
from rich import print # Pretty printing
import system

# Choose Ancient Greek
nlp = NLP(language="grc")

# Input: either hardcoded or via terminal
if len(sys.argv) > 1:
    text= sys.argv[1]
else:
    text = "Enter Greek text: ")

# Process the text
doc = nlp.analyze(text)
print("\n[bold green]Token Analysis:[/bold green]")
for token in doc.tokens:
    print(f"[cyan]{token.string}[/cyan] POS: {token.pos}, Lemma: {token.lemma}, Morphology: {token.morphology}")
    print("\n[bold green]Dependency Parsing:[/bold green]")
for dep in doc.dependencies:
    print(f"[cyan]{dep.head.string}[/cyan] -> [magenta]{dep.child.string}[/magenta] ({dep.label})")
print("\n[bold green]Named Entities:[/bold green]")
for entity in doc.entities:
    print(f"[yellow]{entity.string}[/yellow] ({entity.label})")
# Save the results to a file
with open("analysis_results.txt", "w") as f:
    f.write("Token Analysis:\n")
    for token in doc.tokens:
        f.write(f"{token.string} POS: {token.pos}, Lemma: {token.lemma}, Morphology: {token.morphology}\n")
    f.write("\nDependency Parsing:\n")
    for dep in doc.dependencies:
        f.write(f"{dep.head.string} -> {dep.child.string} ({dep.label})\n")
    f.write("\nNamed Entities:\n")
    for entity in doc.entities:
        f.write(f"{entity.string} ({entity.label})\n")
print("\n[bold green]Analysis complete! Results saved to analysis_results.txt[/bold green]")
# Run the script
if __name__ == "__main__":  
    import sys
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = input("Enter Greek text: ")
    nlp = NLP(language="grc")
    doc = nlp.analyze(text)
    print("\n[bold green]Token Analysis:[/bold green]")
    for token in doc.tokens:
        print(f"[cyan]{token.string}[/cyan] POS: {token.pos}, Lemma: {token.lemma}, Morphology: {token.morphology}")
    print("\n[bold green]Dependency Parsing:[/bold green]")
    for dep in doc.dependencies:
        print(f"[cyan]{dep.head.string}[/cyan] -> [magenta]{dep.child.string}[/magenta] ({dep.label})")
    print("\n[bold green]Named Entities:[/bold green]")
    for entity in doc.entities:
        print(f"[yellow]{entity.string}[/yellow] ({entity.label})")
    with open("analysis_results.txt", "w") as f:
        f.write("Token Analysis:\n")
        for token in doc.tokens:
            f.write(f"{token.string} POS: {token.pos}, Lemma: {token.lemma}, Morphology: {token.morphology}\n")
        f.write("\nDependency Parsing:\n")
        for dep in doc.dependencies:
            f.write(f"{dep.head.string} -> {dep.child.string} ({dep.label})\n")
        f.write("\nNamed Entities:\n")
        for entity in doc.entities:
            f.write(f"{entity.string} ({entity.label})\n")
    print("\n[bold green]Analysis complete! Results saved to analysis_results.txt[/bold green]")
# To run the script, use the command:
# python main.py "Your Greek text here"
# This will analyze the provided Greek text and save the results to analysis_results.txt.
# Make sure to replace "Your Greek text here" with the actual text you want to analyze.
# You can also run the script without any arguments, and it will prompt you to enter the
# Greek text interactively.
# If you want to analyze a different text, simply change the text variable in the script or
# provide a new text via the command line.

# Note: Ensure that you have the necessary permissions to write to the current directory
# where the script is executed, as it will create or overwrite the analysis_results.txt file.
# This script is designed to analyze Ancient Greek text using the CLTK library.
# It performs token analysis, dependency parsing, and named entity recognition,
# and saves the results to a text file.
# Make sure to have the CLTK library installed and properly configured for Ancient Greek.
# You can find more information about CLTK and its installation at https://cltk.org/.
# This script is a basic example of how to use the CLTK library for text analysis.
# You can extend it further by adding more features or improving the analysis methods.
# For more advanced usage, refer to the CLTK documentation and explore additional functionalities.


Use open('1maccabees.txt', 'r') as file:
    text = file.read()
# This will read the content of the file '1maccabees.txt' and store it in the variable 'text'.
# You can then use this text variable in your analysis or processing functions.
# Example usage:

