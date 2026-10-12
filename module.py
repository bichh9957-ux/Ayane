import config, requests, asyncio, sqlite3

async def exchange_code(code, redirect_uri):
    data = {
      'client_id': config.CLIENT_ID,
      'client_secret': config.CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': redirect_uri
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        r = requests.post('%s/oauth2/token' % config.API_ENDPOINT, data=data, headers=headers)
        if (r.status_code != 429):
            break
        limitinfo = r.json()
        await asyncio.sleep(limitinfo.get("retry_after", 2) + 2)
    return False if "error" in r.json() else r.json()

async def refresh_token(refresh_token):
    data = {
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        r = requests.post('%s/oauth2/token' % config.API_ENDPOINT, data=data, headers=headers)
        if (r.status_code != 429):
            break
        limitinfo = r.json()
        await asyncio.sleep(limitinfo.get("retry_after", 2) + 2)
    return False if "error" in r.json() else r.json()

async def add_user(access_token, guild_id, user_id):
    while True:
        jsonData = {"access_token": access_token}
        header = {"Authorization": "Bot " + config.token}
        r = requests.put(f"{config.API_ENDPOINT}/guilds/{guild_id}/members/{user_id}", json=jsonData, headers=header)
        if (r.status_code != 429):
            break
        limitinfo = r.json()
        await asyncio.sleep(limitinfo.get("retry_after", 2) + 2)

    if r.status_code in [201, 204]:
        return True
    else:
        print(f"{config.RED}LỖI{config.RESET}: Không thể thêm thành viên. Mã lỗi: {r.status_code}")
        return False

def opendb():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        refresh_token TEXT
                    );''')
    return con, cur

async def get_user_profile(token):
    header = {"Authorization": "Bearer " + token}
    res = requests.get("https://discord.com/api/v10/users/@me", headers=header)
    if res.status_code != 200:
        return False
    ves = res.json()
    print(f"{config.GREEN}THÔNG BÁO{config.RESET}: Xác thực mới từ", ves.get('username'), ves.get('id'))
    return ves
