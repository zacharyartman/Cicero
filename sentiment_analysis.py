#Import text file
from spacy import displacy
import spacy
nlp = spacy.load("output/model-last")

def render_text(financial_text):
    """
    financial text @string String of financial text excerpt from a 10k
    html @return Returns an html string containing markup.  May need to 
    transition to returning to json format though and utilizing javascript.

    Creates an spacy object known as docx and then uses displacy to render 
    this object into labeled annotated text which can be displayed.
    """
    colors = {'CHEMICAL': "red", 
              'CHEMICALS': "red", "DISEASE": "green", "LAW": "blue", 
              "MEDICAL DEVICE TECHNOLOGY": "purple"}
    options = {"ents": ['CHEMICAL', 'CHEMICALS', 'DISEASE', 'LAW', 'MEDICAL DEVICE TECHNOLOGY'], "colors": colors}
    docx = nlp(financial_text)
    html = displacy.render(docx, style = 'ent', options=options)
    return html
