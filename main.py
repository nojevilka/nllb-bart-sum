from flask import Flask, render_template, request, url_for, flash, redirect
import urllib.parse
from subprocess import PIPE, Popen

def escape(s):
    return s.translate(str.maketrans({"\"":  "\\\""}))

app = Flask(__name__)

messages = []
_action = ""

# TRANSLATOR_PORT = 5400
TRANSLATOR_PORT = 5000
# BACK_TRANSLATOR_PORT = 5000
BACK_TRANSLATOR_PORT = 6000

@app.route('/', methods=('GET', 'POST'))
def index():
    global _action
    _action = ""
    if request.method == 'POST':
        content = request.form['content']

        if not content:
            return
        else:
            text_to_translate = content
            print("!!!will translate", text_to_translate)

            _action = "translating..."
            with Popen(f"curl -X POST -H 'Content-Type: application/text' -d \"<rus_Cyrl><eng_Latn>{escape(text_to_translate)}\" http://localhost:{TRANSLATOR_PORT}", stdout=PIPE, stderr=None, shell=True) as process:
                
                translated_text = process.communicate()[0].decode("utf-8")
                print(f"!!!translated_text: {translated_text}")
                _action = "summarizing..."
                with Popen(f"curl -X POST -H 'Content-Type: application/text' -d \"{escape(translated_text)}\" http://localhost:5200", stdout=PIPE, stderr=None, shell=True) as process2:
                    
                    summary = process2.communicate()[0].decode("utf-8")
                    print(f"!!!summary: {summary}")
                    _action = "translating back..."
                    with Popen(f"curl -X POST -H 'Content-Type: application/text' -d \"<eng_Latn><rus_Cyrl>{escape(summary)}\" http://localhost:{BACK_TRANSLATOR_PORT}", stdout=PIPE, stderr=None, shell=True) as process3:
                        
                        translated_summary = process3.communicate()[0].decode("utf-8")
                        print("translated_summary:", translated_summary)
                        messages.insert(0, {'translated_title': translated_summary, 'title': summary, 'content': translated_text, 'orig_content': text_to_translate})

                        return redirect(url_for('index'))

    return render_template('index.html', messages=messages)

@app.route('/progress')
def progress():
    global _action
    with Popen(f"curl http://localhost:{TRANSLATOR_PORT}/progress", stdout=PIPE, stderr=None, shell=True) as process:
        r = process.communicate()[0].decode("utf-8")
        return f"{_action},{r}"
