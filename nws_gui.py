"""
    Name: nws_GUI.py
    Author:
    Created:
    Purpose: OOP Tkinter app
    Get weather data from the National Weather Service
    Claude.ai and GitHub Copilot were code helpers
"""

from base64 import b64decode
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from tktooltip import ToolTip
from nws_class import WeatherClass
from geocode_geopy import geocode
from weather_icon import weather_16
from weather_icon import weather_32


class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("National Weather Service Weather App")

        self.root.geometry("+75+75")

        # Remove the title bar
        self.root.overrideredirect(True)

        # Set window and taskbar icon using base64 encoded image data
        small_icon = ttk.PhotoImage(data=b64decode(weather_16))
        large_icon = ttk.PhotoImage(data=b64decode(weather_32))
        self.root.iconphoto(False, large_icon, small_icon)

        # Set style for Treeview rowheight to separate rows
        style = ttk.Style()

        # Adjust rowheight as needed
        style.configure("Treeview", rowheight=35)

        # Bind mouse events to enable dragging
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        self.x = None
        self.y = None
        self.create_widgets()
        self.weather = WeatherClass()

# ----------------------- FETCH WEATHER ---------------------------------- #
    def fetch_weather(self, *args):
        try:
            city = self.city_entry.get().strip()
            state = self.state_entry.get().strip()

            # Check if city and state are entered
            if not city or not state:
                ttk.messagebox.showerror(
                    "Error", "Please enter both city and state")
                return

            # Geocode city and astate to get coordinates from city/state
            location_info = geocode(city, state, country="US")
            if not location_info:
                return

            # Unpack location_info tuple
            lat, lng, address = location_info

            # Update coordinates and address display
            self.coords_var.set(f"Coordinates: {lat:.4f}, {lng:.4f}")
            self.address_var.set(f"Location: {address}")

        # ----------------- GET WEATHER DATA ----------------------------- #
            self.weather.get_gridpoints(lat, lng)
            self.weather.get_latest_weather_observation()
            self.weather.process_latest_weather_observation()
            self.weather.get_active_weather_alerts(lat, lng)
            self.weather.get_weather_alerts(lat, lng)
            self.weather.get_7_day_forecast()
            self.weather.get_hourly_forecast()

        # ----------------- UPDATE CURRENT WEATHER ----------------------- #
            self.station_var.set(f"Station Name: {self.weather.station_name}")
            self.temp_var.set(f"{self.weather.temperature}°F")
            self.desc_var.set(self.weather.description)
            self.humidity_var.set(f"{self.weather.humidity}%")
            self.wind_var.set(f"{self.weather.wind_speed} mph {
                              self.weather.wind_cardinal}")
            self.pressure_var.set(f"{self.weather.pressure} inHg")
            self.visibility_var.set(f"{self.weather.visibility} miles")

            self.dewpoint_var.set(f"{self.weather.dewpoint}°F" if hasattr(
                self.weather, 'dewpoint') else "N/A")
            self.windchill_var.set(f"{self.weather.windchill}°F" if hasattr(
                self.weather, 'windchill') else "N/A")
            self.heatindex_var.set(f"{self.weather.heatindex}°F" if hasattr(
                self.weather, 'heatindex') else "N/A")
            self.elevation_var.set(f"{self.weather.elevation} ft" if hasattr(
                self.weather, 'elevation') else "N/A")

        # ----------------- CLEAR ALERTS TEXT ---------------------------- #
            self.alerts_text.delete(1.0, END)

        # ----------------- DISPLAY ACTIVE ALERTS ------------------------ #
            self.alerts_text.insert(END, "Active Alerts:\n")
            active_alerts = self.weather.active_weather_alert_dict.get(
                'features', [])
            if active_alerts:
                for alert in active_alerts:
                    properties = alert.get('properties', {})
                    self.alerts_text.insert(
                        END, f"Event: {properties.get('event', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Severity: {properties.get('severity', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Headline: {properties.get('headline', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Description: {properties.get('description', 'N/A')}\n\n")
            else:
                self.alerts_text.insert(END, "No active alerts\n\n")

        # ----------------- DISPLAY GENERAL ALERTS ----------------------- #
            self.alerts_text.insert(END, "General Alerts:\n")
            general_alerts = self.weather.weather_alert_dict.get(
                'features', [])
            if general_alerts:
                for alert in general_alerts:
                    properties = alert.get('properties', {})
                    self.alerts_text.insert(
                        END, f"Event: {properties.get('event', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Severity: {properties.get('severity', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Headline: {properties.get('headline', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Description: {properties.get('description', 'N/A')}\n\n")
            else:
                self.alerts_text.insert(END, "No general alerts\n")

        # ----------------- UPDATE HOURLY FORECAST ----------------------- #
            self.hourly_tree.delete(*self.hourly_tree.get_children())

            if hasattr(self.weather, 'forecast_hourly_list'):
                for index, period in enumerate(self.weather.forecast_hourly_list[:24]):
                    # Apply "oddrow" tag to even-indexed rows
                    # and "evenrow" to odd-indexed rows
                    row_tag = "oddrow" if index % 2 == 0 else "evenrow"
                    self.hourly_tree.insert(
                        "",
                        "end",
                        values=(
                            period['startTime'].split('T')[1][:5],  # Time
                            f"{period['temperature']}°{
                                period['temperatureUnit']}",
                            f"{period['windSpeed']}",
                            f"{period['windDirection']}",
                            period['shortForecast']
                        ),
                        tags=(row_tag,)  # Added tags parameter
                    )

        # ----------------- UPDATE 7-DAY FORECAST ------------------------ #
            self.forecast_tree.delete(*self.forecast_tree.get_children())
            self.detailed_forecast_tree.delete(
                *self.detailed_forecast_tree.get_children())

            if hasattr(self.weather, 'forecast_list'):
                for index, period in enumerate(self.weather.forecast_list):
                    # Apply "oddrow" tag to even-indexed rows
                    # and "evenrow" to odd-indexed rows
                    row_tag = "oddrow" if index % 2 == 0 else "evenrow"
                    # Update simple forecast
                    self.forecast_tree.insert("", "end", values=(
                        period['name'],
                        f"{period['temperature']}°{period['temperatureUnit']}",
                        f"{period['windSpeed']}",
                        f"{period['windDirection']}",
                        period['shortForecast']
                    ),
                        tags=(row_tag,)  # Added tags parameter
                    )

                    # Update detailed forecast
                    self.detailed_forecast_tree.insert("", "end", values=(
                        period['name'],
                        period.get(
                            'detailedForecast',
                            'No detailed forecast available'
                        )
                    ),
                        tags=(row_tag,)  # Added tags parameter
                    )

        except Exception as e:
            ttk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Focus on city entry and select all text for ease of data entry
        self.city_entry.focus()
        self.city_entry.select_range(0, END)

