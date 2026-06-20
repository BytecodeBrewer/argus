import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from legacy.analytics.charts.trend_chart import create_trendchart


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
    hide_trend_chart()

    menu_frame.pack(side="right", fill=tk.BOTH, expand=True)

def show_trend() -> None:
    """
    Displays the trend chart in the application. It prepares the data for trend analysis,
    creates the trend chart, and updates the GUI to show the chart.
    """
    global trend_canvas
    global trend_chart_widget

    mock_dates = {
        "date": [
            "2026-06-01",
            "2026-06-02",
            "2026-06-03",
            "2026-06-04",
            "2026-06-05",
            "2026-06-06",
            "2026-06-07",
            "2026-06-08",
            "2026-06-09",
            "2026-06-10",
            "2026-06-11",
            "2026-06-12",
            "2026-06-13",
            "2026-06-14",
            "2026-06-15",
        ]
    }
    mock_dates = pd.DataFrame(mock_dates)
    mock_curr = "USD"

    menu_frame.pack_forget()

    app_frame.pack(fill=tk.BOTH, expand=True)
    sidebar.pack(side="top", fill="x")
    content.pack(side="top", fill=tk.BOTH, expand=True)

    if trend_canvas is None:
        fig = create_trendchart(mock_curr, mock_dates)
        fig.set_size_inches(7, 4)

        trend_canvas = FigureCanvasTkAgg(fig, master=content)
        trend_chart_widget = trend_canvas.get_tk_widget()

    if trend_chart_widget is None:
        return
    trend_canvas.draw()
    trend_chart_widget.pack(fill=tk.BOTH, expand=True)


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

# Trend chart is loaded lazily
trend_canvas = None
trend_chart_widget = None

# Labels
menu_label = tk.Label(menu_frame, text="Menu", font=("Arial", 20))
menu_label.pack(pady=20)


# Buttons
from_menu_trend_chart = tk.Button(menu_frame, text="Trend Chart", command=show_trend)
from_sidebar_trend_chart = tk.Button(sidebar, text="Trend Chart", command=show_trend)
return_menu = tk.Button(sidebar, text="Back to menu", command=show_menu)

from_menu_trend_chart.pack(fill="x", padx=50, pady=15)
from_sidebar_trend_chart.pack(side="left")
return_menu.pack(side="left")

show_menu()

if __name__ == "__main__":
    app()
