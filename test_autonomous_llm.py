import os
from autonomous_llm1 import AutonomousLLM1
import logging

def test_whatsapp_message():
    """Test the autonomous LLM1 with WhatsApp messaging goal"""
    try:
        # Initialize LLM1
        print("\n1. Initializing Autonomous LLM1...")
        llm1 = AutonomousLLM1()
        
        # Test goal execution
        print("\n2. Executing WhatsApp messaging goal...")
        goal_file = "goals/Goal3.txt"
        
        if not os.path.exists(goal_file):
            print(f"❌ Error: Goal file {goal_file} not found")
            return
            
        print(f"\n📝 Executing goal file: {goal_file}")
        goal = llm1.read_goal(goal_file)
        
        # Print goal details
        print("\nGoal Details:")
        print(f"Task: {goal.get('Task', 'Unknown')}")
        print(f"Action: {goal.get('Action', 'Unknown')}")
        print(f"Content: {goal.get('Content', 'Unknown')}")
        print(f"Context: {goal.get('Context', 'Unknown')}")
        
        # Execute the goal
        llm1.execute_goal(goal)
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run test
    test_whatsapp_message() 