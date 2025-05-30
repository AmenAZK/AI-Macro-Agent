import os
import json
import glob
from typing import List, Dict, Optional
from .llm_client import LLMClient
from .typer import CursorTyper
from .memory import MemoryManager
from datetime import datetime
import time

def load_rules(rules_file: str) -> str:
    """Load rules from the specified file."""
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def get_example_images(examples_dir: str) -> List[str]:
    """Get all image files from the examples directory."""
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif']:
        image_files.extend(glob.glob(os.path.join(examples_dir, ext)))
    return image_files

class MacroAgent:
    def __init__(self, config_path: str = "config.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize components
        self.llm_client = LLMClient(self.config)
        self.typer = CursorTyper(self.config)
        self.memory = MemoryManager(self.config)
        
        # Create necessary directories
        os.makedirs(self.config["paths"]["input"]["designs"], exist_ok=True)
        os.makedirs(self.config["paths"]["input"]["specs"], exist_ok=True)
        os.makedirs(self.config["paths"]["results_dir"], exist_ok=True)
        
        # Load rules
        self.rules = load_rules(self.config["paths"]["rules_file"])

    def run_image_task(self, image_path: str, goal: str) -> Dict:
        """Run a task based on an image and goal."""
        # Get example images for context
        example_images = get_example_images(self.config["paths"]["input"]["designs"])
        
        # Analyze image and goal
        analysis = self.llm_client.analyze_image_and_goal(
            image_path=image_path,
            goal=goal,
            rules=self.rules
        )
        
        # Generate prompt for Cursor
        cursor_prompt = self.llm_client.generate_cursor_prompt(
            analysis=analysis,
            rules=self.rules
        )
        
        # Type the prompt to Cursor
        self.typer.type_to_cursor(cursor_prompt)
        
        # Monitor and evaluate results
        max_attempts = self.config["task"]["max_attempts"]
        current_attempt = 0
        
        while current_attempt < max_attempts:
            # Wait for result
            time.sleep(self.config["task"]["result_wait_time"])
            
            # Get current result
            result = self.llm_client.get_current_result()
            
            # Evaluate result
            evaluation = self.llm_client.evaluate_result(
                goal=goal,
                result=result,
                rules=self.rules
            )
            
            # Save attempt to memory
            self.memory.save_attempt(
                image_path=image_path,
                goal=goal,
                prompt=cursor_prompt,
                result=result,
                evaluation=evaluation
            )
            
            # Check if goal is achieved
            if evaluation["success"]:
                self.save_task_result(image_path, goal, result, evaluation)
                return {
                    "success": True,
                    "result": result,
                    "evaluation": evaluation
                }
            
            # Generate follow-up prompt if needed
            if current_attempt < max_attempts - 1:
                follow_up = self.llm_client.generate_follow_up(
                    goal=goal,
                    current_result=result,
                    evaluation=evaluation,
                    rules=self.rules
                )
                self.typer.type_to_cursor(follow_up)
            
            current_attempt += 1
        
        # If we get here, we've exceeded max attempts
        return {
            "success": False,
            "result": result,
            "evaluation": evaluation
        }

    def save_task_result(self, image_path: str, goal: str, result: str, evaluation: Dict):
        """Save the final task result."""
        result_data = {
            "image_path": image_path,
            "goal": goal,
            "result": result,
            "evaluation": evaluation,
            "rules_applied": self.rules
        }
        
        result_file = os.path.join(
            self.config["paths"]["results_dir"],
            f"result_{int(time.time())}.json"
        )
        
        with open(result_file, 'w') as f:
            json.dump(result_data, f, indent=2)

def main():
    agent = MacroAgent()
    print("🤖 AI Macro Agent initialized!")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            print("\nPlease provide:")
            print("\nAvailable example images:")
            example_images = get_example_images(agent.config["paths"]["input"]["designs"])
            for i, img in enumerate(example_images, 1):
                print(f"{i}. {os.path.basename(img)}")
            
            image_path = input("\nImage path (or 'exit'): ")
            if image_path.lower() == 'exit':
                break
                
            goal = input("Goal: ")
            
            if agent.run_image_task(image_path, goal):
                print("Task completed successfully!")
            else:
                print("Task did not achieve 100% success.")
                
    except KeyboardInterrupt:
        print("\nExiting AI Macro Agent...")

if __name__ == "__main__":
    main() 