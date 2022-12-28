import anvil.server
from flask import Flask, request
import re

class Translator:
    def __init__(self):
        anvil.server.connect("Y46UREHKLE2PE57C4DOZVMMU-ONM3O23ZU7X7RR6B-CLIENT")

    def translate(self, sentence):
        print("!!!will work on:", sentence)
        return anvil.server.call('translate', sentence)

translator = Translator()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def translate_endpoint():
    return translator.translate(request.data.decode("utf-8"))
