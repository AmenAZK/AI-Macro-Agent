import time
from macro_ai_agent.typer import CursorTyper
from macro_ai_agent.llm_client import LLMClient
import json

def simulate_human_typing():
    # Load configuration
    with open("macro_ai_agent/config.json", "r") as f:
        config = json.load(f)
    
    # Initialize components
    typer = CursorTyper(config)
    llm = LLMClient(config)
    
    print("🤖 Starting typing simulation...")
    print("Press Ctrl+C to exit")
    
    while True:
        try:
            print("\nWhere would you like to type?")
            print("1. Cursor IDE")
            print("2. Google Search")
            print("3. Notes")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ")
            
            if choice == "4":
                break
                
            # Get the content to type
            content = input("\nWhat would you like to type? ")
            
            if choice == "1":
                print("\n🎯 Typing into Cursor IDE...")
                typer.type_to_cursor(content)
                
            elif choice == "2":
                print("\n🔍 Typing into Google Search...")
                # Simulate opening Google
                typer.focus_cursor_chat()  # This would be replaced with actual Google focus
                typer.type_text(content)
                typer.send_message()
                
            elif choice == "3":
                print("\n📝 Typing into Notes...")
                # Simulate opening Notes
                typer.focus_cursor_chat()  # This would be replaced with actual Notes focus
                typer.type_text(content)
                
            else:
                print("Invalid choice. Please try again.")
                continue
            
            # Simulate LLM1's thought process
            print("\n🤔 LLM1's thought process:")
            print("1. Analyzing the input...")
            time.sleep(1)
            print("2. Planning the typing pattern...")
            time.sleep(1)
            print("3. Simulating human-like behavior...")
            time.sleep(1)
            
            # Show what was typed
            print(f"\n✍️ Typed: {content}")
            
            # Ask if user wants to continue
            if input("\nContinue? (y/n): ").lower() != 'y':
                break
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    simulate_human_typing() 