# Cicero Finance - 2024
# Summary:

This tool was created for my Senior Project class to enable users to upload a financial document, such as a 10-K, and extract particular components. Currently, it focuses on publicly available Dexcom 10-K's to tailor the model to one specific company.

**Key Features:**

- **Natural Language Processing:** Utilizes the spaCy library to highlight specific key terms pertinent to the company.
- **Summary Generation:** Connects to the OpenAI API to create a summary with components labeled as `good`, `medium`, and `bad`. These summaries may include calculations of income loss compared to previous years.
- **Highlighting Significant Points:** The API picks out the most significant points that a user might miss when skimming through the document, aiding financial analysts in identifying critical areas for further review.

**Purpose:** This tool assists financial analysts in getting a comprehensive overview of crucial details in financial documents but is not designed to replace a financial analyst.


# Initial Setup:
Generate an OpenAI API Key from [`this link`](https://platform.openai.com/api-keys). Copy it to your clipboard.

Run [`setup.py`](setup.py) to create a virtual environment and install the required packages.

Additionally, install wkhtmltopdf using Homebrew via `brew install Caskroom/cask/wkhtmltopdf`

*If this does not work, you can do so manually by following the steps below.*

### On macOS and Windows:
Create a file called `API_KEY.txt`. In this file, paste your OpenAI API key.

### On macOS:

```bash
# Create a virtual environment in the project directory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install necessary packages
pip install openai python-dotenv Flask PyMuPDF flask-cors spacy tiktoken pdfkit

# Deactivate the virtual environment when done
deactivate
```

### On Windows:

```cmd
python -m venv venv

.venv\Scripts\activate

pip install openai python-dotenv Flask PyMuPDF flask-cors spacy tiktoken pdfkit

deactivate
```

# Running the program:

Run [`app.py`](./app.py)\
Visit the URL that is printed to the console.

# Project Structure
[`api.py`](./api.py) contains methods to create the prompt to be sent to the API, call the API and return the result, convert the JSON from the API into HTML, and calculate the number of tokens and cost for sending the prompt.
[`app.py`](./app.py) contains methods that are called from the webpage using app.route. These methods include one that handles uploading a file, calling the api function from api.py, and save as pdf.
[`sentiment_analysis.py`](./sentiment_analysis.py) creates a spaCy object and returns it in html.
[`setup.py`](./setup.py) runs the commands listed above to make setup easier
[`text_extractor.py`](./text_extractor.py) is used to extract the footnotes from text that is passed through
