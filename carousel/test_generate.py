import os
import json
from engine_v3 import AestheticEngine

# Manually mapped JSON structure for IG-EDU-01
content = {
    "slides": [
        {
            "type": "opener",
            "headline": "Nobody explained this in music school.\nAnd it's worth more than anything they did teach you. ↓",
            "bg_color": "#5252E0"
        },
        {
            "type": "standard",
            "headline": "Sync licensing = your music in film, TV, ads & games.",
            "body": "",
            "bg_color": "#0A0A20"
        },
        {
            "type": "stat",
            "stat": "$5k-$75k",
            "headline": "One Netflix scene: $5,000–$20,000.\nOne global ad campaign: $10,000–$75,000.\nUpfront. Not per stream.",
            "bg_color": "#5252E0"
        },
        {
            "type": "standard",
            "headline": "Here's the full breakdown — swipe through:",
            "body": "→ What sync licensing actually is\n→ Who's involved and what they each do\n→ What placements actually pay",
            "bg_color": "#0A0A20"
        },
        {
            "type": "standard",
            "headline": "The Details",
            "body": "→ The two licences in every single deal\n→ What music supervisors actually look for\n→ What \"sync-ready\" means for your catalogue",
            "bg_color": "#5252E0"
        },
        {
            "type": "standard",
            "headline": "The African opportunity right now",
            "body": "→ How to get started\n\nThis is the foundation. Everything else builds on it.",
            "bg_color": "#0A0A20"
        },
        {
            "type": "standard",
            "headline": "Save this.",
            "body": "Share it with a composer who needs to know.",
            "bg_color": "#5252E0"
        }
    ]
}

def main():
    base_path = r"c:\Users\infon\Documents\Claude Code\Projects\syncmaster-marketing-1.0\carousel"
    theme_path = os.path.join(base_path, "styles", "linkedin_space_grotesk.json")
    output_dir = os.path.join(base_path, "exports")
    output_path = os.path.join(output_dir, "IG-EDU-01-test.pptx")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    engine = AestheticEngine(theme_path)
    engine.generate(content, output_path)

if __name__ == "__main__":
    main()
