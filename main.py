import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.resizable(False, False)
        self.geometry("300x250")

        window_width = 300
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.python_path = None  # Store the path to python.exe

        self.button1 = ttk.Button(self, text="Matrix feedback register", command=self.run_fsr, state=tk.DISABLED)
        self.button1.pack(pady=10)

        self.button2 = ttk.Button(self, text="Matrix shift register", command=self.run_mzr, state=tk.DISABLED)
        self.button2.pack(pady=10)

        self.button3 = ttk.Button(self, text="Matrix shift register Individual", command=self.run_ind,
                                  state=tk.DISABLED)
        self.button3.pack(pady=10)

        self.choose_python_button = ttk.Button(self, text="Choose python.exe", command=self.choose_python)
        self.choose_python_button.pack(pady=5)

        self.exit_button = ttk.Button(self, text="Exit", command=self.quit)
        self.exit_button.pack(pady=10)

    def choose_python(self):
        python_path = filedialog.askopenfilename(title="Choose python.exe", filetypes=[("Python Executable",
                                                                                        "python.exe")])
        if python_path:
            self.python_path = python_path
            messagebox.showinfo("Information", "Path to python.exe was successfully chosen.")
            self.enable_buttons()
        else:
            messagebox.showwarning("Warning", "Choose the path to python.exe.")

    def enable_buttons(self):
        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.NORMAL)
        self.button3.config(state=tk.NORMAL)

    def run_script(self, script_name):
        file_path = script_name  # Assume script_name is the full path to the script
        if os.path.exists(file_path):
            os.system(f"{self.python_path} {file_path}")
        else:
            messagebox.showerror("Error", f"File {script_name} wasn't found.")

    def run_fsr(self):
        self.run_script("FSR.py")

    def run_mzr(self):
        self.run_script("MSR.py")

    def run_ind(self):
        self.run_script("MSR_individual.py")


if __name__ == "__main__":
    app = MainWindow()
    icon_path = "scr/images/icon.ico"
    app.iconbitmap(default=icon_path)
    app.mainloop()
