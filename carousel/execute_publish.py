"""
execute_publish.py
------------------
Executes the figma_publisher.py plan against Figma using the figma-mcp-go bridge.

Usage:
  python3 execute_publish.py --month 1              # Publish Month 1 posts (real)
  python3 execute_publish.py --month 1 --dry-run    # Preview Month 1 posts only
  python3 execute_publish.py --id IG-EDU-01         # Publish single post
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

# Add parent directory to path so we can import figma_publisher
sys.path.insert(0, str(Path(__file__).resolve().parent))
import figma_publisher


class FigmaMCPClient:
    def __init__(self):
        self.proc = None
        self.req_id = 1

    def connect(self):
        print("Connecting to figma-mcp-go server...")
        self.proc = subprocess.Popen(
            ["npx", "-y", "@vkhanhqui/figma-mcp-go"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Initialize MCP protocol
        self._write_line({
            "jsonrpc": "2.0",
            "id": self.req_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "execute-publish-agent", "version": "1.0"}
            }
        })
        init_resp = self._read_response(self.req_id)
        self.req_id += 1

        # Send initialized notification
        self._write_line({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        })
        print("Connected and initialized successfully.")

    def close(self):
        if self.proc:
            self.proc.terminate()
            self.proc.wait()
            print("figma-mcp-go client closed.")

    def _write_line(self, data):
        line = json.dumps(data) + "\n"
        self.proc.stdin.write(line)
        self.proc.stdin.flush()

    def _read_response(self, expected_id):
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("figma-mcp-go disconnected unexpectedly")
            
            # Skip any blank lines or non-json noise
            line_str = line.strip()
            if not line_str:
                continue
            
            try:
                data = json.loads(line_str)
            except json.JSONDecodeError:
                # Log non-JSON output to stderr/stdout for debugging
                print(f"  [raw stdout]: {line_str}")
                continue

            if data.get("id") == expected_id:
                if "error" in data:
                    raise RuntimeError(f"MCP Error: {data['error']}")
                return data

    def call_tool(self, tool_name, arguments=None):
        if arguments is None:
            arguments = {}
        
        current_id = self.req_id
        self.req_id += 1

        self._write_line({
            "jsonrpc": "2.0",
            "id": current_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        })

        resp = self._read_response(current_id)
        result = resp.get("result", {})
        
        if result.get("isError"):
            error_msg = result.get("content", [{"text": "Unknown error"}])[0].get("text", "Unknown error")
            raise RuntimeError(f"Figma Tool Error calling '{tool_name}': {error_msg}")
        
        content = result.get("content", [])
        if not content:
            return None
        
        text_val = content[0].get("text", "")
        try:
            return json.loads(text_val)
        except json.JSONDecodeError:
            return text_val


def execute_plan(plan, dry_run=False):
    client = None
    if not dry_run:
        client = FigmaMCPClient()
        client.connect()

    try:
        # Get target pages cache
        existing_pages = {}
        if not dry_run:
            meta = client.call_tool("get_pages")
            if meta and "pages" in meta:
                existing_pages = {p["name"].lower(): p["id"] for p in meta["pages"]}

        print(f"\nExecuting plan: {len(plan['posts'])} posts...")
        for post in plan["posts"]:
            pid = post["post_id"]
            figma_page = post["figma_page"]
            ptype = post["type"]
            template = post["template"]
            page_y = post["page_y"]

            print(f"\n👉 Processing {pid} [{ptype}] ({template}) on page '{figma_page}' at y={page_y}...")

            # 1. Page Resolution / Creation
            page_id = None
            if not dry_run:
                page_key = figma_page.lower()
                if page_key not in existing_pages:
                    print(f"  Page '{figma_page}' not found. Creating it...")
                    resp = client.call_tool("add_page", {"name": figma_page})
                    # Refresh pages list to find the ID of the new page
                    meta = client.call_tool("get_pages")
                    existing_pages = {p["name"].lower(): p["id"] for p in meta["pages"]}
                
                page_id = existing_pages.get(page_key)
                print(f"  Navigating to page '{figma_page}' (ID: {page_id})...")
                client.call_tool("navigate_to_page", {"pageId": page_id})

            # 2. Slide / Single Layout Creation
            for slide in post["slides"]:
                slide_num = slide["slide_num"]
                sec_template_id = slide["section_template_id"]
                clone_x = slide["clone_x"]
                role = slide["role"]

                print(f"  Slide {slide_num} ({role}): Cloning template node '{sec_template_id}' to coordinates ({clone_x}, {page_y})...")
                
                if dry_run:
                    for op in slide["text_ops"]:
                        print(f"    [DRY RUN] Set layer '{op['find_by_name']}' -> '{op['set_text'][:40]}...'")
                    continue

                # Clone the slide template frame
                clone_resp = client.call_tool("clone_node", {
                    "nodeId": sec_template_id,
                    "parentId": page_id,
                    "x": clone_x,
                    "y": page_y
                })
                
                if not clone_resp or "id" not in clone_resp:
                    print(f"    [error] Failed to clone slide template {sec_template_id}")
                    continue
                
                cloned_id = clone_resp["id"]
                print(f"    Cloned successfully! New Node ID: {cloned_id}")

                # Rename the cloned slide container for cleaner layers panel
                slide_name = f"{pid} · Slide {slide_num:02d} ({role})" if ptype == "Carousel" else f"{pid} · Single"
                client.call_tool("rename_node", {
                    "nodeId": cloned_id,
                    "name": slide_name
                })

                # Retrieve all text nodes in the clone to find target layers by name
                text_nodes_data = client.call_tool("scan_text_nodes", {"nodeId": cloned_id})
                cloned_text_nodes = {}
                if text_nodes_data and "textNodes" in text_nodes_data:
                    cloned_text_nodes = {node["name"].lower().strip(): node["id"] for node in text_nodes_data["textNodes"]}
                elif isinstance(text_nodes_data, list):
                    cloned_text_nodes = {node["name"].lower().strip(): node["id"] for node in text_nodes_data}
                
                # Perform text substitutions
                for op in slide["text_ops"]:
                    find_name = op["find_by_name"].lower().strip()
                    set_text_val = op["set_text"]

                    if find_name in cloned_text_nodes:
                        target_node_id = cloned_text_nodes[find_name]
                        client.call_tool("set_text", {
                            "nodeId": target_node_id,
                            "text": set_text_val
                        })
                        print(f"    Updated layer '{op['find_by_name']}' -> '{set_text_val[:40]}...'")
                    else:
                        print(f"    [warn] Target text layer '{op['find_by_name']}' not found in cloned node tree")

        print("\n✅ Execution completed successfully.")

    finally:
        if client:
            client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SyncMaster Figma Plan Executor")
    parser.add_argument("--month", type=int, default=1, help="Month to publish (1/2/3)")
    parser.add_argument("--id", dest="post_id", help="Publish a single post by ID")
    parser.add_argument("--template", choices=["dark", "light"], default=None, help="Figma template override")
    parser.add_argument("--dry-run", action="store_true", help="Preview plan and layout choices without writing to Figma")
    args = parser.parse_args()

    # Generate the publishing plan using the standard builder
    plan = figma_publisher.build_publish_plan(month=args.month, post_id=args.post_id, template=args.template)
    
    if args.dry_run:
        print("✨ DRY RUN MODE ACTIVE — NO FIGMA EDITS WILL BE COMMITTED ✨")
    
    execute_plan(plan, dry_run=args.dry_run)
