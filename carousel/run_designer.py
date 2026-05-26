import os
import json
import argparse
from scripts.calendar_connector import CalendarConnector
from copy_mapper import CopyMapper
from engine_v3 import AestheticEngine

def main():
    parser = argparse.ArgumentParser(description="SyncMaster Designer Agent Orchestrator")
    parser.add_argument("--id", help="The Post ID from the calendar (e.g., IG-EDU-01)")
    parser.add_argument("--style", default="syncmaster", help="Theme name (syncmaster or midnight_minimal)")
    args = parser.parse_args()

    # Paths
    BASE_DIR = "C:/Users/infon/Documents/Claude Code/Projects/syncmaster-marketing-1.0"
    CAL_PATH = os.path.join(BASE_DIR, "syncmaster-content-calendar.html")
    CB_PATH = os.path.join(BASE_DIR, "copy-bank-m2.html")
    STYLE_PATH = os.path.join(BASE_DIR, "carousel/styles", f"{args.style}.json")
    OUTPUT_PATH = os.path.join(BASE_DIR, "carousel/exports", f"automated_{args.id}_{args.style}.pptx")

    print(f"🚀 Starting Designer Agent for Post: {args.id}...")

    # 1. Connect to Calendar
    print("📡 Fetching copy from bank...")
    conn = CalendarConnector(CAL_PATH, CB_PATH)
    raw_copy = conn.get_copy(args.id)
    
    if not raw_copy:
        print(f"❌ Error: Could not find copy for ID {args.id}")
        return

    # 2. Map Copy to Slides
    print("🧠 Mapping copy to design system...")
    mapper = CopyMapper({})
    content_json = mapper.map_to_slides(raw_copy, topic=args.id)

    # 3. Generate Aesthetic Asset
    print(f"🎨 Generating PPTX with style: {args.style}...")
    engine = AestheticEngine(STYLE_PATH)
    engine.generate(content_json, OUTPUT_PATH)

    print(f"✅ Success! Asset saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
