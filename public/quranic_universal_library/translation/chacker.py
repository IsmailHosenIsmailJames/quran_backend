import os
import json

base = './Simple'
for lang in list(os.listdir(base)):
    for file in list(os.listdir(os.path.join(base, lang))):
        jsonData = dict(json.load(open(os.path.join(base, lang, file), 'r')))
        print(f"{len(jsonData)} -> \t{file}")
        # for key in jsonData.keys():
        #     print(list(jsonData[key].keys()))