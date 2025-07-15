# SimpleMacro
This is a simple macro made it Python and it was basically 100% vibe coded, you are welcome!

A simple macro builder that lets you:
- Set any key as a trigger
- Add mouse moves, clicks, keyboard presses, and text typing
- Run sequences with 0.1s delays between actions
- Modern dark theme interface
- Drag and drop to reorder actions
- Dropdown selection for action types

## Features
- **Global Hotkey Support**: Set any keyboard key as a trigger
- **Action Types**: 
  - `key` - Press a specific key
  - `mouse_move` - Move mouse to coordinates  
  - `mouse_click` - Click at current position
  - `type_string` - Type custom text
- **Drag & Drop**: Reorder actions by dragging them in the list
- **Live Mouse Position**: See current coordinates while setting up mouse moves
- **Modern UI**: Dark theme with custom dialogs

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python macro_gui.py
```

There are also standalone (and distributable) executables in the Releases tab of the GitHub repository which is a preferred way to use.

That's it! 🎯