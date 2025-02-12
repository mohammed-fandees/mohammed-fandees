import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WAKATIME_API_KEY")
API_URL = "https://wakatime.com/api/v1/users/current/summaries?range=all_time"
README_FILE = "README.md"

def get_wakatime_total():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["cumulative_total"]["text"]
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def update_readme(total_time):
    with open(README_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    badge_pattern = r"!\[WakaTime\]\(https://img\.shields\.io/badge/Coding%20Time-[^)]*\)"
    new_badge = f"![WakaTime](https://img.shields.io/badge/Coding%20Time-{total_time.replace(' ', '%20')}-blue?style=for-the-badge)"

    new_content = re.sub(badge_pattern, new_badge, content)

    with open(README_FILE, "w", encoding="utf-8") as file:
        file.write(new_content)

    print("README updated successfully!")

if __name__ == "__main__":
    if not API_KEY:
        print("Error: WAKATIME_API_KEY is missing from .env file.")
    else:
        total_time = get_wakatime_total()
        if total_time:
            update_readme(total_time)
