import sys
import subprocess

def create_and_activate_venv():
    is_windows = sys.platform.startswith('win')
    api_key = input("Enter your OpenAI API Key, or press enter to skip: ")
    f = open("API_KEY.txt", 'w')
    if api_key:
        f.write(api_key)
    f.close()
    # creates venv
    venv_cmd = 'python -m venv venv' if is_windows else 'python3 -m venv venv'
    subprocess.check_call(venv_cmd, shell=True)

    # activates venv
    activate_script = '.\\venv\\Scripts\\activate' if is_windows else 'source venv/bin/activate'
    pip_install_cmd = f'{activate_script} && pip install openai python-dotenv Flask PyMuPDF flask-cors spacy tiktoken pdfkit && python -m spacy download en_core_web_sm'

    if is_windows:
        # Windows requires a different approach for sequential commands
        subprocess.check_call(['cmd', '/V', '/C', f'{activate_script} && pip install openai python-dotenv Flask PyMuPDF flask-cors spacy tiktoken pdfkit && python -m spacy download en_core_web_sm'], shell=True)
    else:
        subprocess.check_call(pip_install_cmd, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    create_and_activate_venv()
