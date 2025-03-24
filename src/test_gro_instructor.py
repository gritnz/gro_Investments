import sys
import os
sys.path.append("F:/gro_Grok_Template/src")  # Add src to path
from gro_instructor import GroInstructor  # Import the class

def run_test():
    # Create instance
    agent = GroInstructor()
    
    # Test inputs
    inputs = [
        "Hello #e5",
        "Help #e3",
        "Debug #e1",
        "Debug #e1",
        "Debug #e1"
    ]
    
    # Run each input and print response
    for message in inputs:
        reply = agent.respond(message)
        print(f"You: {message}")
        print(f"gro_instructor: {reply}\n")

if __name__ == "__main__":
    run_test()