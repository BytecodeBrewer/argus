import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from argus.analytics.charts.trend_chart import create_trendchart
from argus.services.calculator_service import calc, check_op
from argus.services.conversion_service import convert, check_currency
from argus.domain.validation import parse_amount


def on_close() -> None:
    """
    Handles the closing of the application window. It ensures that any open trend chart is destroyed and
    the application is properly closed.
    """
    if trend_chart_widget is not None:
        trend_chart_widget.destroy()

    root.quit()
    root.destroy()


def hide_trend_chart() -> None:
    """
    Hides the trend chart from the GUI if it is currently displayed.
    """
    if trend_chart_widget is not None:
        trend_chart_widget.pack_forget()


def show_menu() -> None:
    """
    Displays the main menu in the application. It updates the GUI to show the menu interface.
    """
    app_frame.pack_forget()
    calc_frame.pack_forget()
    conv_frame.pack_forget()
    hide_trend_chart()

    menu_frame.pack(side="right", fill=tk.BOTH, expand=True)


def show_calc() -> None:
    """
    Displays the calculator in the application. It updates the GUI to show the calculator interface.
    """
    conv_frame.pack_forget()
    hide_trend_chart()
    menu_frame.pack_forget()

    app_frame.pack(fill=tk.BOTH, expand=True)
    sidebar.pack(side="top", fill="x")
    content.pack(side="top", fill=tk.BOTH, expand=True)

    calc_frame.pack(fill=tk.BOTH, expand=True)


def show_conv() -> None:
    """
    Displays the currency converter in the application. It updates the GUI to show the converter interface.
    """
    calc_frame.pack_forget()
    hide_trend_chart()
    menu_frame.pack_forget()

    app_frame.pack(fill=tk.BOTH, expand=True)
    sidebar.pack(side="top", fill="x")
    content.pack(side="top", fill=tk.BOTH, expand=True)

    conv_frame.pack(fill=tk.BOTH, expand=True)


def show_trend() -> None:
    """
    Displays the trend chart in the application. It prepares the data for trend analysis,
    creates the trend chart, and updates the GUI to show the chart.
    """
    global trend_canvas
    global trend_chart_widget

    curr_symbol = "EURUSD=X",
    start="2024-01-01",
    end="2024-02-01",
    interval="1d"

    calc_frame.pack_forget()
    conv_frame.pack_forget()
    menu_frame.pack_forget()

    app_frame.pack(fill=tk.BOTH, expand=True)
    sidebar.pack(side="top", fill="x")
    content.pack(side="top", fill=tk.BOTH, expand=True)

    if trend_canvas is None:
        fig = create_trendchart(curr_symbol,start,end,interval)
        fig.set_size_inches(7, 4)

        trend_canvas = FigureCanvasTkAgg(fig, master=content)
        trend_chart_widget = trend_canvas.get_tk_widget()

    if trend_chart_widget is None:
        return
    trend_canvas.draw()
    trend_chart_widget.pack(fill=tk.BOTH, expand=True)


def act_calculate() -> None:
    """
    Handles the calculation action when the "Calculate" button is clicked.
    It checks the validity of the input numbers and operator, performs the calculation,
    and updates the result label accordingly.
    """
    resp1 = num1.get()
    resp1 = parse_amount(resp1)

    resp2 = num2.get()
    resp2 = parse_amount(resp2)

    op = op_e.get()

    if resp1 is None:
        result_calc_label.config(text="Please enter a valid number for 'Number 1'.")
        return

    if resp2 is None:
        result_calc_label.config(text="Please enter a valid number for 'Number 2'.")
        return

    if check_op(op) is False:
        result_calc_label.config(text="Please enter a valid operation for 'Operation'.")
        return

    result = calc(resp1, resp2, op)

    if result is None:
        result_calc_label.config(text="Division by zero is not possible.")
        return

    result_calc_label.config(text=f"{resp1} {op} {resp2} = {result}")


def act_convert() -> None:
    """
    Handles the conversion action when the "Convert" button is clicked.
    It checks the validity of the input currencies and amount, performs the conversion,
    and updates the result label accordingly.
    """
    resp1 = check_currency(curr1.get())
    resp2 = check_currency(curr2.get())
    amount = parse_amount(amount_e.get())

    if resp1 is None:
        result_conv_label.config(text="Please enter a valid currency for 'Currency 1'")
        return

    if resp2 is None:
        result_conv_label.config(text="Please enter a valid currency for 'Currency 2'")
        return

    if amount is None:
        result_conv_label.config(
            text="Please enter a valid amount in the 'Amount' field"
        )
        return

    response = convert(amount, resp1, resp2)

    if response is None:
        result_conv_label.config(text="Currency conversion error")
        return

    result = response
    result_conv_label.config(
        text=f"The exchange rate from {resp1} to {resp2} for {amount} {resp1} is {result} {resp2}"
    )


