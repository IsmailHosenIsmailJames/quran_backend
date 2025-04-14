import json
import re
import os # Import os module to work with files

def find_html_tags_in_json_data(data):
    """
    Finds all unique HTML-like tags in specific string fields of a nested dictionary.

    Args:
        data (dict): The dictionary loaded from the JSON data.

    Returns:
        set: A set containing all unique HTML-like tags found.
    """
    # Regular expression to find patterns that look like HTML tags
    # It matches '<', followed by one or more characters that are NOT '>', then '>'.
    # This is a simple regex and might match things that aren't strictly valid HTML,
    # but it should capture the examples you provided (<span>, <sup>, <i>, <b>, <a>).
    html_tag_pattern = re.compile(r"<[^>]+>")

    found_tags = set()

    # Iterate through each top-level key (like "1:1", "1:2")
    for key, value_dict in data.items():
        # Check the main text field 't'
        if 't' in value_dict and isinstance(value_dict['t'], str):
            tags_in_t = html_tag_pattern.findall(value_dict['t'])
            found_tags.update(tags_in_t) # Add all found tags to the set

        # Check the footnote field 'f', which is expected to be a dictionary
        if 'f' in value_dict and isinstance(value_dict['f'], dict):
            # Iterate through the values (the actual footnote texts) in the 'f' dictionary
            for footnote_text in value_dict['f'].values():
                if isinstance(footnote_text, str):
                    tags_in_f = html_tag_pattern.findall(footnote_text)
                    found_tags.update(tags_in_f) # Add all found tags to the set

    return found_tags

def process_json_file(file_path):
    """
    Loads JSON data from a file and finds HTML tags within it.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        set: A set of unique HTML tags found, or an empty set if errors occur.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return find_html_tags_in_json_data(data)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return set()
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from file {file_path}")
        return set()
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")
        return set()


baseDir = 'public/quranic_universal_library/translation/Simple'
listOfDirs = os.listdir(baseDir)
listOfAllTags = []
for dir in listOfDirs:
    listOfFile = os.listdir(os.path.join(baseDir, dir ))
    for file in listOfFile:
        with open(os.path.join(baseDir, dir, file), 'r') as f:
            jsonData = json.load(f)
            tags = find_html_tags_in_json_data(jsonData)
            listOfAllTags+=tags

listOfTagsWithoutNumbers = set()
for tag in listOfAllTags:
    firstIndex = str(tag).find('"')
    lastIndex =len(tag) - str(tag)[::-1].find('"')
    if(firstIndex != -1 and lastIndex != -1):
        listOfTagsWithoutNumbers.add(tag[0:firstIndex] + tag[lastIndex::])
    else:
        listOfTagsWithoutNumbers.add(tag)
    

print(len(listOfTagsWithoutNumbers))

with open('tags.json', 'w') as f:
    json.dump(list(listOfTagsWithoutNumbers), f, indent=2, ensure_ascii=False)
