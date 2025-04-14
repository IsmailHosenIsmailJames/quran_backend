import json
import os

errorAyahs = 0
score = dict()
base = 'public/quranic_universal_library/tafsir'
for languageFolder in os.listdir(base):
    if(languageFolder=='score_maker.py'): continue
    for file in os.listdir(os.path.join(base,languageFolder)):
        jsonData =dict(json.load(open(os.path.join(base,languageFolder,file),"r")))
        totalAyahs = len(jsonData.keys())
        hasTafsir = 0
        for ayahKey in list(jsonData.keys()):
            if(type(jsonData[ayahKey])== dict):
                try:
                    text = jsonData[ayahKey]['text']
                    if(len(text) > 0): hasTafsir += 1
                except:
                    if(len(dict(jsonData[ayahKey]).keys()) == 0):
                        errorAyahs += 1
                        jsonData[ayahKey]={"text": "",}
                    else:
                        lastKey = list(jsonData[ayahKey]['ayah_keys'])[-1]
                        jsonData[ayahKey]['ayah_keys'] = lastKey
        

        errorAyahs=0
        if(languageFolder not in score.keys()):
            score[languageFolder] = [
                {
                    "fileName" : file,
                    "totalAyahs" : totalAyahs,
                    "hasTafsir" : hasTafsir,
                    "score" : int((hasTafsir/totalAyahs)*100),
                    "full_path" : os.path.join("quranic_universal_library/tafsir",languageFolder,file).replace(" ", "_")
                }
            ]
        else:
            score[languageFolder].append(
                 {
                    "fileName" : file,
                    "totalAyahs" : totalAyahs,
                    "hasTafsir" : hasTafsir,
                    "score" : int((hasTafsir/totalAyahs)*100),
                    "full_path" : os.path.join("quranic_universal_library/tafsir",languageFolder,file).replace(" ", "_")

                }
            )
            


json.dump(score,open(f"./score.json","w", encoding='utf-8'),ensure_ascii=False, indent=4)