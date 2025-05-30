import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class MemoryManager:
    def __init__(self, config: dict):
        self.config = config
        self.memory_dir = os.path.join(config["paths"]["results_dir"], "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.current_task = None
        self.attempts = []

    def start_task(self, image_path: str, goal: str):
        """Start a new task and initialize memory."""
        self.current_task = {
            "image_path": image_path,
            "goal": goal,
            "start_time": time.time(),
            "attempts": []
        }
        self.attempts = []

    def save_attempt(self, image_path: str, goal: str, prompt: str, result: str, evaluation: Dict):
        """Save an attempt to memory."""
        if not self.current_task:
            self.start_task(image_path, goal)

        attempt = {
            "timestamp": time.time(),
            "prompt": prompt,
            "result": result,
            "evaluation": evaluation
        }
        
        self.attempts.append(attempt)
        self.current_task["attempts"] = self.attempts

        # Save to file
        self._save_to_file()

    def _save_to_file(self):
        """Save current task to a file."""
        if not self.current_task:
            return

        filename = f"task_{int(time.time())}.json"
        filepath = os.path.join(self.memory_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.current_task, f, indent=2)

    def get_task_history(self) -> List[Dict]:
        """Get history of all tasks."""
        history = []
        for filename in os.listdir(self.memory_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.memory_dir, filename)
                with open(filepath, 'r') as f:
                    history.append(json.load(f))
        return sorted(history, key=lambda x: x["start_time"], reverse=True)

    def get_last_attempt(self) -> Optional[Dict]:
        """Get the last attempt from the current task."""
        if not self.attempts:
            return None
        return self.attempts[-1]

    def get_successful_attempts(self) -> List[Dict]:
        """Get all successful attempts from the current task."""
        return [
            attempt for attempt in self.attempts
            if attempt["evaluation"].get("success", False)
        ]

    def clear_current_task(self):
        """Clear the current task from memory."""
        self.current_task = None
        self.attempts = []

class Memory:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.history: List[Dict[str, Any]] = []
        self.current_state: Dict[str, Any] = {}
        self.load_memory()

    def load_memory(self):
        """Load memory from file if it exists."""
        if os.path.exists(self.config["memory"]["save_path"]):
            with open(self.config["memory"]["save_path"], "r") as f:
                data = json.load(f)
                self.history = data.get("history", [])
                self.current_state = data.get("current_state", {})

    def save_memory(self):
        """Save memory to file."""
        with open(self.config["memory"]["save_path"], "w") as f:
            json.dump({
                "history": self.history,
                "current_state": self.current_state
            }, f, indent=2)

    def add_to_history(self, action: str, result: Any, status: str = "success"):
        """Add an action and its result to history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result,
            "status": status
        }
        self.history.append(entry)
        
        # Maintain max history size
        if len(self.history) > self.config["memory"]["max_history"]:
            self.history = self.history[-self.config["memory"]["max_history"]:]
        
        self.save_memory()

    def update_state(self, key: str, value: Any):
        """Update the current state."""
        self.current_state[key] = value
        self.save_memory()

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a value from the current state."""
        return self.current_state.get(key, default)

    def get_recent_history(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get the n most recent history entries."""
        return self.history[-n:] 