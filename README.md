# SimpleMacro
This is a simple macro made in Python and it was basically 100% vibe coded, you are welcome!

A simple macro builder that lets you:
- Set any key or key combination as a trigger (supports Ctrl, Shift, Alt, etc.)
- Add mouse moves, clicks, keyboard presses, and text typing
- Run sequences with 0.1s delays between actions
- Modern dark theme interface
- Drag and drop to reorder actions
- Dropdown selection for action types
- Live key and key combination recording dialogs
- Live mouse position display when setting mouse moves
- Global hotkey support (works system-wide)
- Only triggers macro once per key press (no repeats while holding)
- Clean, user-friendly dialogs for all actions
- Cross-platform: works on both Windows and Linux

## Features
- **Global Hotkey Support**: Set any keyboard key or key combination as a trigger (e.g., Ctrl+Shift+A)
- **Action Types**: 
  - `key` - Press a specific key
  - `mouse_move` - Move mouse to coordinates  
  - `mouse_click` - Click at current position
  - `type_string` - Type custom text
- **Drag & Drop**: Reorder actions by dragging them in the list
- **Live Mouse Position**: See current coordinates while setting up mouse moves
- **Live Key Recording**: Dialogs for recording single keys or key combinations, with real-time feedback
- **Modern UI**: Dark theme with custom dialogs and clear, centered instructions
- **No Repeat Triggering**: Macro only triggers once per key press, not repeatedly while holding
- **Cross-Platform**: Works on both Windows and Linux (tested)

## ⚠️ Windows Mouse Note
On Windows, when the macro runs, the mouse actions (move/click) are performed by a virtual mouse. This means:
- The macro will click and interact with things as expected
- **But your actual mouse cursor may not visibly move**
- This is normal and does not affect macro functionality

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