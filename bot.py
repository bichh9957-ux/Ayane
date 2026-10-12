import discord, config, role
from module import opendb, refresh_token, add_user, get_user_profile
from embed_manager import build_embed
from emoji_manager import get_emoji
from discord import Option, default_permissions

intents = discord.Intents.all()
client = discord.Bot(intents=intents, debug_guilds=[config.guildid])

@client.slash_command(name="pull", description="Khôi phục kéo lại các thành viên đã xác thực")
@default_permissions(manage_messages=True)
async def restore(ctx, key: Option(str, description="Mã khôi phục bí mật")):
    if key != config.recover_key:
        return await ctx.respond(embed=build_embed("error_wrong_key"), ephemeral=True)
    
    await ctx.respond(embed=build_embed("restore_start"))
    con, cur = opendb()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()

    for user in list(set(users)):
        try:
            new_token = await refresh_token(user[1])
            if new_token:
                cur.execute("UPDATE users SET refresh_token = ? WHERE id = ?;", (new_token["refresh_token"], user[0]))
                con.commit()
                await add_user(new_token["access_token"], ctx.guild.id, user[0])
                profile = await get_user_profile(new_token["access_token"])
                if profile:
                    role.add_role(config.guildid, profile["id"], config.roleid)
        except Exception as e:
            print(f"{config.RED}LỖI{config.RESET}: Exception: {e}")
    con.close()
    await ctx.channel.send(embed=build_embed("restore_finish"))
    
@client.slash_command(name="setup", description="Gửi bảng điều khiển xác thực (Verify Panel)")
@default_permissions(manage_messages=True)
async def verifypanel(ctx):
    await ctx.channel.send(embed=build_embed("verify_panel", oauth_url=config.oauth2_url))
    await ctx.respond(f"{get_emoji('check')} Đã gửi bảng xác thực thành công!", ephemeral=True)

@client.slash_command(name="database-delete", description="Xóa toàn bộ cơ sở dữ liệu người dùng")
@default_permissions(manage_messages=True)
async def erasedb(ctx):
    con, cur = opendb()
    cur.execute("DELETE FROM users;")
    con.commit()
    count = cur.rowcount
    con.close()
    await ctx.respond(f"{get_emoji('database')} Đã xóa {count} người dùng khỏi cơ sở dữ liệu.", ephemeral=True)

@client.slash_command(name="database-size", description="Xem số lượng người dùng trong cơ sở dữ liệu")
@default_permissions(manage_messages=True)
async def dbsize(ctx):
    con, cur = opendb()
    cur.execute("SELECT COUNT(*) FROM users;")
    count = cur.fetchone()[0]
    con.close()
    await ctx.respond(f"{get_emoji('user')} Hiện có **{count}** người dùng trong cơ sở dữ liệu.", ephemeral=True)
    
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Hệ thống Xác thực OAuth2'))
    print(f'{config.GREEN}THÔNG BÁO{config.RESET}: Đã đăng nhập dưới tên {client.user} (ID: {client.user.id})')

if config.token == '':
    print(f'{config.RED}LỖI{config.RESET}: Thiếu token bot trong config.py!')
else:
    client.run(config.token)
