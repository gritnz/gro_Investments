import sys
import os
sys.path.append("F:/gro_Grok_Template")
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
try:
    from src.GrokAgent.GrokAgent import GrokAgent
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Received POST request")
        state_file = "F:/gro_Grok_Template/data/historical/state.json"
        try:
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length).decode())
            print(f"Data received: {data}")
            agent = GrokAgent()
            agent.scrape_data(data)
            print("Data scraped")

            # Load state
            try:
                with open(state_file, "r") as f:
                    state = json.load(f)
            except FileNotFoundError:
                state = {"history": [], "chat_summaries": [], "wip": {}, "related_data": {}, "progress": "", "latest_input": ""}

            # Parse e-value tag
            latest_input = data.get("input", "")
            weight = 2  # Default to #e2 (medium)
            for i in range(1, 6):
                if f"#e{i}" in latest_input:
                    weight = i
                    break

            # Add to history with weight
            new_entry = {
                "input": latest_input,
                "timestamp": datetime.now().isoformat(),
                "weight": weight
            }
            state["history"].append(new_entry)

            # Sort by weight (desc), then timestamp (desc), keep top 5
            if len(state["history"]) > 5:
                state["history"] = sorted(state["history"], key=lambda x: (x["weight"], x["timestamp"]), reverse=True)[:5]
            state["latest_input"] = latest_input
            state["progress"] = f"Updated on {datetime.now().isoformat()}"

            # Save state
            with open(state_file, "w") as f:
                json.dump(state, f, indent=2)
            print(f"State saved to: {os.path.abspath(state_file)}")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved"}).encode())
        except Exception as e:
            print(f"Error in POST: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print("Server running at localhost:8000")
httpd.serve_forever()