import os
import sys
import time
import json
import ctypes
import asyncio
import webbrowser
import psutil
import tempfile
import pyautogui
import numpy as np
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import discord
from discord.ext import commands
from discord.ui import Button, View

# 🔥 AMELIX ASCII BANNER (Green Gradient)
GREEN_SHADES = ["\033[38;5;46m", "\033[38;5;47m", "\033[38;5;48m", "\033[38;5;49m", "\033[38;5;50m"]
RESET = "\033[0m"

ascii_art = """
    █████╗ ███╗   ███╗███████╗██╗     ██╗██╗  ██╗
   ██╔══██╗████╗ ████║██╔════╝██║     ██║╚██╗██╔╝
   ███████║██╔████╔██║█████╗  ██║     ██║ ╚███╔╝ 
   ██╔══██║██║╚██╔╝██║██╔══╝  ██║     ██║ ██╔██╗ 
   ██║  ██║██║ ╚═╝ ██║███████╗███████╗██║██╔╝ ██╗
   ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝
"""

os.system('cls' if os.name == 'nt' else 'clear')
lines = ascii_art.split('\n')
for i, line in enumerate(lines):
    shade = GREEN_SHADES[i % len(GREEN_SHADES)]
    print(shade + line + RESET)

print(f"{GREEN_SHADES[0]}=== Amelix Control Center ==={RESET}\n")

