import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
import datetime
import pdfkit

import sentiment_analysis, text_extractor, api
app = Flask(__name__)
CORS(app)

if not os.path.exists("logs"):
    # Create the directory
    os.makedirs("logs")
log_filename = datetime.datetime.now().strftime("cicero_log_%Y-%m-%d_%H-%M-%S.log")
logging.basicConfig(filename=f"./logs/{log_filename}", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

global_prompt = None
global_displacy_html = None

@app.route("/")
def home():
    """
    Responsible for home page of website.  Uses render_templates to access index.html which n
    needs to be stored in the templates folder.  
    """
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handler which is triggered instantaneously after pdf document is uploaded.  
    @return extracted_phrase (string) - represents currently all the footnotes related
    to cash flows.  Uses regular expressions to obtain string of all footnotes based on 
    a target and end phrase.
    """
    logging.info("Upload file clicked")
    file = request.files['file']
    model_type = request.form.get('model_type')
    if file:   
        logging.info("File uploaded")
        global global_prompt
        global global_displacy_html
        if model_type == "Basic":
            beginning_phrase = 'The following table sets forth a summary of our cash flows for the periods indicated'
            end_phrase = "Recent Accounting Guidance"
            extracted_phrase = text_extractor.extract_text_after_phrase(text_extractor.pdf_to_text(file), beginning_phrase, end_phrase)
        else:
            extracted_phrase = text_extractor.extract_text(file)

        if extracted_phrase == "":
            logging.error(f"Error extracting phrase.")
        else:
            logging.info(f"Extracted Phrase: {extracted_phrase}")
        html = sentiment_analysis.render_text(extracted_phrase)
        prompt = api.create_prompt(extracted_phrase)
        if prompt == "":
            logging.error("Could not generate prompt. Error extracting footnotes")
        else:
            logging.info(f"Prompt: {prompt}")
        global_prompt = prompt
        global_displacy_html = html

        return jsonify({'html': html, 'prompt': prompt, 'cost': api.get_request_cost(prompt, 0.50/1_000_000)}) 
    logging.warn("File error: no file or empty file.")
    return jsonify({'html': "No file or empty file.", 'prompt': '', 'cost': 0})

@app.route('/run-report', methods=['POST'])
def run_report():
    if global_prompt:
        good, medium, bad = api.call_api(global_prompt)
        logging.info(f"GOOD: {good}\n, MEDIUM: {medium}\n, BAD: {bad}\n")
        return jsonify({
            "good": good,
            "medium": medium,
            "bad": bad
        })
    else:
        logging.error("No Prompt Created")
        return jsonify({"error": "No prompt available. Upload a file first."})

@app.route('/save-as-pdf', methods=['GET'])
def save_as_pdf():
    if global_displacy_html != "":
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'cicero-output.pdf')
        pdfkit.from_string(global_displacy_html, downloads_path)
        logging.info("File created")
        return '', 200
    else:
        logging.error("No displaCy HTML found")
        return '', 404

if __name__ == '__main__': 
    app.run(debug=True)