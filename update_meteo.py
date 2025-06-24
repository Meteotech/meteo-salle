import requests
import datetime
import os
from bs4 import BeautifulSoup

# Configuration
API_KEY = "799db06a223c052d8a87d583898c2d3d"  # Replace with your actual OpenWeatherMap API key
CITY = "Guyancourt"
IMAGE_RULES = [
    (0, 27, "Picture1.png"),
    (27, 30, "Picture2.png"),
    (30, 31.9, "Picture3.png"),
    (31.9, float("inf"), "Picture4.png")
]

# Function to get forecast temperatures for today and tomorrow (morning, noon, evening)
def get_forecast_temperatures():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    temps = {"today": {"morning": None, "noon": None, "evening": None},
             "tomorrow": {"morning": None, "noon": None, "evening": None}}

    for entry in data["list"]:
        dt = datetime.datetime.fromtimestamp(entry["dt"])
        date = dt.date()
        hour = dt.hour
        temp = entry["main"]["temp"]

        if date == today:
            if hour == 9 and temps["today"]["morning"] is None:
                temps["today"]["morning"] = temp
            elif hour == 12 and temps["today"]["noon"] is None:
                temps["today"]["noon"] = temp
            elif hour == 18 and temps["today"]["evening"] is None:
                temps["today"]["evening"] = temp
        elif date == tomorrow:
            if hour == 9 and temps["tomorrow"]["morning"] is None:
                temps["tomorrow"]["morning"] = temp
            elif hour == 12 and temps["tomorrow"]["noon"] is None:
                temps["tomorrow"]["noon"] = temp
            elif hour == 18 and temps["tomorrow"]["evening"] is None:
                temps["tomorrow"]["evening"] = temp

    return temps

# Function to select image based on temperature
def select_image(temp):
    for min_temp, max_temp, image in IMAGE_RULES:
        if min_temp <= temp < max_temp:
            return image
    return IMAGE_RULES[-1][2]

# Function to update HTML file
def update_html(temps, html_path="index.html"):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for day in ["today", "tomorrow"]:
        for time_of_day in ["morning", "noon", "evening"]:
            temp = temps[day][time_of_day]
            if temp is not None:
                image_file = select_image(temp)
                img_tag = soup.find("div", {"id": f"{day}_{time_of_day}"}).find("img")
                img_tag["src"] = f"images/{image_file}"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

# Main execution
if __name__ == "__main__":
    forecast_temps = get_forecast_temperatures()
    update_html(forecast_temps)
    print("HTML updated with current and next day weather images.")
