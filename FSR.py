from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from binary_utilities import oct_to_bin, binary_table
from polynomial_utilities import generate_states, compute_ACF, generate_C, find_experimental_period
from polynomials import polynomials

import tkinter as tk
import numpy as np
import re
import matplotlib.pyplot as plt


class App:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Feedback shift register (FSR)")
        self.root.resizable(False, False)
        self.acf_figure = None
        self.acf_canvas_agg = None

        # Get window size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = 1100
        window_height = 450

        # Calculate center screen position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set center screen values
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Polynomial input frame
        self.polynomial_frame = ttk.LabelFrame(self.root, text="Polynomial input")
        self.polynomial_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Result frame
        self.result_frame = ttk.LabelFrame(self.root, text="Results")
        self.result_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nswe")

        # Polynomial frame elements
        self.degree_label = ttk.Label(self.polynomial_frame, text="Polynomial degree:")
        self.degree_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.degree_combobox = ttk.Combobox(self.polynomial_frame, values=list(range(2, 16)))
        self.degree_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.polynomial_label = ttk.Label(self.polynomial_frame, text="Choose polynomial:")
        self.polynomial_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.polynomial_listbox = tk.Listbox(self.polynomial_frame, selectmode="single", exportselection=False)
        self.polynomial_listbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.seed_label = ttk.Label(self.polynomial_frame, text="Seed:")
        self.seed_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.seed_value = tk.IntVar()
        self.seed_entry = ttk.Entry(self.polynomial_frame, textvariable=self.seed_value)
        self.seed_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.select_button = ttk.Button(self.polynomial_frame, text="OK", command=self.submit)
        self.select_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Result frame elements
        self.C_label = ttk.Label(self.result_frame, text="Sequence C:")
        self.C_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.C_text = tk.Text(self.result_frame, height=1, width=40, wrap="none")
        self.C_text.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        self.C_text_scrollbar = tk.Scrollbar(self.result_frame, orient="horizontal", command=self.C_text.xview)
        self.C_text_scrollbar.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.C_text.config(xscrollcommand=self.C_text_scrollbar.set)

        self.table_label = ttk.Label(self.result_frame, text="Structural matrix:")
        self.table_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.table_text = tk.Text(self.result_frame, height=5, width=15)
        self.table_text.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.states_label = ttk.Label(self.result_frame, text="Generator states:")
        self.states_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.states_text = tk.Text(self.result_frame, height=5, width=15)
        self.states_text.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.hamming_weight_label = ttk.Label(self.result_frame, text="wH:")
        self.hamming_weight_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.hamming_weight_value = tk.StringVar()
        self.hamming_weight_label_value = ttk.Label(self.result_frame, textvariable=self.hamming_weight_value)
        self.hamming_weight_label_value.grid(row=7, column=0, padx=30, pady=5, sticky="we")

        self.experimental_period_label = ttk.Label(self.result_frame, text="T(exp):")
        self.experimental_period_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

        self.experimental_period_value = tk.StringVar()
        self.experimental_period_label_value = ttk.Label(self.result_frame, textvariable=self.experimental_period_value)
        self.experimental_period_label_value.grid(row=8, column=0, padx=50, pady=5, sticky="we")

        self.period_label = ttk.Label(self.result_frame, text="T:")
        self.period_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")

        self.period_value = tk.StringVar()
        self.period_label_value = ttk.Label(self.result_frame, textvariable=self.period_value)
        self.period_label_value.grid(row=9, column=0, padx=20, pady=5, sticky="we")

        # Graph canvas
        self.acf_canvas = tk.Canvas(self.root, bg="white")
        self.acf_canvas.grid(row=0, column=2, padx=10, pady=5, sticky="nswe")

        # Event binding to update the list of polynomials when the degree changes
        self.degree_combobox.bind("<<ComboboxSelected>>", self.update_polynomial_list)

    # Update polynomial list in correct format
    def update_polynomial_list(self, event):
        degree = int(self.degree_combobox.get())
        polynomial_list = polynomials.get(degree, [])
        self.polynomial_listbox.delete(0, "end")
        for polynomial in polynomial_list:
            self.polynomial_listbox.insert("end", f"<{polynomial[0]} {polynomial[1]}{polynomial[2]}>")

    def submit(self):
        # Get chosen polynomial
        selected_index = self.polynomial_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Error", "Please, choose the polynimoal.")
            return

        selected_polynomial = self.polynomial_listbox.get(selected_index)

        degree = int(self.degree_combobox.get())

        # Parsing polynomials values
        match = re.match(r"<(\d+) (\d+)([A-Z])>", selected_polynomial)
        if match:
            j, value = map(int, match.groups()[:2])
            binary_value = oct_to_bin(value)
            table = binary_table(binary_value)
        else:
            messagebox.showerror("Error", "Wrong polynomial format")
            return

        self.table_text.delete(1.0, "end")
        self.table_text.insert("end", "\n".join("".join(str(cell) for cell in row) for row in table))

        # Cut binary value
        trimmed_binary_value = binary_value[1:]
        polynomial_coef = [int(bit) for bit in trimmed_binary_value]

        # Calculate period
        T = 2 ** degree - 1

        self.period_value.set(T)

        states = generate_states(polynomial_coef, degree)
        states_str = "\n".join("".join(str(bit) for bit in state) for state in states)
        self.states_text.delete(1.0, "end")
        self.states_text.insert("end", states_str)

        # Get seed
        seed = self.seed_value.get()

        # Set seed
        np.random.seed(seed)

        C = generate_C(polynomial_coef, T)
        self.C_text.delete(1.0, "end")
        self.C_text.insert("end", " ".join(str(bit) for bit in C))

        R = compute_ACF(C, degree)

        # Calling the plot_ACF method with passing num_values
        experimental_period = find_experimental_period(C, degree)
        self.experimental_period_value.set(experimental_period if experimental_period is not None else T)

        # If the experimental period is empty, we assign it the value of the period T
        if experimental_period is None:
            experimental_period = T

        # Calculate Hamming weight
        wt_C = round(experimental_period / 2)

        self.hamming_weight_value.set(str(wt_C))

        self.plot_ACF(R, experimental_period=experimental_period)

    def plot_ACF(self, R, experimental_period):
        # Check if exists
        if hasattr(self, "acf_canvas") and isinstance(self.acf_canvas, FigureCanvasTkAgg):
            self.acf_canvas.get_tk_widget().destroy()  # Delete previous graph

        self.acf_figure = plt.figure(figsize=(4, 3))
        ax = self.acf_figure.add_subplot(111)
        if experimental_period is not None:
            ax.plot(np.arange(experimental_period), R[:experimental_period])
            ax.set_xlim(0, experimental_period)
        else:
            ax.plot(R)
        ax.set_title("ACF")
        ax.set_xlabel("Shift")
        ax.set_ylabel("Autocorrelation")
        ax.grid(True)

        # Setting graph size
        self.acf_figure.tight_layout()
        self.acf_canvas = FigureCanvasTkAgg(self.acf_figure, master=self.root)
        self.acf_canvas.draw()
        canvas_widget = self.acf_canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=2, padx=10, pady=5, sticky="nswe")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    icon_path = "scr/images/icon.ico"
    root.iconbitmap(default=icon_path)
    root.mainloop()
