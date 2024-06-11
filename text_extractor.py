import fitz
def pdf_to_text(file):
    """
    Reads in a pdf file and converts to text.  Creates a new text file Dexcomm10k.txt stored in the same directory
    """
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_after_phrase(text_content, beginning_phrase, end_phrase):
    """
    Read in a text file and save contents of file in a string based on 
    a beginning and endphrase
    """
    found = False
    lines = text_content.split('\n')
    extracted_text = ''
    for line in lines:
        if beginning_phrase in line:
            found = True
        if found:
            extracted_text += f" {line}"
        if end_phrase in line:
            break
    return extracted_text

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    extraction_mode = False
    extracted_text = ""
    start_keywords = ["ITEM 1 - BUSINESS", "ITEM 1A - RISK FACTORS", "ITEM 7 - MANAGEMENT'S DISCUSSION AND ANALYSIS", "ITEM 8 - FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA"]
    end_keywords = ["ITEM 1B", "ITEM 2 -", "ITEM 9 -", "ITEM 9A -"]

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        for start_keyword in start_keywords:
            if start_keyword in text.upper():
                extraction_mode = True
                start_keywords.remove(start_keyword)  
                break  
        
        if extraction_mode:
            extracted_text += text + "\n\n"

        for end_keyword in end_keywords:
            if end_keyword in text.upper() and extraction_mode:
                extraction_mode = False
                end_keywords.remove(end_keyword)  
                break  
    return extracted_text