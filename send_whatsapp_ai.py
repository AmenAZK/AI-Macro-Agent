import pyautogui
import time
import keyboard
from PIL import Image

def find_color_on_screen(target_rgb, tolerance=20):
    """
    Captures the screen and searches for a pixel matching the target RGB color
    within a given tolerance. Returns the (x, y) coordinates if found, otherwise None.
    """
    try:
        screenshot = pyautogui.screenshot()
        width, height = screenshot.size
        print(f"Captured screenshot with size: {width}x{height}") # Debugging print
        for x in range(0, width, 5): # Step by 5 pixels for faster scanning
            for y in range(0, height, 5): # Step by 5 pixels for faster scanning
                r, g, b = screenshot.getpixel((x, y))
                if all(abs(c1 - c2) < tolerance for c1, c2 in zip((r, g, b), target_rgb)):
                    # Refine search around the found coordinate
                    for sub_x in range(max(0, x-5), min(width, x+5)):
                        for sub_y in range(max(0, y-5), min(height, y+5)):
                             sr, sg, sb = screenshot.getpixel((sub_x, sub_y))
                             if all(abs(c1 - c2) < tolerance for c1, c2 in zip((sr, sg, sb), target_rgb)):
                                print(f"Found color at: {sub_x},{sub_y}") # Debugging print
                                return sub_x, sub_y
        print("Color not found on screen.") # Debugging print
        return None
    except Exception as e:
        print(f"Error during screen color search: {e}")
        return None


def send_message_to_contact(contact_name, message):
    """
    Automates opening browser search, typing contact name, clicking highlight,
    typing message, and sending it via keyboard simulation.
    """
    print(f"Attempting to send message to '{contact_name}'...") # Debugging print

    # Make sure the target application (WhatsApp Web) is open and focused!
    # You might need a mechanism here to switch focus if it's not already focused.
    print("Assuming WhatsApp Web is already open and focused...") # Debugging message
    time.sleep(3) # Give a little time to ensure the window is ready

    # Open browser search (works in most browsers)
    print("Pressing Ctrl+F...") # Debugging print
    keyboard.press_and_release('ctrl+f')
    time.sleep(1) # Give browser search time to appear

    # Type the contact name into the search bar
    print(f"Typing contact name: '{contact_name}'") # Debugging print
    keyboard.write(contact_name)
    time.sleep(2) # Give search results time to appear

    # --- Find the orange highlight ---
    # You might need to adjust this RGB and tolerance based on your browser/OS.
    # Use a color picker tool on a screenshot of the highlight to get the exact RGB.
    orange_rgb = (255, 192, 47) # Common Chrome highlight color
    print(f"Searching for highlight color {orange_rgb}...") # Debugging print
    coords = find_color_on_screen(orange_rgb, tolerance=30) # Increased tolerance slightly

    if coords:
        print(f"Found highlight at coordinates: {coords}") # Debugging print
        # Click the found coordinates
        pyautogui.click(coords[0], coords[1])
        time.sleep(1.5) # Give chat time to load

        # Close the browser search bar (usually Esc key)
        print("Pressing Esc to close search bar...") # Debugging print
        keyboard.press('esc')
        time.sleep(0.5)

        # Type the message
        print(f"Typing message: '{message}'") # Debugging print
        keyboard.write(message)
        time.sleep(1)

        # Press Enter to send the message
        print("Pressing Enter to send message...") # Debugging print
        keyboard.press('enter')
        time.sleep(1)

        print("Message sending sequence completed.") # Debugging print
    else:
        print("Could not find the highlighted contact on the screen. Message not sent.") # Debugging print
        print("Possible issues: WhatsApp Web not focused, contact name not found, or highlight color is different.")


# --- EDIT THESE VARIABLES ---
# Make sure the contact name matches exactly how it appears in WhatsApp Web
contact_to_message = "Mohamed"
message_content = "Hello! This is a test message from the AI agent using screen search."

# --- Run the function ---
if __name__ == "__main__":
     # Before running, ensure WhatsApp Web is open and the browser window is active!
     print("Starting WhatsApp automation script...")
     send_message_to_contact(contact_to_message, message_content)
     print("Script finished.")