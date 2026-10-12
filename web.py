from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from module import exchange_code, opendb, get_user_profile
import role, config
from emoji_manager import load_emojis, save_emojis
from embed_manager import load_embeds, save_embeds

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

@app.get("/callback")
async def callback(code: str):
    exchange_res = await exchange_code(code, config.REDIRECT_URI)
    if not exchange_res:
        raise HTTPException(status_code=400, detail="Ủy quyền không thành công")
    profile = await get_user_profile(exchange_res["access_token"])
    if not profile:
        raise HTTPException(status_code=400, detail="Không thể lấy thông tin người dùng")
    
    con, cur = opendb()
    cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?);", (profile["id"], exchange_res["refresh_token"]))
    con.commit()
    con.close()
    
    role.add_role(config.guildid, profile["id"], config.roleid)
    return RedirectResponse("https://discord.com/oauth2/authorized")

@app.get("/dashboard/login")
async def dashboard_login():
    return RedirectResponse(config.dashboard_oauth_url)

@app.get("/dashboard/callback")
async def dashboard_callback(request: Request, code: str):
    exchange_res = await exchange_code(code, config.DASHBOARD_REDIRECT_URI)
    if not exchange_res or "access_token" not in exchange_res:
        return HTMLResponse("<h3>Lỗi đăng nhập OAuth2 Dashboard!</h3>", status_code=400)
    
    profile = await get_user_profile(exchange_res["access_token"])
    if profile:
        request.session["user"] = profile
    return RedirectResponse("/dashboard")

