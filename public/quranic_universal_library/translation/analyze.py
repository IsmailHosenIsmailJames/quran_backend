import os
import json

topNumber = 83664
base = 'word_by_word'
fileInfo = dict()
for lang in list(os.listdir(base)):
    print("\n"+lang + "->")
    count=1
    fileInfo[lang]=[]
    for file in list(os.listdir(os.path.join(base, lang))):
        full_path = os.path.join(base, lang, file)
        
        new_filename = (os.path.join(base, lang, file)).replace(" ", "_")
        if new_filename != full_path: 
            os.rename(full_path, new_filename)
            print(f"Renamed : '{full_path}' \t->\t '{new_filename}'")
            full_path = new_filename
        
        count+=1
        jsonData = dict(json.load(open(full_path, 'r')))
        lengthOfAyahs = len(jsonData)
        print(f"\t{count}. -> {lengthOfAyahs} -> {full_path}")
        score = round((lengthOfAyahs / topNumber) * 100, 2)
        if(file.find('translation-with-footnote-tags') != -1):
            fileInfo[lang].append({
                    "language" : lang,
                    "name" : file.replace(".translation-with-footnote-tags", "").replace(".json", ""),
                    "file_name" : file,
                    "score": score,
                    "type" : "translation-with-footnote-tags",
                    "full_path" : full_path
                })
        elif(file.find('.simple') != -1):
            fileInfo[lang].append({
                    "language" : lang,
                    "name" : file.replace(".simple", "").replace(".json", ""),
                    "file_name" : file,
                    "score": score,
                    "type" : "simple",
                    "full_path" : full_path
                })
        elif(file.find(' wbw translation') != -1):
            fileInfo[lang].append({
                    "language" : lang,
                    "name" : file.replace(" wbw translation", "").replace(".json", ""),
                    "file_name" : file,
                    "score": score,
                    "type" : "word by word",
                    "full_path" : full_path
                })
        else:
            fileInfo[lang].append({
                    "language" : lang,
                    "name" : file.replace(".json", ""),
                    "file_name" : file,
                    "score": score,
                    "type" : "None",
                    "full_path" : full_path
                })
        

json.dump(fileInfo, open(base+'.json', 'w'),indent=4, ensure_ascii=False)
        
    