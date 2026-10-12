import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("DISCORD_TOKEN", "")

recover_key = "Ayane"

guildid = "1373474219714805821"

roleid = "1558000426953998367"

CLIENT_ID = "1532922217216610475"

CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

BASE_URL = 'https://oauth2.ayane.isroot.in'

WEB_IP = '0.0.0.0'

WEB_PORT = 3094
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
