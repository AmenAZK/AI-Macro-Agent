import os
from pathlib import Path
from macro_ai_agent.agent import MacroAgent
import logging

def setup_test_environment():
    """Create necessary directories and test files"""
    # Create directories if they don't exist
    Path("input/images").mkdir(parents=True, exist_ok=True)
    Path("input/tasks").mkdir(parents=True, exist_ok=True)
    Path("output/logs").mkdir(parents=True, exist_ok=True)
    Path("output/projects").mkdir(parents=True, exist_ok=True)
    Path("output/results").mkdir(parents=True, exist_ok=True)

def create_test_task():
    """Create a simple test task file"""
    test_task = """Task: Create a Simple Calculator App

Visual Reference: calculator_design.png

Requirements:
1. Frontend:
   - Clean, modern calculator interface
   - Basic arithmetic operations
   - Clear and delete functionality
   - Responsive design

2. Features:
   - Addition, subtraction, multiplication, division
   - Clear button
   - Delete button
   - Error handling for invalid operations

Success Criteria:
- Calculator matches the design in the image
- All basic operations work correctly
- Mobile responsive
- Clean error handling

Constraints:
- Must use React for frontend
- Must include unit tests
- Must follow accessibility guidelines
"""
    
    with open("input/tasks/test_calculator.txt", "w") as f:
        f.write(test_task)

def test_agent():
    """Test the AI Macro Agent with a simple task"""
    try:
        # Setup environment
        setup_test_environment()
        create_test_task()
        
        # Initialize agent
        agent = MacroAgent()
        
        # Test task processing
        print("\n1. Testing task processing...")
        task_plan = agent.process_input("test_calculator.txt")
        print(f"Task plan created: {bool(task_plan)}")
        
        # Test task execution
        print("\n2. Testing task execution...")
        agent.execute_task("test_calculator.txt")
        
        # Test task status
        print("\n3. Testing task status...")
        status = agent.get_task_status("test_calculator.txt")
        print(f"Task status: {status}")
        
        # Test task listing
        print("\n4. Testing task listing...")
        tasks = agent.list_tasks()
        print(f"Total tasks: {len(tasks)}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run tests
    test_agent() 