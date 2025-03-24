import json
from datetime import datetime

class SummarizerAgent:
    def __init__(self):
        self.state_file = "F:/gro_Grok_Template/data/historical/state.json"

    def summarize_and_prune(self, input_text=""):
        # Read the current state
        try:
            with open(self.state_file, "r") as f:
                state = json.load(f)
        except FileNotFoundError:
            state = {"history": [], "chat_summaries": [], "wip": {}, "related_data": {}, "progress": "", "latest_input": ""}
            print(f"State file not found, initializing new state: {state}")

        # Ensure history exists
        if "history" not in state or not isinstance(state["history"], list):
            state["history"] = []

        # Use provided input if given, else fall back to state["input"]
        latest_input = input_text if input_text else state.get("input", "")
        print(f"Latest input from state: {latest_input}")

        # Add the latest input if it’s not empty
        if latest_input:
            state["history"].append({
                "input": latest_input,
                "timestamp": datetime.now().isoformat()
            })
            state["history"] = state["history"][-5:]  # Keep last 5
            state["latest_input"] = latest_input
            state["progress"] = f"Updated on {datetime.now().isoformat()}"
            print(f"Updated history: {state['history']}")

        # Save the updated state
        try:
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2)
            print("Data summarized and pruned successfully")
        except Exception as e:
            print(f"Error writing to state file: {e}")

if __name__ == "__main__":
    summarizer = SummarizerAgent()
    summarizer.summarize_and_prune()