import os
import json

base = 'word_by_word'

listOfDirs = os.listdir(base)

for dir in listOfDirs:
    listOfFiles = os.listdir(os.path.join(base, dir))
    for file in listOfFiles:
        with open(os.path.join(base, dir, file), 'r') as f:
            data = json.load(f)
            new_data = dict()
            for key, value in data.items():
                surahNumber, ayahNumber, wordNumber = key.split(':')
                if new_data.get(f'{surahNumber}:{ayahNumber}', None) == None:
                    new_data[f'{surahNumber}:{ayahNumber}'] = list()
                new_data[f'{surahNumber}:{ayahNumber}'].append(value)
        
        if not os.path.exists(f'wdw_simplifer/{dir}'):
            os.makedirs(f'wdw_simplifer/{dir}')
        with open(f'wdw_simplifer/{dir}/' + file, 'w') as f:
            json.dump(new_data, f, ensure_ascii=False)
            print(f'File {file} simplified successfully.')
        print(f'File {file} simplified successfully.')