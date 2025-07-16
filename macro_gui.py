import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import pyautogui
import threading
import time

# --- Custom Dialogs ---
def custom_input_dialog(root, title, prompt, font, input_type='string'):
    result = {}  # value can be int or str
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.configure(bg="#23272f")
    dialog.grab_set()
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.geometry(f"400x140+{root.winfo_x()+60}+{root.winfo_y()+60}")

    ttk.Label(dialog, text=prompt, style='TLabel', font=(font, 12)).pack(pady=(18, 8))
    entry_var = tk.StringVar()
    entry = tk.Entry(dialog, textvariable=entry_var, font=(font, 12), bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2", relief="flat", highlightthickness=1, highlightbackground="#44475a")
    entry.pack(pady=(0, 10), ipadx=4, ipady=2)
    entry.focus_set()

    def on_ok():
        val = entry_var.get()
        if input_type == 'int':
            try:
                val = int(val)
            except ValueError:
                custom_message_dialog(root, "Invalid Input", "Please enter a valid integer.", font, error=True)
                return
        result['value'] = val
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    btn_frame = ttk.Frame(dialog, style='TFrame')
    btn_frame.pack(pady=(0, 10))
    ok_btn = ttk.Button(btn_frame, text="OK", command=on_ok, style='TButton')
    ok_btn.pack(side=tk.LEFT, padx=(0, 10))
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=on_cancel, style='TButton')
    cancel_btn.pack(side=tk.LEFT)

    dialog.bind('<Return>', lambda e: on_ok())
    dialog.bind('<Escape>', lambda e: on_cancel())
    dialog.wait_window()
    return result.get('value', None)

def custom_message_dialog(root, title, message, font, error=False):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.configure(bg="#23272f")
    dialog.grab_set()
    dialog.resizable(False, False)
    dialog.transient(root)
    # Increase height for longer messages
    dialog.geometry(f"400x170+{root.winfo_x()+60}+{root.winfo_y()+60}")
    color = "#ff5555" if error else "#8be9fd"
    ttk.Label(dialog, text=title, style='Header.TLabel', font=(font, 14, "bold"), foreground=color, background="#23272f").pack(pady=(18, 2))
    # Use a wrapping label for the message
    msg_label = tk.Label(dialog, text=message, font=(font, 12), bg="#23272f", fg="#f8f8f2", wraplength=360, justify="center")
    msg_label.pack(pady=(0, 10), padx=10)
    ok_btn = ttk.Button(dialog, text="OK", command=dialog.destroy, style='TButton')
    ok_btn.pack(pady=(0, 10))
    dialog.bind('<Return>', lambda e: dialog.destroy())
    dialog.bind('<Escape>', lambda e: dialog.destroy())
    dialog.wait_window()

