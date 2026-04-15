import os
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

class StructureGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Structure Creator (StructureGen)")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")

        self.label = tk.Label(root, text="Paste your file structure below:", fg="white", bg="#1e1e1e", font=("Segoe UI", 12))
        self.label.pack(pady=10)

        # Editor-like text area (Monaco-inspired dark theme)
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, bg="#1e1e1e", fg="#d4d4d4", 
                                                  insertbackground="white", font=("Consolas", 11),
                                                  undo=True, borderwidth=0, padx=10, pady=10)
        self.text_area.pack(expand=True, fill="both", padx=20, pady=10)

        # Bottom bar
        self.button_frame = tk.Frame(root, bg="#1e1e1e")
        self.button_frame.pack(fill="x", pady=20)

        self.create_btn = tk.Button(self.button_frame, text="Generate Structure", command=self.generate,
                                   bg="#007acc", fg="white", font=("Segoe UI", 11, "bold"), 
                                   padx=30, pady=5, relief=tk.FLAT, activebackground="#005a9e", activeforeground="white")
        self.create_btn.pack(side="right", padx=20)
        
        self.info_label = tk.Label(self.button_frame, text="Files will be created in current directory.", 
                                   fg="#888888", bg="#1e1e1e", font=("Segoe UI", 9))
        self.info_label.pack(side="left", padx=20)

    def generate(self):
        text = self.text_area.get("1.0", tk.END)
        if not text.strip():
            messagebox.showwarning("Empty", "Please paste a structure first.")
            return
            
        try:
            self.parse_and_create(os.getcwd(), text)
            messagebox.showinfo("Success", f"Structure created successfully in:\n{os.getcwd()}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def parse_and_create(self, base_path, text):
        lines = text.splitlines()
        # Stack of (indent_level, current_directory_path)
        stack = [(-1, base_path)]
        
        for line in lines:
            if not line.strip(): continue
            
            # 1. Detect indent level by finding the first name-related character
            # Handles tree chars: │, ├, └, ─ and spaces
            match = re.search(r'[a-zA-Z0-9_\+\-\.\[\]]', line)
            if not match: continue
            
            depth = match.start()
            content = line[depth:].strip()
            
            # 2. Strip comments (e.g., # Reusable components)
            if ' #' in content:
                content = content.split(' #')[0].strip()
            elif '  ' in content: 
                parts = re.split(r'\s{2,}', content)
                if len(parts) > 1:
                    content = parts[0].strip()

            # 3. Guess if it's a directory
            # Dir if: ends with /, has no dot, or starts with + (Svelte layout logic) but we check if it looks like a file extension
            is_dir = content.endswith('/') or ('.' not in content and not content.startswith('+'))
            
            # Exception: if it ends with common extensions, it's a file even without a dot (rare)
            if any(content.endswith(ext) for ext in ['.svelte', '.js', '.ts', '.css', '.html', '.json', '.md', '.py']):
                is_dir = False
            
            name = content.rstrip('/')
            if not name: continue
            
            # 4. Pop stack to find the correct parent
            while len(stack) > 1 and stack[-1][0] >= depth:
                stack.pop()
            
            parent_path = stack[-1][1]
            current_path = os.path.join(parent_path, name)
            
            if is_dir:
                os.makedirs(current_path, exist_ok=True)
                stack.append((depth, current_path))
            else:
                os.makedirs(os.path.dirname(current_path), exist_ok=True)
                if not os.path.exists(current_path):
                    with open(current_path, 'w') as f:
                        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StructureGenApp(root)
    root.mainloop()
