import keyboard
import pyautogui
import time
import random
from typing import Optional

class CursorTyper:
    def __init__(self, config: dict):
        self.config = config
        self.typing_speed = config["macro_driver"]["typing_speed"]
        self.cursor_shortcut = config["macro_driver"]["cursor_chat_shortcut"]
        self.app_shortcuts = {
            "cursor": "ctrl+shift+l",
            "google": "ctrl+t",  # Open new tab
            "notes": "win+n"     # Windows Notes
        }

    def focus_application(self, app: str):
        """Focus the specified application using its shortcut."""
        if app in self.app_shortcuts:
            keyboard.press_and_release(self.app_shortcuts[app])
            time.sleep(0.5)  # Wait for app to focus

    def type_text(self, text: str, human_like: bool = True):
        """Type text with optional human-like behavior."""
        # Handle special key combinations
        if '{' in text and '}' in text:
            parts = text.split('{')
            for part in parts:
                if '}' in part:
                    key, rest = part.split('}', 1)
                    # Handle special keys
                    if key == 'ctrl+f':
                        keyboard.press_and_release('ctrl+f')
                        time.sleep(0.5)
                    elif key == 'enter':
                        keyboard.press('enter')
                        time.sleep(0.5)
                    # Type the rest of the text
                    if rest:
                        if human_like:
                            self._type_human_like(rest)
                        else:
                            keyboard.write(rest)
                else:
                    if human_like:
                        self._type_human_like(part)
                    else:
                        keyboard.write(part)
        else:
            if human_like:
                self._type_human_like(text)
            else:
                keyboard.write(text)

    def _type_human_like(self, text: str):
        """Simulate human-like typing with random delays and occasional mistakes."""
        # Split text into words for more natural typing
        words = text.split()
        
        for i, word in enumerate(words):
            # Add space between words
            if i > 0:
                keyboard.write(" ")
                time.sleep(random.uniform(0.1, 0.3))  # Natural pause between words
            
            # Type each character in the word
            for char in word:
                # Random delay between keystrokes
                delay = random.uniform(0.05, 0.2)
                time.sleep(delay)
                
                # Occasionally make a typo and correct it
                if random.random() < 0.05:  # 5% chance of typo
                    wrong_char = self._get_adjacent_key(char)
                    keyboard.write(wrong_char)
                    time.sleep(0.1)
                    keyboard.press('backspace')
                    time.sleep(0.1)
                
                keyboard.write(char)
            
            # Occasionally pause at the end of words
            if random.random() < 0.1:  # 10% chance of pause
                time.sleep(random.uniform(0.2, 0.5))

    def _get_adjacent_key(self, char: str) -> str:
        """Get a random adjacent key on the keyboard for realistic typos."""
        adjacent_keys = {
            'a': 'sqwz',
            's': 'awdxz',
            'd': 'sefcx',
            'f': 'drgvc',
            'g': 'fthbv',
            'h': 'gynjb',
            'j': 'hukmn',
            'k': 'jiolm',
            'l': 'kop',
            'z': 'asx',
            'x': 'zsdc',
            'c': 'xdfv',
            'v': 'cfgb',
            'b': 'vghn',
            'n': 'bhjm',
            'm': 'njk',
            'q': 'wa',
            'w': 'qasd',
            'e': 'wsdf',
            'r': 'edfg',
            't': 'rfgh',
            'y': 'tghj',
            'u': 'yhjk',
            'i': 'ujkl',
            'o': 'iklp',
            'p': 'ol',
            '1': '2q',
            '2': '13qw',
            '3': '24we',
            '4': '35er',
            '5': '46rt',
            '6': '57ty',
            '7': '68yu',
            '8': '79ui',
            '9': '80io',
            '0': '9op',
            ' ': ' '  # Space has no adjacent keys
        }
        
        if char.lower() in adjacent_keys:
            return random.choice(adjacent_keys[char.lower()])
        return char

    def accept_suggestion(self):
        """Accept the current suggestion."""
        keyboard.press('tab')
        time.sleep(0.1)

    def reject_suggestion(self):
        """Reject the current suggestion."""
        keyboard.press('escape')
        time.sleep(0.1)

    def send_message(self):
        """Send the message or submit the form."""
        keyboard.press('enter')
        time.sleep(0.5)  # Wait for message to send

    def clear_text(self):
        """Clear the current text input."""
        keyboard.press('ctrl+a')
        time.sleep(0.1)
        keyboard.press('backspace')
        time.sleep(0.1)

    def type_to_cursor(self, text: str, human_like: bool = True):
        """Complete workflow to type to Cursor chat."""
        self.focus_application("cursor")
        time.sleep(0.5)
        self.clear_text()
        self.type_text(text, human_like)
        self.send_message()

    def type_to_google(self, text: str, human_like: bool = True):
        """Complete workflow to type into Google search."""
        self.focus_application("google")
        time.sleep(0.5)
        self.clear_text()
        # Press CTRL before typing
        keyboard.press('ctrl')
        time.sleep(0.1)
        self.type_text(text, human_like)
        keyboard.release('ctrl')
        self.send_message()

    def type_to_notes(self, text: str, human_like: bool = True):
        """Complete workflow to type into Notes."""
        self.focus_application("notes")
        time.sleep(0.5)
        self.clear_text()
        self.type_text(text, human_like)

if __name__ == "__main__":
    # Example usage
    config = {
        "macro_driver": {
            "typing_speed": 0.1,
            "cursor_chat_shortcut": "ctrl+shift+l"
        }
    }
    typer = CursorTyper(config)
    typer.type_text("Hello, world!") 