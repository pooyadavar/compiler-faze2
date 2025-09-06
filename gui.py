import tkinter as tk
from tkinter import filedialog, messagebox
import os
from cli import run_pipeline


class ObfuscatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-C Obfuscator")
        self.root.geometry("500x420")

        self.input_path = tk.StringVar(value="input/input1.mc")
        self.output_path = tk.StringVar(value="output_gui/output.mc")

        tk.Label(root, text="Input File:").pack(pady=5)
        tk.Entry(root, textvariable=self.input_path, width=50).pack()
        tk.Button(root, text="Browse", command=self.browse_input).pack()

        tk.Label(root, text="Output File:").pack(pady=5)
        tk.Entry(root, textvariable=self.output_path, width=50).pack()

        self.options = {
            "rename": tk.BooleanVar(),
            "dead": tk.BooleanVar(),
            "expr": tk.BooleanVar(),
            "flatten": tk.BooleanVar(),
            "inline": tk.BooleanVar(),
            "all": tk.BooleanVar(),
            "check": tk.BooleanVar(),
        }

        tk.Label(root, text="Transformations:").pack(pady=10)
        for key in self.options:
            tk.Checkbutton(
                root, text=key.capitalize(), variable=self.options[key]
            ).pack(anchor="w", padx=20)

        tk.Button(root, text="Run Obfuscation", command=self.run).pack(pady=20)

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("Mini-C Files", "*.mc")])
        if path:
            self.input_path.set(path)

    def run(self):
        in_path = self.input_path.get()
        out_path = self.output_path.get()

        if not os.path.isfile(in_path):
            messagebox.showerror("Error", "Input file does not exist.")
            return

        stages = []
        if self.options["all"].get():
            stages = ["rename", "dead", "expr", "flatten", "inline"]
        else:
            for key in ["rename", "dead", "expr", "flatten", "inline"]:
                if self.options[key].get():
                    stages.append(key)

        try:
            run_pipeline(in_path, out_path, stages, self.options["check"].get())
            messagebox.showinfo("Success", f"Obfuscated code saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ObfuscatorGUI(root)
    root.mainloop()
