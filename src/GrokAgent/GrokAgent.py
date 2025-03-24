import os
import json
import yaml
from datetime import datetime

class GrokAgent:
    def __init__(self):
        with open("F:/gro_Grok_Template/config/dev_config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

    def scrape_data(self, chat_input):
        keywords = self.config["data"]["keywords"]
        filtered = {k: v for k, v in chat_input.items() if any(kw in str(v).lower() for kw in keywords)}
        state_file = "F:/gro_Grok_Template/data/historical/state.json"
        state = self.load_state()
        # Explicitly update input if present in chat_input
        if "input" in filtered:
            state["input"] = filtered["input"]
        state["progress"] = "Updated on " + datetime.now().isoformat()
        with open(state_file, "w") as f:
            json.dump(state, f)

    def load_state(self):
        state_file = "F:/gro_Grok_Template/data/historical/state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                return {}
        return {}

if __name__ == "__main__":
    agent = GrokAgent()
    chat = {"input": "Project task: Setup gro_Grok"}
    agent.scrape_data(chat)
    print(agent.load_state())