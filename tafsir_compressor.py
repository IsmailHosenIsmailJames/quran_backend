import os
import json
from pathlib import Path
from compressor_utils import (
    compress_content, write_if_different, normalize_lang_name, 
    get_target_lang_path, save_json
)

# Global index for tafsirs
tafsir_index = {}

def process_tafsir_directory(source_root, target_root):
    source_root = Path(source_root)
    target_root = Path(target_root)
    
    for lang_dir in source_root.iterdir():
        if not lang_dir.is_dir():
            continue
        
        lang_name = normalize_lang_name(lang_dir.name)

        for json_file in lang_dir.glob("*.json"):
            print(f"Processing Tafsir: {json_file}")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
                continue

            compressed_str = compress_content(data)
            lang_path = get_target_lang_path(target_root, lang_name)
            
            save_name = json_file.name.replace(" ", "_") + ".txt"
            final_path = lang_path / save_name
            
            write_if_different(final_path, compressed_str)

            # Metadata collection
            if lang_name not in tafsir_index:
                tafsir_index[lang_name] = []
            
            rel_path = final_path.relative_to("public/quranic_universal_library")
            
            tafsir_index[lang_name].append({
                "language": lang_name,
                "name": json_file.stem.replace("_", " "),
                "file_name": save_name,
                "full_path": str(rel_path)
            })

if __name__ == "__main__":
    SOURCE_DIR = "quran_tafsirs"
    TARGET_DIR = "public/quranic_universal_library/compressed_tafsir_v2"

    print("--- Processing Tafsirs ---")
    if os.path.exists(SOURCE_DIR):
        process_tafsir_directory(SOURCE_DIR, TARGET_DIR)
        save_json(tafsir_index, os.path.join(TARGET_DIR, "index.json"))
    else:
        print(f"Source directory {SOURCE_DIR} not found.")
