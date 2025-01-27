from __future__ import annotations

from typing import Optional
import os
from discord import Activity, ActivityType, Guild, Message, Interaction, Intents
from discord.ext import commands
from clients import supabase_db, virustotal

#Setting up intents
intents = Intents.all()
default_prefix = "*"  

class bot_class(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = default_prefix, 
            help_command = None, 
            intents = intents)
        self.dbClient = supabase_db.getClient()
        self.vtClient = virustotal.getClient()
        
    async def initial_load(self):    
        try:
            for file in os.listdir("./HiddenBot-py/cogs"):
                if file.endswith(".py"):
                    await self.load_extension(f"cogs.{file[:-3]}")
        except Exception as e:
            print(f"Failed to load cog {file[:-3]}: {e}")
            raise e
                
                
    @commands.command()
    async def load(self, ctx, extension):
        try:
            await self.load_extension(f"cogs.{extension}")
            await ctx.send("Extensions loaded successfully")
        except Exception as e:
            print(e)

    @commands.command()
    async def unload(self, ctx, extension):
        try:
            await self.unload_extension(f"cogs.{extension}")
            await ctx.send("Extensions unloaded successfully")
        except Exception as e:
            print(e)
    
    @commands.command()
    async def reload(self, ctx, extension):
        try:
            await self.unload_extension(f"cogs.{extension}")
            await self.load_extension(f"cogs.{extension}")
            await ctx.send("Extensions reloaded successfully")
        except Exception as e:
            print(e)
    
    async def on_guild_join(self, guild):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return
        try:
            # if self.user.mentioned_in(message):
                # await message.channel.send(f"Execute slash commands")
            await self.process_commands(message)
        except Exception as e:
            print(e)
            raise e
    
    async def on_ready(self):
        try: 
            await self.wait_until_ready();
            await self.change_presence(activity = Activity(type = ActivityType.listening, name = "Henchforth/結城さくな(cover)"));
            await self.tree.sync()
            print(f"\nThe Discord Bot has been logged in as {self.user}\n");
            print("Running on {0} {1}\n".format(len(self.guilds), "server" if len(self.guilds) == 1 else "servers"));
        except Exception as e:
            print(e)
        
       
    async def success(self, content: str, interaction: Interaction, ephemeral: Optional[bool]):
        pass
        
    async def error(self, content: str, interaction: Interaction, ephemeral: Optional[bool]):
        pass 
        
    async def close(self):
        try:
            await self.vtClient.close_async()
            await super().close()
        except Exception as e:
            print(e)