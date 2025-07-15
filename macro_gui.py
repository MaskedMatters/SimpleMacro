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
        custom_message_dialog(self.root, "Set Trigger Key", "After closing this dialog, press the key you want to use as the macro trigger.", self.preferred_font)
        self.root.withdraw()
        key = self.wait_for_key()
        self.root.deiconify()
        if key:
            self.trigger_key = key
            self.trigger_label.config(text=f"Trigger Key: {self.key_to_str(key)}")

    def wait_for_key(self):
        key_pressed = {'key': None}
        def on_press(key):
            key_pressed['key'] = key
            listener.stop()  # Stop listener after key is pressed
            # Do not return anything (None)
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        return key_pressed['key']

    def key_to_str(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char or f"vk={key.vk}"
        else:
            return str(key)

    def add_action(self):
        action_type = custom_input_dialog(self.root, "Add Action", "Type: 'key', 'mouse_move', or 'mouse_click'", self.preferred_font)
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
        else:
            custom_message_dialog(self.root, "Invalid Action", "Unknown action type.", self.preferred_font, error=True)

    def get_key_from_user(self):
        custom_message_dialog(self.root, "Key Press", "After closing this dialog, press the key you want to add as an action.", self.preferred_font)
        self.root.withdraw()
        key = self.wait_for_key()
        self.root.deiconify()
        return key

    def remove_action(self):
        sel = self.actions_listbox.curselection()
        if sel:
            idx = sel[0]
            self.actions_listbox.delete(idx)
            del self.actions[idx]

    def start_macro_listener(self):
        if not self.trigger_key:
            custom_message_dialog(self.root, "No Trigger Key", "Please set a trigger key first.", self.preferred_font, error=True)
            return
        if not self.actions:
            custom_message_dialog(self.root, "No Actions", "Please add at least one action.", self.preferred_font, error=True)
            return
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_global_key)
        self.listener.start()
        self.start_macro_btn.config(state=tk.DISABLED)
        self.stop_macro_btn.config(state=tk.NORMAL)
        custom_message_dialog(self.root, "Macro Running", "Macro listener started. Minimize this window if you want.", self.preferred_font)

    def stop_macro_listener(self):
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.start_macro_btn.config(state=tk.NORMAL)
        self.stop_macro_btn.config(state=tk.DISABLED)

    def on_global_key(self, key):
        if self.running and self.keys_match(key, self.trigger_key):
            threading.Thread(target=self.run_macro, daemon=True).start()

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