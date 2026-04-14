import os
import json
import bz2
import base64
from pathlib import Path

# Ayah counts for each surah (1-114)
AYAH_COUNTS = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]

def compress_content(json_data):
    """
    Compresses JSON data using BZip2 and encodes it in Base64
    """
    json_str = json.dumps(json_data, ensure_ascii=False)
    compressed = bz2.compress(json_str.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def get_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def write_if_different(target_path, new_content):
    """
    Writes content to target_path only if it differs from current content
    """
    target_path = Path(target_path)
    current_content = get_file_content(target_path)
    
    if current_content != new_content:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {target_path}")
        return True
    return False

def normalize_lang_name(name):
    """
    Strips underscores and common suffixes to get a clean language name.
    """
    name = name.lstrip('_')
    suffixes = [
        "_Tafsir", "_Translation", "_With_footnotes", "_with_footnotes", 
        "_wbw", "_WBW", "_Word_by_word_resources", "_Word_by_Word_resources",
        "_Word_by_word", "_Tajweed"
    ]
    for suffix in suffixes:
        name = name.replace(suffix, "")
    return name

def get_target_lang_path(target_root, lang_name):
    """
    Finds the existing language directory in the target root or returns a new path.
    Preference is given to existing directories to avoid case-sensitivity issues.
    """
    if not target_root.exists():
        return target_root / lang_name
        
    # Try exact match
    exact_path = target_root / lang_name
    if exact_path.exists():
        return exact_path
        
    # Try case-insensitive match
    for existing in target_root.iterdir():
        if existing.is_dir() and existing.name.lower() == lang_name.lower():
            return existing
            
    return exact_path

def save_json(data, target_path):
    target_path = Path(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Index saved to: {target_path}")
