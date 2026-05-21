import os
import re
import json

class CalendarConnector:
    def __init__(self, calendar_path, copy_bank_path):
        self.calendar_path = calendar_path
        self.copy_bank_path = copy_bank_path

    def get_upcoming(self):
        with open(self.calendar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the POSTS array from the JS in the HTML
        match = re.search(r'const\s+POSTS\s*=\s*\[(.*?)\s*\];', content, re.DOTALL)
        if not match:
            return []
            
        posts_raw = match.group(1)
        objects = re.findall(r'\{(.*?)\}', posts_raw, re.DOTALL)
        
        carousels = []
        for obj in objects:
            if "'Carousel'" in obj or '"Carousel"' in obj:
                id_m = re.search(r"id:\s*['\"](.*?)['\"]", obj)
                top_m = re.search(r"topic:\s*['\"](.*?)['\"]", obj)
                if id_m:
                    carousels.append({
                        'id': id_m.group(1), 
                        'topic': top_m.group(1) if top_m else ''
                    })
        return carousels

    def get_copy(self, post_id):
        with open(self.copy_bank_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = rf"'{post_id}':\s*\{{(.*?)\}}"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            obj_content = match.group(1)
            body_match = re.search(r"body:\s*[`'\"](.*?)[`'\"]", obj_content, re.DOTALL)
            if body_match:
                return body_match.group(1).replace('\\n', '\n')
        return None

if __name__ == '__main__':
    # Default paths for testing
    cal_path = 'C:/Users/infon/Documents/Claude Code/Projects/syncmaster-marketing-1.0/syncmaster-content-calendar.html'
    cb_path = 'C:/Users/infon/Documents/Claude Code/Projects/syncmaster-marketing-1.0/copy-bank-m2.html'
    
    conn = CalendarConnector(cal_path, cb_path)
    up = conn.get_upcoming()
    print(f"Found {len(up)} carousels")
    if up:
        post_id = up[0]['id']
        print(f"Fetching copy for: {post_id}")
        copy = conn.get_copy(post_id)
        if copy:
            print(f"Copy snippet: {copy[:100]}...")
