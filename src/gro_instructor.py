import json
import os
import sys
from datetime import datetime

class GroInstructor:
    def __init__(self):
        # Use relative paths based on the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.state_file = os.path.join(project_dir, "data", "historical", "state.json")
        self.log_file = os.path.join(project_dir, "data", "historical", "history_log.jsonl")
        # Define responses for keywords and #e1–#e5 tags
        self.responses = {
            "hello": "Hey there! How can I assist you today?",
            "help": "I’m here to guide you—ask me anything about the project!",
            "debug": "Let’s troubleshoot—what’s the issue?",
            "summarize": "Summarizing recent history—check state.json!",
            "#e1": "Debug info: Low relevance, focusing on setup or minor issues.",
            "#e2": "Plan update: I’ll help outline the next steps for the project.",
            "#e3": "Action required: Let’s execute a specific task or command.",
            "#e4": "Command suggestion: I’ll provide a command to run.",
            "#e5": "User interaction: I’ll respond directly to your query."
        }

    def respond(self, message):
        state = self.load_state()
        weight = 2  # Default #e2
        valid_tags = [f"#e{i}" for i in range(1, 6)]
        found_weight = None
        found_tag = None

        # Check for #e1–#e5 tags
        for i in range(5, 0, -1):
            tag = f"#e{i}"
            if tag in message:
                found_weight = i
                found_tag = tag
                break

        if found_weight is not None:
            weight = found_weight
        elif any(tag not in valid_tags and "#e" in tag for tag in message.split()):
            print("Warning: Invalid #e tag detected—using default #e2.")

        new_entry = {
            "input": message,
            "timestamp": datetime.now().isoformat(),
            "weight": weight
        }

        # Log every entry
        self.log_entry(new_entry)

        # Update history
        if "history" not in state or not isinstance(state["history"], list):
            state["history"] = []
        state["history"].append(new_entry)
        state["history"] = sorted(state["history"], key=lambda x: (x.get("timestamp", ""), x.get("weight", 2)), reverse=True)[:5]

        state["latest_input"] = message
        state["progress"] = f"Updated on {datetime.now().isoformat()}"

        # Track input count and auto-summarize every 10 inputs
        if "input_count" not in state:
            state["input_count"] = 0
        state["input_count"] += 1
        if state["input_count"] % 10 == 0 or "summarize" in message.lower():
            self.summarize_history(state)

        self.save_state(state)

        # Check for #e1–#e5 responses first
        if found_tag and found_tag in self.responses:
            # Add context from recent history
            recent_history = self.get_recent_history(state)
            response = f"{self.responses[found_tag]}\nRecent context: {recent_history}"
            return response

        # Check for keyword responses
        for key, value in self.responses.items():
            if key.startswith("#e"):
                continue  # Skip #e tags, already handled
            if key in message.lower():
                # Add context from recent history
                recent_history = self.get_recent_history(state)
                return f"{value}\nRecent context: {recent_history}"
        return "I’m not sure—can you clarify?"

    def get_recent_history(self, state):
        """Return a summary of recent history for context."""
        if not state.get("history"):
            return "No recent history available."
        recent_inputs = [entry["input"] for entry in state["history"][:3]]  # Last 3 entries
        return f"Recent inputs: {'; '.join(recent_inputs)}"

    def load_state(self):
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = f.read()
                if not data.strip():
                    return self.default_state()
                return json.loads(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading state.json: {e}. Using default state.")
            return self.default_state()

    def default_state(self):
        return {
            "history": [],
            "chat_summaries": [],
            "wip": {},
            "related_data": {},
            "progress": "",
            "latest_input": "",
            "input_count": 0
        }

    def save_state(self, state):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def log_entry(self, entry):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error logging to {self.log_file}: {e}")

    def summarize_history(self, state):
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()[-10:]  # Last 10 entries
                entries = [json.loads(line.strip()) for line in lines if line.strip()]
        except FileNotFoundError:
            entries = []
            print("No history log found—nothing to summarize.")

        if not entries:
            summary = "No recent history to summarize."
        else:
            weight_counts = {}
            for e in entries:
                w = f"#e{e['weight']}"
                weight_counts[w] = weight_counts.get(w, 0) + 1
            summary = "Recent activity: " + ", ".join(f"{v}x {k}" for k, v in weight_counts.items())

        if "chat_summaries" not in state or not isinstance(state["chat_summaries"], list):
            state["chat_summaries"] = []
        state["chat_summaries"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": summary
        })

if __name__ == "__main__":
    agent = GroInstructor()
    # Check if running interactively (i.e., input is from a terminal)
    if sys.stdin.isatty():
        while True:
            try:
                message = input("You: ")
                reply = agent.respond(message)
                print(f"gro_instructor: {reply}")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break
    else:
        # Non-interactive mode: process one input and exit
        message = input("You: ")
        reply = agent.respond(message)
        print(f"gro_instructor: {reply}")