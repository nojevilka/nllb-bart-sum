from flask import Flask, request
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re

class Translator:
    # available models: 'facebook/nllb-200-distilled-600M', 'facebook/nllb-200-1.3B', 'facebook/nllb-200-distilled-1.3B', 'facebook/nllb-200-3.3B'
    # def __init__(self, model_name = "facebook/nllb-200-distilled-600M", src_lang = "rus_Cyrl", tgt_lang = "eng_Latn"):
    def __init__(self, model_name = "facebook/nllb-200-3.3B"):
    # def __init__(self, model_name = "facebook/nllb-200-1.3B"):
    # def __init__(self, model_name = "facebook/nllb-200-distilled-600M"):
        self.model_name = model_name
        self.device = torch.device("cpu") # torch.device("mps") # torch.device("cuda")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)

    def translate(self, sentence):
        print(f"!!!back translate: {sentence}")
        src_lang, tgt_lang = re.findall(r"<(.*?)>", sentence)
        sentence = re.sub(r"<.*?>", '', sentence)
        self.translator = pipeline('translation', model=self.model, tokenizer=self.tokenizer, src_lang=src_lang, tgt_lang=tgt_lang)

        output = self.translator(sentence, max_length=1024)

        return output[0]['translation_text']

translator = Translator()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def translate_endpoint():
    return translator.translate(request.data.decode("utf-8"))
