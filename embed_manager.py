import json
import os
import re
import discord
from emoji_manager import get_emoji

EMBED_FILE = "embeds.json"

DEFAULT_EMBEDS = {
    "verify_panel": {
        "title": "{emoji:shield} XÁC THỰC TÀI KHOẢN",
        "description": "{emoji:link} Để xác thực tài khoản và nhận quyền truy cập máy chủ, vui lòng nhấp vào liên kết dưới đây:\n\n👉 **[NHẤP VÀO ĐÂY ĐỂ XÁC THỰC]({oauth_url})**\n\n{emoji:info} *Sau khi hoàn tất đăng nhập OAuth2, bạn sẽ tự động nhận được vai trò thành viên!*",
        "color": "#32CD32",
        "footer": "Hệ thống xác thực Discord OAuth2",
        "author": "Xác Thực Tự Động",
        "thumbnail": ""
    },
    "verify_success": {
        "title": "{emoji:success} XÁC THỰC THÀNH CÔNG",
        "description": "Chúc mừng bạn đã hoàn tất xác thực OAuth2 thành công! Vai trò của bạn đã được cập nhật.",
        "color": "#00FF7F",
        "footer": "Cảm ơn bạn đã tham gia máy chủ!",
        "author": "",
        "thumbnail": ""
    },
    "restore_start": {
        "title": "{emoji:refresh} ĐANG KHÔI PHỤC THÀNH VIÊN",
        "description": "{emoji:info} Bắt đầu kéo các thành viên đã lưu trong cơ sở dữ liệu vào máy chủ...",
        "color": "#3498DB",
        "footer": "Hệ thống kéo khôi phục thành viên",
        "author": "",
        "thumbnail": ""
    },
    "restore_finish": {
        "title": "{emoji:check} HOÀN TẤT KHÔI PHỤC",
        "description": "{emoji:success} Đã hoàn tất quá trình khôi phục kéo thành viên vào máy chủ thành công!",
        "color": "#2ECC71",
        "footer": "Hệ thống quản trị",
        "author": "",
        "thumbnail": ""
    },
    "error_wrong_key": {
        "title": "{emoji:error} LỖI XÁC THỰC",
        "description": "Mã khôi phục (Recovery Key) không chính xác! Vui lòng kiểm tra lại.",
        "color": "#E74C3C",
        "footer": "Cảnh báo bảo mật",
        "author": "",
        "thumbnail": ""
    }
}

def load_embeds():
    if not os.path.exists(EMBED_FILE):
        save_embeds(DEFAULT_EMBEDS)
        return DEFAULT_EMBEDS.copy()
    try:
        with open(EMBED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = DEFAULT_EMBEDS.copy()
            merged.update(data)
            return merged
    except Exception as e:
        print(f"Lỗi đọc embeds.json: {e}")
        return DEFAULT_EMBEDS.copy()

def save_embeds(data):
    try:
        with open(EMBED_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Lỗi lưu embeds.json: {e}")
        return False

def replace_emojis_in_text(text):
    if not text:
        return text
    def repl(match):
        emoji_key = match.group(1)
        return get_emoji(emoji_key)
    return re.sub(r'\{emoji:([a-zA-Z0-9_]+)\}', repl, text)

def build_embed(embed_key, **format_kwargs):
    embeds = load_embeds()
    cfg = embeds.get(embed_key, DEFAULT_EMBEDS.get(embed_key, {}))
    
    title = cfg.get("title", "")
    description = cfg.get("description", "")
    footer = cfg.get("footer", "")
    author = cfg.get("author", "")
    color_hex = cfg.get("color", "#3498DB").lstrip("#")
    
    try:
        color_val = int(color_hex, 16)
    except Exception:
        color_val = 0x3498DB

    if format_kwargs:
        try:
            title = title.format(**format_kwargs)
            description = description.format(**format_kwargs)
            footer = footer.format(**format_kwargs)
            author = author.format(**format_kwargs)
        except Exception as e:
            print(f"Lỗi format embed {embed_key}: {e}")

    title = replace_emojis_in_text(title)
    description = replace_emojis_in_text(description)
    footer = replace_emojis_in_text(footer)
    author = replace_emojis_in_text(author)

    embed = discord.Embed(title=title, description=description, color=color_val)
    if footer:
        embed.set_footer(text=footer)
    if author:
        embed.set_author(name=author)
    if cfg.get("thumbnail"):
        embed.set_thumbnail(url=cfg["thumbnail"])
        
    return embed
