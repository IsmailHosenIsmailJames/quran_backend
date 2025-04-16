import os
import json

base = 'word_by_word'

listOfDirs = os.listdir(base)

ayahCount = [7,  286,  200,  176,  120,  165,  206,  75,  129,  109,  123,  111,  43,  52,  99,  128,  111,  110,  98,  135,  112,  78,  118,  64,  77,  227,  93,  88,  69,  60,  34,  30,  73,  54,  45,  83,  182,  88,  75,  85,  54,  53,  89,  59,  37,  35,  38,  29,  18,  45,  60,  49,  62,  55,  78,  96,  29,  22,  24,  13,  14,  11,  11,  18,  12,  12,  30,  52,  52,  44,  28,  28,  20,  56,  40,  31,  50,  40,  46,  42,  29,  19,  36,  25,  22,  17,  19,  26,  30,  20,  15,  21,  11,  8,  8,  19,  5,  8,  8,  11,  11,  8,  3,  9,  5,  4,  7,  3,  6,  3,  5,  4,  5,  6,]

for dir in listOfDirs:
    listOfFiles = os.listdir(os.path.join(base, dir))
    for file in listOfFiles:
        with open(os.path.join(base, dir, file), 'r') as f:
            data = dict(json.load(f))
            new_data = dict()
            for surahNumber in range(0, len(ayahCount)):
                ayahNumber = ayahCount[surahNumber]
                surahNumber+=1
                for ayahNumber in range(0, ayahNumber):
                    ayahNumber+=1
                    wordNumber = 1
                    while True:
                        if(data.get(f'{surahNumber}:{ayahNumber}:{wordNumber}', None) == None):
                            break
                        word = data.get(f'{surahNumber}:{ayahNumber}:{wordNumber}')
                        if new_data.get(f'{surahNumber}:{ayahNumber}', None) == None:
                            new_data[f'{surahNumber}:{ayahNumber}'] = list()
                        new_data[f'{surahNumber}:{ayahNumber}'].append(word)
                        wordNumber += 1

        
        if not os.path.exists(f'fix_wdw_simplifer/{dir}'):
            os.makedirs(f'fix_wdw_simplifer/{dir}')
        with open(f'fix_wdw_simplifer/{dir}/' + file, 'w') as f:
            json.dump(new_data, f, ensure_ascii=False)
            print(f'File {file} simplified successfully.')
        print(f'File {file} simplified successfully.')