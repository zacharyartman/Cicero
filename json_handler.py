import json
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

def reformat_json(old_filename, new_filename):
    """
    Indents a json file so its easier for a user to read.
    """
    with open(old_filename, 'r') as file:
        data = json.load(file)
    with open(new_filename, 'w') as file:
        json.dump(data, file, indent=4) #Dumps old data into new json file with indentations.

def create_spacy_file(file_path):
    """
    Iterates through a json file and appends training data stored in spans to doc.ents
    """
    nlp = spacy.load("en_core_web_sm") # load other spacy model
    db = DocBin() # create a DocBin object
    with open(file_path, "r") as file:
        data = json.load(file)
    #tqdm library responsible for loading bar when file is running.
    for text, annot in tqdm(data["annotations"]): 
        doc = nlp.make_doc(text) # create doc object from text
        ents = []
        for start, end, label in annot["entities"]: 
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents # label the text with the ents
        db.add(doc)
    db.to_disk("./train.spacy") # save the docbin object

if __name__ == "__main__":
    create_spacy_file("annotations_two.json")