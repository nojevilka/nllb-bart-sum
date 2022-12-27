import json
import random

with open('all_translated_data.json') as f:
    es = json.load(f)
    random.shuffle(es)

    n = len(es)
    train_size = int(0.9*n)

    train = es[:train_size]
    test = es[train_size:]

with open('train_translated_data.json', 'w') as outfile:
    outfile.write(json.dumps(train, ensure_ascii=False, indent=2))

with open('test_translated_data.json', 'w') as outfile:
    outfile.write(json.dumps(test, ensure_ascii=False, indent=2))
