import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class TextEditor:
    def __init__(self) -> None:
        pass

    def open_file(self, filepath):
        """Open a file for editing."""
        
        self.loadWindow()
        self.filepath = filepath
        try:
            with open(filepath, "r", encoding="UTF-8") as input_file:
                text = input_file.read()
                self.txt_edit.insert(tk.END, text)
        except FileNotFoundError:
            return

        self.window.title(f"Text Editor Application - {filepath}")
        self.window.mainloop()

    def save_file(self):
        """Save the current file as a new file."""

        with open(self.filepath, "w", encoding="UTF-8") as output_file:
            text = self.txt_edit.get(1.0, tk.END)
            output_file.write(text)
        self.window.title(f"Text Editor Application - {self.filepath}")
        self.window.destroy()

    def loadWindow(self):
        self.window = tk.Tk()
        print("loadWindow")
        self.window.title("Text Editor Application")
        self.window.rowconfigure(0, minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)

        self.txt_edit = tk.Text(self.window)
        self.fr_buttons = tk.Frame(self.window, relief=tk.RAISED, bd=2)
        self.btn_save = tk.Button(
            self.fr_buttons, text="Save", command=self.save_file)

        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.txt_edit.grid(row=0, column=1, sticky="nsew")