@app.get("/dashboard/logout")
async def dashboard_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_index(request: Request):
    user = request.session.get("user")
    
    con, cur = opendb()
    cur.execute("SELECT COUNT(*) FROM users;")
    user_count = cur.fetchone()[0]
    con.close()

    emojis = load_emojis()
    embeds = load_embeds()

    login_btn = f'''
        <a href="/dashboard/login" class="btn btn-discord">
            <i class="fa-brands fa-discord"></i> Đăng nhập quản trị viên (OAuth2)
        </a>
    ''' if not user else f'''
        <div class="user-info">
            <img src="https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png" class="avatar"/>
            <span><strong>{user.get('global_name', user['username'])}</strong></span>
            <a href="/dashboard/logout" class="btn btn-danger btn-sm">Đăng xuất</a>
        </div>
    '''

    content_panel = ""
    if user:
        content_panel = f'''
        <div class="card my-4">
            <h2>{emojis.get('settings', '⚙️')} Quản Lý Emoji Bot (`emojis.json`)</h2>
            <p class="subtitle">Thay đổi trực tiếp các biểu tượng cảm xúc hiển thị trong Embed và Bot.</p>
            <form action="/dashboard/save-emojis" method="post">
                <div class="grid-4">
        '''
        for k, v in emojis.items():
            content_panel += f'''
                <div class="form-group">
                    <label>{k}:</label>
                    <input type="text" name="emoji_{k}" value="{v}" class="form-control text-center"/>
                </div>
            '''
        content_panel += '''
                </div>
                <button type="submit" class="btn btn-primary mt-3">Lưu Thay Đổi Emoji</button>
            </form>
        </div>

        <div class="card my-4">
            <h2>🛡️ Quản Lý Toàn Bộ Embed Bot (`embeds.json`)</h2>
            <p class="subtitle">Tùy chỉnh tiêu đề, nội dung, màu sắc và chân trang cho từng thông báo.</p>
            <form action="/dashboard/save-embeds" method="post">
        '''
        for emb_key, emb_val in embeds.items():
            content_panel += f'''
                <div class="embed-box">
                    <h3>📌 Cấu hình Embed: <code>{emb_key}</code></h3>
                    <div class="form-group">
                        <label>Tiêu đề (Title):</label>
                        <input type="text" name="emb_{emb_key}_title" value="{emb_val.get('title','')}" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Nội dung (Description):</label>
                        <textarea name="emb_{emb_key}_desc" class="form-control" rows="4">{emb_val.get('description','')}</textarea>
                    </div>
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Màu sắc (Hex Code):</label>
                            <input type="text" name="emb_{emb_key}_color" value="{emb_val.get('color','#3498DB')}" class="form-control"/>
                        </div>
                        <div class="form-group">
                            <label>Chân trang (Footer):</label>
                            <input type="text" name="emb_{emb_key}_footer" value="{emb_val.get('footer','')}" class="form-control"/>
                        </div>
                    </div>
                </div>
            '''
        content_panel += '''
                <button type="submit" class="btn btn-success mt-3">Lưu Toàn Bộ Cấu Hình Embed</button>
            </form>
        </div>
        '''
    else:
        content_panel = '''
        <div class="card text-center my-4" style="padding: 50px;">
            <h3>🔒 Bạn cần đăng nhập tài khoản Discord để truy cập bảng quản trị Dashboard.</h3>
            <p class="text-muted mt-2">Chỉ quản trị viên có quyền quản lý hệ thống.</p>
        </div>
        '''

    html = f'''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard Quản Lý Discord Bot</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
            .container {{ max-width: 1100px; margin: auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 20px 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
            .card {{ background: #1e293b; border-radius: 12px; padding: 24px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
            .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .grid-4 {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }}
            .stats-card {{ background: linear-gradient(135deg, #6366f1, #4f46e5); padding: 20px; border-radius: 10px; font-size: 20px; font-weight: bold; text-align: center; color: #fff; }}
            .form-group {{ margin-bottom: 12px; display: flex; flex-direction: column; }}
            .form-group label {{ margin-bottom: 6px; font-weight: 600; color: #94a3b8; font-size: 14px; }}
            .form-control {{ background: #0f172a; border: 1px solid #334155; color: #fff; padding: 10px; border-radius: 6px; outline: none; font-size: 14px; }}
            .form-control:focus {{ border-color: #6366f1; }}
            .btn {{ padding: 10px 18px; border-radius: 6px; text-decoration: none; border: none; cursor: pointer; font-weight: bold; display: inline-block; font-size: 14px; transition: 0.2s; }}
            .btn:hover {{ opacity: 0.9; }}
            .btn-discord {{ background: #5865F2; color: #fff; }}
            .btn-primary {{ background: #3b82f6; color: #fff; }}
            .btn-success {{ background: #10b981; color: #fff; width: 100%; font-size: 16px; padding: 14px; }}
            .btn-danger {{ background: #ef4444; color: #fff; }}
            .avatar {{ width: 36px; height: 36px; border-radius: 50%; vertical-align: middle; margin-right: 8px; }}
            .embed-box {{ background: #0f172a; padding: 18px; border-radius: 8px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }}
            .user-info {{ display: flex; align-items: center; gap: 12px; }}
            .subtitle {{ color: #94a3b8; font-size: 13px; margin-top: -5px; margin-bottom: 15px; }}
            .text-center {{ text-align: center; }}
            .mt-2 {{ margin-top: 10px; }}
            .mt-3 {{ margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2><i class="fa-solid fa-robot"></i> Dashboard Quản Lý Discord Bot</h2>
                <div>{login_btn}</div>
            </div>
            
            <div class="card">
                <div class="stats-card">
                    {emojis.get('database', '💾')} Tổng số người dùng đã xác thực trong Database: {user_count}
                </div>
            </div>

            {content_panel}
        </div>
    </body>
    </html>
    '''
    return html

@app.post("/dashboard/save-emojis")
async def save_emojis_route(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="Chưa đăng nhập")
    
    form_data = await request.form()
    emojis = load_emojis()
    for k in emojis.keys():
        if f"emoji_{k}" in form_data:
            emojis[k] = form_data[f"emoji_{k}"]
    
    save_emojis(emojis)
    return RedirectResponse("/dashboard", status_code=303)

@app.post("/dashboard/save-embeds")
async def save_embeds_route(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="Chưa đăng nhập")
    
    form_data = await request.form()
    embeds = load_embeds()
    
    for emb_key in embeds.keys():
        embeds[emb_key]["title"] = form_data.get(f"emb_{emb_key}_title", "")
        embeds[emb_key]["description"] = form_data.get(f"emb_{emb_key}_desc", "")
        embeds[emb_key]["color"] = form_data.get(f"emb_{emb_key}_color", "#3498DB")
        embeds[emb_key]["footer"] = form_data.get(f"emb_{emb_key}_footer", "")
    
    save_embeds(embeds)
    return RedirectResponse("/dashboard", status_code=303)
