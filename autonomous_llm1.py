import json
import time
import os
import sys
import argparse
from macro_ai_agent.typer import CursorTyper
from macro_ai_agent.llm_client import LLMClient

class AutonomousLLM1:
    def __init__(self):
        # Load configuration
        with open("macro_ai_agent/config.json", "r") as f:
            self.config = json.load(f)
        
        # Initialize components
        self.typer = CursorTyper(self.config)
        self.llm = LLMClient(self.config)
        
        # Create goals directory if it doesn't exist
        self.goals_dir = "goals"
        os.makedirs(self.goals_dir, exist_ok=True)
        
    def get_next_goal_number(self) -> int:
        """Get the next available goal number."""
        existing_goals = [f for f in os.listdir(self.goals_dir) if f.startswith("Goal") and f.endswith(".txt")]
        if not existing_goals:
            return 0
        numbers = [int(f[4:-4]) for f in existing_goals]  # Extract numbers from "GoalX.txt"
        return max(numbers) + 1 if numbers else 0
        
    def create_goal_file(self, task: str, action: str, content: str, context: str) -> str:
        """Create a new goal file with the next available number."""
        goal_number = self.get_next_goal_number()
        filename = f"Goal{goal_number}.txt"
        filepath = os.path.join(self.goals_dir, filename)
        
        goal_content = f"""Task: {task}
Action: {action}
Content: {content}
Context: {context}"""
        
        with open(filepath, 'w') as f:
            f.write(goal_content)
            
        return filepath
        
    def read_goal(self, goal_file: str) -> dict:
        """Read and parse the goal file."""
        with open(goal_file, 'r') as f:
            content = f.read()
            
        # Parse the goal file
        goal = {}
        for line in content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                goal[key.strip()] = value.strip()
        return goal
    
    def execute_goal(self, goal: dict):
        """Execute the goal using LLM1's capabilities."""
        print(f"\n🤖 LLM1 is executing task: {goal.get('Task', 'Unknown task')}")
        print(f"📝 Context: {goal.get('Context', 'No context provided')}")
        
        # Simulate LLM1's thought process
        print("\n🤔 LLM1's thought process:")
        print("1. Analyzing the task...")
        time.sleep(1)
        print("2. Planning the execution...")
        time.sleep(1)
        print("3. Preparing to act as a human user...")
        time.sleep(1)
        
        # Execute the action
        action = goal.get('Action', '').lower()
        content = goal.get('Content', '')
        
        print(f"\n🎯 Executing action: {action}")
        print(f"📝 Content: {content}")
        
        if action == 'type_to_google':
            print("\n🔍 Opening Google and typing search query...")
            self.typer.type_to_google(content)
            
        elif action == 'type_to_cursor':
            print("\n💻 Opening Cursor IDE and typing...")
            self.typer.type_to_cursor(content)
            
        elif action == 'type_to_notes':
            print("\n📝 Opening Notes and typing...")
            self.typer.type_to_notes(content)
            
        else:
            print(f"❌ Unknown action: {action}")
            return
        
        print("\n✅ Task completed!")
        print("LLM1 has successfully executed the task as if it were a human user.")

    def execute_goal_sequence(self, goal_files: list):
        """Execute multiple goals in sequence."""
        for goal_file in goal_files:
            if not os.path.exists(goal_file):
                print(f"❌ Error: Goal file {goal_file} not found")
                continue
                
            print(f"\n📝 Executing goal file: {goal_file}")
            goal = self.read_goal(goal_file)
            self.execute_goal(goal)
            
            # Only wait if it's not the last goal
            if goal_file != goal_files[-1]:
                time.sleep(2)  # Wait 2 seconds between goals

def main():
    parser = argparse.ArgumentParser(description='Run autonomous LLM tasks')
    parser.add_argument('--goals', nargs='+', help='List of goal files to execute in sequence')
    args = parser.parse_args()

    llm1 = AutonomousLLM1()
    
    try:
        if args.goals:
            # Execute multiple goals in sequence
            llm1.execute_goal_sequence(args.goals)
        else:
            # Create new goal (existing behavior)
            print("\n📝 Create a new goal:")
            task = input("Task description: ")
            action = input("Action (type_to_google/type_to_cursor/type_to_notes): ")
            content = input("Content to type: ")
            context = input("Context: ")
            
            goal_file = llm1.create_goal_file(task, action, content, context)
            print(f"\n✅ Created goal file: {goal_file}")
            
            goal = llm1.read_goal(goal_file)
            llm1.execute_goal(goal)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 