# ----------------------- CREATE WIDGETS --------------------------------- #
    def create_widgets(self):
        # Set padding for all widgets
        PADX = 6
        PADY = 6
        IPADX = 2
        IPADY = 2

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(self.root, padding="8")
        self.notebook.grid(row=0, column=0, sticky=(W, E, N, S))

        # Create frames for each tab
        self.current_weather_frame = ttk.Frame(self.notebook)
        self.alerts_frame = ttk.Frame(self.notebook)
        self.hourly_forecast_frame = ttk.Frame(self.notebook)
        self.forecast_frame = ttk.Frame(self.notebook)
        self.detailed_forecast_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.current_weather_frame, text="Current Weather")
        self.notebook.add(self.alerts_frame, text="Weather Alerts")
        self.notebook.add(self.hourly_forecast_frame, text="Hourly Forecast")
        self.notebook.add(self.forecast_frame, text="7-Day Forecast")
        self.notebook.add(
            self.detailed_forecast_frame,
            text="7-Day Detailed Forecast"
        )

    # -------------------- CURRENT WEATHER FRAME ------------------------- #
        self.desc_var = ttk.StringVar()
        self.temp_var = ttk.StringVar()
        self.humidity_var = ttk.StringVar()
        self.wind_var = ttk.StringVar()
        self.pressure_var = ttk.StringVar()
        self.visibility_var = ttk.StringVar()
        self.dewpoint_var = ttk.StringVar()
        self.windchill_var = ttk.StringVar()
        self.heatindex_var = ttk.StringVar()
        self.elevation_var = ttk.StringVar()

        weather_items = [
            ("Description:", self.desc_var),
            ("Temperature:", self.temp_var),
            ("Humidity:", self.humidity_var),
            ("Wind:", self.wind_var),
            ("Pressure:", self.pressure_var),
            ("Visibility:", self.visibility_var),
            ("Dew Point:", self.dewpoint_var),
            ("Wind Chill:", self.windchill_var),
            ("Heat Index:", self.heatindex_var),
            ("Elevation:", self.elevation_var)
        ]

        # Create labels and text variables for current weather
        # enumerate(weather_items) returns an iterator that produces pairs
        # of an index and the corresponding item from weather_items.
        # for i, (label, var) in enumerate(weather_items):
        # iterates over these pairs, unpacking each pair into
        # i (the index), label, and var.
        for i, (label, var) in enumerate(weather_items):
            ttk.Label(self.current_weather_frame, text=label).grid(
                row=i, column=0, sticky=E)
            ttk.Label(self.current_weather_frame, textvariable=var).grid(
                row=i, column=1, sticky=W)

        self.lbl_icon = ttk.Label(self.current_weather_frame)
        self.lbl_icon.grid(row=0, column=2)
        # self.weather_icon_url = "https://example.com/weather_icon.png"
        # self.weather_icon_image = ttk.PhotoImage(file=self.weather_icon_url)
        # self.lbl_icon.config(image=self.weather_icon_image)

    # --------------------- ALERTS FRAME --------------------------------- #
        self.alerts_text = ttk.Text(self.alerts_frame, width=105, height=17)
        self.alerts_text.grid(row=0, column=0, sticky=(W, E, N, S))

        # Add vertical scrollbar to alerts frame
        alerts_scrollbar = ttk.Scrollbar(
            self.alerts_frame,
            orient="vertical",
            command=self.alerts_text.yview
        )
        alerts_scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.alerts_text.configure(yscrollcommand=alerts_scrollbar.set)

    # ------------------ HOURLY FORECAST TREEVIEW ------------------------ #
        TREE_HEIGHT = 11
        self.hourly_tree = ttk.Treeview(
            self.hourly_forecast_frame,
            columns=(
                "Time", "Temp", "Wind Spd", "Wind Dir", "Forecast"
            ),
            show="headings",
            height=TREE_HEIGHT
        )

        # Define alternating row tags for banded row display
        self.hourly_tree.tag_configure("oddrow", background="gray30")
        self.hourly_tree.tag_configure("evenrow", background="gray15")

        self.hourly_tree.heading("Time", text="Time")
        self.hourly_tree.heading("Temp", text="Temp")
        self.hourly_tree.heading("Wind Spd", text="Wind Spd")
        self.hourly_tree.heading("Wind Dir", text="Wind Dir")
        self.hourly_tree.heading("Forecast", text="Forecast")

        self.hourly_tree.column("Time", width=95)
        self.hourly_tree.column("Temp", width=95)
        self.hourly_tree.column("Wind Spd", width=100)
        self.hourly_tree.column("Wind Dir", width=100)
        self.hourly_tree.column("Forecast", width=300)

        self.hourly_tree.grid(row=0, column=0, sticky=(W, E, N, S))

        hourly_scrollbar = ttk.Scrollbar(
            self.hourly_forecast_frame,
            orient="vertical",
            command=self.hourly_tree.yview
        )
        hourly_scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.hourly_tree.configure(yscrollcommand=hourly_scrollbar.set)

    # ----------------------- COORDINATES FRAME -------------------------- #
        self.coords_frame = ttk.LabelFrame(self.root, text="Coordinates")
        self.coords_frame.grid(row=1, column=0, columnspan=2, sticky=(W, E))

        self.address_var = ttk.StringVar()
        self.coords_var = ttk.StringVar()
        self.station_var = ttk.StringVar()

        ttk.Label(self.coords_frame, textvariable=self.address_var,
                  wraplength=900).grid(row=1, column=0, sticky=W)
        ttk.Label(self.coords_frame, textvariable=self.coords_var).grid(
            row=2, column=0, sticky=W)
        ttk.Label(self.coords_frame, textvariable=self.station_var).grid(
            row=3, column=0, sticky=W)

    # ----------------------- LOCATION FRAME ----------------------------- #
        self.location_frame = ttk.LabelFrame(
            self.root, text="Location", padding="5")
        self.location_frame.grid(row=2, column=0, columnspan=2, sticky=(W, E))

        # City Entry
        ttk.Label(self.location_frame, text="City:").grid(row=0, column=0)
        self.city_entry = ttk.Entry(self.location_frame, width=30)
        self.city_entry.grid(row=0, column=1)

        # State Entry
        ttk.Label(self.location_frame, text="State:").grid(row=0, column=2)
        self.state_entry = ttk.Entry(self.location_frame, width=15)
        self.state_entry.grid(row=0, column=3)

        # Get Weather Button
        self.btn_get_weather = ttk.Button(
            self.location_frame, text="Get Weather",
            command=self.fetch_weather, width=14)
        self.btn_get_weather.grid(row=0, column=4)

        # Exit Button
        self.btn_quit = ttk.Button(
            self.location_frame, text="Quit", command=self.quit, width=14
        )
        self.btn_quit.grid(row=0, column=5)

    # ----------------- 7-DAY FORECAST TREEVIEW -------------------------- #
        self.forecast_tree = ttk.Treeview(
            self.forecast_frame, columns=(
                "Period", "Temperature", "Wind Spd", "Wind Dir", "Forecast"
            ),
            show="headings",
            height=TREE_HEIGHT
        )

        # Define alternating row tags for banded row display
        self.forecast_tree.tag_configure("oddrow", background="gray30")
        self.forecast_tree.tag_configure("evenrow", background="gray15")

        self.forecast_tree.heading("Period", text="Period")
        self.forecast_tree.heading("Temperature", text="Temp")
        self.forecast_tree.heading("Wind Spd", text="Wind Spd")
        self.forecast_tree.heading("Wind Dir", text="Wind Dir")
        self.forecast_tree.heading("Forecast", text="Forecast")

        self.forecast_tree.column("Period", width=175)
        self.forecast_tree.column("Temperature", width=85)
        self.forecast_tree.column("Wind Spd", width=135)
        self.forecast_tree.column("Wind Dir", width=90)
        self.forecast_tree.column("Forecast", width=525)

        forecast_scrollbar = ttk.Scrollbar(
            self.forecast_frame, orient="vertical",
            command=self.forecast_tree.yview
        )
        forecast_scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.forecast_tree.configure(yscrollcommand=forecast_scrollbar.set)
        self.forecast_tree.grid(row=0, column=0, sticky=(W, E, N, S))

    # ------------------ DETAILED FORECAST TREEVIEW ---------------------- #
        self.detailed_forecast_tree = ttk.Treeview(
            self.detailed_forecast_frame,
            columns=("Period", "Details"), show="headings",
            height=TREE_HEIGHT
        )

        # Define alternating row tags for banded row display
        self.detailed_forecast_tree.tag_configure(
            "oddrow", background="gray30")
        self.detailed_forecast_tree.tag_configure(
            "evenrow", background="gray15")

        self.detailed_forecast_tree.heading("Period", text="Period")
        self.detailed_forecast_tree.heading(
            "Details", text="Detailed Forecast")

        self.detailed_forecast_tree.column("Period", width=150)
        self.detailed_forecast_tree.column("Details", width=900)

        xdetailed_forecast_scrollbar = ttk.Scrollbar(
            self.detailed_forecast_frame, orient="horizontal",
            command=self.detailed_forecast_tree.xview
        )
        xdetailed_forecast_scrollbar.grid(row=1, column=0, sticky=(E, W))

        detailed_forecast_scrollbar = ttk.Scrollbar(
            self.detailed_forecast_frame, orient="vertical",
            command=self.detailed_forecast_tree.yview)
        detailed_forecast_scrollbar.grid(row=0, column=1, sticky=(N, S))

        self.detailed_forecast_tree.configure(
            yscrollcommand=detailed_forecast_scrollbar.set,
            xscrollcommand=xdetailed_forecast_scrollbar.set
        )

        self.detailed_forecast_tree.grid(row=0, column=0, sticky=(W, E, N, S))

        for child in self.root.winfo_children():
            child.grid_configure(padx=10, pady=10, ipadx=IPADX, ipady=IPADY)

        for child in self.location_frame.winfo_children():
            child.grid_configure(padx=PADX,
                                 ipadx=IPADX, ipady=IPADY)
        for child in self.coords_frame.winfo_children():
            child.grid_configure(padx=PADX,
                                 ipadx=IPADX, ipady=IPADY)

        for child in self.current_weather_frame.winfo_children():
            child.grid_configure(padx=PADX, pady=PADY,
                                 ipadx=IPADX, ipady=IPADY)
        for child in self.hourly_forecast_frame.winfo_children():
            child.grid_configure(padx=PADX, pady=PADY,
                                 ipadx=IPADX, ipady=IPADY)
        for child in self.forecast_frame.winfo_children():
            child.grid_configure(padx=PADX, pady=PADY,
                                 ipadx=IPADX, ipady=IPADY)
        for child in self.detailed_forecast_frame.winfo_children():
            child.grid_configure(padx=PADX, pady=PADY,
                                 ipadx=IPADX, ipady=IPADY)
        for child in self.alerts_frame.winfo_children():
            child.grid_configure(padx=PADX, pady=PADY,
                                 ipadx=IPADX, ipady=IPADY)

        # Add tooltips to buttons
        ToolTip(self.btn_quit, "Press Esc to quit")
        ToolTip(self.btn_get_weather, "Press Enter to get weather")

        # Set some sample values (e.g., New York)
        self.city_entry.insert(0, "Scottsbluff")
        self.state_entry.insert(0, "NE")

        # Focus on city entry and select all text for ease of data entry
        self.city_entry.focus()
        self.city_entry.select_range(0, END)

        # Either enter key will call the method
        self.root.bind("<Return>", self.fetch_weather)
        self.root.bind("<KP_Enter>", self.fetch_weather)
        self.root.bind("<Escape>", self.quit)

# -------------------------- DRAG WINDOW --------------------------------- #
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        # Calculate the change in position
        deltax = event.x - self.x
        deltay = event.y - self.y
        # Move the window to the new position
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        # Update the window position
        self.root.geometry(f"+{x}+{y}")

# ---------------------------- QUIT -------------------------------------- #
    def quit(self, *args):
        self.root.destroy()


def main():
    root = ttk.Window(themename="darkly")
    app = WeatherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
