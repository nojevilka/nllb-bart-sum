import json

def parse_translation(s):
    _, t1 = s.split("___translated_title___: ")
    translated_title, translated_text = t1.split("\n___translated_text___: ")
    return {
        'translated_title': translated_title,
        'translated_text': translated_text.strip(),
    }

with open('nplus1/data.json') as f:
    es = json.load(f)
    print("es:", len(es))
    with open('translated_part1') as f:
        # r = f.read().split("!#")[1:]
        # print(r[256])
        ts = [parse_translation(t) for t in f.read().split("!#")[1:]]
        print("ts:", len(ts))
        result = [{**e, **t} for (e,t) in zip(es, ts)]

json_string = json.dumps(result, ensure_ascii=False, indent=2)

with open('merged1.json', 'w') as outfile:
    outfile.write(json_string)