def mouse_position_dialog(root, font):
    import pyautogui
    result = {}  # value can be int
    dialog = tk.Toplevel(root)
    dialog.title("Mouse Move")
    dialog.configure(bg="#23272f")
    dialog.grab_set()
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.geometry(f"400x200+{root.winfo_x()+60}+{root.winfo_y()+60}")

    ttk.Label(dialog, text="Enter mouse coordinates:", style='TLabel', font=(font, 12)).pack(pady=(18, 8))

    pos_frame = ttk.Frame(dialog, style='TFrame')
    pos_frame.pack(pady=(0, 10))
    ttk.Label(pos_frame, text="X:", style='TLabel', font=(font, 12)).grid(row=0, column=0, padx=(0, 4))
    x_var = tk.StringVar()
    x_entry = tk.Entry(pos_frame, textvariable=x_var, font=(font, 12), width=8, bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2", relief="flat", highlightthickness=1, highlightbackground="#44475a")
    x_entry.grid(row=0, column=1, padx=(0, 12))
    ttk.Label(pos_frame, text="Y:", style='TLabel', font=(font, 12)).grid(row=0, column=2, padx=(0, 4))
    y_var = tk.StringVar()
    y_entry = tk.Entry(pos_frame, textvariable=y_var, font=(font, 12), width=8, bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2", relief="flat", highlightthickness=1, highlightbackground="#44475a")
    y_entry.grid(row=0, column=3)

    # Live mouse position label
    mouse_pos_label = tk.Label(dialog, text="Current mouse position: (0, 0)", font=(font, 11), bg="#23272f", fg="#8be9fd")
    mouse_pos_label.pack(pady=(0, 10))

    running = [True]
    def update_mouse_pos():
        if running[0]:
            x, y = pyautogui.position()
            mouse_pos_label.config(text=f"Current mouse position: ({x}, {y})")
            dialog.after(100, update_mouse_pos)
    update_mouse_pos()

    def on_ok():
        try:
            x = int(x_var.get())
            y = int(y_var.get())
            result['x'] = x
            result['y'] = y
            running[0] = False
            dialog.destroy()
        except ValueError:
            custom_message_dialog(root, "Invalid Input", "Please enter valid integers for X and Y.", font, error=True)

    def on_cancel():
        running[0] = False
        dialog.destroy()

    btn_frame = ttk.Frame(dialog, style='TFrame')
    btn_frame.pack(pady=(0, 10))
    ok_btn = ttk.Button(btn_frame, text="OK", command=on_ok, style='TButton')
    ok_btn.pack(side=tk.LEFT, padx=(0, 10))
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=on_cancel, style='TButton')
    cancel_btn.pack(side=tk.LEFT)

    dialog.bind('<Return>', lambda e: on_ok())
    dialog.bind('<Escape>', lambda e: on_cancel())
    dialog.wait_window()
    if 'x' in result and 'y' in result:
        return result['x'], result['y']
    return None, None

def action_type_dialog(root, font):
    result = {}  # value can be str
    dialog = tk.Toplevel(root)
    dialog.title("Add Action")
    dialog.configure(bg="#23272f")
    dialog.grab_set()
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.geometry(f"480x280+{root.winfo_x()+60}+{root.winfo_y()+60}")

    ttk.Label(dialog, text="Select action type:", style='TLabel', font=(font, 12)).pack(pady=(18, 8))
    
    action_types = ['key', 'mouse_move', 'mouse_click', 'type_string']
    
    # Create listbox for action types
    listbox = tk.Listbox(dialog, font=(font, 12), bg="#282a36", fg="#f8f8f2", selectbackground="#44475a", selectforeground="#8be9fd", borderwidth=0, highlightthickness=0, height=6)
    listbox.pack(pady=(0, 10), padx=20, fill=tk.BOTH, expand=True)
    
    # Add action types to listbox
    for action_type in action_types:
        listbox.insert(tk.END, action_type)
    
    # Select first item by default
    listbox.selection_set(0)
    listbox.focus_set()

    def on_ok():
        selection = listbox.curselection()
        if selection:
            result['action_type'] = listbox.get(selection[0])
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    btn_frame = ttk.Frame(dialog, style='TFrame')
    btn_frame.pack(pady=(0, 10))
    ok_btn = ttk.Button(btn_frame, text="OK", command=on_ok, style='TButton')
    ok_btn.pack(side=tk.LEFT, padx=(0, 10))
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=on_cancel, style='TButton')
    cancel_btn.pack(side=tk.LEFT)

    dialog.bind('<Return>', lambda e: on_ok())
    dialog.bind('<Escape>', lambda e: on_cancel())
    dialog.wait_window()
    return result.get('action_type', None)

