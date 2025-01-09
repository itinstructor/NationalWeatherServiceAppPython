"""
    Name: nws_GUI.py
    Author:
    Created:
    Purpose: OOP Tkinter app
    Get weather data from the National Weather Service
"""

from base64 import b64decode
from tkinter import Canvas, Tk, messagebox, StringVar
from tkinter import W, E, N, S, Text, END, PhotoImage
from tkinter.ttk import Frame, Scrollbar, Treeview
from tkinter.ttk import LabelFrame, Entry, Label, Button
from nws_class import WeatherClass
from geocode_geopy import geocode
from weather_icon import weather_16
from weather_icon import weather_32


class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("National Weather Service Weather App")
        # Increased window size for hourly forecast
        self.root.geometry("870x800")

        # Set window and taskbar icon
        small_icon = PhotoImage(data=b64decode(weather_16))
        large_icon = PhotoImage(data=b64decode(weather_32))
        self.root.iconphoto(False, large_icon, small_icon)

        self.create_widgets()
        self.weather = WeatherClass()

# ----------------------- CREATE WIDGETS --------------------------------- #
    def create_widgets(self):
        # Create main container with scrollbar
        self.main_canvas = Canvas(self.root)
        self.scrollbar = Scrollbar(
            self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = Frame(self.main_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )
        )

        self.main_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Location Entry Frame
        self.location_frame = LabelFrame(
            self.scrollable_frame, text="Location", padding="5")
        self.location_frame.grid(
            row=0, column=0, columnspan=2, sticky=(W, E), pady=5, padx=5)

        # City/State Entry
        Label(self.location_frame, text="City:").grid(
            row=0, column=0, padx=5)
        self.city_entry = Entry(self.location_frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=5)

        Label(self.location_frame, text="State:").grid(
            row=0, column=2, padx=5)
        self.state_entry = Entry(self.location_frame, width=15)
        self.state_entry.grid(row=0, column=3, padx=5)

        self.city_entry.focus()
        self.city_entry.select_range(0, END)

        self.get_weather_btn = Button(
            self.location_frame, text="Get Weather", command=self.fetch_weather)
        self.get_weather_btn.grid(row=0, column=4, padx=10)

        # Coordinates Display Frame
        self.coords_frame = LabelFrame(
            self.scrollable_frame, text="Coordinates", padding="5")
        self.coords_frame.grid(
            row=1, column=0, columnspan=2, sticky=(W, E), pady=5, padx=5
        )

        self.address_var = StringVar()
        self.coords_var = StringVar()
        self.station_var = StringVar()

        Label(self.coords_frame, textvariable=self.address_var,
              wraplength=900).grid(row=1, column=0, padx=5)
        Label(self.coords_frame, textvariable=self.coords_var).grid(
            row=2, column=0, columnspan=2, padx=5, sticky=W)
        Label(self.coords_frame, textvariable=self.station_var).grid(
            row=3, column=0, columnspan=2, padx=5, sticky=W)

        # Current Weather Frame
        self.current_frame = LabelFrame(
            self.scrollable_frame, text="Current Weather", padding="5")
        self.current_frame.grid(row=2, column=0, sticky=(
            W, E, N, S), pady=5, padx=5)

        # Weather Info Variables
        self.temp_var = StringVar()
        self.desc_var = StringVar()
        self.humidity_var = StringVar()
        self.wind_var = StringVar()
        self.pressure_var = StringVar()
        self.visibility_var = StringVar()
        self.dewpoint_var = StringVar()
        self.windchill_var = StringVar()
        self.heatindex_var = StringVar()
        self.elevation_var = StringVar()

        # Current Weather Labels - Including new metrics
        weather_items = [

            ("Temperature:", self.temp_var),
            ("Description:", self.desc_var),
            ("Humidity:", self.humidity_var),
            ("Wind:", self.wind_var),
            ("Pressure:", self.pressure_var),
            ("Visibility:", self.visibility_var),
            ("Dew Point:", self.dewpoint_var),
            ("Wind Chill:", self.windchill_var),
            ("Heat Index:", self.heatindex_var),
            ("Elevation:", self.elevation_var)
        ]

        # Current Weather Labels
        for i, (label, var) in enumerate(weather_items):
            Label(self.current_frame, text=label).grid(
                row=i, column=0, sticky=W, padx=5)
            Label(self.current_frame, textvariable=var).grid(
                row=i, column=1, sticky=W)

        # Alerts Frame
        self.alerts_frame = LabelFrame(
            self.scrollable_frame, text="Weather Alerts", padding="5")
        self.alerts_frame.grid(
            row=2, column=1, sticky=(W, E, N, S), pady=5, padx=5
        )

        self.alerts_text = Text(self.alerts_frame, width=70, height=11)
        self.alerts_text.grid(row=0, column=0, sticky=(W, E, N, S))

        # Hourly Forecast Frame
        self.hourly_frame = LabelFrame(
            self.scrollable_frame, text="Hourly Forecast (Next 24 Hours)", padding="5")
        self.hourly_frame.grid(row=3, column=0, columnspan=2, sticky=(
            W, E, N, S), pady=5, padx=5)

        # Create Treeview for hourly forecast
        self.hourly_tree = Treeview(self.hourly_frame, columns=(
            "Time", "Temp", "Wind", "Forecast"), show="headings")
        self.hourly_tree.heading("Time", text="Time")
        self.hourly_tree.heading("Temp", text="Temperature")
        self.hourly_tree.heading("Wind", text="Wind")
        self.hourly_tree.heading("Forecast", text="Forecast")

        self.hourly_tree.column("Time", width=150)
        self.hourly_tree.column("Temp", width=100)
        self.hourly_tree.column("Wind", width=150)
        self.hourly_tree.column("Forecast", width=400)

        self.hourly_tree.grid(row=0, column=0, sticky=(W, E, N, S))

        # Add scrollbar to hourly forecast
        hourly_scrollbar = Scrollbar(
            self.hourly_frame, orient="vertical", command=self.hourly_tree.yview)
        hourly_scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.hourly_tree.configure(yscrollcommand=hourly_scrollbar.set)

        # 7-Day Forecast Frame - Modified to use Treeview instead of Text
        self.forecast_frame = LabelFrame(
            self.scrollable_frame, text="7-Day Forecast", padding="5")
        self.forecast_frame.grid(row=4, column=0, columnspan=2, sticky=(
            W, E, N, S), pady=5, padx=5)

        # Create Treeview for 7-day forecast
        self.forecast_tree = Treeview(
            self.forecast_frame,
            columns=(
                "Period", "Temperature", "Wind", "Forecast"),
            show="headings")

        # Configure column headings
        self.forecast_tree.heading("Period", text="Period")
        self.forecast_tree.heading("Temperature", text="Temperature")
        self.forecast_tree.heading("Wind", text="Wind")
        self.forecast_tree.heading("Forecast", text="Forecast")

        # Configure column widths
        self.forecast_tree.column("Period", width=150)
        self.forecast_tree.column("Temperature", width=100)
        self.forecast_tree.column("Wind", width=150)
        self.forecast_tree.column("Forecast", width=400)

        # Add scrollbar to forecast
        forecast_scrollbar = Scrollbar(
            self.forecast_frame, orient="vertical", command=self.forecast_tree.yview)
        forecast_scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.forecast_tree.configure(yscrollcommand=forecast_scrollbar.set)

        # Grid the Treeview
        self.forecast_tree.grid(
            row=0, column=0, sticky=(W, E, N, S))

        # 7-Day Detailed Forecast Frame
        self.detailed_forecast_frame = LabelFrame(
            self.scrollable_frame, text="7-Day Detailed Forecast", padding="5")
        self.detailed_forecast_frame.grid(
            row=5, column=0, columnspan=2, sticky=(W, E, N, S), pady=5, padx=5)

        # Create Treeview for detailed forecast
        self.detailed_forecast_tree = Treeview(
            self.detailed_forecast_frame,
            columns=(
                "Period", "Details"
            ),
            show="headings")

        # Configure column headings
        self.detailed_forecast_tree.heading("Period", text="Period")
        self.detailed_forecast_tree.heading(
            "Details", text="Detailed Forecast")

        # Configure column widths
        self.detailed_forecast_tree.column("Period", width=150)
        self.detailed_forecast_tree.column("Details", width=650)

        # Add scrollbar to detailed forecast
        detailed_forecast_scrollbar = Scrollbar(
            self.detailed_forecast_frame, orient="vertical",
            command=self.detailed_forecast_tree.yview
        )
        detailed_forecast_scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.detailed_forecast_tree.configure(
            yscrollcommand=detailed_forecast_scrollbar.set)
        self.detailed_forecast_tree.grid(
            row=0, column=0, sticky=(W, E, N, S))

        # Pack the main canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both",
                              expand=True, padx=5, pady=5)
        self.scrollbar.pack(side="right", fill="y")

        # Set some sample values (e.g., New York)
        self.city_entry.insert(0, "Scottsbluff")
        self.state_entry.insert(0, "NE")

        # Either enter key will call the method
        self.root.bind("<Return>", self.fetch_weather)
        self.root.bind("<KP_Enter>", self.fetch_weather)
        self.root.bind("<Escape>", self.quit)

