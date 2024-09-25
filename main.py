import os
from dotenv import load_dotenv
import json
from pathlib import Path

import discord
from discord.ext import commands

import pytz
from datetime import datetime
from colorama import Fore, Back, Style
import platform

load_dotenv()
with open("config.json", 'r', encoding='utf-8') as file:
    config = json.load(file)


if not os.path.exists("json"):
    os.makedirs("json")
if not os.path.exists("json/list_emojis.json"):
    with open("json/list_emojis.json", 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)
if not os.path.exists("json/list_images.json"):
    with open("json/list_images.json", 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/disabled', intents=intents)

        self.cogslist = ['.'.join(file.relative_to('cogs').with_suffix('').parts) for file in Path('cogs').rglob('*.py') if not file.name.startswith('__')]
        with open("json/list_emojis.json", 'r', encoding='utf-8') as file:
            self.emoji_list = json.load(file)
        with open("json/list_images.json", 'r', encoding='utf-8') as file:
            self.image_list = json.load(file)


    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension("cogs."+cog)

    async def on_ready(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        prfx = (Back.BLACK + Fore.CYAN + datetime.now(pytz.timezone('Europe/Berlin')).strftime("%H:%M:%S") + Back.RESET + Fore.WHITE + Style.NORMAL)
        print(prfx + " Logged in as " + Fore.BLUE + self.user.name)
        print(prfx + " Bot ID " + Fore.BLUE + str(self.user.id))
        print(prfx + " Discord Version " + Fore.BLUE+ discord.__version__)
        print(prfx + " Python Version " + Fore.BLUE + str(platform.python_version()))
        print (prfx + " Cogs Loaded " + Fore.BLUE + str(len(self.cogslist)))
        global_commands = await self.tree.sync()
        guild_commands = await self.tree.sync(guild=discord.Object(id=config["admin_guild_id"]))
        print(prfx + " Slash CMDs Synced " + Fore.BLUE + str(len(guild_commands)+len(global_commands)) + " Commands")
        print("")
        await client.change_presence(activity = discord.CustomActivity(name=config["custom_bot_statu"]))

if __name__ == "__main__":
    client = Client()
    client.remove_command('help')
    client.run(os.getenv('TOKEN'))