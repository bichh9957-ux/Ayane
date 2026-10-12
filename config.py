import os
from dotenv import load_dotenv
load_dotenv()

# Bot token
token = os.getenv("DISCORD_TOKEN", "")

# Mã khôi phục khi dùng /restore
recover_key = "Ayane"

# Guild ID của bạn
guildid = "1373474219714805821"

# ID vai trò được cấp khi xác thực
roleid = "1558000426953998367"

# Client ID của Discord Application
CLIENT_ID = "1532922217216610475"

# Client Secret của Discord Application
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

# URL Webserver (Ví dụ: http://localhost:3000 hoặc https://domain-cua-ban.com)
BASE_URL = 'http://bots.meowlix.us:3094'

# IP Webserver
WEB_IP = '0.0.0.0'

# Port Webserver
WEB_PORT = 3094

# Secret Key cho Session Dashboard
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-this")

REDIRECT_URI = BASE_URL + '/callback'
DASHBOARD_REDIRECT_URI = BASE_URL + '/dashboard/callback'

API_ENDPOINT = "https://discord.com/api/v10"

oauth2_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds.join"
dashboard_oauth_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={DASHBOARD_REDIRECT_URI}&response_type=code&scope=identify"

BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
