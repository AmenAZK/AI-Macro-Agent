import os
import shutil

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def move_file(src, dst):
    if os.path.exists(src):
        shutil.move(src, dst)

# Create new directory structure
directories = [
    'input/images',
    'input/tasks',
    'macro_ai_agent/vision',
    'macro_ai_agent/planner',
    'macro_ai_agent/executor',
    'macro_ai_agent/memory',
    'output/projects',
    'output/logs',
    'output/results',
    'goals',
    'rules'
]

for directory in directories:
    create_directory(directory)

# Move files to their new locations
moves = [
    # Move test files to appropriate directories
    ('test_vision.py', 'macro_ai_agent/vision/test_vision.py'),
    ('test_agent.py', 'macro_ai_agent/test_agent.py'),
    ('test_macro_agent.py', 'macro_ai_agent/test_macro_agent.py'),
    ('test_typing_simulation.py', 'macro_ai_agent/executor/test_typing_simulation.py'),
    ('test_image_task.py', 'macro_ai_agent/vision/test_image_task.py'),
    ('test_autonomous_llm.py', 'macro_ai_agent/planner/test_autonomous_llm.py'),
    ('test_ollama.py', 'macro_ai_agent/planner/test_ollama.py'),
    
    # Move task files
    ('goal.txt', 'input/tasks/goal.txt'),
    ('send_whatsapp_ai.py', 'macro_ai_agent/executor/send_whatsapp_ai.py'),
    ('autonomous_llm1.py', 'macro_ai_agent/planner/autonomous_llm1.py'),
    
    # Move memory and results
    ('memory.json', 'memory.json'),
    ('task_results/*', 'output/results/'),
]

for src, dst in moves:
    if '*' in src:
        # Handle wildcard moves
        src_dir = os.path.dirname(src)
        if os.path.exists(src_dir):
            for file in os.listdir(src_dir):
                if file != '.' and file != '..':
                    move_file(os.path.join(src_dir, file), os.path.join(dst, file))
    else:
        move_file(src, dst)

print("Repository reorganization complete!") 