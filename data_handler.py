import os
import json

FILE_NAME = "data.txt"

def load_data():
    """خواندن امتیازات از فایل data.txt و برگرداندن لیستی از امتیازات و زمان‌ها."""
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    records = []
    for line in lines:
        line = line.strip()
        if line.startswith("Score:"):
            try:
                score_part, time_part = line.split(", ")
                score = int(score_part.split(": ")[1])
                time = int(time_part.split(": ")[1])
                records.append({'score': score, 'time': time})
            except ValueError:
                continue  # اگر داده‌ها به درستی استخراج نشدند، آن خط نادیده گرفته می‌شود
    
    return records

def save_data(data):
    """ذخیره اطلاعات در فایل تکست."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for record in data:
            score = record.get('score', 0)
            time = record.get('time', 0)
            file.write(f"Score: {score}, Time: {time}\n")

def save_music_state(music_enabled):
    """ذخیره وضعیت موزیک (فعال یا غیرفعال)."""
    music_state = {
        "music_enabled": music_enabled
    }
    with open("music_state.json", "w") as f:
        json.dump(music_state, f)

# تابعی برای بارگذاری وضعیت موزیک
def load_music_state():
    """بارگذاری وضعیت موزیک از فایل."""
    try:
        with open("music_state.json", "r") as f:
            music_state = json.load(f)
            return music_state.get("music_enabled", True)  # پیش‌فرض موزیک فعال است
    except FileNotFoundError:
        # اگر فایل پیدا نشد، پیش‌فرض موزیک فعال است
        return True