def key_combination_dialog(root, font):
    """Dialog for recording key combinations with live display"""
    result = {'combination': []}
    dialog = tk.Toplevel(root)
    dialog.title("Record Key Combination")
    dialog.configure(bg="#23272f")
    dialog.grab_set()
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.geometry(f"460x260+{root.winfo_x()+60}+{root.winfo_y()+60}")

    # Title
    ttk.Label(dialog, text="Recording Key Combination", style='Header.TLabel', font=(font, 14, "bold"), foreground="#8be9fd", background="#23272f").pack(pady=(18, 5))
    
    # Instructions
    ttk.Label(dialog, text="Press the keys for your combination.", style='TLabel', font=(font, 11), foreground="#f8f8f2", background="#23272f").pack(pady=(0, 15))
    
    # Live display of combination
    combination_label = tk.Label(dialog, text="No keys pressed yet", font=(font, 12), bg="#23272f", fg="#ffb86c", wraplength=460)
    combination_label.pack(pady=(0, 15))
    
    # Status label
    status_label = tk.Label(dialog, text="Press keys now...", font=(font, 10), bg="#23272f", fg="#50fa7b", wraplength=460, justify="center")
    status_label.pack(pady=(0, 35))

    # Button frame
    btn_frame = ttk.Frame(dialog, style='TFrame')
    btn_frame.pack(pady=(0, 25))
    done_btn = ttk.Button(btn_frame, text="Done", command=lambda: on_done(), style='TButton')
    done_btn.pack(side=tk.LEFT, padx=(0, 15))
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=lambda: on_cancel(), style='TButton')
    cancel_btn.pack(side=tk.LEFT)

    # Key tracking
    pressed_keys = set()
    key_names = []
    recorded_keys = []  # Store the actual key objects
    
    def update_display():
        if key_names:
            display_text = " + ".join(key_names)
            combination_label.config(text=display_text)
        else:
            combination_label.config(text="No keys pressed yet")
    
    def on_key_press(key):
        if key not in pressed_keys:
            pressed_keys.add(key)
            key_name = get_key_display_name(key)
            if key_name not in key_names:
                key_names.append(key_name)
                recorded_keys.append(key)  # Store the actual key object
            update_display()
            status_label.config(text=f"Added: {key_name}")
    
    def on_key_release(key):
        if key in pressed_keys:
            pressed_keys.remove(key)
            # Don't remove from key_names or recorded_keys to allow for combination recording
    
    def get_key_display_name(key):
        """Convert key to readable display name"""
        if isinstance(key, keyboard.KeyCode):
            if key.char:
                return key.char.upper()
            else:
                return f"Key({key.vk})"
        else:
            # Handle special keys
            key_str = str(key)
            if key_str.startswith('Key.'):
                return key_str[4:].title()  # Remove 'Key.' prefix and capitalize
            return key_str
    
    def on_done():
        if recorded_keys:
            result['combination'] = recorded_keys
            dialog.destroy()
        else:
            status_label.config(text="Please press at least one key", fg="#ff5555")
    
    def on_cancel():
        dialog.destroy()
    
    # Start listening for keys
    listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    listener.start()
    
    # Focus the dialog
    dialog.focus_set()
    
    dialog.wait_window()
    listener.stop()
    
    return result.get('combination', [])

def single_key_dialog(root, font):
    """Dialog for recording a single key with live display"""
    result = {'key': None}
    dialog = tk.Toplevel(root)
    dialog.title("Record Single Key")
    dialog.configure(bg="#23272f")
    dialog.grab_set()
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.geometry(f"460x260+{root.winfo_x()+60}+{root.winfo_y()+60}")

    # Title
    ttk.Label(dialog, text="Recording Single Key", style='Header.TLabel', font=(font, 14, "bold"), foreground="#8be9fd", background="#23272f").pack(pady=(18, 5))
    
    # Instructions
    ttk.Label(dialog, text="Press any key to record it.", style='TLabel', font=(font, 11), foreground="#f8f8f2", background="#23272f").pack(pady=(0, 15))
    
    # Live display of key
    key_label = tk.Label(dialog, text="No key pressed yet", font=(font, 12), bg="#23272f", fg="#ffb86c", wraplength=450)
    key_label.pack(pady=(0, 15))
    
    # Status label
    status_label = tk.Label(dialog, text="Press any key now...", font=(font, 10), bg="#23272f", fg="#50fa7b", wraplength=450, justify="center")
    status_label.pack(pady=(0, 35))

    # Button frame
    btn_frame = ttk.Frame(dialog, style='TFrame')
    btn_frame.pack(pady=(0, 25))
    done_btn = ttk.Button(btn_frame, text="Done", command=lambda: on_done(), style='TButton')
    done_btn.pack(side=tk.LEFT, padx=(0, 15))
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=lambda: on_cancel(), style='TButton')
    cancel_btn.pack(side=tk.LEFT)

    recorded_key = None
    
    def update_display():
        if recorded_key:
            key_name = get_key_display_name(recorded_key)
            key_label.config(text=f"Recorded: {key_name}")
            status_label.config(text="Key recorded! Press another key to change.", fg="#50fa7b")
        else:
            key_label.config(text="No key pressed yet")
            status_label.config(text="Press any key now...", fg="#50fa7b")
    
    def get_key_display_name(key):
        """Convert key to readable display name"""
        if isinstance(key, keyboard.KeyCode):
            if key.char:
                return key.char.upper()
            else:
                return f"Key({key.vk})"
        else:
            # Handle special keys
            key_str = str(key)
            if key_str.startswith('Key.'):
                return key_str[4:].title()  # Remove 'Key.' prefix and capitalize
            return key_str
    
    def on_key_press(key):
        nonlocal recorded_key
        # Allow recording any key, including Space, Backspace, Enter, Escape, etc.
        recorded_key = key
        update_display()
    
    def on_done():
        if recorded_key:
            result['key'] = recorded_key
            dialog.destroy()
        else:
            status_label.config(text="Please press a key first", fg="#ff5555")
    
    def on_cancel():
        dialog.destroy()
    
    # Start listening for keys
    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()
    
    # Focus the dialog
    dialog.focus_set()
    
    dialog.wait_window()
    listener.stop()
    
    return result.get('key', None)

