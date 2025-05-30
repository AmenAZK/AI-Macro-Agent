import os
from pathlib import Path
import numpy as np
import cv2
from macro_ai_agent.vision.processor import VisionProcessor
import logging

def create_test_image():
    """Create a simple test image with some UI elements"""
    # Create a white background
    image = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw a button
    cv2.rectangle(image, (50, 50), (150, 100), (0, 120, 255), -1)
    cv2.putText(image, "Button", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Draw an input field
    cv2.rectangle(image, (50, 150), (250, 200), (200, 200, 200), -1)
    cv2.putText(image, "Input Field", (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Draw some text
    cv2.putText(image, "Test Application", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Save the image
    Path("input/images").mkdir(parents=True, exist_ok=True)
    cv2.imwrite("input/images/test_ui.png", image)
    return "test_ui.png"

def test_vision_processor():
    """Test the vision processor with a simple UI image"""
    try:
        # Create test image
        print("\n1. Creating test image...")
        image_file = create_test_image()
        print(f"Test image created: {image_file}")
        
        # Initialize vision processor
        processor = VisionProcessor()
        
        # Test image processing
        print("\n2. Testing image processing...")
        image_path = Path("input/images") / image_file
        features = processor.process_image(image_path)
        
        # Print results
        print("\nExtracted Features:")
        print(f"- Layout sections: {len(features['layout']['sections'])}")
        print(f"- Dominant colors: {len(features['colors']['dominant_colors'])}")
        print(f"- Text elements: {len(features['text'])}")
        print(f"- UI components: {len(features['components'])}")
        
        # Test specific features
        print("\n3. Testing specific features...")
        
        # Test color extraction
        colors = features['colors']['dominant_colors']
        print(f"Color scheme: {features['colors']['color_scheme']}")
        
        # Test text extraction
        text_elements = features['text']
        print(f"Found text elements: {[elem['text'] for elem in text_elements]}")
        
        # Test layout analysis
        layout = features['layout']
        print(f"Grid structure: {layout['grid_structure']}")
        print(f"Symmetry: {layout['symmetry']}")
        
        print("\nVision processing test completed successfully!")
        
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
    test_vision_processor() 