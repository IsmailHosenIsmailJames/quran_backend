import os
import re
import io
import time
import random
import zipfile
import requests
from bs4 import BeautifulSoup

# --- Configuration ---
BASE_URL = "https://qul.tarteel.ai"
RESOURCES_URL = f"{BASE_URL}/resources/tafsir" # Updated to Tafsir
DOWNLOAD_DIR = "quran_tafsirs"
MIN_DELAY = 2
MAX_DELAY = 5

# Generic tags for Tafsir page to append to the folder name
GENERIC_TAGS = ["Tafsir", "Multiple Ayahs", "Single Ayah"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Ensure your cookie is fresh
COOKIE_STRING = "R2TCXhdGXolOpM3GxkpOFy1XGT%2BjnLd0KV2P51%2BxyUAXgyJ5nM2vCYBGHp2lZ4PKdn8eAt2yxNls1G8ihVzLU9IyBFCPiooyLW94KX8J37htkTvlTdDeJ0VRXBaq3CkTP%2F5advJTSIn1V0ukuuwBmgW2cfP1nvxNGtGjnGSHRX58i3LHVjl4ID%2BLP6614Jfpc%2Fma4l4A0cSitofN%2BKO%2BUisB8TgUUBTyW8nduAv80JuuVAk8dD5FpUfhbsUZxNY7NJGn71gjA13V34V3f1lQvH9OpJfMetvBHeN36k8MV9msCswiRcTOpgMSIwYD0GpTQDaabPJm2OC7QpZceTv441eBaWU9yWLAf6nU%2FvqEELO0c1SWcgDfPTl0LdiPb%2FFOVqVWIq%2BFwLA7K3inh6FdmB3tXFvFAN3x--gfypRXSSQ9zimnsO--xXFpfq9rR6G3lnkiKKkNeA%3D%3D"

def sanitize_name(name):
    """Removes illegal characters and keeps paths clean."""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip().replace(" ", "_")

def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.set("_quran_com-community_session", COOKIE_STRING, domain="qul.tarteel.ai")
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    print(f"Connecting to {RESOURCES_URL}...")
    try:
        response = session.get(RESOURCES_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to load page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr', class_='tw-border-b')
    print(f"Scanning {len(rows)} Tafsir entries...\n")

    for row in rows:
        title_elem = row.find('p', class_='tw-font-semibold')
        if not title_elem: continue
        
        tafsir_name = sanitize_name(title_elem.text)

        # 1. Build the folder name (Language_Tag1_Tag2)
        tags = [t.get_text(strip=True) for t in row.find_all('a', class_='tag')]
        lang_tags = [t for t in tags if t not in GENERIC_TAGS]
        other_tags = [t for t in tags if t in GENERIC_TAGS]
        combined_folder_name = sanitize_name("_".join(lang_tags + other_tags))
        
        lang_dir = os.path.join(DOWNLOAD_DIR, combined_folder_name)
        final_json_path = os.path.join(lang_dir, f"{tafsir_name}.json")

        # 2. Skip if already downloaded
        if os.path.exists(final_json_path):
            continue

        # 3. Find the JSON download link 
        # (Using a regex that handles both "Download json" and "Download simple.json")
        json_link_elem = row.find('a', string=re.compile(r'Download (simple\.)?json', re.IGNORECASE))
        
        if json_link_elem and 'href' in json_link_elem.attrs:
            download_url = BASE_URL + json_link_elem['href']
            os.makedirs(lang_dir, exist_ok=True)

            print(f"[NEW] {combined_folder_name} -> {tafsir_name}")
            
            try:
                zip_response = session.get(download_url)
                zip_response.raise_for_status()
                
                with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
                    json_files = [f for f in z.namelist() if f.lower().endswith('.json')]
                    if json_files:
                        with z.open(json_files[0]) as source, open(final_json_path, 'wb') as target:
                            target.write(source.read())
                        
                        wait_time = random.uniform(MIN_DELAY, MAX_DELAY)
                        print(f"  -> Extracted. Sleeping {wait_time:.1f}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"  ! No JSON inside zip for {tafsir_name}")
                        
            except Exception as e:
                print(f"  ! Error processing {tafsir_name}: {e}")
                time.sleep(5)

    print("\nAll available Tafsir files synced!")

if __name__ == "__main__":
    main()