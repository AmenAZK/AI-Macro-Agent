import requests
import json
import base64
from typing import Dict, Any, List, Optional
import os
from PIL import Image
import io
import time

class LLMClient:
    def __init__(self, config: dict):
        self.config = config
        self.api_url = config["llm"]["api_url"]
        self.model = config["llm"]["model"]
        self.temperature = config["llm"]["temperature"]
        self.max_tokens = config["llm"]["max_tokens"]

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _make_request(self, prompt: str) -> str:
        """Make a request to the LLM API."""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Error making LLM request: {e}")
            return ""

    def analyze_image_and_goal(self, image_path: str, goal: str, rules: str) -> Dict:
        """Analyze the image and goal to generate a plan."""
        prompt = f"""As an AI assistant, analyze this image and goal to create a development plan.

Image: {image_path}
Goal: {goal}

Rules to follow:
{rules}

Please provide:
1. Key visual elements to implement
2. Technical requirements
3. Step-by-step implementation plan
4. Potential challenges and solutions

Format your response as a JSON object with these keys:
{{
    "visual_elements": [],
    "technical_requirements": [],
    "implementation_steps": [],
    "challenges": []
}}"""

        response = self._make_request(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "visual_elements": [],
                "technical_requirements": [],
                "implementation_steps": [],
                "challenges": []
            }

    def generate_cursor_prompt(self, analysis: Dict, rules: str) -> str:
        """Generate a prompt for Cursor IDE."""
        prompt = f"""As a developer, help me implement this design based on the analysis.

Analysis:
{json.dumps(analysis, indent=2)}

Rules to follow:
{rules}

Please provide:
1. Initial code structure
2. Key components to implement
3. Specific implementation details
4. Any questions or clarifications needed

Format your response as a clear, actionable prompt that I can use to guide the implementation."""

        return self._make_request(prompt)

    def generate_follow_up(self, goal: str, current_result: str, evaluation: Dict, rules: str) -> str:
        """Generate a follow-up prompt based on the current result and evaluation."""
        prompt = f"""Based on the current implementation and evaluation, help me improve the code.

Goal: {goal}
Current Result: {current_result}
Evaluation: {json.dumps(evaluation, indent=2)}

Rules to follow:
{rules}

Please provide:
1. What needs to be improved
2. Specific code changes needed
3. Additional considerations
4. Next steps

Format your response as a clear, actionable prompt that I can use to guide the improvements."""

        return self._make_request(prompt)

    def evaluate_result(self, goal: str, result: str, rules: str) -> Dict:
        """Evaluate the current result against the goal and rules."""
        prompt = f"""Evaluate this implementation against the goal and rules.

Goal: {goal}
Current Result: {result}

Rules to follow:
{rules}

Please evaluate:
1. Visual match with design
2. Technical implementation
3. Rule compliance
4. Overall success

Format your response as a JSON object with these keys:
{{
    "visual_match_score": 0-100,
    "technical_score": 0-100,
    "rule_compliance_score": 0-100,
    "overall_score": 0-100,
    "success": true/false,
    "feedback": "",
    "improvements_needed": []
}}"""

        response = self._make_request(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "visual_match_score": 0,
                "technical_score": 0,
                "rule_compliance_score": 0,
                "overall_score": 0,
                "success": False,
                "feedback": "Error evaluating result",
                "improvements_needed": []
            }

    def get_current_result(self) -> str:
        """Get the current result from the implementation."""
        # This would need to be implemented based on how you're tracking the current state
        # For now, returning a placeholder
        return "Current implementation state"

    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response from the LLM with optional context."""
        full_prompt = self._build_prompt(prompt, context)
        
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "temperature": self.config["temperature"],
                "max_tokens": self.config["max_tokens"]
            }
        )
        response.raise_for_status()
        return response.json()["response"]

    def _build_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build a prompt with context and system instructions."""
        system_instructions = """
        You are an AI assistant that helps break down tasks into executable steps.
        For each task:
        1. Break it down into clear, sequential steps
        2. Consider potential errors and edge cases
        3. Provide specific, actionable instructions
        4. Include verification steps
        """
        
        if context:
            context_str = f"\nContext:\n{json.dumps(context, indent=2)}"
        else:
            context_str = ""
            
        return f"{system_instructions}\n{context_str}\nTask: {prompt}\nResponse:"

    def break_down_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Break down a task into executable steps."""
        prompt = f"Break down this task into specific steps: {task}"
        response = self.generate_response(prompt, context)
        
        # Parse the response into structured steps
        # This is a simple implementation - you might want to make it more robust
        steps = []
        for line in response.split('\n'):
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                steps.append({
                    "description": line.strip(),
                    "status": "pending",
                    "result": None
                })
        return steps

    def analyze_feedback(self, feedback: Dict[str, Any], task: str) -> Dict[str, Any]:
        """Analyze feedback and determine next steps."""
        prompt = f"""
        Analyze this feedback and determine if the task was successful or needs adjustment.
        Task: {task}
        Feedback: {json.dumps(feedback, indent=2)}
        """
        response = self.generate_response(prompt)
        return {
            "analysis": response,
            "success": "success" in response.lower(),
            "suggestions": self._extract_suggestions(response)
        }

    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract specific suggestions from the LLM response."""
        suggestions = []
        for line in response.split('\n'):
            if line.strip().startswith(('-', '*', '•')):
                suggestions.append(line.strip()[1:].strip())
        return suggestions

if __name__ == "__main__":
    # Example usage
    print(generate_response("Write a Python function that prints 'hi'")) 