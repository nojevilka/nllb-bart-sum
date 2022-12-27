import json
import urllib.parse
from subprocess import PIPE, Popen
import os

es = []

for file in os.listdir("all_pages"):
    path = f"all_pages/{file}"
    with Popen(f"perl extract_link.pl {path}", stdout=PIPE, stderr=None, shell=True) as process:
        link = process.communicate()[0].decode("utf-8")
    with Popen(f"perl extract_title.pl {path}", stdout=PIPE, stderr=None, shell=True) as process:
        title = process.communicate()[0].decode("utf-8")
    with Popen(f"perl extract_article.pl {path}", stdout=PIPE, stderr=None, shell=True) as process:
        article = process.communicate()[0].decode("utf-8")
    es.append({"title": title, "article": article, "link": link})

with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(es, ensure_ascii=False))
