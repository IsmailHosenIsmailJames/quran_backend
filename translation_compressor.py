import os
import json
from pathlib import Path
from compressor_utils import (
    AYAH_COUNTS, compress_content, write_if_different, 
    normalize_lang_name, get_target_lang_path, save_json
)

# Global index for translations
translation_index = {}

def simplify_wbw(data):
    """
    Simplifies word-by-word data from {"1:1:1": "Word"} to {"1:1": ["Word"]}
    """
    new_data = {}
    for surah_idx, max_ayahs in enumerate(AYAH_COUNTS):
        surah_num = surah_idx + 1
        for ayah_num in range(1, max_ayahs + 1):
            word_num = 1
            while True:
                key = f"{surah_num}:{ayah_num}:{word_num}"
                word = data.get(key)
                if word is None:
                    break
                
                ayah_key = f"{surah_num}:{ayah_num}"
                if ayah_key not in new_data:
                    new_data[ayah_key] = []
                new_data[ayah_key].append(word)
                word_num += 1
    return new_data

def is_word_by_word(data):
    """
    Heuristic to check if a JSON file is word-by-word based on key structure.
    """
    sample_keys = list(data.keys())[:100]
    for key in sample_keys:
        if key.count(':') == 2:
            return True
    return False

def process_translation_directory(source_root, target_root):
    source_root = Path(source_root)
    target_root = Path(target_root)
    
    simple_target_root = target_root / "compressed_translation_simple"
    wbw_target_root = target_root / "compressed_translation_word_by_word"

    for lang_dir in source_root.iterdir():
        if not lang_dir.is_dir():
            continue
        
        lang_name = normalize_lang_name(lang_dir.name)

        # Detect types from folder name
        is_footnote_folder = "With_footnotes" in lang_dir.name or "with_footnotes" in lang_dir.name
        is_tajweed_folder = "Tajweed" in lang_dir.name

        for json_file in lang_dir.glob("*.json"):
            print(f"Processing Translation: {json_file}")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
                continue

            current_wbw = False
            if is_word_by_word(data):
                data = simplify_wbw(data)
                current_wbw = True
            
            compressed_str = compress_content(data)
            
            # Decide target root and language path
            current_root = wbw_target_root if current_wbw else simple_target_root
            lang_path = get_target_lang_path(current_root, lang_name)
            
            save_name = json_file.name.replace(" ", "_") + ".txt"
            final_path = lang_path / save_name
            
            write_if_different(final_path, compressed_str)

            # Metadata collection
            if lang_name not in translation_index:
                translation_index[lang_name] = []
            
            rel_path = final_path.relative_to("public/quranic_universal_library")
            
            # Determine type
            if current_wbw:
                tr_type = "word_by_word"
            elif is_footnote_folder:
                tr_type = "with_footnote"
            else:
                tr_type = "simple"

            translation_index[lang_name].append({
                "language": lang_name,
                "name": json_file.stem.replace("_", " "),
                "file_name": save_name,
                "full_path": str(rel_path),
                "type": tr_type,
                "is_tajweed": is_tajweed_folder
            })

if __name__ == "__main__":
    SOURCE_DIRS = ["quran_translations", "word_by_word"]
    TARGET_ROOT = "public/quranic_universal_library/translation_v2"

    print("--- Processing Translations ---")
    for source in SOURCE_DIRS:
        if os.path.exists(source):
            print(f"\nProcessing source: {source}")
            process_translation_directory(source, TARGET_ROOT)
        else:
            print(f"Source directory {source} not found.")

    save_json(translation_index, os.path.join(TARGET_ROOT, "index.json"))
