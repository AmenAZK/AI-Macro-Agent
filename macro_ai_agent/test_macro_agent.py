import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from macro_ai_agent.main import MacroAgent

def test_simple_task():
    agent = MacroAgent()
    
    # Test task: Create a simple Python function
    task = "Create a Python function that adds two numbers and prints the result"
    
    print("\n🔍 Testing Macro Agent with task:", task)
    print("=" * 50)
    
    success = agent.run_task(task)
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")

if __name__ == "__main__":
    test_simple_task() 