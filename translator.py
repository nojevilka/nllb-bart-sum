from flask import Flask, request
import urllib.parse
from subprocess import PIPE, Popen
import re
import asyncio
import time


app = Flask(__name__)

@app.route('/progress')
def progress():
    global _i
    global _n
    return f"{_i},{_n}"


@app.route('/', methods=['POST'])
def index():
    return translate(request.data.decode("utf-8"))

_src_lang = "rus_Cyrl"
_tgt_lang = "eng_Latn"

def translate(text):
    global _src_lang
    global _tgt_lang
    global _i

    _i = 0

    tags = re.findall(r"<(.*?)>", text)
    src_lang = tags[0]
    tgt_lang = tags[1]
    _src_lang = src_lang
    _tgt_lang = tgt_lang
    article = re.sub(r"<.*?>", '', text)

    sentences = split_by_sentences(preprocess(article))
    return " ".join([postprocess_sentence(s) for s in translate_sentences(sentences)])

def preprocess(s):
    s = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|\-|\.|\/|%|_|\(.*?\))+', '', s)
    s = re.sub(r'(«|»)', '"', s)
    return s

def postprocess_sentence(s):
    s = re.sub(r'(\<\/s\>|eng_Latn|rus_Cyrl)', '', s)
    return s

def split_by_sentences(article):
    text_parts = re.split('(\. |\.|\! |\!|\n)', article) + [""]
    sentences = [i+j for i,j in zip(text_parts[::2], text_parts[1::2])]
    return [sentence for sentence in [sentence.strip() for sentence in sentences] if len(sentence) > 0]

def translate_sentences(sentences):
    return asyncio.run(async_translate_sentences(sentences))

# no_of_workers = 8
no_of_workers = 3

async def async_translate_sentences(sentences):
    global _n
    translated_sentences = sentences
    loop = asyncio.get_event_loop()

    queue = asyncio.Queue()

    print("fill queue")
    _n = len(sentences)
    for i in range(len(sentences)):
        queue.put_nowait((i, sentences[i]))
        print("added", i)

    tasks = []
    print("creating tasks")
    for i in range(no_of_workers):
        print("create", i)
        task = asyncio.create_task(worker(i, queue, loop, translated_sentences))
        tasks.append(task)
        print("created")
    
    print("wait for join")
    await queue.join()
    print("joined")

    for task in tasks:
        task.cancel()
    print("all canceled")

    _i = 0
    _n = 0

    print("translated_sentences:", translated_sentences)

    return sentences

def escape(s):
    return s.translate(str.maketrans({"\"":  "\\\""}))

def translate_sentence(sentence, worker_index):
    port = 5001 + worker_index

    print("!!!_src_lang:", _src_lang)
    print("!!!_tgt_lang:", _tgt_lang)
    text = f"<{_src_lang}><{_tgt_lang}>{escape(sentence)}"
    print("text:", text)

    with Popen(f"curl -X POST -H 'Content-Type: application/text' -d \"{text}\" http://localhost:{port}", stdout=PIPE, stderr=None, shell=True) as process:
        return process.communicate()[0].decode("utf-8")

_i = 0
_n = 0

async def worker(worker_index, queue, loop, translated_sentences):
    global _i

    while True:
        print(f"worker {worker_index} iter start")
        sentence_index, sentence = await queue.get()
        print(f"dequeued sentence {sentence}")

        start = time.time()
        r = await loop.run_in_executor(None, translate_sentence, sentence, worker_index)
        end = time.time()
        print(f"translated, time: {end - start}, worker_index: {worker_index}, result: {r}")

        _i += 1
        print("i:", _i)
        
        translated_sentences[sentence_index] = r

        # Notify the queue that the "work item" has been processed.
        queue.task_done()
