import os
import requests
import sys

def download_asset(url, folder, filename):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    path = os.path.join(folder, filename)
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {path}")
            return path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

if __name__ == "__main__":
    # This is a placeholder for the logic where Gemini (via search tools) 
    # provides the URL to this script.
    if len(sys.argv) < 3:
        print("Usage: python researcher.py <url> <filename>")
    else:
        url = sys.argv[1]
        filename = sys.argv[2]
        download_asset(url, "carousel/assets", filename)
