import os
import requests

# Supabase settings
SUPABASE_URL = "https://xzbozofttuvyijeimxkj.supabase.co/rest/v1/portal_pages"
SUPABASE_KEY = "dnHmzMkSQhvMmCj8"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Folder where your HTML files are stored
HTML_FOLDER = os.path.expanduser("~/codac_portal")

# Iterate over all .html files
for filename in os.listdir(HTML_FOLDER):
    if filename.endswith(".html"):
        filepath = os.path.join(HTML_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        data = {
            "filename": filename,
            "content": content
        }

        response = requests.post(SUPABASE_URL, json=data, headers=HEADERS, params={"return": "representation"})
        print(f"{filename}: {response.status_code} → {response.text}")

print("✅ All HTML files have been uploaded to Supabase!")
