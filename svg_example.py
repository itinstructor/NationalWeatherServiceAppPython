import tkinter as tk
from tkinter import ttk
import urllib.request
import os
import sys
import io
import traceback
from PIL import Image, ImageTk
import tksvg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# Raw GitHub content URL for Erik Flowers' Weather Icons SVG files
BASE_URL = "https://raw.githubusercontent.com/erikflowers/weather-icons/master/svg/"

# Mapping of our descriptions to Erik Flowers' icon names
WEATHER_ICON_MAPPING = {
    "Sunny": "wi-day-sunny.svg",
    "Clear": "wi-night-clear.svg",
    "Partly Cloudy": "wi-day-cloudy.svg",
    "Mostly Cloudy": "wi-cloudy.svg",
    "Cloudy": "wi-cloud.svg",
    "Rain": "wi-rain.svg",
    "Light Rain": "wi-day-rain.svg",
    "Heavy Rain": "wi-rain-wind.svg",
    "Snow": "wi-snow.svg",
    "Light Snow": "wi-day-snow.svg",
    "Thunderstorms": "wi-thunderstorm.svg",
    "Windy": "wi-strong-wind.svg",
    "Fog": "wi-fog.svg",
    "Mist": "wi-day-haze.svg",
    "Drizzle": "wi-sprinkle.svg"
}


class WeatherIconViewer:
    def __init__(self, master):
        self.master = master
        master.title("Weather Icons by Erik Flowers")
        master.geometry("600x500")

        # Ensure weather_icons directory exists
        os.makedirs("weather_icons", exist_ok=True)

        # Description Dropdown
        self.description_var = tk.StringVar()
        self.description_dropdown = ttk.Combobox(
            master,
            textvariable=self.description_var,
            values=list(WEATHER_ICON_MAPPING.keys()),
            state="readonly",
            width=50
        )
        self.description_dropdown.pack(pady=10)
        self.description_dropdown.bind('<<ComboboxSelected>>', self.load_svg)

        # SVG Display Frame
        self.svg_frame = tk.Frame(master, width=400, height=400)
        self.svg_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Image Label
        self.image_label = ttk.Label(self.svg_frame)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Debug Text Area
        self.debug_text = tk.Text(master, height=10, width=70)
        self.debug_text.pack(pady=10)

        # Download Status Label
        self.status_label = ttk.Label(
            master, text="Select a weather description")
        self.status_label.pack(pady=5)

    def log_debug(self, message):
        """Log debug message to text widget"""
        self.debug_text.insert(tk.END, message + "\n")
        self.debug_text.see(tk.END)

    def load_svg(self, event=None):
        """Fetch and display SVG from GitHub with multiple fallback methods"""
        # Clear previous debug messages
        self.debug_text.delete(1.0, tk.END)

        try:
            # Get selected description
            description = self.description_var.get()
            icon_filename = WEATHER_ICON_MAPPING.get(description)

            if not icon_filename:
                raise ValueError(f"No icon found for {description}")

            # Local file path
            local_path = f"weather_icons/{icon_filename}"

            # Attempt to load SVG content
            try:
                # First try local file
                with open(local_path, 'rb') as f:
                    svg_content = f.read()
            except FileNotFoundError:
                # If local file not found, fetch from GitHub
                url = BASE_URL + icon_filename
                self.log_debug(f"Downloading from: {url}")

                with urllib.request.urlopen(url) as response:
                    svg_content = response.read()

                # Save to local file for future use
                with open(local_path, 'wb') as f:
                    f.write(svg_content)

            # Multiple image rendering attempts
            rendered_image = None

            # Method 1: tksvg (if available)
            if tksvg:
                try:
                    self.log_debug("Attempting to render with tksvg")
                    svg_image = tksvg.load(local_path)
                    self.image_label.configure(image=svg_image)
                    self.image_label.image = svg_image
                    rendered_image = svg_image
                    self.log_debug("Successfully rendered with tksvg")
                except Exception as tksvg_err:
                    self.log_debug(f"tksvg rendering failed: {tksvg_err}")

            # Method 2: Pillow SVG to PNG conversion
            if rendered_image is None:
                try:
                    from svglib.svglib import svg2rlg
                    from reportlab.graphics import renderPM

                    self.log_debug(
                        "Attempting to render with svglib and reportlab")
                    drawing = svg2rlg(local_path)
                    png_data = renderPM.drawToString(drawing, fmt='PNG')

                    pil_image = Image.open(io.BytesIO(png_data))
                    pil_image = pil_image.resize((300, 300), Image.LANCZOS)

                    tk_image = ImageTk.PhotoImage(pil_image)
                    self.image_label.configure(image=tk_image)
                    self.image_label.image = tk_image
                    rendered_image = tk_image
                    self.log_debug("Successfully rendered with Pillow")
                except Exception as pil_err:
                    self.log_debug(f"Pillow rendering failed: {pil_err}")

            # Final error if no rendering method works
            if rendered_image is None:
                raise ValueError("Could not render SVG using any method")

            # Update status
            self.status_label.config(
                text=f"Displaying icon for: {description}")

        except Exception as e:
            # Log full traceback
            error_msg = traceback.format_exc()
            self.log_debug(f"Error: {error_msg}")

            # Update status with error
            self.status_label.config(text=f"Error: {str(e)}")


def main():
    # Comprehensive library check and import
    try:
        import tksvg
        import io
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
    except ImportError as e:
        print(f"Missing library: {e}")
        print("Please install with:")
        print("pip install tksvg pillow svglib reportlab")
        sys.exit(1)

    root = tk.Tk()
    app = WeatherIconViewer(root)
    root.mainloop()


if __name__ == "__main__":
    # Installation instructions
    # pip install tksvg pillow svglib reportlab urllib3
    main()
