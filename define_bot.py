from __future__ import annotations

from typing import Optional
import os, vt
from discord import Activity, ActivityType
from discord.ext import commands
from supabase.client import Client as supabaseClient

class bot_class(commands.Bot):
    def __init__(self, *args, dbClient: supabaseClient, vtClient: vt.Client, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbClient = dbClient
        self.vtClient = vtClient
    
    # def __init__(self):
    #     super().__init__(
    #         command_prefix = default_prefix, 
    #         help_command = None, 
    #         intents = intents)
    #     self.dbClient = supabase_db.getClient()
    #     self.vtClient = virustotal.getClient()
        
    async def initial_load(self):    
        try:
            for file in os.listdir("./HiddenBot-py/cogs"):
                if file.endswith(".py") and file != "__init__.py" and file != "prototype.py":
                    await self.load_extension(f"cogs.{file[:-3]}")
        except Exception as e:
            print(f"Failed to load cog {file[:-3]}: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        try:
            await self.process_commands(message)
        except Exception as e:
            print(e)
    
    async def on_ready(self):
        try: 
            await self.wait_until_ready();
            await self.change_presence(activity = Activity(type = ActivityType.listening, name = "Henchforth/結城さくな(cover)"));
            await self.tree.sync()
            print(f"\nThe Discord Bot has been logged in as {self.user}\n");
            print("Running on {0} {1}\n".format(len(self.guilds), "server" if len(self.guilds) == 1 else "servers"));
        except Exception as e:
            print(e)
        
    async def close(self):
        try:
            await self.vtClient.close_async()
            await super().close()
        except Exception as e:
            print(e)