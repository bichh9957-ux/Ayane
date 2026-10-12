import config
from threading import Thread

if config.WEB_PORT != 3094:
    port = config.WEB_PORT
else:
    port = 3094

def run_web():
    import uvicorn
    print(f"{config.BOLD}{config.YELLOW}Đang khởi động webserver...{config.RESET}")
    uvicorn.run("web:app", host=config.WEB_IP, port=port, log_level="info")

print(f"{config.BOLD}{config.BLUE}------------ Discord OAuth2 Verify Bot ------------{config.RESET}")
print(f"{config.BOLD}{config.BLUE}----- Đã tích hợp Dashboard, Emoji & Embed Manager -----{config.RESET}")

web_thread = Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

print(f"{config.BOLD}{config.GREEN}Webserver đã chạy{config.RESET}")
print(f"{config.BOLD}{config.YELLOW}Đang khởi động Discord Bot...{config.RESET}")

if config.token == '':
    print(f'{config.BOLD}LỖI{config.RED}: Chưa có Token Bot, vui lòng cấu hình trong config.py!')
else:
    __import__("bot")
