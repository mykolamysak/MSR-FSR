from calculator import Calculator
from polynomial_utilities import Polynomial
from binary_utilities import validate, Binary_C, binary_to_F
from polynomials import polynomials
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib
import tkinter as tk
matplotlib.use('TkAgg')


class App(tk.Tk):
    # Updating rank values while polynomial degree changed
    def update_rank_values(self):
        degree_A_value = self.degree_A_combobox.get()
        if degree_A_value:
            degree_A = int(degree_A_value)
            self.rank_combobox['values'] = [str(i) for i in range(1, degree_A + 1)]

    # Update list of polynomials while degree changed
    def update_polynomials_A(self, event=None):
        degree_A_value = self.degree_A_combobox.get()
        if degree_A_value:
            self.degree_A = int(degree_A_value)
            self.polynomial_A_combobox['values'] = [f"<{j} {g8}{letter}>" for j, g8, letter in
                                                    polynomials[self.degree_A]]
            self.update_rank_values()
            self.update_i_values()

    def update_polynomials_B(self, event=None):
        degree_B_value = self.degree_B_combobox.get()
        if degree_B_value:
            self.degree_B = int(degree_B_value)
            self.polynomial_B_combobox['values'] = [f"<{j} {g8}{letter}>" for j, g8, letter in
                                                    polynomials[self.degree_B]]
            self.update_j_values()

    # Update i and j values while degree changed
    def update_i_values(self):
        degree_A_value = self.degree_A_combobox.get()
        if degree_A_value:
            degree_A = int(degree_A_value)
            self.i_combobox['values'] = [str(i) for i in range(1, degree_A + 1)]

    def update_j_values(self):
        degree_B_value = self.degree_B_combobox.get()
        if degree_B_value:
            degree_B = int(degree_B_value)
            self.j_combobox['values'] = [str(i) for i in range(1, degree_B + 1)]

    # Read i and j values
    def selected_i_changed(self, event=None):
        self.selected_i = self.i_combobox.get()

    def selected_j_changed(self, event=None):
        self.selected_j = self.j_combobox.get()

    def initialize_ui(self):
        # your UI initialization code goes here

        # Calculate position to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1100
        window_height = 700
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.resizable(False, False)

        self.selected_polynomial_A = None
        self.selected_polynomial_B = None

        self.selected_i = None
        self.selected_j = None

        self.title("Matrix shift register (MSR)")
        self.degree_A = 2
        self.degree_B = 2

        # Polynomial input frame
        self.polynomial_frame = ttk.LabelFrame(self, text="Choose polynomial:")
        self.polynomial_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Result frame
        self.result_frame = ttk.LabelFrame(self, text="Results")
        self.result_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Additional results frame
        self.additional_results = ttk.LabelFrame(self, text="Additional results")
        self.additional_results.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="w")

        # Graph frame
        self.graph_frame = ttk.LabelFrame(self, text="Graph")
        self.graph_frame.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="w")

        # Polynomial input frame elements
        self.degree_A_label = tk.Label(self.polynomial_frame, text="Degree A:")
        self.degree_A_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.degree_A_combobox = ttk.Combobox(self.polynomial_frame, values=[str(i) for i in range(2, 16)],
                                              state="readonly")
        self.degree_A_combobox.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.degree_A_combobox.bind("<<ComboboxSelected>>", self.update_polynomials_A)

        self.polynomial_A_combobox = ttk.Combobox(self.polynomial_frame, width=20)
        self.polynomial_A_combobox.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.polynomial_A_combobox.bind("<<ComboboxSelected>>", self.selected_polynomial_A)

        self.degree_B_label = tk.Label(self.polynomial_frame, text="Degree B:")
        self.degree_B_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.degree_B_combobox = ttk.Combobox(self.polynomial_frame, values=[str(i) for i in range(2, 16)],
                                              state="readonly")
        self.degree_B_combobox.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.degree_B_combobox.bind("<<ComboboxSelected>>", self.update_polynomials_B)

        self.polynomial_B_combobox = ttk.Combobox(self.polynomial_frame, width=20)
        self.polynomial_B_combobox.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.polynomial_B_combobox.bind("<<ComboboxSelected>>", self.selected_polynomial_B)

        self.rank_label = tk.Label(self.polynomial_frame, text="Rank:")
        self.rank_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.rank_combobox = ttk.Combobox(self.polynomial_frame, state="readonly", width=5)
        self.rank_combobox.grid(row=4, column=0, sticky="w", padx=10)

        self.position_i = tk.Label(self.polynomial_frame, text="Value it:")
        self.position_i.grid(row=3, column=1, sticky="w", padx=8, pady=5)

        self.i_combobox = ttk.Combobox(self.polynomial_frame, state="readonly", width=5)
        self.i_combobox.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        self.position_j = tk.Label(self.polynomial_frame, text="Value jt:")
        self.position_j.grid(row=3, column=1, sticky="w", padx=100, pady=5)

        self.j_combobox = ttk.Combobox(self.polynomial_frame, state="readonly", width=5)
        self.j_combobox.grid(row=4, column=1, sticky="w", padx=100, pady=5)

        self.submit_button = tk.Button(self.polynomial_frame, text="Calculate", command=self.submit, width=10)
        self.submit_button.grid(row=8, column=0, sticky="w", padx=10, pady=15)

        # Result frame elements
        self.result_text_A_label = tk.Label(self.result_frame, text="Matrix A:")
        self.result_text_A_label.grid(row=0, column=0, padx=10, sticky="w")

        self.result_text_A = tk.Text(self.result_frame, height=5, width=20)
        self.result_text_A.grid(row=1, column=0, padx=10)

        self.result_text_B_label = tk.Label(self.result_frame, text="Matrix B:")
        self.result_text_B_label.grid(row=0, column=2, padx=20, pady=5, sticky="w")

        self.result_text_B = tk.Text(self.result_frame, height=5, width=20)
        self.result_text_B.grid(row=1, column=2, padx=20, pady=5)

        self.result_text_S_label = tk.Label(self.result_frame, text="Matrix S:")
        self.result_text_S_label.grid(row=0, column=1, padx=20, pady=5, sticky="w")

        self.result_text_S = tk.Text(self.result_frame, height=5, width=20)
        self.result_text_S.grid(row=1, column=1, padx=20, pady=5)

        self.period_label = tk.Label(self.result_frame, text="T:")
        self.period_label.grid(row=2, column=1, padx=20, pady=5, sticky="w")

        self.period_exp_label = tk.Label(self.result_frame, text="T(exp):")
        self.period_exp_label.grid(row=3, column=1, padx=20, pady=5, sticky="w")

        self.period_label_A = tk.Label(self.result_frame, text="T(A):")
        self.period_label_A.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.period_label_B = tk.Label(self.result_frame, text="T(B):")
        self.period_label_B.grid(row=2, column=2, padx=20, pady=5, sticky="w")

        self.hamming_weight_value = tk.Label(self.result_frame, text="wH:")
        self.hamming_weight_value.grid(row=4, column=1, padx=20, pady=5, sticky="w")

        self.hamming_weight_exp_value = tk.Label(self.result_frame, text="wH(exp):")
        self.hamming_weight_exp_value.grid(row=5, column=1, padx=20, pady=5, sticky="w")

        # Additional results frame elements
        self.sequence_C_label = tk.Label(self.additional_results, text="C sequence:")
        self.sequence_C_label.grid(row=3, column=0, padx=30, pady=5, sticky="w")

        self.sequence_C = tk.Text(self.additional_results, height=1, width=50, wrap="none")
        self.sequence_C.grid(row=4, column=0, padx=10, pady=5)

        self.sequence_C_scrollbar = tk.Scrollbar(self.additional_results, orient="horizontal",
                                                 command=self.sequence_C.xview)
        self.sequence_C_scrollbar.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.sequence_C.config(xscrollcommand=self.sequence_C_scrollbar.set)

        self.binary_C_Label = tk.Label(self.additional_results, text="Binary sequence:")
        self.binary_C_Label.grid(row=6, column=0, padx=30, pady=5, sticky="w")

        self.Binary_C_result = tk.Text(self.additional_results, height=1, width=50, wrap="none")
        self.Binary_C_result.grid(row=7, column=0, padx=10, pady=5)

        self.Binary_C_scrollbar = tk.Scrollbar(self.additional_results, orient="horizontal",
                                               command=self.Binary_C_result.xview)
        self.Binary_C_scrollbar.grid(row=8, column=0, padx=10, pady=5, sticky="ew")
        self.Binary_C_result.config(xscrollcommand=self.Binary_C_scrollbar.set)

        self.F_label_A = tk.Label(self.additional_results, text="Fa(x):")
        self.F_label_A.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.F_label_B = tk.Label(self.additional_results, text="Fb(x):")
        self.F_label_B.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        # Graph frame elements
        self.figure = Figure(figsize=(6, 3.8), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.plot_canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.degree_A_combobox.bind("<<ComboboxSelected>>", self.update_polynomials_A)
        self.degree_B_combobox.bind("<<ComboboxSelected>>", self.update_polynomials_B)
        self.i_combobox.bind("<<ComboboxSelected>>", self.selected_i_changed)
        self.j_combobox.bind("<<ComboboxSelected>>", self.selected_j_changed)

        # Update values
        self.update_polynomials_A()
        self.update_polynomials_B()
        self.update_rank_values()

    def submit(self):

        # Get values
        selected_polynomial_A_str = self.polynomial_A_combobox.get()
        selected_polynomial_B_str = self.polynomial_B_combobox.get()

        polynomial_A = next((poly for poly in polynomials[int(self.degree_A_combobox.get())] if
                             f"<{poly[0]} {poly[1]}{poly[2]}>" == selected_polynomial_A_str), None)
        polynomial_B = next((poly for poly in polynomials[int(self.degree_B_combobox.get())] if
                             f"<{poly[0]} {poly[1]}{poly[2]}>" == selected_polynomial_B_str), None)

        if polynomial_A is None or polynomial_B is None:
            messagebox.showerror("Error", "Choose polynomials A and B")
            return

        j_A, g8_A, letter_A = polynomial_A
        j_B, g8_B, letter_B = polynomial_B

        i = int(self.i_combobox.get()) - 1
        j = int(self.j_combobox.get()) - 1

        # Check for correct input
        try:
            poly_A = Polynomial(j_A, g8_A, int(self.degree_A_combobox.get()))
            poly_B = Polynomial(j_B, g8_B, int(self.degree_B_combobox.get()))
            validate(poly_A, poly_B)

        except Exception as e:
            messagebox.showerror("Error occured while choosing polynomial", str(e))
            return

        # Get r
        r = int(self.rank_combobox.get())

        # Creating HammingCalculator object
        calculator = Calculator(poly_A, poly_B, i, j)

        # Output results
        self.result_text_A.delete('1.0', tk.END)
        self.result_text_A.insert(tk.END, "\n".join(" ".join(str(cell) for cell in row) for row in calculator.matrix_A))

        self.result_text_B.delete('1.0', tk.END)
        self.result_text_B.insert(tk.END, "\n".join(" ".join(str(cell) for cell in row) for row in calculator.matrix_B))

        matrix_S = calculator.new_matrix_s(r)
        self.result_text_S.delete('1.0', tk.END)
        self.result_text_S.insert(tk.END, "\n".join(" ".join(str(cell) for cell in row) for row in matrix_S))

        first_row_A = calculator.matrix_A[0]
        first_row_B = calculator.matrix_B[0]

        binary_A = ''.join(map(str, first_row_A))
        binary_B = ''.join(map(str, first_row_B))

        self.F_label_A.config(text=f"Fa(x): {binary_to_F(binary_A)}")
        self.F_label_B.config(text=f"Fb(x): {binary_to_F(binary_B)}")

        self.hamming_weight_value.config(text=f"w(H): {calculator.get_hamming_weight()}")
        self.period_label_A.config(text=f"T(A): {calculator.a_poly.get_period()}")
        self.period_label_B.config(text=f"T(B): {calculator.b_poly.get_period()}")
        self.period_label.config(text=f"T: {calculator.get_matrix_s_period(r)}")
        self.period_exp_label.config(text=f"T(exp): {calculator.get_matrix_s_period(r)}")

        seq = calculator.calculate()
        self.sequence_C.delete('1.0', tk.END)
        self.sequence_C.insert(tk.END, " ".join(str(val) for val in seq))

        hamming_weight_exp = sum(seq)
        self.hamming_weight_exp_value.config(text=f"wH(exp): {hamming_weight_exp}")

        binary_seq = Binary_C(seq)
        self.Binary_C_result.delete('1.0', tk.END)
        self.Binary_C_result.insert(tk.END, "".join(str(bit) for bit in binary_seq))

        acf = calculator.get_acf()
        self.figure.clear()
        plot = self.figure.add_subplot(111)
        plot.plot(acf)
        plot.set_title(f'ACF (Rank {r})')
        plot.set_xlabel('Shift')
        plot.set_ylabel('Autocorrelation')
        plot.grid(True)
        self.plot_canvas.draw()


if __name__ == "__main__":
    app = App()
    icon_path = "scr/images/icon.ico"
    app.iconbitmap(default=icon_path)
    app.mainloop()
