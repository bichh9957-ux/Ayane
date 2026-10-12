import requests, config

URL = "https://discord.com/api/v10"

def add_role(guildid, userid, roleid):
    url = f"{URL}/guilds/{guildid}/members/{userid}/roles/{roleid}"
    headers = {
        "Authorization": f"Bot {config.token}",
        'Content-Type': 'application/json'
    }
    response = requests.put(url=url, headers=headers)
    if response.status_code == 204:
        print(f"{config.GREEN}THÔNG BÁO{config.RESET}: Đã thêm vai trò cho người dùng ({userid})")
    else:
        print(f"{config.RED}LỖI{config.RESET}: Không thể thêm vai trò (Mã: {response.status_code}). Kiểm tra thứ hạng vai trò của bot!")
