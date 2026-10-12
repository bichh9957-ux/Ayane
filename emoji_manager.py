import json
import os

EMOJI_FILE = "emojis.json"

DEFAULT_EMOJIS = {
    "verify": "✅",
    "success": "🎉",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "bot": "🤖",
    "user": "👤",
    "shield": "🛡️",
    "link": "🔗",
    "database": "💾",
    "refresh": "🔄",
    "settings": "⚙️",
    "star": "⭐",
    "check": "✔",
    "cross": "✖",
    "lock": "🔒",
    "key": "🔑",
    "crown": "👑",
    "rocket": "🚀",
    "ping": "🏓"
}

def load_emojis():
    if not os.path.exists(EMOJI_FILE):
        save_emojis(DEFAULT_EMOJIS)
        return DEFAULT_EMOJIS.copy()
    try:
        with open(EMOJI_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = DEFAULT_EMOJIS.copy()
            merged.update(data)
            return merged
    except Exception as e:
        print(f"Lỗi đọc emojis.json: {e}")
        return DEFAULT_EMOJIS.copy()

def save_emojis(data):
    try:
        with open(EMOJI_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Lỗi lưu emojis.json: {e}")
        return False

def get_emoji(key):
    emojis = load_emojis()
    return emojis.get(key, "❓")
