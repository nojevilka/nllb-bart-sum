import json
import urllib.parse
from subprocess import PIPE, Popen

def escape(s):
    return s.translate(str.maketrans({"\"":  "\\\""}))

translated_es = []

try:

    with open('nplus1/data.json') as f:
        es = json.load(f)
        print(len(es))
        # for e in es:
        for i in range(len(es)):
            e = es[i]
            print(f"!#{i}")
            print("___title___:", e['title'])
            print("___text___:", e['text'])
            translated_e = {}
            with Popen(f"curl -s -X POST -H 'Content-Type: application/text' -d \"<rus_Cyrl><eng_Latn>{escape(e['title'])}\" http://localhost:5000", stdout=PIPE, stderr=None, shell=True) as process:
                translated_title = process.communicate()[0].decode("utf-8")
                translated_e['translated_title'] = translated_title
                print("___translated_title___:", translated_title)
            with Popen(f"curl -s -X POST -H 'Content-Type: application/text' -d \"<rus_Cyrl><eng_Latn>{escape(e['text'])}\" http://localhost:5000", stdout=PIPE, stderr=None, shell=True) as process:
                translated_text = process.communicate()[0].decode("utf-8")
                translated_e['translated_text'] = translated_text
                print("___translated_text___:", translated_text)
            translated_es.append(translated_e)

            

except:
    json_string = json.dumps(translated_es)
    with open('nplus1/translated_data.json', 'w') as outfile:
        outfile.write(json_string)