# --- Macro Logic ---
class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro GUI")
        self.root.geometry("420x600")
        self.root.configure(bg="#23272f")
        self.trigger_key = None
        self.actions = []  # List of (action_type, params)
        self.listener = None
        self.running = False
        self.currently_pressed = set()  # Track currently pressed keys

        # Try to use Inter, fallback to Segoe UI, then Arial Rounded MT Bold
        preferred_font = None
        for f in ("Inter", "Segoe UI", "Arial Rounded MT Bold", "Arial", "sans-serif"):
            try:
                tk.Label(root, font=(f, 12))
                preferred_font = f
                break
            except:
                continue
        if not preferred_font:
            preferred_font = "Arial"
        self.preferred_font = preferred_font

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background="#23272f")
        style.configure('TLabel', background="#23272f", foreground="#f8f8f2", font=(preferred_font, 12))
        style.configure('Header.TLabel', font=(preferred_font, 16, "bold"), foreground="#8be9fd", background="#23272f")
        style.configure('TButton', font=(preferred_font, 11), padding=6, background="#44475a", foreground="#f8f8f2", borderwidth=0, relief="flat")
        style.map('TButton', background=[('active', '#6272a4')])
        style.configure('TListbox', font=(preferred_font, 11), background="#282a36", foreground="#f8f8f2")
        style.configure('TCombobox', font=(preferred_font, 12), background="#282a36", foreground="#f8f8f2", fieldbackground="#282a36", selectbackground="#44475a", selectforeground="#8be9fd")
        style.map('TCombobox', fieldbackground=[('readonly', '#282a36')], selectbackground=[('readonly', '#44475a')])

        # --- Layout ---
        main_frame = ttk.Frame(root, padding=20, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Macro Builder", style='Header.TLabel').pack(pady=(0, 10))

        trigger_frame = ttk.Frame(main_frame, style='TFrame')
        trigger_frame.pack(fill=tk.X, pady=(0, 10))
        self.trigger_label = ttk.Label(trigger_frame, text="Trigger Key: None", style='TLabel')
        self.trigger_label.pack(side=tk.LEFT)
        self.set_trigger_btn = ttk.Button(trigger_frame, text="Set Trigger Key", command=self.set_trigger_key, style='TButton')
        self.set_trigger_btn.pack(side=tk.RIGHT)

        ttk.Label(main_frame, text="Macro Actions", style='Header.TLabel').pack(pady=(10, 5))
        actions_frame = ttk.Frame(main_frame, style='TFrame')
        actions_frame.pack(fill=tk.BOTH, expand=True)

        self.actions_listbox = tk.Listbox(actions_frame, width=40, height=10, font=(preferred_font, 11), bg="#282a36", fg="#f8f8f2", selectbackground="#44475a", selectforeground="#8be9fd", borderwidth=0, highlightthickness=0)
        self.actions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 10))
        scrollbar = ttk.Scrollbar(actions_frame, orient="vertical", command=self.actions_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.actions_listbox.config(yscrollcommand=scrollbar.set)
        
        # Drag and drop variables
        self.drag_data = {'item': None, 'x': 0, 'y': 0}
        
        # Bind drag and drop events
        self.actions_listbox.bind('<Button-1>', self.on_click)
        self.actions_listbox.bind('<B1-Motion>', self.on_drag)
        self.actions_listbox.bind('<ButtonRelease-1>', self.on_release)

        btns_frame = ttk.Frame(main_frame, style='TFrame')
        btns_frame.pack(fill=tk.X, pady=(5, 10))
        self.add_action_btn = ttk.Button(btns_frame, text="Add Action", command=self.add_action, style='TButton')
        self.add_action_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.remove_action_btn = ttk.Button(btns_frame, text="Remove Selected Action", command=self.remove_action, style='TButton')
        self.remove_action_btn.pack(side=tk.LEFT)

        macro_frame = ttk.Frame(main_frame, style='TFrame')
        macro_frame.pack(fill=tk.X, pady=(20, 0))
        self.start_macro_btn = ttk.Button(macro_frame, text="Start Macro Listener", command=self.start_macro_listener, style='TButton')
        self.start_macro_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.stop_macro_btn = ttk.Button(macro_frame, text="Stop Macro Listener", command=self.stop_macro_listener, state=tk.DISABLED, style='TButton')
        self.stop_macro_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # --- GUI Actions ---
    def set_trigger_key(self):
        combination = key_combination_dialog(self.root, self.preferred_font)
        if combination:
            self.trigger_key = combination
            self.trigger_label.config(text=f"Trigger Keys: {self.combination_to_str(combination)}")

    def combination_to_str(self, combination):
        """Convert key combination to readable string"""
        if not combination:
            return "None"
        key_names = []
        for key in combination:
            if isinstance(key, keyboard.KeyCode):
                if key.char:
                    key_names.append(key.char.upper())
                else:
                    key_names.append(f"Key({key.vk})")
            else:
                # Handle special keys
                key_str = str(key)
                if key_str.startswith('Key.'):
                    key_names.append(key_str[4:].title())  # Remove 'Key.' prefix and capitalize
                else:
                    key_names.append(key_str)
        return " + ".join(key_names)

    def key_to_str(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char or f"vk={key.vk}"
        else:
            return str(key)

    def add_action(self):
        action_type = action_type_dialog(self.root, self.preferred_font)
        if not action_type:
            return
        action_type = action_type.strip().lower()
        if action_type == 'key':
            key = self.get_key_from_user()
            if key:
                self.actions.append(('key', key))
                self.actions_listbox.insert(tk.END, f"Key press: {self.key_to_str(key)}")
        elif action_type == 'mouse_move':
            x, y = mouse_position_dialog(self.root, self.preferred_font)
            if x is not None and y is not None:
                self.actions.append(('mouse_move', (x, y)))
                self.actions_listbox.insert(tk.END, f"Mouse move to: ({x}, {y})")
        elif action_type == 'mouse_click':
            self.actions.append(('mouse_click', None))
            self.actions_listbox.insert(tk.END, "Mouse click")
        elif action_type == 'type_string':
            string_to_type = custom_input_dialog(self.root, "Type String", "Enter the text to type:", self.preferred_font)
            if string_to_type:
                self.actions.append(('type_string', string_to_type))
                self.actions_listbox.insert(tk.END, f"Type: '{string_to_type}'")
        else:
            custom_message_dialog(self.root, "Invalid Action", "Unknown action type.", self.preferred_font, error=True)

    def get_key_from_user(self):
        key = single_key_dialog(self.root, self.preferred_font)
        return key

    def remove_action(self):
        sel = self.actions_listbox.curselection()
        if sel:
            idx = sel[0]
            self.actions_listbox.delete(idx)
            del self.actions[idx]

    def on_click(self, event):
        """Handle mouse click to start drag"""
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        
    def on_drag(self, event):
        """Handle mouse drag"""
        if self.drag_data['item'] is None:
            # Start drag
            selection = self.actions_listbox.curselection()
            if selection:
                self.drag_data['item'] = selection[0]
        else:
            # Continue drag
            pass
            
    def on_release(self, event):
        """Handle mouse release to complete drag and drop"""
        if self.drag_data['item'] is not None:
            # Get the target position
            target_index = self.actions_listbox.nearest(event.y)
            
            # Only move if target is different
            if target_index != self.drag_data['item']:
                # Get the action to move
                action_to_move = self.actions[self.drag_data['item']]
                action_text = self.actions_listbox.get(self.drag_data['item'])
                
                # Remove from old position
                del self.actions[self.drag_data['item']]
                self.actions_listbox.delete(self.drag_data['item'])
                
                # Insert at new position
                self.actions.insert(target_index, action_to_move)
                self.actions_listbox.insert(target_index, action_text)
                
                # Select the moved item
                self.actions_listbox.selection_clear(0, tk.END)
                self.actions_listbox.selection_set(target_index)
            
            # Reset drag data
            self.drag_data['item'] = None

    def start_macro_listener(self):
        if not self.trigger_key:
            custom_message_dialog(self.root, "No Trigger Key", "Please set a trigger key first.", self.preferred_font, error=True)
            return
        if not self.actions:
            custom_message_dialog(self.root, "No Actions", "Please add at least one action.", self.preferred_font, error=True)
            return
        self.running = True
        self.currently_pressed.clear()  # Clear any existing pressed keys
        self.listener = keyboard.Listener(on_press=self.on_global_key, on_release=self.on_global_key_release)
        self.listener.start()
        self.start_macro_btn.config(state=tk.DISABLED)
        self.stop_macro_btn.config(state=tk.NORMAL)
        custom_message_dialog(self.root, "Macro Running", "Macro listener started. Minimize this window if you want.", self.preferred_font)

    def stop_macro_listener(self):
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.currently_pressed.clear()
        self.start_macro_btn.config(state=tk.NORMAL)
        self.stop_macro_btn.config(state=tk.DISABLED)

    def on_global_key(self, key):
        if not self.running:
            return
        self.currently_pressed.add(key)
        if self.keys_match_combination(self.currently_pressed, self.trigger_key):
            threading.Thread(target=self.run_macro, daemon=True).start()

    def on_global_key_release(self, key):
        if not self.running:
            return
        self.currently_pressed.discard(key)

    def update_currently_pressed_display(self):
        if self.currently_pressed:
            display_text = " + ".join([self.key_to_str(k) for k in self.currently_pressed])
            self.trigger_label.config(text=f"Trigger Keys: {display_text}")
        else:
            self.trigger_label.config(text="Trigger Key: None")

    def keys_match_combination(self, pressed_keys, combination):
        """Check if all keys in the combination are currently pressed"""
        if not combination or not pressed_keys:
            return False
        
        # Check if all keys in the combination are currently pressed
        for combo_key in combination:
            key_found = False
            for pressed_key in pressed_keys:
                if self.keys_match(pressed_key, combo_key):
                    key_found = True
                    break
            if not key_found:
                return False
        return True

    def keys_match(self, key1, key2):
        # Compare Key or KeyCode
        if type(key1) != type(key2):
            return False
        if isinstance(key1, keyboard.KeyCode):
            return key1.vk == key2.vk and key1.char == key2.char
        else:
            return key1 == key2

    def run_macro(self):
        kbd_ctrl = keyboard.Controller()
        for action in self.actions:
            action_type, param = action
            if action_type == 'key':
                # param is a pynput Key or KeyCode
                kbd_ctrl.press(param)
                kbd_ctrl.release(param)
            elif action_type == 'mouse_move':
                x, y = param
                pyautogui.moveTo(x, y)
            elif action_type == 'mouse_click':
                pyautogui.click()
            elif action_type == 'type_string':
                # param is the string to type
                kbd_ctrl.type(param)
            time.sleep(0.1)

    def on_close(self):
        self.stop_macro_listener()
        self.root.destroy()

# --- Main ---
def main():
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 