def app() -> None:
    """
    The main function that initializes and starts the GUI application. It sets up the main window, frames, labels, entries, and buttons, and defines the layout of the application.
    """
    root.mainloop()


# Window
root = tk.Tk()
root.title("FX-Converter Lab")
root.geometry("800x600")  # Width x Length
root.protocol("WM_DELETE_WINDOW", on_close)

# Frames
menu_frame = tk.Frame(root)
app_frame = tk.Frame(root)
sidebar = tk.Frame(app_frame)
content = tk.Frame(app_frame)
conv_frame = tk.Frame(content)
calc_frame = tk.Frame(content)

# Trend chart is loaded lazily
trend_canvas = None
trend_chart_widget = None

# Labels
menu_label = tk.Label(menu_frame, text="Menu", font=("Arial", 20))
calc_label = tk.Label(calc_frame, text="Calculator", font=("Arial", 20))
conv_label = tk.Label(conv_frame, text="Converter", font=("Arial", 20))

num1_label = tk.Label(calc_frame, text="Number 1:")
num2_label = tk.Label(calc_frame, text="Number 2:")
op_label = tk.Label(calc_frame, text="Operation:")

amount_label = tk.Label(conv_frame, text="Amount:")
curr1_label = tk.Label(conv_frame, text="Currency 1:")
curr2_label = tk.Label(conv_frame, text="Currency 2:")

result_calc_label = tk.Label(calc_frame)
result_conv_label = tk.Label(conv_frame)

menu_label.pack(pady=20)

calc_label.grid(pady=20, column=1, row=0)
conv_label.grid(pady=20, column=1, row=0)

num1_label.grid(pady=5, column=0, row=1)
num2_label.grid(pady=5, column=0, row=2)
op_label.grid(pady=5, column=0, row=3)

amount_label.grid(pady=5, column=0, row=1)
curr1_label.grid(pady=5, column=0, row=2)
curr2_label.grid(pady=5, column=0, row=3)

result_calc_label.grid(column=1, row=5)
result_conv_label.grid(column=1, row=5)

# Entries
num1 = tk.Entry(calc_frame)
num2 = tk.Entry(calc_frame)
op_e = tk.Entry(calc_frame)

amount_e = tk.Entry(conv_frame)
curr1 = tk.Entry(conv_frame)
curr2 = tk.Entry(conv_frame)

num1.grid(pady=5, column=1, row=1)
num2.grid(pady=5, column=1, row=2)
op_e.grid(pady=5, column=1, row=3)

amount_e.grid(pady=5, column=1, row=1)
curr1.grid(pady=5, column=1, row=2)
curr2.grid(pady=5, column=1, row=3)

num1.focus()

# Buttons
from_menu_calc = tk.Button(menu_frame, text="Calculator", command=show_calc)
from_menu_conv = tk.Button(menu_frame, text="Converter", command=show_conv)
from_menu_trend_chart = tk.Button(menu_frame, text="Trend Chart", command=show_trend)

from_sidebar_calc = tk.Button(sidebar, text="Calculator", command=show_calc)
from_sidebar_conv = tk.Button(sidebar, text="Converter", command=show_conv)
from_sidebar_trend_chart = tk.Button(sidebar, text="Trend Chart", command=show_trend)
return_menu = tk.Button(sidebar, text="Back to menu", command=show_menu)

click_calculate = tk.Button(calc_frame, text="Calculate", command=act_calculate)
click_converter = tk.Button(conv_frame, text="Convert", command=act_convert)

from_menu_calc.pack(fill="x", padx=50, pady=15)
from_menu_conv.pack(fill="x", padx=50, pady=15)
from_menu_trend_chart.pack(fill="x", padx=50, pady=15)

from_sidebar_calc.pack(side="left")
from_sidebar_conv.pack(side="left")
from_sidebar_trend_chart.pack(side="left")
return_menu.pack(side="left")

click_calculate.grid(column=1, row=4)
click_converter.grid(column=1, row=4)

show_menu()

if __name__ == "__main__":
    app()
