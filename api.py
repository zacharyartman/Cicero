# file used for openai api processing
import json
import os
from dotenv import load_dotenv
import openai
import tiktoken

def create_prompt(text):
    prompt = f"""
    Given the 10-Q financial document text provided, categorize the key financial highlights into 'good', 'medium', and 'bad' based on the following criteria:

    - 'Good' should include significant positive financial growth, increased revenue, reduced debts, or other positive financial indicators.
    - 'Medium' should capture stable financial conditions, no significant change in revenue or expenses, and consistent financial performance.
    - 'Bad' should highlight negative financial trends, such as decreased revenue, increased debt, losses, or any financial instability.

    Return the analysis in JSON format with summaries for 'good', 'medium', and 'bad'.
    Please provide the response in plain JSON format, without any markdown or additional characters

    Here is the text to analyze:
    {text}
    """ if text != "" else ""

    return prompt

def call_api(prompt):

    f = open("./API_KEY.txt", "r")

    client = openai.OpenAI(api_key=f.readline())


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial assistant, skilled in summarizing important information in financial documents and categorizing them into good, medium, and bad."},
            {"role": "user", "content": prompt}
        ]
    )

    response_content = completion.choices[0].message.content if completion.choices else '{}'
    print(f"RESPONSE CONTENT: {response_content}")

    try:
        analysis = json.loads(response_content)
        print(f"ANALYSIS: {analysis}")
    except json.JSONDecodeError:
        print("Failed to decode JSON")
        return None

    # Extracting the categories
    good = analysis.get('good', [])
    medium = analysis.get('medium', [])
    bad = analysis.get('bad', [])

    html_good = to_html(good)
    html_medium = to_html(medium)
    html_bad = to_html(bad)

    
    return html_good, html_medium, html_bad

def format_key(key):
    return key.replace('_', ' ').capitalize()

def to_html(value, level=0):
    indent = ' ' * 4 * level
    if isinstance(value, dict):
        html = ''
        for k, v in value.items():
            html += f'{indent}<div><strong>{format_key(k)}:</strong></div>\n'
            html += f'{to_html(v, level + 1)}'
        return html
    elif isinstance(value, list):
        html = ''
        for item in value:
            html += f'{indent}<div>- {item}</div>\n'
        return html
    else:
        return f'{indent}<div>{value}</div>\n'


def num_tokens_from_string(string: str, encoding_name:str="gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_request_cost(string: str, cost_per_token: float, encoding_name:str="gpt-3.5-turbo"):
    return num_tokens_from_string(string) * cost_per_token