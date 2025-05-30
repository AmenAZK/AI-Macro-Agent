# AI Macro Agent 🤖

An autonomous AI agent that can understand and execute complex tasks by analyzing images and text instructions, working continuously until goals are achieved. The agent can control your PC, develop applications, handle communications, and perform tasks just like a human would.

## 🌟 Core Features

- **Autonomous Task Execution**: Works independently until goals are achieved
- **Multi-Modal Understanding**: Processes both images and text instructions
- **PC Control**: Full system automation and control
- **Web Development**: Can create and modify websites/apps based on visual examples
- **Communication**: Handles messaging and email autonomously
- **Project Building**: Can create and manage entire projects
- **Continuous Learning**: Improves from each task execution

## 🚀 How It Works

### Input System
1. **Image Input** (`input/images/`):
   - Screenshots of desired UI/UX
   - Example layouts
   - Reference designs
   - Target application states

2. **Task Instructions** (`input/tasks/`):
   - Detailed requirements in .txt files
   - Step-by-step instructions
   - Success criteria
   - Constraints and preferences

### Processing Flow
1. **Input Analysis**:
   - Image processing for visual requirements
   - Text analysis for functional requirements
   - Context understanding and goal extraction

2. **Task Planning**:
   - Breaking down goals into actionable steps
   - Creating execution strategy
   - Resource allocation

3. **Execution**:
   - Autonomous task performance
   - Progress monitoring
   - Error handling and recovery
   - Continuous improvement

### Output System
- Generated code and applications
- Task execution logs
- Progress reports
- Success/failure metrics

## 📁 Project Structure

```
ai-macro-agent/
├── input/
│   ├── images/          # Visual examples and references
│   └── tasks/           # Task instruction files
├── macro_ai_agent/      # Core agent implementation
│   ├── vision/          # Image processing modules
│   ├── planner/         # Task planning and execution
│   ├── executor/        # Task execution modules
│   └── memory/          # Learning and memory systems
├── output/
│   ├── projects/        # Generated projects
│   ├── logs/           # Execution logs
│   └── results/        # Task results
├── goals/              # Goal definitions
├── rules/              # Execution rules
└── memory.json        # Persistent memory
```

## 🛠️ Usage Examples

1. **Web Development Task**:
   ```
   input/
   ├── images/
   │   └── website_design.png
   └── tasks/
       └── build_website.txt
   ```
   Content of build_website.txt:
   ```
   Create a responsive website matching the design in website_design.png
   Requirements:
   - Use React for frontend
   - Implement all shown features
   - Ensure mobile responsiveness
   - Add contact form functionality
   ```

2. **Automation Task**:
   ```
   input/
   ├── images/
   │   └── workflow_screenshot.png
   └── tasks/
       └── automate_process.txt
   ```
   Content of automate_process.txt:
   ```
   Automate the process shown in workflow_screenshot.png
   Steps:
   1. Monitor incoming emails
   2. Extract specific data
   3. Update database
   4. Send confirmation
   ```

## 🔧 Making it Better

### Current Capabilities
- Image and text understanding
- Basic task automation
- Web development
- System control
- Communication handling

### Future Improvements
1. **Enhanced Understanding**
   - Better context awareness
   - Improved goal interpretation
   - Advanced visual processing

2. **Extended Capabilities**
   - Mobile app development
   - Database management
   - Cloud service integration
   - Advanced security features

3. **Improved Autonomy**
   - Better decision making
   - Self-improvement capabilities
   - Advanced error recovery
   - Resource optimization

4. **User Interface**
   - Web dashboard
   - Progress monitoring
   - Task management
   - Result visualization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- HuggingFace for providing free AI models
- Ollama for local LLM capabilities
- PyAutoGUI for automation features
- EasyOCR for text recognition

## Required Packages
- openai: For AI language model integration
- pyautogui: For GUI automation
- keyboard: For keyboard input simulation
- easyocr (optional): For OCR capabilities
- opencv-python (optional): For computer vision tasks

## Usage
[Usage instructions will be added as the project develops] 