# ----------------------- FETCH WEATHER ---------------------------------- #
    def fetch_weather(self, *args):
        try:
            city = self.city_entry.get().strip()
            state = self.state_entry.get().strip()

            if not city or not state:
                messagebox.showerror(
                    "Error", "Please enter both city and state")
                return

            # Get coordinates from city/state
            location_info = geocode(city, state, country="US")
            if not location_info:
                return

            lat, lng, address = location_info

            # Update coordinates and address display
            self.coords_var.set(f"Coordinates: {lat:.4f}, {lng:.4f}")
            self.address_var.set(f"Location: {address}")

            # Get weather data
            self.weather.get_gridpoints(lat, lng)
            self.weather.get_latest_weather_observation()
            self.weather.process_latest_weather_observation()
            self.weather.get_active_weather_alerts(lat, lng)
            self.weather.get_weather_alerts(lat, lng)
            self.weather.get_7_day_forecast()
            self.weather.get_hourly_forecast()

            # Update current weather display
            self.station_var.set(f"Station Name: {self.weather.station_name}")
            self.temp_var.set(f"{self.weather.temperature}°F")
            self.desc_var.set(self.weather.description)
            self.humidity_var.set(f"{self.weather.humidity}%")
            self.wind_var.set(
                f"{self.weather.wind_speed} mph {
                    self.weather.wind_cardinal}"
            )
            self.pressure_var.set(f"{self.weather.pressure} inHg")
            self.visibility_var.set(f"{self.weather.visibility} miles")

            # Add new metrics (assuming these properties exist in WeatherClass)
            self.dewpoint_var.set(f"{self.weather.dewpoint}°F" if hasattr(
                self.weather, 'dewpoint') else "N/A")
            self.windchill_var.set(f"{self.weather.windchill}°F" if hasattr(
                self.weather, 'windchill') else "N/A")
            self.heatindex_var.set(f"{self.weather.heatindex}°F" if hasattr(
                self.weather, 'heatindex') else "N/A")
            self.elevation_var.set(f"{self.weather.elevation} ft" if hasattr(
                self.weather, 'elevation') else "N/A")

            # Update alerts
            self.alerts_text.delete(1.0, END)
            # Display active alerts
            self.alerts_text.insert(END, "Active Alerts:\n")
            active_alerts = self.weather.active_weather_alert_dict.get(
                'features', [])
            if active_alerts:
                for alert in active_alerts:
                    properties = alert.get('properties', {})
                    self.alerts_text.insert(
                        END, f"Event: {properties.get('event', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Severity: {properties.get('severity', 'N/A')}\n"
                    )
                    self.alerts_text.insert(
                        END,
                        f"Headline: {properties.get('headline', 'N/A')}\n\n"
                    )
            else:
                self.alerts_text.insert(END, "No active alerts\n\n")

            # Display general weather alerts
            self.alerts_text.insert(END, "General Alerts:\n")
            general_alerts = self.weather.weather_alert_dict.get(
                'features', [])
            if general_alerts:
                for alert in general_alerts:
                    properties = alert.get('properties', {})
                    self.alerts_text.insert(
                        END, f"Event: {properties.get('event', 'N/A')}\n")
                    self.alerts_text.insert(
                        END, f"Severity: {properties.get('severity', 'N/A')}\n"
                    )
                    self.alerts_text.insert(
                        END,
                        f"Headline: {properties.get('headline', 'N/A')}\n\n"
                    )
            else:
                self.alerts_text.insert(END, "No general alerts\n")

            # Update hourly forecast
            self.hourly_tree.delete(*self.hourly_tree.get_children())
            if hasattr(self.weather, 'forecast_hourly_list'):
                # Show next 24 hours
                for period in self.weather.forecast_hourly_list[:24]:
                    self.hourly_tree.insert("", "end", values=(
                        period['startTime'].split('T')[1][:5],  # Time
                        f"{period['temperature']}°{period['temperatureUnit']}",
                        f"{period['windSpeed']} {period['windDirection']}",
                        period['shortForecast']
                    ))

            self.forecast_tree.delete(*self.forecast_tree.get_children())
            self.detailed_forecast_tree.delete(
                *self.detailed_forecast_tree.get_children())

            if hasattr(self.weather, 'forecast_list'):
                for period in self.weather.forecast_list:
                    # Update simple forecast
                    self.forecast_tree.insert("", "end", values=(
                        period['name'],
                        f"{period['temperature']}°{period['temperatureUnit']}",
                        f"{period['windSpeed']} {period['windDirection']}",
                        period['shortForecast']
                    ))

                    # Update detailed forecast
                    self.detailed_forecast_tree.insert("", "end", values=(
                        period['name'],
                        period.get(
                            'detailedForecast', 'No detailed forecast available')
                    ))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        self.city_entry.focus()
        self.city_entry.select_range(0, END)

# ------------------------- QUIT PROGRAM --------------------------------- #
    def quit(self, *args):
        self.root.destroy()


def main():
    root = Tk()
    app = WeatherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
