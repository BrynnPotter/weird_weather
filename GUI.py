
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import os
from app_core import geocode_city, get_weather_data

def run_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return
    
    result_text.set("Loading weather data....")

    def task1(city_name):
        try:
                location = geocode_city(city_name)
                data = get_weather_data(location)

                temp = data["temperature"]
                humidity = data["humidity"]

                if temp > 30.0:
                    msg = "It's a hot day! but is this measuring Fahrenheit or Celsius? (Celsius for now.)"
                elif temp > 20.0:
                    msg = "It's a nice day! or maybe very cold, I don't know yet."
                else:
                    msg = "Bring a jacket maybe. I don't know lol."

                output = (
                    f"Weather for {city_name}:\n"
                    f"Temperature: {temp}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"{msg}"
                )
                result_text.set(output)

        except Exception as e:
                result_text.set("")
                messagebox.showerror("Error", str(e))

    threading.Thread(target=lambda: task1(city)).start()

# GUI Setup
window = tk.Tk()
window.title("Weird_Weather")
window.geometry("500x400")
window.configure(bg="black")

tk.Label(window, text="Enter a city name:", bg="black", fg="white").pack(pady=10)
city_entry = tk.Entry(window, width=30)
city_entry.pack()

tk.Button(window, text="Get Weather", command=run_weather).pack(pady=10)

result_text = tk.StringVar()
tk.Label(window, textvariable=result_text, bg="black", fg="white", wraplength=400, justify="left").pack(pady=20)

window.mainloop()