# 📂 PERSISTENT CONFIGURATION LOGIC
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_config(token, owner_id, accepted=False):
    config_data = {
        "token": token,
        "owner_id": owner_id,
        "accepted": accepted
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

config = load_config()

if config is None:
    print(f"{GREEN_SHADES[1]}[*] No configuration file found. Starting first-time setup...{RESET}")
    TOKEN = input("👉 Enter your Discord Bot TOKEN: ").strip()
    OWNER_ID = int(input("👉 Enter your Discord User ID (Owner): ").strip())
    ACCEPTED = False
    save_config(TOKEN, OWNER_ID, ACCEPTED)
    print(f"\n✅ Configuration saved to {CONFIG_FILE} successfully!")
else:
    print(f"{GREEN_SHADES[2]}[+] Configuration loaded automatically from cached file.{RESET}")
    TOKEN = config.get("token")
    OWNER_ID = config.get("owner_id")
    ACCEPTED = config.get("accepted", False)

accepted_users = set()
if ACCEPTED:
    accepted_users.add(OWNER_ID)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# 🛑 SECURITY & ERROR HANDLING FOR NON-OWNERS
async def is_owner_and_dm(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ **Access Denied:** You are not authorized to control this machine. Access is restricted to the host owner.")
        return False
    if not isinstance(ctx.channel, discord.DMChannel):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.author.send("🔒 **Security Alert:** All Amelix commands must be executed here in Direct Messages (DMs).")
        return False
    return True

@bot.event
async def on_ready():
    print(f"\n[+] Amelix is online and connected as: {bot.user.name}")
    if OWNER_ID not in accepted_users:
        print("[!] Awaiting the !start command in DMs to initialize configuration permissions...")
    else:
        print("[+] Authentication fully unlocked. Machine is fully responsive to control hooks.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
        
    # Check if a non-owner tries to execute a DM exploit hook
    if isinstance(message.channel, discord.DMChannel) and message.author.id != OWNER_ID:
        if message.content.startswith('!'):
            await message.channel.send("❌ **Access Denied:** Connection unauthorized.")
            return

    if message.author.id == OWNER_ID and isinstance(message.channel, discord.DMChannel):
        if not message.content.startswith('!start') and OWNER_ID not in accepted_users:
            await message.channel.send("❌ **Access Denied.** Please initialize the tool first by using the `!start` command.")
            return
            
    await bot.process_commands(message)

# --- 📋 INITIALIZATION SYSTEM (!start) ---

class AcceptanceView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accept Terms", style=discord.ButtonStyle.green, custom_id="accept_terms")
    async def accept(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("❌ Unauthorized interaction.", ephemeral=True)
        
        accepted_users.add(OWNER_ID)
        save_config(TOKEN, OWNER_ID, accepted=True)
        
        await interaction.response.send_message("✅ **Terms Accepted!** All Amelix commands are now unlocked permanently. Type `!help` to see the full list.", ephemeral=False)
        self.clear_items()
        await interaction.message.edit(view=self)

@bot.command()
async def start(ctx):
    if not await is_owner_and_dm(ctx): return
    
    if OWNER_ID in accepted_users:
        await ctx.send("ℹ️ You have already accepted the terms of service. Amelix is fully operational!")
        return

    embed = discord.Embed(
        title="🛡️ Amelix Terms of Service & End-User License",
        description=(
            "By accepting below, you authorize this bot to interact directly with your operating system.\n\n"
            "⚠️ **CRITICAL WARNING & ETHICAL USE POLICY:**\n"
            "This software is strictly designed for remote management of your **own personal computer**. "
            "You are **strictly prohibited** from installing or using this tool to spy on, monitor, "
            "or control anyone else's computer without their explicit, legal consent. "
            "Unauthorized monitoring is illegal and violates privacy laws. Use responsibly."
        ),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=AcceptanceView())

# --- 🛠️ COMMANDS CATALOGUE ---

@bot.command()
async def help(ctx):
    if not await is_owner_and_dm(ctx): return
    
    embed = discord.Embed(title="🟢 Amelix Control Panel - Help Menu", color=discord.Color.green())
    commands_list = (
        "`!stats` : View system info (CPU, RAM...)\n"
        "`!fps` : Check current system refresh rate / FPS status\n"
        "`!clip [seconds]` : Record an MP4 video clip of the screen\n"
        "`!wallpaper` : Change desktop wallpaper (attach an image)\n"
        "`!background` : List active user applications (excludes Windows system tasks)\n"
        "`!go [url]` : Open a link inside the default web browser\n"
        "`!start_app [name]` : Execute an application (ex: `!start_app notepad`)\n"
        "`!sleep` : Put the computer to sleep mode\n"
        "`!restart` : Force reboot the machine\n"
        "`!shutdown` : Completely power off the PC"
    )
    embed.add_field(name="Available Commands", value=commands_list, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    if not await is_owner_and_dm(ctx): return
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    
    msg = (
        f"🖥️ **System Statistics:**\n"
        f"🔹 **CPU Usage:** {cpu}%\n"
        f"🔹 **RAM Usage:** {round(ram.used / (1024**3), 2)}GB / {round(ram.total / (1024**3), 2)}GB ({ram.percent}%)"
    )
    await ctx.send(msg)

@bot.command()
async def fps(ctx):
    if not await is_owner_and_dm(ctx): return
    await ctx.send("📊 Measuring system frame performance... Please wait 3 seconds.")
    
    start_time = time.time()
    counter = 0
    while time.time() - start_time < 3.0:
        pyautogui.screenshot()
        counter += 1
    
    calculated_fps = round(counter / 3.0, 1)
    await ctx.send(f"🎮 **Performance Status:** Your PC can process screen captures at **{calculated_fps} FPS** under current background load.")

@bot.command()
async def clip(ctx, seconds_input: str = None):
    if not await is_owner_and_dm(ctx): return
    
    if seconds_input is None:
        await ctx.send("💡 **Tip:** Use the command like this: `!clip [number of seconds]`. (Ex: `!clip 10` or `!clip 10s`).")
        return

    clean_input = seconds_input.lower().replace("seconds", "").replace("sec", "").replace("s", "").strip()

    if not clean_input.isdigit():
        await ctx.send("❌ **Error:** Please input a valid integer number of seconds (e.g., `!clip 15`).")
        return

    seconds = int(clean_input)

    if seconds > 30:
        await ctx.send("⚠️ **Time Limit Exceeded!** The video file would be too heavy to send over Discord. **Please specify a lower time limit under 30 seconds.**")
        return

    await ctx.send(f"🎥 Recording screen frames ({seconds} seconds)... Please wait.")

    frames = []
    fps_rate = 10
    start_time = time.time()

    while time.time() - start_time < seconds:
        img = pyautogui.screenshot()
        img_resized = img.resize((1280, 720))
        frames.append(np.array(img_resized))
        await asyncio.sleep(1 / fps_rate)

    await ctx.send("⏳ Compiling and compressing MP4 file... Almost done.")

    unique_id = int(time.time())
    temp_dir = tempfile.gettempdir()
    output_filename = os.path.join(temp_dir, f"amelix_clip_{unique_id}.mp4")

    try:
        clip_obj = ImageSequenceClip(frames, fps=fps_rate)
        clip_obj.write_videofile(output_filename, codec="libx264", audio=False, logger=None)
        clip_obj.close()

        if os.path.exists(output_filename):
            await ctx.send("📤 Screen captured successfully! Here is your clip:", file=discord.File(output_filename))
            os.remove(output_filename)
        else:
            await ctx.send("❌ **Internal Error:** The MP4 video file could not be written to the temporary directory.")

    except Exception as e:
        await ctx.send(f"❌ An error occurred during video creation processing: `{e}`")
        if os.path.exists(output_filename):
            try: os.remove(output_filename)
            except: pass

@bot.command()
async def wallpaper(ctx):
    if not await is_owner_and_dm(ctx): return
    
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach an image file to your command message to change your desktop wallpaper.")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        await ctx.send("❌ Invalid format. File must be an image extension (png, jpg, jpeg).")
        return

    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, "amelix_wallpaper.jpg")

    try:
        await attachment.save(image_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        await ctx.send("🖼️ Desktop background wallpaper updated successfully!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred while applying wallpaper: `{e}`")

@bot.command()
async def background(ctx):
    if not await is_owner_and_dm(ctx): return
    
    apps = []
    for proc in psutil.process_iter(['name', 'username']):
        try:
            if proc.info['username'] and "SYSTEM" not in proc.info['username'] and "LOCAL SERVICE" not in proc.info['username']:
                name = proc.info['name']
                if name not in apps and not name.lower().startswith("svchost"):
                    apps.append(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    apps_text = "\n".join([f"▪️ {app}" for app in apps[:30]])
    await ctx.send(f"📂 **Active User Background Applications:**\n{apps_text if apps_text else 'No major apps running.'}")

@bot.command()
async def go(ctx, url: str):
    if not await is_owner_and_dm(ctx): return
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    await ctx.send(f"🌐 Opening external link destination URL `{url}` inside the default system browser.")

@bot.command()
async def start_app(ctx, *, app_name: str):
    if not await is_owner_and_dm(ctx): return
    try:
        os.system(f"start {app_name}")
        await ctx.send(f"🚀 Execution initialization signal sent for: `{app_name}`")
    except Exception:
        await ctx.send(f"❌ Failed to start application command.")

@bot.command()
async def sleep(ctx):
    if not await is_owner_and_dm(ctx): return
    await ctx.send("💤 Putting the computer into sleep/suspend power state mode...")
    # Safe non-admin native call
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

@bot.command()
async def restart(ctx):
    if not await is_owner_and_dm(ctx): return
    await ctx.send("🔄 System reboot triggered... Restarting PC immediately.")
    # Standard user-level execution command
    os.system("shutdown /r /t 1")

@bot.command()
async def shutdown(ctx):
    if not await is_owner_and_dm(ctx): return
    await ctx.send("⚠️ System shutdown sequence initialized... Turning off PC.")
    # Standard user-level execution command
    os.system("shutdown /s /t 1")

bot.run(TOKEN)
