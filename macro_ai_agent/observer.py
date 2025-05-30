# observer.py
# This module will contain functions to observe the environment (screen, logs, etc.)

import pyautogui
import easyocr
import time
from typing import Dict, Any, List, Optional
import subprocess
import os

class Observer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.reader = None
        if "easyocr" in config["feedback"]["sources"]:
            self.reader = easyocr.Reader(['en'])
        self.last_screenshot_time = 0

    def get_screen_text(self) -> str:
        """Capture screen and extract text using OCR."""
        current_time = time.time()
        if current_time - self.last_screenshot_time < self.config["feedback"]["screenshot_interval"]:
            return ""

        screenshot = pyautogui.screenshot()
        if self.reader:
            results = self.reader.readtext(numpy.array(screenshot))
            return " ".join([text for _, text, _ in results])
        return ""

    def get_terminal_output(self) -> str:
        """Get the last few lines of terminal output."""
        try:
            # This is a placeholder - you'll need to implement actual terminal capture
            return ""
        except Exception as e:
            return f"Error reading terminal: {str(e)}"

    def observe(self) -> Dict[str, Any]:
        """Gather feedback from all configured sources."""
        feedback = {}
        
        if "screen" in self.config["feedback"]["sources"]:
            feedback["screen_text"] = self.get_screen_text()
        
        if "terminal" in self.config["feedback"]["sources"]:
            feedback["terminal_output"] = self.get_terminal_output()
        
        return feedback

    def wait_for_condition(self, condition_func, timeout: int = 30, interval: float = 1.0) -> bool:
        """Wait for a condition to be met, with timeout."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False

    def check_for_errors(self, feedback: Dict[str, Any]) -> List[str]:
        """Check feedback for common error patterns."""
        errors = []
        
        # Check terminal output for error patterns
        if "terminal_output" in feedback:
            output = feedback["terminal_output"].lower()
            error_patterns = ["error:", "exception:", "failed:", "not found"]
            for pattern in error_patterns:
                if pattern in output:
                    errors.append(f"Found error pattern: {pattern}")
        
        return errors

if __name__ == "__main__":
    observe() 