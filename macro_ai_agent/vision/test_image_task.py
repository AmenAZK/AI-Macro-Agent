import os
from macro_ai_agent.main import MacroAgent
import glob

def main():
    # Initialize the agent
    agent = MacroAgent()
    print("🤖 AI Macro Agent initialized!")
    
    # Create test directories if they don't exist
    os.makedirs("input/designs", exist_ok=True)
    os.makedirs("input/specs", exist_ok=True)
    os.makedirs("rules", exist_ok=True)
    
    # Create a sample rules file
    rules_content = """# AI Macro Agent Rules and Goals

## General Rules
- Maintain professional tone and language
- Follow best practices for code organization
- Ensure responsive design principles
- Implement proper error handling

## Design Guidelines
- Match visual elements with 95% accuracy
- Use consistent color schemes
- Maintain proper spacing and alignment
- Ensure accessibility standards

## Development Goals
- Write clean, maintainable code
- Optimize performance
- Include proper documentation
- Follow security best practices

## Success Criteria
- Visual match score > 90%
- Technical implementation score > 85%
- Rule compliance score > 95%
- Overall success score > 90%"""
    
    with open("rules/Notes.txt", "w") as f:
        f.write(rules_content)
    
    print("\n📋 Rules file created at: rules/Notes.txt")
    
    # Get available images
    example_images = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif']:
        example_images.extend(glob.glob(os.path.join("input/designs", ext)))
    
    if not example_images:
        print("\n⚠️ No images found in input/designs directory!")
        print("Please add some images to test with.")
        return
    
    print("\n📸 Available images:")
    for i, img in enumerate(example_images, 1):
        print(f"{i}. {os.path.basename(img)}")
    
    # Get user input
    while True:
        try:
            choice = int(input("\nSelect an image number (or 0 to exit): "))
            if choice == 0:
                break
            if 1 <= choice <= len(example_images):
                image_path = example_images[choice - 1]
                goal = input("\nEnter your goal for this image: ")
                
                print(f"\n🎯 Starting task with goal: {goal}")
                print(f"📸 Using image: {os.path.basename(image_path)}")
                
                # Run the task
                result = agent.run_image_task(image_path, goal)
                
                if result["success"]:
                    print("\n✅ Task completed successfully!")
                    print(f"📊 Evaluation: {result['evaluation']}")
                else:
                    print("\n⚠️ Task did not achieve 100% success.")
                    print(f"📊 Evaluation: {result['evaluation']}")
                
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main() 