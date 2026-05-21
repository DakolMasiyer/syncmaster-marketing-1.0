import json
import re

class CopyMapper:
    """
    The 'Brain' that maps raw marketing copy to structured slide data.
    In a full implementation, this calls Gemini. 
    As a fallback for slow networks, it uses robust regex/logic to split text.
    """
    def __init__(self, theme_config):
        self.theme = theme_config

    def map_to_slides(self, raw_text, topic=""):
        # Pattern-based splitting (Fallback for when AI is restricted)
        # We look for numbered lists, bullet points, or paragraphs.
        
        paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        slides = []
        
        # 1. Slide 1: Opener
        slides.append({
            "type": "opener",
            "headline": topic if topic else (paragraphs[0][:50] + "..." if paragraphs else "SyncMaster"),
            "bg_color": "#5252E0" # Brand Purple
        })
        
        # 2. Middle Slides: Distribute remaining paragraphs
        for i, para in enumerate(paragraphs[1:8]):
            # Check if it looks like a stat
            if re.search(r'\d+%', para) or re.search(r'\$\d+', para):
                stat_match = re.search(r'(\d+%|\$\d+[A-Za-z]*)', para)
                slides.append({
                    "type": "stat",
                    "stat": stat_match.group(1) if stat_match else "812%",
                    "headline": para.replace(stat_match.group(1), "").strip() if stat_match else para,
                    "bg_color": "#0A0A20" # Dark
                })
            else:
                slides.append({
                    "type": "standard",
                    "headline": para[:80] + "..." if len(para) > 80 else para,
                    "body": para,
                    "bg_color": "#5252E0" if i % 2 == 0 else "#0A0A20"
                })
        
        # 3. Slide 10: CTA
        slides.append({
            "type": "standard",
            "headline": "That's the gap we're closing.",
            "body": "Join the waitlist at syncmaster.io",
            "bg_color": "#5252E0"
        })
        
        return {"slides": slides}

if __name__ == "__main__":
    test_text = "Music licensing is broken.\n\n812% growth in demand for African sounds.\n\nWe connect composers to global briefs.\n\nKeep your publishing rights."
    mapper = CopyMapper({})
    print(json.dumps(mapper.map_to_slides(test_text, "The Sync Problem"), indent=2))
