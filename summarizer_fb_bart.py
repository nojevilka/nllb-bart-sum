from flask import Flask, request
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, AutoModelForSeq2SeqLM
from transformers import pipeline

class Summarizer:
    def __init__(self, model_name = "facebook/bart-large-xsum"):
        self.model_name = model_name

        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)

        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        # self.model.load_state_dict(torch.load('./results_backup/checkpoint-900/pytorch_model.bin'))
        # self.model.eval()


    def summarize(self, text):
        inputs = self.tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = self.model.generate(inputs["input_ids"])
        return self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

summarizer = Summarizer()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def summarize_endpoint():
    r = summarizer.summarize(request.data.decode("utf-8"))
    print("summarized:", r)
    return r
